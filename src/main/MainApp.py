import os
import sys
import pathlib as pl
curr_file = pl.Path(os.path.realpath(__file__))
# curr_file_dir = curr_file.parents[0]

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

from src.main import *
from src.model.CommonUtils import CommonUtils as CU

class MainApp(App):
    """

    """
    theme_cls = ThemeManager()
    theme_cls.primary_palette = "Brown"
    theme_cls.accent_palette = "LightGreen"
    title = CU.tfs.dic['APP_NAME'].value + " - v" + CU.tfs.dic['MAJOR_MINOR_VERSION'].value
    theme_cls.theme_style = "Light"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.Window = Window


    def build(self):
        self.icon = str(pl.Path(CU.tfs.dic['IMG_DIR'].value) / "ToneFlow_Logo_TaskBarIcon.png")
        self.main_widget = Builder.load_file(str(curr_file.with_suffix(".kv")))
        # self.Window.bind(on_request_close= lambda x:self.on_stop())
        return self.main_widget


    def callback(self, instance, value):
        toast(f"Pressed item menu {value}")

    def on_start(self):

        playlists_ndib = NavigationDrawerIconButton(
            icon="playlist-music", text="Playlists",
            on_release=lambda x, y="Playlists Screen": self.callback(x, y))

        songs_ndib = NavigationDrawerIconButton(
            icon="music-note", text="Songs",
            on_release=lambda x, y="Songs Screen": self.callback(x, y))

        settings_ndib = NavigationDrawerIconButton(
            icon="settings", text="Settings",
            on_release=lambda x, y="Settings Screen": self.callback(x, y))

        shut_down_ndib = NavigationDrawerIconButton(
            icon="power", text="Quit",
            on_release=lambda x:self.on_stop())

        self.main_widget.ids.nav_drawer.add_widget(playlists_ndib)
        self.main_widget.ids.nav_drawer.add_widget(songs_ndib)
        self.main_widget.ids.nav_drawer.add_widget(settings_ndib)
        self.main_widget.ids.nav_drawer.add_widget(shut_down_ndib)

        # original icons: checkbox-blank-circle

        # As a proposal, the actual (default)value of the tf_workspace-param is copied to the clipboard:
        workspace_path_proposal = CU.tfs.dic['tf_workspace'].value
        pyperclip.copy(str(workspace_path_proposal))
        self.show_example_input_dialog(title=f"Enter Path to \"{CU.tfs.dic['WORKSPACE_NAME'].value}\"-Folder or its Parent Folder",
                                       hint_text=f"{CU.tfs.dic['tf_workspace'].description}",
                                       text=f"{CU.tfs.dic['tf_workspace'].description}",
                                       size_hint=(.8, .3), text_button_ok="Load/Create",
                                       callback=lambda text_button, instance: {CU.tfs.create_load_tf_workspace(instance.text_field.text, workspace_path_proposal), toast(str(CU.tfs.dic['tf_workspace'].value))})

    def on_pause(self):
        return True

    def on_stop(self, *kwargs):
        self.show_cancel_dialog(title="Confirmation dialog", text=f"Are you sure you want to [color={get_hex_from_color(self.theme_cls.primary_color)}][b]quit[/b][/color] {CU.tfs.dic['APP_NAME'].value}?", size_hint=(0.5, 0.3), text_button_ok="Yes", text_button_cancel="No", callback=self.decide_stop_or_not)

    def decide_stop_or_not(self, *args):
        if args[0] is not None:
            # print(f"args0 {str(args[0])}")
            if (CU.safe_cast(args[0], str, "")).lower() == "yes":
                self.stop()
            else:
                toast("Not quitting")
        else:
            toast("Not quitting")

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

    def show_example_input_dialog(self, title="Enter", hint_text=None, text="Type here", size_hint=(.8, .4), text_button_ok="Ok", callback=None):
        dialog = MDInputDialog(
            title=title,
            hint_text=hint_text,
            size_hint=size_hint,
            text_button_ok=text_button_ok,
            events_callback=callback)
        dialog.text_field.text = text
        dialog.open()

if __name__ == "__main__":
    mapp = MainApp()
    CU.tfs.export_tf_settings_to_config()
    mapp.run()