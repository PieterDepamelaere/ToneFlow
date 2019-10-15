# https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041

import os
import sys
import pathlib as pl
import json

from src.model.TFSetting import TFSetting

curr_file = pl.Path(os.path.realpath(__file__))

class TFSettings:
    def __init__(self):

        self.dic = dict()

        # Add new TFSetting-objects to dic (_name, _value, _default_value, _description="", _is_editable=False))
        self.dic['APP_NAME'] = TFSetting("Name of Application", None, str("ToneFlow" + u"\u00AE"), None, False)
        self.dic['MAJOR_MINOR_VERSION'] = TFSetting(f"{self.dic['APP_NAME'].value} Version MAJOR.MINOR", None, "0.1", "In theory, an update of the minor version alone shouldn't induce breaking changes.", False)
        self.dic['CONFIG_FILE_PATH'] = TFSetting("Path to Config File", None, curr_file.parents[2] / "Config_TF.json", None, False)
        self.dic['IMG_DIR_PATH'] = TFSetting("Internal Directory of Images", None, curr_file.parents[2] / "img", None, False)
        self.dic['WORKSPACE_NAME'] = TFSetting("Name of Workspace", None, "Workspace_TF", None, False)
        self.dic['FILE_SEP_TEXT'] = TFSetting("Exportable File Separator", None, "/FS/", None, False)
        self.dic['IMAGES_VIDEOS_DIR_NAME'] = TFSetting("Name of Images_Videos Folder in Workspace", None, "Images_Videos", None, False)
        self.dic['PLAYLISTS_DIR_NAME'] = TFSetting("Name of Playlists Folder in Workspace", None, "Playlists", None, False)
        self.dic['PREP_MIDI_DIR_NAME'] = TFSetting("Name of Prep_MIDI Folder in Workspace", None, "Prep_MIDI", None, False)
        self.dic['RAW_MIDI_DIR_NAME'] = TFSetting("Name of Raw_MIDI Folder in Workspace", None, "Raw_MIDI", None, False)
        self.dic['tf_workspace_path'] = TFSetting("Path to ToneFlow Workspace", None, curr_file.parents[3] / f"{self.dic['WORKSPACE_NAME'].value}", f"???{os.sep}{self.dic['WORKSPACE_NAME'].value} \t(Preferably path on external device like flash drive)", True)


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
        # TODO: Test what happens when missing:
        with open(f"{self.dic['CONFIG_FILE_PATH'].value}") as config_file:
            config_dic = json.load(config_file)

            for key in config_dic:
                self.dic[key].value = config_dic[key]['value']

            print("Parsing of the JSON-configfile was successful.")

    def create_load_tf_workspace(self, tf_workspace_path, tf_workspace_path_proposal):

        # Without whitespace the length of ans_user should be bigger than 0:
        if (tf_workspace_path is not None and str(tf_workspace_path).strip().__len__() > 0):
            tf_workspace_path = pl.Path(tf_workspace_path)
        else:
            # In case of trivial tf_workspace_path, the original proposal is used:
            tf_workspace_path = pl.Path(tf_workspace_path_proposal)

        # Make sure that tf_workspace_path is actually a Path-object:
        tf_workspace_path = pl.Path(tf_workspace_path)

        if (tf_workspace_path.is_file()):
            # If one would have specified a file, then the workspace will be created under its parent
            tf_workspace_path = tf_workspace_path.parents[0]

        # Check whether innermost subdirectory is already the workspace itself:
        if (tf_workspace_path.name != str(self.dic['WORKSPACE_NAME'].value)):
            tf_workspace_path = tf_workspace_path / self.dic['WORKSPACE_NAME'].value

        # Update the tf_workspace_path TFSetting:
        self.dic['tf_workspace_path'].value = tf_workspace_path

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