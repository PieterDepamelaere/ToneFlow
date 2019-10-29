# https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041

import os
import sys
import pathlib as pl
import json
from kivy.uix.screenmanager import Screen

from src.model.TFSetting import TFSetting
from src.model.PlayList import PlayList
from src.model.PlayLists import PlayLists
from src.model.Songs import Songs

curr_file = pl.Path(os.path.realpath(__file__))

class TFSettings(Screen):
    def __init__(self, **kwargs):
        super(TFSettings, self).__init__(name=type(self).__name__, **kwargs)
        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a list of callbacks
        self._context_menus = list()

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
        self.dic['PREP_MIDI_DIR_NAME'] = TFSetting("Name of Prep_MIDI Folder in Workspace", None, "Prep_MIDI", None, False, None)
        self.dic['RAW_MIDI_DIR_NAME'] = TFSetting("Name of Raw_MIDI Folder in Workspace", None, "Raw_MIDI", None, False, None)
        self.dic['SCREEN_HELP_CLASS'] = TFSetting("Help", None, None, False, None)
        self.dic['SCREEN_PLAYLIST_CLASS'] = TFSetting("Lineup", None, PlayList, False, None)
        self.dic['SCREEN_PLAYLISTS_CLASS'] = TFSetting("Playlists", None, PlayLists, False, None)
        self.dic['SCREEN_SETTINGS_CLASS'] = TFSetting("Settings", None, TFSettings, False, None)
        self.dic['SCREEN_SONGS_CLASS'] = TFSetting("Songs", None, Songs, False, None)

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