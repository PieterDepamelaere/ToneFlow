import os
import sys
import pathlib as pl
curr_file = pl.Path(os.path.realpath(__file__))
curr_file_dir = curr_file.parents[0]

sys.path.insert(0, str(curr_file.parents[0]))
sys.path.insert(0, str(curr_file.parents[1]))
sys.path.insert(0, str(curr_file.parents[2]))
img_dir = pl.Path(curr_file.parents[2] / "img")

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


# from src.main import MainApp
from src.model.CommonUtils import CommonUtils as CU

# In theory, an update of the minor version alone shouldn't induce breaking changes.
MAJOR_MINOR_VERSION = "0.1"
APP_NAME = str("ToneFlow " + u"\u00a9")

class MainApp(App):
    """

    """
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Purple'
    theme_cls.accent_palette = "Green"
    title = APP_NAME + " - v" + MAJOR_MINOR_VERSION
    theme_cls.theme_style = "Light"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.Window = Window


    def build(self):
        self.icon = str(pl.Path(img_dir / "ToneFlow_Logo_Filled.png"))
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

        # Copy path_proposal to clipboard:
        path_proposal = pl.Path(curr_file.parents[3] / "Workspace_TF")
        pyperclip.copy(str(path_proposal))
        self.show_example_input_dialog(title="Enter Path to TF Workspace Folder", hint_text="Please specify path on external device like USB", text="/home/pieter", size_hint=(.8, .4), text_button_ok="Confirm", callback=lambda text_button, instance: toast(str(instance.text_field.text)))

        # TODO: Make this below into a callback
        # # Without whitespace the length of ans_user should be bigger than 0 to return it:
        # if (ans_user.strip().__len__() > 0):
        #     return pl.Path(ans_user)
        # else:
        #     # In case of trivial ans_user, the original proposal is returned:
        #     return pl.Path(path_proposal)

    def set_title_toolbar(self, title):
        """Set string title in MDToolbar for the whole application."""
        self.main_widget.ids.toolbar.title = title

    def on_stop(self, *kwargs):
        self.show_cancel_dialog(title="Confirmation dialog", text=f"Are you sure you want to [color={get_hex_from_color(self.theme_cls.primary_color)}][b]quit[/b][/color] {APP_NAME}?", size_hint=(0.5, 0.3), text_button_ok="Yes", text_button_cancel="No", callback=self.decide_stop_or_not)

    def decide_stop_or_not(self, *args):
        if args[0] is not None:
            # print(f"args0 {str(args[0])}")
            if (CU.safe_cast(args[0], str, "")).lower() == "yes":
                self.stop()
            else:
                toast("Not quitting")
        else:
            toast("Not quitting")

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
            #text=text,
            size_hint=size_hint,
            text_button_ok=text_button_ok,
            events_callback=callback)
        dialog.open()

if __name__ == "__main__":
    mapp = MainApp()
    # TODO: Make this work
    # tfa.set_title_toolbar("TEstje")
    mapp.run()