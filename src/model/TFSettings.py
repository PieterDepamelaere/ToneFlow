# https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041

import os
import sys
import re
import aiofiles
import pathlib as pl
import json
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.utils import get_hex_from_color
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty

from kivymd.utils import asynckivy
from kivymd.toast import toast

from src.model.TFSetting import TFSetting
from src.model.PlayList import PlayList
from src.model.PlayLists import PlayLists
from src.model.Songs import Songs
from src.model.Help import Help
from src.model.ToneFlower import ToneFlower

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.CommonUtils import CommonUtils as CU

class TFSettings(Screen):

    app = None
    is_kv_loaded = False
    theme_primary_color = 'LightGreen'  # 'LightGreen'
    theme_accent_color = 'Green'  # Lime

    def __init__(self, kv_file_main_widget=None, **kwargs):
        self._dic = dict()
        self.initialize_tfsettings_dict()

        # Add only the editable TFSettings to the _editable_list
        # [value for key, value in self._dic.items() if value.is_editable]
        self._editable_list = list()

        # Make the settings public & update the app's title:
        CU.tfs = self
        TFSettings.app = App.get_running_app()
        CU.app = TFSettings.app
        TFSettings.app.title = CU.tfs.dic['APP_NAME'].value + " - v" + CU.tfs.dic['MAJOR_MINOR_VERSION'].value

        if kv_file_main_widget is not None and len(kv_file_main_widget) > 0:
            # Create the main widget here in TFSettings because it already needs tfs settings:
            TFSettings.app.set_main_widget(Builder.load_file(kv_file_main_widget))

        # Create TFSettings widget and underlying base-object:
        if (not TFSettings.is_kv_loaded):
            # Make sure it's only loaded once:
            Builder.load_file(str(curr_file.parents[1] / "view" / (pl.Path(TFSettings.__name__).with_suffix(".kv")).name))
            TFSettings.is_kv_loaded = True

        super(TFSettings, self).__init__(name=type(self).__name__, **kwargs)

        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a dict of callbacks
        self._context_menus = {"Clear Input": lambda x: {self.clear_search_pattern()},
                               "Sort Settings": lambda x: {self.sort_editable_list()},
                               "Refresh": lambda x: {self.refresh_editable_list(), toast(f"Refreshed")},
                               "Restore Factory Settings": lambda x: toast("TODO: WIP"),
                               "Help": lambda x: toast("TODO: WIP")}
        # TODO: Implement the other context menus

    def get_dic(self):
        return self._dic

    def get_editable_list(self):
        return self._editable_list

    def set_editable_list(self, editable_list):
        editable_list = CU.safe_cast(editable_list, self._editable_list.__class__, "")
        self._editable_list = editable_list

    def get_context_menus(self):
        return self._context_menus

    dic = property(get_dic)
    editable_list = property(get_editable_list, set_editable_list)
    context_menus = property(get_context_menus)

    def create_load_tf_workspace(self, tf_workspace_path):
        tf_workspace_path = str(tf_workspace_path)

        # Without whitespace the length of ans_user should be bigger than 0, also make sure that when the tf_workspace_path's description is returned, that :
        if ((tf_workspace_path is not None) and (len(str(tf_workspace_path).strip()) > 0) and (str(tf_workspace_path) != self._dic['tf_workspace_path'].description)):
            # If user didn't omit the explanation on the workspace's path, then auto-ignore it:
            tf_workspace_path = str(tf_workspace_path).replace(f"{self._dic['tf_workspace_path'].description}", "")

            # Again check whether the remaining path is not empty:
            if (len(str(tf_workspace_path).strip()) > 0):
                # Not a stripped tf_workspace_path is stored, this allows for people that have folders with trailing whitspace (although strongly discouraged).
                tf_workspace_path = pl.Path(tf_workspace_path)
            else:
                # In case of trivial tf_workspace_path, the original proposal is used:
                tf_workspace_path = self._dic['tf_workspace_path'].default_value
        else:
            # In case of trivial tf_workspace_path, the original proposal is used:
            tf_workspace_path = self._dic['tf_workspace_path'].default_value

        # Make sure that tf_workspace_path is actually a Path-object:
        tf_workspace_path = pl.Path(tf_workspace_path)

        if (tf_workspace_path.is_file()):
            # If one would have specified a file, then the workspace will be created under its parent
            tf_workspace_path = tf_workspace_path.parents[0]

        # Check whether innermost subdirectory is already the workspace itself:
        if (tf_workspace_path.name != str(self._dic['WORKSPACE_NAME'].value)):
            tf_workspace_path = tf_workspace_path / self._dic['WORKSPACE_NAME'].value

        # Create tf_workspace_path in case it doesn't exist yet, when it did, it doesn't get overridden:
        images_videos_dir = tf_workspace_path / self._dic['IMAGES_VIDEOS_DIR_NAME'].value
        playlists_dir = tf_workspace_path / self._dic['PLAYLISTS_DIR_NAME'].value
        prep_midi_dir = tf_workspace_path / self._dic['PREP_MIDI_DIR_NAME'].value
        raw_midi_dir = tf_workspace_path / self._dic['RAW_MIDI_DIR_NAME'].value

        # There's no explicit creation of the tf_workspace_path folder itself because parents will be auto-created, while creating its children:
        # If this workspace with these subfolders already exists, then it doesn't get overridden:
        images_videos_dir.mkdir(exist_ok=True, parents=True)
        playlists_dir.mkdir(exist_ok=True, parents=True)
        prep_midi_dir.mkdir(exist_ok=True, parents=True)
        raw_midi_dir.mkdir(exist_ok=True, parents=True)

        # Finally return the value to set in the setter (Because there's a chance that it got modified along the way):
        return pl.Path(tf_workspace_path)

    def export_tf_settings_to_config(self):
        with open(f"{self._dic['CONFIG_FILE_PATH'].value}", 'w') as config_file:
            # Only dump editable properties
            json.dump({k: v for k, v in self._dic.items() if v.is_editable}, fp=config_file, default=lambda s: s.to_json(), indent=4,
                      sort_keys=True)

    def import_tf_settings_from_config(self):
        with open(f"{self._dic['CONFIG_FILE_PATH'].value}") as config_file:
            config_dic = json.load(config_file)

            for key in config_dic:
                self._dic[key].value = config_dic[key]['value']

            print("Parsing of the JSON-configfile was successful.")

    def initialize_tfsettings_dict(self):
        """
        Add new TFSetting-objects to _dic (_name, _value, _default_value, _description="", _is_editable=False, _callback_on_set=None))
        :return:
        """
        # Add non-user editable ones:
        self._dic['APP_NAME'] = TFSetting("Name of Application", None, str("ToneFlow" + u"\u00AE"), None, False, None)
        self._dic['MAJOR_MINOR_VERSION'] = TFSetting(f"{self._dic['APP_NAME'].value} Version MAJOR.MINOR", None, "0.5", "In theory, an update of the minor version alone shouldn't induce breaking changes.", False, None)
        self._dic['CONFIG_FILE_PATH'] = TFSetting("Path to Config File", None, curr_file.parents[2] / "Config_TF.json", None, False, None)
        self._dic['IMG_DIR_PATH'] = TFSetting("Internal Directory of Images", None, curr_file.parents[2] / "img", None, False, None)
        self._dic['WORKSPACE_NAME'] = TFSetting("Name of Workspace", None, "Workspace_TF", None, False, None)
        self._dic['EXPLANATION_PLAYLIST_SONG_NAME'] = TFSetting("Explanation Playlist Song Name", None, f"No spaces, only alphanumeric characters & \"_-\".", None, False, None)
        self._dic['EXPLANATION_WORKSPACE_PATH'] = TFSetting("Explanation Workspace Name", None, f"Preferably choose path on external device like USB flash drive.", None, False, None)
        self._dic['FILE_SEP_TEXT'] = TFSetting("Exportable File Separator", None, "/FS/", None, False, None)
        self._dic['IMAGES_VIDEOS_DIR_NAME'] = TFSetting("Name of Images_Videos Folder in Workspace", None, "Images_Videos", None, False, None)
        self._dic['PLAYLISTS_DIR_NAME'] = TFSetting("Name of Playlists Folder in Workspace", None, "Playlists", None, False, None)
        self._dic['PREP_MIDI_DIR_NAME'] = TFSetting("Name of Prep_MIDI Folder in Workspace", None, "Songs_Prep_MIDI", None, False, None)
        self._dic['RAW_MIDI_DIR_NAME'] = TFSetting("Name of Raw_MIDI Folder in Workspace", None, "Songs_Raw_MIDI", None, False, None)
        self._dic['SCREEN_HELP_CLASS'] = TFSetting("Help", None, Help, False, None)
        self._dic['SCREEN_PLAYLIST_CLASS'] = TFSetting("Lineup", None, PlayList, False, None)
        self._dic['SCREEN_PLAYLISTS_CLASS'] = TFSetting("Playlists", None, PlayLists, False, None)
        self._dic['SCREEN_SETTINGS_CLASS'] = TFSetting("Settings", None, TFSettings, False, None)
        self._dic['SCREEN_SONGS_CLASS'] = TFSetting("Songs", None, Songs, False, None)
        self._dic['SCREEN_TONEFLOWER_CLASS'] = TFSetting(" ToneFlower", None, ToneFlower, False, None)
        self._dic['THEME_BACKGROUND_HUE'] = TFSetting("Background hue influencing text color", None, '500', False, None)

        # Add user editable ones:
        self._dic['tf_workspace_path'] = TFSetting("Path to ToneFlow Workspace", None, curr_file.parents[3] / f"{self._dic['WORKSPACE_NAME'].value}", f"???{os.sep}{self._dic['WORKSPACE_NAME'].value}", True, lambda value: self.create_load_tf_workspace(value))
        self._dic['overall_speedfactor'] = TFSetting("Overall Speedfactor", None, 1.0, f"Premultiplied speedfactor that affects the overall speed of the flowing tones.", True, None)
        # TODO: Provide callback that pushes changes in low/high_pitch_limit to toneflower for example.
        self._dic['low_pitch_limit'] = TFSetting("Low Pitch Limit", None, "C4", f"Pitch-underbound of your instrument(s). Supported formats {{'C4', 'C#4', 'Db4', 'C#4/Db4', 'Db4/C#4', 'C#/Db4', 'Db/C#4'}} '4' = central octave.", True, None)
        self._dic['high_pitch_limit'] = TFSetting("High Pitch Limit", None, "E5", f"Pitch-underbound of your instrument(s). Supported formats {{'C4', 'C#4', 'Db4', 'C#4/Db4', 'Db4/C#4', 'C#/Db4', 'Db/C#4'}} '4' = central octave.", True, None)
        # TODO: Invent a color_scheme object, try a dictionary for this?
        self._dic['tone_color_scheme'] = TFSetting("Tone Color Scheme", None, dict(), f"The color scheme maps every tone to a color.", True, None)
        self._dic['show_gridlines'] = TFSetting("Show Gridlines", None, True, f"Toggle Gridlines during playback.", True, None)

        # TODO: This setting is probably way to difficult to implement, and not even usefull:
        self._dic['tone_flow_orientation'] = TFSetting("Flowing Direction", None, "Vertical", f"Flowing direction of the tones, either \'Vertical\' or \'Horizontal\'.", True, None)
        self._dic['overall_mute_play_along'] = TFSetting("Mute Play Along", None, True, f"Mute the song's audio while performing", True, None)

        # TODO: When saving a path to json make sure to do in platform indep fashion so that is is recoverable on other system, yet the config file is never meant to be ported across platform
        # TODO: Config file itself can not be saved to workspace, because one of it's props is the location of the workspace
        # TODO: Implement settings:

    # def add_setting(self, name_new_setting):
    #     """
    #     Fires async method to add a setting.
    #     :param name_new_setting:
    #     :return:
    #     """
    #     asynckivy.start(self.async_add_setting(name_new_setting))
    #
    # async def async_add_setting(self, name_new_setting):
    #     """
    #     Actual process to add a setting.
    #     :param name_new_setting:
    #     :return:
    #     """
    #     # Omit the provided explanation-text in case it was not omitted:
    #     name_new_setting = str(name_new_setting).replace(f"{TFSettings.EXPLANATION_PLAYLIST_NAME}", "")
    #
    #     # Check the name_new_setting by means of a regular expression:
    #     # Only allow names entirely consisting of alphanumeric characters, dashes and underscores
    #     if re.match("^[\w\d_-]+$", str(name_new_setting)):
    #         filename_setting = f"{str(name_new_setting)}.json"
    #         if len(list(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).glob(filename_setting))) > 0:
    #             toast(f"{name_new_setting} already exists")
    #         else:
    #             file_path = pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value / filename_setting)
    #             with open(str(file_path), "w") as json_file:
    #                 json_file.write("")
    #
    #             # TODO: async option doesn't work in combination with asynckivy.start() error is TypeError: '_asyncio.Future' object is not callable
    #             # async with open(str(file_path), 'w') as json_file:
    #             #     await json_file.write("")
    #
    #             toast(f"{name_new_setting} added")
    #     else:
    #         toast(f"Name cannot be empty nor contain{os.linesep}non-alphanumeric characters except for \"-_\")")
    #     await asynckivy.sleep(0)

    def edit_setting(self, setting_rowview, new_name_setting):
        """
        Fires async method to edit a setting.
        :param setting_rowview:
        :param new_name_setting:
        :return:
        """
        asynckivy.start(self.async_edit_setting(setting_rowview, new_name_setting))

    async def async_edit_setting(self, setting_rowview, new_name_setting):
        """
        Actual process to edit a setting.
        :param setting_rowview:
        :param new_name_setting:
        :return:
        """
        # Omit the provided explanation-text in case it was not omitted:
        new_name_setting = str(new_name_setting).replace(f"{TFSettings.EXPLANATION_PLAYLIST_NAME}", "")

        # Check the new_name_setting by means of a regular expression:
        # Only allow names entirely consisting of alphanumeric characters, dashes and underscores
        setting_to_edit = setting_rowview.setting_obj

        if re.match("^[\w\d_-]+$", str(new_name_setting)):
            filename_setting = f"{str(new_name_setting)}.json"
            if len(list(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).glob(filename_setting))) > 0:
                toast(f"{new_name_setting} already exists")

            elif setting_to_edit.file_path.exists():
                old_name = str(setting_to_edit.file_path.stem)
                file_path = pl.Path(setting_to_edit.file_path.parents[0] / filename_setting)
                pl.Path(setting_to_edit.file_path).rename(file_path)
                toast(f"{old_name} edited to {new_name_setting}")
            else:
                toast(f"Setting {setting_to_edit.file_path.stem} not found")
        else:
            toast(f"Name cannot be empty nor contain{os.linesep}non-alphanumeric characters except for \"-_\")")
        await asynckivy.sleep(0)

    def restore_factory_setting(self, setting_rowview, *args):
        """
        Fires async method to restore a setting.
        :param setting_rowview:
        :param args:
        :return:
        """
        asynckivy.start(self.async_restore_factory_setting(setting_rowview, *args))

    async def async_restore_factory_setting(self, setting_rowview, *args):
        """
        Actual process to restore a setting.
        :param setting_rowview:
        :param args:
        :return:
        """
        decision = args[0]
        setting_to_restore = setting_rowview.setting_obj

        if (str(decision).lower() == "restore"):

            setting_to_restore.value = setting_to_restore.default_value
            toast(f"{str(setting_to_restore.file_path.stem)} successfully restored")
        else:
            toast(f"Canceled restoration of factory setting for {str(setting_to_restore.name)}")
        await asynckivy.sleep(0)

    def clear_search_pattern(self):
        """
        Clear the search pattern in the filter.
        :return:
        """
        self.ids.search_field.text=""
        toast("Input cleared")
        # After the filter text is changed, the filter_editable_list() method is automatically triggered.

    def filter_editable_list(self):
        """
        Fires async method to filter the visual editable_list.
        :return:
        """
        asynckivy.start(self.async_editable_filter_list())

    async def async_editable_filter_list(self):
        """
        Filter the visual editable_list on the provided search pattern.
        :return:
        """
        search_pattern = CU.safe_cast(self.ids.search_field.text, str, "")
        # print(f"search pattern is {search_pattern}")
        self.ids.rv.data = []

        for tfsetting in self._editable_list:
            # Make sure that user can also search by entering a snippet of the value or the description.
            setting_name = f"{tfsetting.name}{str(tfsetting.value)}{str(tfsetting.description)}"
            if (len(search_pattern) == 0 or ((len(search_pattern) > 0) and (search_pattern.lower() in setting_name.lower()))):

                self.ids.rv.data.append(
                    {
                        "viewclass": "TFSettingRowView",
                        "list_obj": self,
                        "tfsetting_obj": tfsetting,
                        "callback": None
                    }
                )
        await asynckivy.sleep(0)

    def refresh_editable_list(self):
        """
        Fires async method to refresh the internal editable_list.
        :return:
        """
        # Clear existing editable_list<TFSetting>:
        self._editable_list.clear()

        asynckivy.start(self.async_refresh_editable_list())

    async def async_refresh_editable_list(self):
        """
        Scan the workspace-Settings folder for settings.
        :return:
        """
        # Sync alternative
        # [tfsetting for key, tfsetting in self._dic.items() if tfsetting.is_editable]

        # Depending on the amount of time it takes to run through the refresh, the spinner will be more/longer visible:
        for key, tf_setting in self._dic.items():
            if tf_setting.is_editable:
                self._editable_list.append(tf_setting)
            await asynckivy.sleep(0)

        # TODO: Make overscroll easier than it is now, in fact scrollbar should be always visible
        await self.async_editable_filter_list()
        self.ids.refresh_layout.refresh_done()

    # def show_dialog_add_setting(self):
    #     """
    #     Show a dialog to ask the name of the new setting.
    #     :return:
    #     """
    #     creation_time = datetime.now()
    #
    #     dialog_text = f"{TFSettings.EXPLANATION_PLAYLIST_NAME}" \
    #         f"Concert_{creation_time.year}{creation_time.month}{creation_time.day}-{creation_time.hour}{creation_time.minute}{creation_time.second}"
    #
    #     CU.show_input_dialog(title=f"Enter Name of New Setting",
    #                          hint_text=dialog_text,
    #                          text=dialog_text,
    #                          size_hint=(.7, .4),
    #                          text_button_ok="Add",
    #                          callback=lambda text_button, instance, *args: {self.add_setting(instance.text_field.text), self.refresh_editable_list()})

    def show_dialog_edit_setting(self, setting_rowview):
        """
        Show a dialog to ask for the new name of the setting.
        :param setting_rowview:
        :return:
        """
        pass
        # text = f"{TFSettings.EXPLANATION_PLAYLIST_NAME}" \
        #     f"{str(setting_rowview.setting_obj.file_path.stem)}"
        #
        # CU.show_input_dialog(title=f"Enter New Name for Setting",
        #                      hint_text=dialog_text,
        #                      text=text,
        #                      size_hint=(.7, .4),
        #                      text_button_ok="Update",
        #                      callback=lambda text_button, instance, *args, **kwargs: (self.edit_setting(setting_rowview, instance.text_field.text), self.refresh_editable_list()))

    def show_dialog_restore_factory_setting(self, setting_rowview):
        """
        Show a dialog to ask for confirmation of the removal.
        :param setting_rowview:
        :return:
        """
        text=f"Are you sure want to restore [color={get_hex_from_color(TFSettings.app.theme_cls.primary_color)}][b]{str(setting_rowview.setting_obj.file_path.stem)}[/b][/color] from the editable_list? This action cannot be undone."

        CU.show_ok_cancel_dialog(title=f"Are You Sure?",
                                 text=text,
                                 size_hint=(.7, .4),
                                 text_button_ok="Ok",
                                 text_button_cancel="Cancel",
                                 ok_callback_set=lambda *args, **kwargs: (self.restore_factory_setting(setting_rowview, args), self.refresh_editable_list()))

    def sort_editable_list(self):
        """
        Will sort the internal editable_list in alphabetic order.
        :return:
        """
        self.set_editable_list(sorted(self._editable_list, key=lambda setting: str(setting.file_path.stem)))
        self.filter_editable_list()
        toast("Settings sorted")

#########################################################################################################

