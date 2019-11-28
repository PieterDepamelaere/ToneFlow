import os
import sys
import time
import traceback
import pathlib as pl

curr_file = pl.Path(os.path.realpath(__file__))

sys.path.insert(0, str(curr_file.parents[0]))
sys.path.insert(0, str(curr_file.parents[1]))
sys.path.insert(0, str(curr_file.parents[2]))

# Below statement if you want to use the video player, do this before the kivy import!
os.environ['KIVY_VIDEO']='ffpyplayer'

import kivy
kivy.require('1.11.1') # replace with your current kivy version!
import pyperclip

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_hex_from_color
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivymd.utils import asynckivy
from kivymd.uix.navigationdrawer import NavigationDrawerIconButton
from kivymd.theming import ThemeManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivymd.color_definitions import palette

from src.main.TFExceptionHandler import TFExceptionHandler
from src.model.CommonUtils import CommonUtils as CU
from src.model.TFSettings import TFSettings

from kivy.base import ExceptionManager


class MainApp(App):
    """

    """
    # Foresee custom handling of errors, user can bypass them (maybe own mistake) or quit the app, but he sees pop up of the error:
    ExceptionManager.add_handler(TFExceptionHandler())

    theme_cls = ThemeManager()
    theme_cls.primary_palette = "Brown"
    theme_cls.accent_palette = "LightGreen"
    theme_cls.theme_style = "Light"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create ToneFlow-settings object and corresponding settings:
        CU.tfs = TFSettings()
        Builder.load_file(str(curr_file.parents[1] / "view" / (pl.Path(TFSettings.__name__).with_suffix(".kv")).name))

        self._exception_counter = 0
        self._context_menus = None
        MainApp.title = CU.tfs.dic['APP_NAME'].value + " - v" + CU.tfs.dic['MAJOR_MINOR_VERSION'].value

        # self.Window = Window

    def build(self):
        self.icon = str(pl.Path(CU.tfs.dic['IMG_DIR_PATH'].value) / "ToneFlow_Logo_TaskBarIcon.png")
        self.main_widget = Builder.load_file(str(curr_file.parents[1] / "view" / (curr_file.with_suffix(".kv")).name))
        # self.Window.bind(on_request_close= lambda x:self.on_stop())

        self.main_widget.ids.scr_mngr.add_widget(CU.tfs)

        return self.main_widget

    def create_uninstantiated_screen(self, screen_class):
        class_name = screen_class.__name__
        Builder.load_file(str(curr_file.parents[1] / "view" / (pl.Path(class_name).with_suffix(".kv")).name))
        screen_object = screen_class()
        return screen_object

    def decide_stop_or_not(self, *args):
        # TODO: Stop warning is not shown yet when you close via closing the window by itself.
        if args[0] is not None:
            # print(f"args0 {str(args[0])}")
            if (CU.safe_cast(args[0], str, "")).lower() == "yes":
                self.stop()
            else:
                toast("Not quitting")
        else:
            toast("Not quitting")

    def get_context_menus(self):
        return self._context_menus

    def set_context_menus(self, items):
        # Depending on the screen other context oriented options should appear under the three vertical dots
        if (items is not None):
            self._context_menus = [
                {
                    "viewclass": "MDMenuItem",
                    "text": f"{key}",
                    "callback": items[key]
                }
                for key in items
            ]
        else:
            self._context_menus = None

    context_menus = property(get_context_menus, set_context_menus)

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
        CU.show_input_dialog(title=f"Enter Path to \"{CU.tfs.dic['WORKSPACE_NAME'].value}\"-Folder or to its Parent Folder",
                               hint_text=f"{CU.tfs.dic['tf_workspace_path'].description}",
                               text=dialog_text,
                               size_hint=(.8, .4), text_button_ok="Load/Create",
                               callback=lambda text_button, instance: {CU.tfs.dic['tf_workspace_path'].set_value(instance.text_field.text),
                                                                               toast(str(CU.tfs.dic['tf_workspace_path'].value))})


    def on_stop(self):
        CU.show_ok_cancel_dialog(title="Confirmation dialog", text=f"Are you sure you want to [color={get_hex_from_color(self.theme_cls.primary_color)}][b]quit[/b][/color] {CU.tfs.dic['APP_NAME'].value}?", size_hint=(0.5, 0.3), text_button_ok="Yes", text_button_cancel="No", callback=lambda *args: self.decide_stop_or_not(*args))

    def open_context_menu(self, instance):
        if (self.context_menus != None):
            MDDropdownMenu(items=self.context_menus, width_mult=3).open(instance)

    def open_settings(self, *args):
        # TODO: Experiment in later stage with kivy settings, because it might ruin the setup
        return False

    def set_theme_toolbar(self, primary_color, accent_color):
        if (primary_color is not None and accent_color is not None):
            primary_color, accent_color = str(primary_color), str(accent_color)
            # Print test below to illustrate the number of times it is fired:
            # print(f"Primary color: {primary_color}")

            if (primary_color in palette) and (accent_color in palette):
                # Update the primary and accent colors
                MainApp.theme_cls.primary_palette = primary_color
                MainApp.theme_cls.accent_palette = accent_color

    def set_title_toolbar(self, title):
        """Set string title in MDToolbar for the whole application."""
        self.main_widget.ids.toolbar.title = title

    def show_screen(self, screen_property, theme_primary_color, theme_accent_color):
        # Get a shorter alias for the screen_manager object:
        scr_mngr = self.main_widget.ids.scr_mngr
        # Extract class & class_name:
        screen_class = screen_property.value
        class_name = screen_class.__name__

        # Update the title, theme:
        self.set_title_toolbar(screen_property.name)
        self.set_theme_toolbar(theme_primary_color, theme_accent_color)

        # If the scr_mngr doesn't have such screen yet, make one:
        if(not scr_mngr.has_screen(class_name)):
            scr_mngr.add_widget(self.create_uninstantiated_screen(screen_class))

        # Update the context menu's and finally show toast when ready:
        self.context_menus = scr_mngr.get_screen(class_name).context_menus
        scr_mngr.current = class_name
        toast(class_name)


if __name__ == "__main__":

    mapp = MainApp()

    if(CU.tfs.dic['CONFIG_FILE_PATH'].value.exists()):
        # If the config-file exists, then try to import it:
        CU.tfs.import_tf_settings_from_config()
    else:
        # Else, when the config-file is absent, then export (a new) one:
        CU.tfs.export_tf_settings_to_config()

    try:
        mapp.run()
    except Exception as e:
        print(f"{CU.tfs.dic['APP_NAME'].value} encountered an error & needs to shut down.{os.linesep}{os.linesep}"
              f"{str(e)}{os.linesep}{os.linesep}-> Our apologies for the inconvenience, please consult the stack trace below:{os.linesep}{traceback.format_exc()}")

    # else:
    #     The else clause is only relevant when some instructions should only take place when the app shuts down correctly.
    #     pass

    finally:
        # This finally block will always be executed no matter whether the app crashed or ended successfully
        try:
            CU.tfs.export_tf_settings_to_config()

            # TODO: + Try to save the workspace if still possible when in error

        except Exception as e:
            print(f"-> {CU.tfs.dic['APP_NAME'].value} encountered unexpected error during the final saving of the workspace.")







    # =========================================================================
    # IDEAS DURING FURTHER IMPLEMENTATION:
    # TODO: Make mouse scrollwheel tempo/speed-control in concert mode.


    