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

# from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.utils import get_hex_from_color
from kivy.utils import get_color_from_hex
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivymd.app import MDApp
from kivymd.utils import asynckivy
# from kivymd.uix.navigationdrawer import NavigationDrawerIconButton
from kivymd.theming import ThemeManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivymd.color_definitions import palette
from kivymd.theming_dynamic_text import get_contrast_text_color
from kivymd.color_definitions import colors

from src.main.TFExceptionHandler import TFExceptionHandler
from src.model.CommonUtils import CommonUtils as CU
from src.model.TFSettings import TFSettings

from kivy.base import ExceptionManager


class MainApp(MDApp):
    """

    """
    # Foresee custom handling of errors, user can bypass them (maybe own mistake) or quit the app, but he sees pop up of the error:
    ExceptionManager.add_handler(TFExceptionHandler())

    def __init__(self, **kwargs):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.accent_palette = "LightGreen"

        super().__init__(**kwargs)

        self._main_widget = None
        self._exception_counter = 0
        self._context_menus = None
        # To prevent the window from closing, when 'X' is pressed on the windows itself:
        Window.bind(on_request_close=self.on_stop)
        Window.exit_on_escape = 1

        # TODO: Test how fullscreen must be used decently: fullscreen option has been deprecated, use Window.borderless or the borderless Config option instead

        #Window.fullscreen = 'fake' # False, True, 'auto', 'fake' are the possibilities: https://kivy.org/doc/stable/api-kivy.config.html#module-kivy.config he ‘fake’ option has been deprecated, use the borderless property instead.
        Window.maximize()

        # Linux way to kill fullscreen app when it doesn't want to close:
        # Ctrl+Alt+F1 > tty1 client (login, remember that numeric extension of keyboard does not work here) next try to
        # {ps aux | less} or {top}, then you will see the list of processes currently active, find the python process
        # {kill -9 27890} (this command sends SIGKILL next return to cinnamon GUI with {Ctrl+Alt+F7}




        # Create ToneFlow-settings object and corresponding settings:
        kv_file_main_widget = str(curr_file.parents[1] / "view" / (curr_file.with_suffix(".kv")).name)
        TFSettings(kv_file_main_widget)

    def build(self):
        self.icon = str(pl.Path(CU.tfs.dic['IMG_DIR_PATH'].value) / "ToneFlow_Logo_TaskBarIcon.png")
        # self.Window.bind(on_request_close= lambda x:self.on_stop())

        self._main_widget.ids.scr_mngr.add_widget(CU.tfs)

        return self._main_widget

    def create_uninstantiated_screen(self, screen_class):
        class_name = screen_class.__name__
        # Builder.load_file(str(curr_file.parents[1] / "view" / (pl.Path(class_name).with_suffix(".kv")).name))
        screen_object = screen_class()
        return screen_object

    def decide_stop_or_not(self, *args):
        # TODO: Stop warning is not shown yet when you close by closing the window with the 'x'-button.
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

    def set_context_menus(self, context_menus):
        self._context_menus = context_menus

    def get_main_widget(self):
        return self._main_widget

    def set_main_widget(self, main_widget):
        self._main_widget = main_widget

    main_widget = property(get_main_widget, set_main_widget)
    context_menus = property(get_context_menus, set_context_menus)

    def convert_dict_to_context_menus(self, items):
        # Depending on the screen other context oriented options should appear under the three vertical dots
        if (items is not None):
            self.context_menus = [
                {
                    "viewclass": "MDMenuItem",
                    "text": f"{key}",
                    "text_color": get_contrast_text_color(self.theme_cls.primary_color, True),
                    "callback": items[key]
                }
                for key in items
            ]
        else:
            self.context_menus = None

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

    def on_stop(self, *args, **kwargs):
        # Important: *args and **kwargs can both be passed to a method, *args takes care of all unexpected
        # (variable amount) of positional arguments and **kwargs takes care of all unexpected (variable amount)
        # of named arguments.
        CU.show_ok_cancel_dialog(title="Confirmation dialog", text=f"Are you sure you want to [color={get_hex_from_color(self.theme_cls.primary_color)}][b]quit[/b][/color] {CU.tfs.dic['APP_NAME'].value}?", size_hint=(0.5, 0.3), text_button_ok="Yes", text_button_cancel="No", callback=lambda *args: self.decide_stop_or_not(*args))
        return True

    def open_context_menu(self, instance):
        if (self.context_menus != None):
            mddm = MDDropdownMenu(items=self.context_menus, width_mult=3).open(instance)

    def open_settings(self, *args):
        # TODO: Experiment in later stage with kivy settings, because it might ruin the setup
        return False

    def set_theme_toolbar(self, primary_color, accent_color):
        if (primary_color is not None and accent_color is not None):
            primary_color, accent_color = str(primary_color), str(accent_color)

            if (primary_color in palette) and (accent_color in palette):
                # Update the primary and accent colors
                self.theme_cls.primary_palette = primary_color
                self.theme_cls.accent_palette = accent_color

    def set_title_toolbar(self, title):
        """Set string title in MDToolbar for the whole application."""
        self._main_widget.ids.toolbar.title = title

    def show_screen(self, screen_property):
        # Get a shorter alias for the screen_manager object:
        scr_mngr = self._main_widget.ids.scr_mngr
        # Extract class & class_name:
        screen_class = screen_property.value
        class_name = screen_class.__name__

        # Update the title, theme:
        self.set_title_toolbar(screen_property.name)
        self.set_theme_toolbar(screen_class.theme_primary_color, screen_class.theme_accent_color)

        # If the scr_mngr doesn't have such screen yet, make one:
        if(not scr_mngr.has_screen(class_name)):
            scr_mngr.add_widget(self.create_uninstantiated_screen(screen_class))

        # Update the context menu's and finally show toast when ready:
        self.convert_dict_to_context_menus(scr_mngr.get_screen(class_name).context_menus)
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


    