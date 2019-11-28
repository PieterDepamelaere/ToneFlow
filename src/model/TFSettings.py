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
from kivy.metrics import dp
from kivy.utils import get_hex_from_color
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty

from kivymd.utils import asynckivy
from kivymd.toast import toast

from src.model.TFSetting import TFSetting
from src.model.PlayList import PlayList
from src.model.PlayLists import PlayLists
from src.model.Songs import Songs

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.CommonUtils import CommonUtils as CU

class TFSettings(Screen):

    app = None
    EXPLANATION_PLAYLIST_NAME = f"(Only alphanumeric characters & \"_-\", leave blank to cancel.){os.linesep}"

    def __init__(self, **kwargs):
        super(TFSettings, self).__init__(name=type(self).__name__, **kwargs)
        Builder.load_file(str(curr_file.parents[1] / "view" / (pl.Path(TFSettings.__name__).with_suffix(".kv")).name))
        TFSettings.app = App.get_running_app()
        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a dict of callbacks
        self._context_menus = {"Clear Input": lambda x: {self.clear_search_pattern()},
                               "Sort Settings": lambda x: {self.sort_list()},
                               "Refresh": lambda x: {self.refresh_list(), toast(f"Refreshed")},
                               "Restore Factory Settings": lambda x: toast("TODO: WIP"),
                               "Help": lambda x: toast("TODO: WIP")}
        # TODO: Implement the other context menus

        self.dic = dict()

        # Add new TFSetting-objects to dic (_name, _value, _default_value, _description="", _is_editable=False, _callback_on_set=None))
        self.dic['APP_NAME'] = TFSetting("Name of Application", None, str("ToneFlow" + u"\u00AE"), None, False, None)
        self.dic['MAJOR_MINOR_VERSION'] = TFSetting(f"{self.dic['APP_NAME'].value} Version MAJOR.MINOR", None, "0.1", "In theory, an update of the minor version alone shouldn't induce breaking changes.", False, None)
        self.dic['CONFIG_FILE_PATH'] = TFSetting("Path to Config File", None, curr_file.parents[2] / "Config_TF.json", None, False, None)
        self.dic['IMG_DIR_PATH'] = TFSetting("Internal Directory of Images", None, curr_file.parents[2] / "img", None, False, None)
        self.dic['WORKSPACE_NAME'] = TFSetting("Name of Workspace", None, "Workspace_TF", None, False, None)
        self.dic['FILE_SEP_TEXT'] = TFSetting("Exportable File Separator", None, "/FS/", None, False, None)
        self.dic['IMAGES_VIDEOS_DIR_NAME'] = TFSetting("Name of Images_Videos Folder in Workspace", None, "Images_Videos", None, False, None)
        self.dic['PLAYLISTS_DIR_NAME'] = TFSetting("Name of Playlists Folder in Workspace", None, "Playlists", None, False, None)
        self.dic['PREP_MIDI_DIR_NAME'] = TFSetting("Name of Prep_MIDI Folder in Workspace", None, "Songs_Prep_MIDI", None, False, None)
        self.dic['RAW_MIDI_DIR_NAME'] = TFSetting("Name of Raw_MIDI Folder in Workspace", None, "Songs_Raw_MIDI", None, False, None)
        self.dic['SCREEN_HELP_CLASS'] = TFSetting("Help", None, None, False, None)
        self.dic['SCREEN_PLAYLIST_CLASS'] = TFSetting("Lineup", None, PlayList, False, None)
        self.dic['SCREEN_PLAYLISTS_CLASS'] = TFSetting("Playlists", None, PlayLists, False, None)
        self.dic['SCREEN_SETTINGS_CLASS'] = TFSetting("Settings", None, TFSettings, False, None)
        self.dic['SCREEN_SONGS_CLASS'] = TFSetting("Songs", None, Songs, False, None)
        self.dic['THEME_BACKGROUND_HUE'] = TFSetting("Background hue influencing text color", None, '500', False, None)

        # User editable ones:
        self.dic['tf_workspace_path'] = TFSetting("Path to ToneFlow Workspace", None, curr_file.parents[3] / f"{self.dic['WORKSPACE_NAME'].value}", f"???{os.sep}{self.dic['WORKSPACE_NAME'].value} \t(Preferably path on external device like flash drive)", True, lambda value: self.cb_create_load_tf_workspace(value))

        # TODO: When saving a path to json make sure to do in platform indep fashion so that is is recoverable on other system, yet the config file is never meant to be ported across platform
        # TODO: Config file itself can not be saved to workspace, because one of it's props is the location of the workspace
        # TODO: Implement settings:
        # overall_speedfactor
        # low_pitch_limit
        # high_pitch_limit
        # tone_color_sheme
        # show_gridlines_concert_mode
        # tone_flow_direction
        # _overall_mute_play_along

    def get_list(self):
        return self._list

    def set_list(self, list):
        list = CU.safe_cast(list, self._list.__class__, "")
        self._list = list

    def get_context_menus(self):
        return self._context_menus

    list = property(get_list, set_list)
    context_menus = property(get_context_menus)

    def cb_create_load_tf_workspace(self, tf_workspace_path):

        # Without whitespace the length of ans_user should be bigger than 0, also make sure that when the tf_workspace_path's description is returned, that :
        if ((tf_workspace_path is not None) and (len(str(tf_workspace_path).strip()) > 0) and (str(tf_workspace_path) != self.dic['tf_workspace_path'].description)):
            tf_workspace_path = pl.Path(tf_workspace_path)
        else:
            # In case of trivial tf_workspace_path, the original proposal is used:
            tf_workspace_path = self.dic['tf_workspace_path'].default_value

        # Make sure that tf_workspace_path is actually a Path-object:
        tf_workspace_path = pl.Path(tf_workspace_path)

        if (tf_workspace_path.is_file()):
            # If one would have specified a file, then the workspace will be created under its parent
            tf_workspace_path = tf_workspace_path.parents[0]

        # Check whether innermost subdirectory is already the workspace itself:
        if (tf_workspace_path.name != str(self.dic['WORKSPACE_NAME'].value)):
            tf_workspace_path = tf_workspace_path / self.dic['WORKSPACE_NAME'].value

        # Create tf_workspace_path in case it doesn't exist yet, when it did, it doesn't get overridden:
        images_videos_dir = tf_workspace_path / self.dic['IMAGES_VIDEOS_DIR_NAME'].value
        playlists_dir = tf_workspace_path / self.dic['PLAYLISTS_DIR_NAME'].value
        prep_midi_dir = tf_workspace_path / self.dic['PREP_MIDI_DIR_NAME'].value
        raw_midi_dir = tf_workspace_path / self.dic['RAW_MIDI_DIR_NAME'].value

        # There's no explicit creation of the tf_workspace_path folder itself because parents will be auto-created, while creating its children:
        images_videos_dir.mkdir(exist_ok=True, parents=True)
        playlists_dir.mkdir(exist_ok=True, parents=True)
        prep_midi_dir.mkdir(exist_ok=True, parents=True)
        raw_midi_dir.mkdir(exist_ok=True, parents=True)

        # TODO: Load workspace (playlists, songcollection)

        # Finally return the value to set in the setter (Because there's a chance that it got modified along the way):
        return pl.Path(tf_workspace_path)

    def export_tf_settings_to_config(self):
        with open(f"{self.dic['CONFIG_FILE_PATH'].value}", 'w') as config_file:
            # Only dump editable properties
            json.dump({k: v for k, v in self.dic.items() if v.is_editable}, fp=config_file, default=lambda s: s.to_json(), indent=4,
                   sort_keys=True)

    def import_tf_settings_from_config(self):
        with open(f"{self.dic['CONFIG_FILE_PATH'].value}") as config_file:
            config_dic = json.load(config_file)

            for key in config_dic:
                self.dic[key].value = config_dic[key]['value']

            print("Parsing of the JSON-configfile was successful.")

    def add_setting(self, name_new_setting):
        """
        Fires async method to add a setting.
        :param name_new_setting:
        :return:
        """
        asynckivy.start(self.async_add_setting(name_new_setting))

    async def async_add_setting(self, name_new_setting):
        """
        Actual process to add a setting.
        :param name_new_setting:
        :return:
        """
        # Omit the provided explanation-text in case it was not omitted:
        name_new_setting = str(name_new_setting).replace(f"{TFSettings.EXPLANATION_PLAYLIST_NAME}", "")

        # Check the name_new_setting by means of a regular expression:
        # Only allow names entirely consisting of alphanumeric characters, dashes and underscores
        if re.match("^[\w\d_-]+$", str(name_new_setting)):
            filename_setting = f"{str(name_new_setting)}.json"
            if len(list(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).glob(filename_setting))) > 0:
                toast(f"{name_new_setting} already exists")
            else:
                file_path = pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value / filename_setting)
                with open(str(file_path), "w") as json_file:
                    json_file.write("")

                # TODO: async option doesn't work in combination with asynckivy.start() error is TypeError: '_asyncio.Future' object is not callable
                # async with open(str(file_path), 'w') as json_file:
                #     await json_file.write("")

                toast(f"{name_new_setting} added")
        else:
            toast(f"Name cannot be empty nor contain{os.linesep}non-alphanumeric characters except for \"-_\")")
        await asynckivy.sleep(0)

    def rename_setting(self, setting_rowview, new_name_setting):
        """
        Fires async method to rename a setting.
        :param setting_rowview:
        :param new_name_setting:
        :return:
        """
        asynckivy.start(self.async_rename_setting(setting_rowview, new_name_setting))

    async def async_rename_setting(self, setting_rowview, new_name_setting):
        """
        Actual process to rename a setting.
        :param setting_rowview:
        :param new_name_setting:
        :return:
        """
        # Omit the provided explanation-text in case it was not omitted:
        new_name_setting = str(new_name_setting).replace(f"{TFSettings.EXPLANATION_PLAYLIST_NAME}", "")

        # Check the new_name_setting by means of a regular expression:
        # Only allow names entirely consisting of alphanumeric characters, dashes and underscores
        setting_to_rename = setting_rowview.setting_obj

        if re.match("^[\w\d_-]+$", str(new_name_setting)):
            filename_setting = f"{str(new_name_setting)}.json"
            if len(list(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).glob(filename_setting))) > 0:
                toast(f"{new_name_setting} already exists")

            elif setting_to_rename.file_path.exists():
                old_name = str(setting_to_rename.file_path.stem)
                file_path = pl.Path(setting_to_rename.file_path.parents[0] / filename_setting)
                pl.Path(setting_to_rename.file_path).rename(file_path)
                toast(f"{old_name} renamed to {new_name_setting}")
            else:
                toast(f"Setting {setting_to_rename.file_path.stem} not found")
        else:
            toast(f"Name cannot be empty nor contain{os.linesep}non-alphanumeric characters except for \"-_\")")
        await asynckivy.sleep(0)

    def remove_setting(self, setting_rowview, *args):
        """
        Fires async method to remove a setting.
        :param setting_rowview:
        :param args:
        :return:
        """
        asynckivy.start(self.async_remove_setting(setting_rowview, *args))

    async def async_remove_setting(self, setting_rowview, *args):
        """
        Actual process to remove a setting.
        :param setting_rowview:
        :param args:
        :return:
        """
        decision = args[0]
        setting_to_delete = setting_rowview.setting_obj

        if (str(decision).lower() == "remove"):
            self._list.remove(setting_to_delete)

            file_path_to_delete = setting_to_delete.file_path
            if (file_path_to_delete.exists() and file_path_to_delete.is_file()):
                pl.Path(file_path_to_delete).unlink()
            toast(f"{str(setting_to_delete.file_path.stem)} successfully removed")
        else:
            toast(f"Canceled removal of {str(setting_to_delete.file_path.stem)}")
        await asynckivy.sleep(0)

    def clear_search_pattern(self):
        """
        Clear the search pattern in the filter.
        :return:
        """
        self.ids.search_field.text=""
        toast("Input cleared")
        # After the filter text is changed, the filter_list() method is automatically triggered.

    def filter_list(self):
        """
        Fires async method to filter the visual list.
        :return:
        """
        asynckivy.start(self.async_filter_list())

    async def async_filter_list(self):
        """
        Filter the visual list on the provided search pattern.
        :return:
        """
        search_pattern = CU.safe_cast(self.ids.search_field.text, str, "")
        # print(f"search pattern is {search_pattern}")
        self.ids.rv.data = []

        for setting in self._list:
            setting_name = str(setting.file_path.stem)
            if (len(search_pattern) == 0 or ((len(search_pattern) > 0) and (search_pattern.lower() in setting_name.lower()))):

                self.ids.rv.data.append(
                    {
                        "viewclass": "TFSettingRowView",
                        "list_obj": self,
                        "setting_obj": setting,
                        "callback": None
                    }
                )
        await asynckivy.sleep(0)

    def refresh_list(self):
        """
        Fires async method to refresh the internal list.
        :return:
        """
        # Clear existing list<TFSetting>:
        self._list.clear()

        asynckivy.start(self.async_refresh_list())

    async def async_refresh_list(self):
        """
        Scan the workspace-Settings folder for settings.
        :return:
        """
        # Depending on the amount of time it takes to run through the refresh, the spinner will be more/longer visible:
        for file_path in pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).rglob("*.json"):

            setting = TFSetting(file_path)

            self._list.append(setting)
            await asynckivy.sleep(0)

        # TODO: Make overscroll easier than it is now, in fact scrollbar should be always visible
        await self.async_filter_list()
        self.ids.refresh_layout.refresh_done()

    def show_dialog_add_setting(self):
        """
        Show a dialog to ask the name of the new setting.
        :return:
        """
        creation_time = datetime.now()

        dialog_text = f"{TFSettings.EXPLANATION_PLAYLIST_NAME}" \
            f"Concert_{creation_time.year}{creation_time.month}{creation_time.day}-{creation_time.hour}{creation_time.minute}{creation_time.second}"

        CU.show_input_dialog(title=f"Enter Name of New Setting",
                             hint_text=dialog_text,
                             text=dialog_text,
                             size_hint=(.6, .4),
                             text_button_ok="Add",
                             callback=lambda text_button, instance, *args: {self.add_setting(instance.text_field.text), self.refresh_list()})

    def show_dialog_rename_setting(self, setting_rowview):
        """
        Show a dialog to ask for the new name of the setting.
        :param setting_rowview:
        :return:
        """
        dialog_text = f"{TFSettings.EXPLANATION_PLAYLIST_NAME}" \
            f"{str(setting_rowview.setting_obj.file_path.stem)}"

        CU.show_input_dialog(title=f"Enter New Name for Setting",
                             hint_text=dialog_text,
                             text=dialog_text,
                             size_hint=(.6, .4),
                             text_button_ok="Update",
                             callback=lambda text_button, instance, *args: {self.rename_setting(setting_rowview, instance.text_field.text), self.refresh_list()})

    def show_dialog_remove_setting(self, setting_rowview):
        """
        Show a dialog to ask for confirmation of the removal.
        :param setting_rowview:
        :return:
        """
        dialog_text=f"Are you sure want to remove [color={get_hex_from_color(TFSettings.app.theme_cls.primary_color)}][b]{str(setting_rowview.setting_obj.file_path.stem)}[/b][/color] from the list? This action cannot be undone."

        CU.show_ok_cancel_dialog(title=f"Are You Sure?",
                                 text=dialog_text,
                                 size_hint=(.6, .4),
                                 text_button_ok="Remove",
                                 text_button_cancel="Cancel",
                                 callback=lambda *args: {self.remove_setting(setting_rowview, *args), self.refresh_list()})

    def sort_list(self):
        """
        Will sort the internal list in alphabetic order.
        :return:
        """
        self.set_list(sorted(self._list, key=lambda setting: str(setting.file_path.stem)))
        self.filter_list()
        toast("Settings sorted")

#########################################################################################################

