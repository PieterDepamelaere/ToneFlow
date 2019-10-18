import os
import sys
import pathlib as pl
curr_file = pl.Path(os.path.realpath(__file__))

sys.path.insert(0, str(curr_file.parents[0]))
sys.path.insert(0, str(curr_file.parents[1]))
sys.path.insert(0, str(curr_file.parents[2]))

# Below statement if you want to use the video player, do this before the kivy import!
os.environ['KIVY_VIDEO']='ffpyplayer'


import kivy
kivy.require('1.11.1') # replace with your current kivy version !
import pyperclip

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_hex_from_color

from kivymd.uix.navigationdrawer import NavigationDrawerIconButton
from kivymd.uix.dialog import MDDialog, MDInputDialog
from kivymd.theming import ThemeManager
from kivymd.toast import toast
from kivymd.color_definitions import palette

from src.main import *
from src.model.CommonUtils import CommonUtils as CU

class MainApp(App):
    """

    """
    title = CU.tfs.dic['APP_NAME'].value + " - v" + CU.tfs.dic['MAJOR_MINOR_VERSION'].value
    theme_cls = ThemeManager()
    theme_cls.primary_palette = "Brown"
    theme_cls.accent_palette = "LightGreen"
    theme_cls.theme_style = "Light"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.Window = Window


    def build(self):
        self.icon = str(pl.Path(CU.tfs.dic['IMG_DIR_PATH'].value) / "ToneFlow_Logo_TaskBarIcon.png")
        self.main_widget = Builder.load_file(str(curr_file.parents[1] / "view" / (curr_file.with_suffix(".kv")).name))
        # self.Window.bind(on_request_close= lambda x:self.on_stop())
        return self.main_widget

    def decide_stop_or_not(self, *args):
        if args[0] is not None:
            # print(f"args0 {str(args[0])}")
            if (CU.safe_cast(args[0], str, "")).lower() == "yes":
                self.stop()
            else:
                toast("Not quitting")
        else:
            toast("Not quitting")

    def on_pause(self):
        return True

    def on_start(self):
        # As a proposal, the actual (default)value of the tf_workspace_path-param is copied to the clipboard:
        workspace_path_proposal = CU.tfs.dic['tf_workspace_path'].default_value

        dialog_text = f"{CU.tfs.dic['tf_workspace_path'].description}"
        if (CU.tfs.dic['tf_workspace_path'].default_value != CU.tfs.dic['tf_workspace_path'].value):
            # This means that the user did configure a customized path:
            dialog_text =f"{CU.tfs.dic['tf_workspace_path'].value}"

        pyperclip.copy(str(workspace_path_proposal))
        self.show_example_input_dialog(title=f"Enter \"{CU.tfs.dic['WORKSPACE_NAME'].value}\"-Folder or its Parent Folder",
                                       hint_text=f"{CU.tfs.dic['tf_workspace_path'].description}",
                                       text=dialog_text,
                                       size_hint=(.8, .3), text_button_ok="Load/Create",
                                       callback=lambda text_button, instance: {CU.tfs.dic['tf_workspace_path'].set_value(instance.text_field.text),
                                                                               toast(str(CU.tfs.dic['tf_workspace_path'].value))})


    def on_stop(self, *kwargs):
        self.show_cancel_dialog(title="Confirmation dialog", text=f"Are you sure you want to [color={get_hex_from_color(self.theme_cls.primary_color)}][b]quit[/b][/color] {CU.tfs.dic['APP_NAME'].value}?", size_hint=(0.5, 0.3), text_button_ok="Yes", text_button_cancel="No", callback=self.decide_stop_or_not)

    def open_settings(self, *args):
        # TODO: Experiment in later stage with kivy settings, because it might ruin the setup
        return False

    def set_color(self):
        pass

    def set_title_toolbar(self, title):
        """Set string title in MDToolbar for the whole application."""
        self.main_widget.ids.toolbar.title = title

    def show_cancel_dialog(self, title, text, size_hint=(.8, .4), text_button_ok="Ok", text_button_cancel="Cancel", callback=None):
        ok_cancel_dialog = MDDialog(
                title=title,
                size_hint=size_hint,
                text=text,
                text_button_ok=text_button_ok,
                text_button_cancel=text_button_cancel,
                events_callback=callback
            )
        ok_cancel_dialog.open()

    def show_example_input_dialog(self, title="Please Enter", hint_text=None, text="Type here", size_hint=(.8, .4), text_button_ok="Ok", callback=None):
        dialog = MDInputDialog(
            title=title,
            hint_text=hint_text,
            size_hint=size_hint,
            text_button_ok=text_button_ok,
            events_callback=callback)
        dialog.text_field.text = text
        dialog.open()

    def show_screen(self, name_screen):
        pass

if __name__ == "__main__":
    if(CU.tfs.dic['CONFIG_FILE_PATH'].value.exists()):
        # If the config-file exists, then try to import it:
        CU.tfs.import_tf_settings_from_config()
    else:
        # Else, when the config-file is absent, then export (a new) one:
        CU.tfs.export_tf_settings_to_config()

    mapp = MainApp()
    mapp.run()

    CU.tfs.export_tf_settings_to_config()