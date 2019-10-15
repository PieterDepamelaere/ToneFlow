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
        self.dic['CONFIG_FILE_PATH'] = TFSetting("Path to Config File", None, curr_file.parents[2] / "Config_TF.json", None, True)
        self.dic['IMG_DIR'] = TFSetting("Internal Directory of Images", None, str(curr_file.parents[2]) + f"{os.sep}img{os.sep}", None, False)
        self.dic['WORKSPACE_NAME'] = TFSetting("Name of Workspace", None, "Workspace_TF", None, False)
        self.dic['IMAGES_VIDEOS_DIR_NAME'] = TFSetting("Name of Images_Videos Folder in Workspace", None, "Images_Videos", None, False)
        self.dic['PLAYLISTS_DIR_NAME'] = TFSetting("Name of Playlists Folder in Workspace", None, "Playlists", None, False)
        self.dic['PREP_MIDI_DIR_NAME'] = TFSetting("Name of Prep_MIDI Folder in Workspace", None, "Prep_MIDI", None, False)
        self.dic['RAW_MIDI_DIR_NAME'] = TFSetting("Name of Raw_MIDI Folder in Workspace", None, "Raw_MIDI", None, False)
        self.dic['tf_workspace'] = TFSetting("ToneFlow Workspace", None, str(pl.Path(curr_file.parents[3] / f"{self.dic['WORKSPACE_NAME'].value}")), f"???{os.sep}{self.dic['WORKSPACE_NAME'].value} \t(Preferably path on external device like flash drive)", True)


        # self.tf_workspace=None
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

        with open(f"{self.dic['CONFIG_FILE_PATH'].value}", 'w') as file:
            # Only dump editable properties
            json.dump({k: v for k, v in self.dic.items() if v.is_editable}, fp=file, default=lambda s: s.to_json(), indent=4,
                   sort_keys=True)

    def import_tf_settings_from_config(self):
        pass

        # TODO: Implement properly
        # if ():
        #
        #     # loading existing json_config_file
        #     if (args["json_config_file"] is not None):
        #         interactive_mode = False
        #         with open(args["json_config_file"]) as config_file:
        #             data = json.load(config_file)
        #
        #         # Default values:
        #     local_workspace = None
        #     decision_use_existing_model = False
        #     existing_model_weights = None
        #     continue_training = True
        #     original_local_img_data = None
        #     original_local_lbl_data = None
        #     scale_factor = 1
        #     batch_size = 64
        #     epochs = 0
        #     run_description = None
        #     IMAGE_EXTENSION = ".bmp"
        #     upperbound_histogram = 122.0
        #     max_target_label_pred_plot = 125
        #
        #     if data is not None:
        #         # Parse the data to according variables:
        #
        #         local_workspace = pl.Path(data["local_workspace"])
        #         decision_use_existing_model = Main.str_to_bool(data["decision_use_existing_model"])
        #         existing_model_weights = pl.Path(data["existing_model_weights"])
        #         continue_training = Main.str_to_bool(data["continue_training"])
        #         original_local_img_data = pl.Path(data["original_local_img_data"])
        #         original_local_lbl_data = pl.Path(data["original_local_lbl_data"])
        #         scale_factor = data["scale_factor"]
        #         batch_size = data["batch_size"]
        #         epochs = data["epochs"]
        #         run_description = data["run_description"]
        #         IMAGE_EXTENSION = data["IMAGE_EXTENSION"]
        #         upperbound_histogram = data["upperbound_histogram"]
        #         max_target_label_pred_plot = data["max_target_label_pred_plot"]
        #
        #         print("Parsing of the JSON-configfile was successfully")
        #
        # else:


    def create_load_tf_workspace(self, tf_workspace, workspace_path_proposal):

        # Without whitespace the length of ans_user should be bigger than 0:
        if (tf_workspace is not None and str(tf_workspace).strip().__len__() > 0):
            tf_workspace = pl.Path(tf_workspace)
        else:
            # In case of trivial tf_workspace, the original proposal is used:
            tf_workspace = pl.Path(workspace_path_proposal)

        # Make sure that tf_workspace is actually a Path-object:
        tf_workspace = pl.Path(tf_workspace)

        if (tf_workspace.is_file()):
            # If one would have specified a file, then the workspace will be created under its parent
            tf_workspace = tf_workspace.parents[0]

        # Check whether innermost subdirectory is already the workspace itself:
        if (tf_workspace.name != str(self.dic['WORKSPACE_NAME'].value)):
            tf_workspace = tf_workspace / self.dic['WORKSPACE_NAME'].value

        # Update the tf_workspace TFSetting:
        self.dic['tf_workspace'].value = tf_workspace
        # TODO: Will I save paths platform indep as string or? => It needs to be human readible as setting, only when exporting fileseparators need to be converted to {FILESEP} for example

        # Create tf_workspace in case it doesn't exist yet, when it did, it doesn't get overridden:
        images_videos_dir = tf_workspace / self.dic['IMAGES_VIDEOS_DIR_NAME'].value
        playlists_dir = tf_workspace / self.dic['PLAYLISTS_DIR_NAME'].value
        prep_midi_dir = tf_workspace / self.dic['PREP_MIDI_DIR_NAME'].value
        raw_midi_dir = tf_workspace / self.dic['RAW_MIDI_DIR_NAME'].value

        # There's no explicit creation of the tf_workspace folder itself because parents will be auto-created, while creating its children:
        images_videos_dir.mkdir(exist_ok=True, parents=True)
        playlists_dir.mkdir(exist_ok=True, parents=True)
        prep_midi_dir.mkdir(exist_ok=True, parents=True)
        raw_midi_dir.mkdir(exist_ok=True, parents=True)

        # TODO: Load workspace (playlists, songcollection)