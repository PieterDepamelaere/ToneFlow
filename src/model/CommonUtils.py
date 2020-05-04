import os
import sys
import pathlib as pl
curr_file = pl.Path(os.path.realpath(__file__))

sys.path.insert(0, str(curr_file.parents[0]))
sys.path.insert(0, str(curr_file.parents[1]))
sys.path.insert(0, str(curr_file.parents[2]))

from functools import partial
from kivy.app import App
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import *


class CommonUtils:

    # App
    app = None

    # ToneFlower-instance
    tf = None

    # TFSettings-instance
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
    def show_ok_cancel_dialog(title, text, size_hint=(.8, .4), text_button_ok="OK", text_button_cancel="CANCEL", callback=None):

        # TODO: Eliminate Quick Fix code, initialisation of app should happen somwhere else
        if CommonUtils.app is None:
            CommonUtils.app = App.get_running_app()

        ok_cancel_dialog = MDDialog(
            title=title,
            type= 'simple', # Options are: ‘alert’, ‘simple’, ‘confirmation’, ‘custom’
            size_hint=size_hint,
            text=text,
            buttons=[
                MDFillRoundFlatButton(text=text_button_ok.upper(), md_bg_color= CommonUtils.App.theme_cls.primary_color, on_release= lambda *args, **kwargs: callback(args, kwargs)),
                # MDRaisedButton (text, md_bg_color),

                MDRoundFlatButton(text=text_button_cancel.upper(), text_color= CommonUtils.App.theme_cls.primary_color)
                # MDFlatButton()
            ]

            #events_callback=callback
        )
        ok_cancel_dialog.open()
        return ok_cancel_dialog

    @staticmethod
    def show_input_dialog(title="Please Enter", content_cls=None, size_hint=(.8, .4), text_button_ok="OK", text_button_cancel="CANCEL", callback_set=None):

        # TODO: Eliminate Quick Fix code, initialisation of app should happen somewhere else
        if CommonUtils.app is None:
            CommonUtils.app = App.get_running_app()

        input_dialog = MDDialog(
            title=title,
            type='custom',  # Type 'custom' is needed to be able to provide content class. Options are: ‘alert’, ‘simple’, ‘confirmation’, ‘custom’
            content_cls=content_cls(),
            size_hint=size_hint,

            buttons=[
                MDFillRoundFlatButton(text=text_button_ok.upper(), md_bg_color=CommonUtils.app.theme_cls.primary_color,
                                      on_release=lambda *args, **kwargs: (callback_set(*args, **kwargs), print("wow inside"), input_dialog.dismiss())),
                # MDRaisedButton (text, md_bg_color),

                MDRoundFlatButton(text=text_button_cancel.upper(), text_color=CommonUtils.app.theme_cls.primary_color, on_release=lambda *args, **kwargs: input_dialog.dismiss())
                # MDFlatButton()
            ]

            # events_callback=callback
        )
        # input_dialog.text_field.text = text


        input_dialog.open()

        print(input_dialog.content_cls.ids.city_field.text)


        return input_dialog

    @staticmethod
    def split_letters_from_digits(text):

        letter_text = ''
        digit_text = ''

        for character in text:
            if(character.isdigit()):
                digit_text.join(character)
            else:
                letter_text.join(character)

        return letter_text, digit_text


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