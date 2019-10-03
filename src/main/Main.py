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

from kivy.app import App
from kivy.lang import Builder

from kivymd.uix.navigationdrawer import NavigationDrawerIconButton
from kivymd.theming import ThemeManager
from kivymd.toast import toast

# from src.main import img_dir
# print(img_dir)


# In theory, an update of the minor version alone shouldn't induce breaking changes.
MAJOR_MINOR_VERSION = "0.1"

class ToneFlowApp(App):
    """

    """
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Brown'
    theme_cls.accent_palette = "Green"
    title = "ToneFlow(c) - v" + MAJOR_MINOR_VERSION
    theme_cls.theme_style = "Light"

    def build(self):
        self.main_widget = Builder.load_file(str(curr_file.with_suffix(".kv")))
        return self.main_widget

    def callback(self, instance, value):
        toast("Pressed item menu %d" % value)

    def on_start(self):

        for i in range(5):
            self.main_widget.ids.nav_drawer.add_widget(
                NavigationDrawerIconButton(
                    icon='checkbox-blank-circle', text="Item menu %d" % i,
                    on_release=lambda x, y=i: self.callback(x, y)))

    def set_title_toolbar(self, title):
        """Set string title in MDToolbar for the whole application."""
        self.main_widget.ids.toolbar.title = title

if __name__ == "__main__":
    tfa = ToneFlowApp()
    # TODO PDP: Make this work
    # tfa.set_title_toolbar("TEstje")
    tfa.run()