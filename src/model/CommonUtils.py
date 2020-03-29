import os
import sys
import pathlib as pl
curr_file = pl.Path(os.path.realpath(__file__))

sys.path.insert(0, str(curr_file.parents[0]))
sys.path.insert(0, str(curr_file.parents[1]))
sys.path.insert(0, str(curr_file.parents[2]))

from functools import partial
from kivymd.uix.dialog import MDDialog, MDInputDialog


class CommonUtils:

    # tfs
    tfs = None

    # dic_screen_switch = {
    #
    #     Songs: partial(Songs.refresh_list, object())
    #     # ,"Songs": partial(SwitchMain.change_local_paths),
    #     # "Settings": partial(SwitchMain.change_online_paths)
    #
    #     # # "3": partial(SwitchMain.download_data),
    #     # # "4": partial(SwitchMain.investigate_data_imbalance),
    #     # "5": partial(CU_Main.Main.split_merge_train_validation_test_sets, local_workspace),
    #     # "6": partial(SwitchMain.generate_fourier_images, local_workspace),
    #     #
    #     # # Resize a folder of images (deep copy)
    #     # "7": partial(CU_Main.Main.resize_img_in_folder, local_workspace, SwitchMain.IMAGE_EXTENSION),
    #     #
    #     # # Resize a folder of images (deep copy)
    #     # "8": partial(CU_Main.Main.prepend_unique_indices_to_img_folder, local_workspace,
    #     #              SwitchMain.IMAGE_EXTENSION),
    #     #
    #     # # "9": partial(SwitchMain.start_training_NN),
    #     # # "10": partial(SwitchMain.start_TensorBoard),
    #     #
    #     # "11": partial(SwitchMain.generate_plot_predictions, local_workspace),
    #     #
    #     # "12": partial(SwitchMain.create_backup_all_trained_models_in_path, local_workspace),
    #     #
    #     # "13": partial(SwitchMain.create_keras_plot_of_model, local_workspace)
    # }

    @staticmethod
    def safe_cast(val, to_type, default=None):
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def show_ok_cancel_dialog(title, text, size_hint=(.8, .4), text_button_ok="Ok", text_button_cancel="Cancel", callback=None):
        ok_cancel_dialog = MDDialog(
            title=title,
            size_hint=size_hint,
            text=text,
            text_button_ok=text_button_ok,
            text_button_cancel=text_button_cancel,
            events_callback=callback
        )
        ok_cancel_dialog.open()
        return ok_cancel_dialog

    @staticmethod
    def show_input_dialog(title="Please Enter", hint_text=None, text="Type here", size_hint=(.8, .4), text_button_ok="Ok", callback=None):
        input_dialog = MDInputDialog(
            title=title,
            hint_text=hint_text,
            size_hint=size_hint,
            text_button_ok=text_button_ok,
            events_callback=callback)
        input_dialog.text_field.text = text
        input_dialog.open()
        return input_dialog

    @staticmethod
    def with_consistent_linesep(text):
        """
        Making lineseparators consistent, no matter what machine ToneFlow is run on.
        :param text:
        :return:
        """
        text = CommonUtils.safe_cast(text, str, "")
        # It turns out that when an input is received from a textfield (in a inputdialog) enters are always returned as \n, whilst running ToneFlow on a Windows machine, one would expect \r\n, therefore conversion:
        text = text.replace(f"\r\n", f"{os.linesep}")
        # Old Apple-compatibility (now, it also uses \n like linux):
        text = text.replace(f"\r", f"{os.linesep}")
        # Windows-compatibility (allows to change \n into \r\n):
        text = text.replace(f"\n", f"{os.linesep}")
        return text

    # @classmethod
    # def switch_screen(cls, choice):
    #     """
    #     Python mechanism to mimic a switch-case-structure, that activates the execution of the intended method.
    #     :param choice: The choice of the user.
    #     :return: the result of the invoked function.
    #     """
    #
    #     func = cls.dic_screen_switch.get(choice, lambda: "ERROR: Unvalid choice")
    #     return func()