import os
import sys
import pathlib as pl
root_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, root_directory)
sys.path.insert(0, str(pl.Path(root_directory).parents[1]))
sys.path.insert(0, str(pl.Path(root_directory).parents[2]))

# Below statement if you want to use the video player, do this before the kivy import!
os.environ['KIVY_VIDEO']='ffpyplayer'

import kivy
kivy.require('1.11.1') # replace with your current kivy version !

from kivy.lang import Builder
Builder.load_file(str(pl.Path(root_directory) / "Pong.kv"))

from kivy.app import App
from kivy.lang import Builder

from kivymd.uix.navigationdrawer import NavigationDrawerIconButton
from kivymd.theming import ThemeManager
from kivymd.toast import toast

main_kv = """
<ContentNavigationDrawer@MDNavigationDrawer>:
    drawer_logo: 'demos/kitchen_sink/assets/drawer_logo.png'

    NavigationDrawerSubheader:
        text: "Menu:"


NavigationLayout:
    id: nav_layout

    ContentNavigationDrawer:
        id: nav_drawer

    BoxLayout:
        orientation: 'vertical'

        MDToolbar:
            id: toolbar
            title: 'KivyMD Kitchen Sink'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            elevation: 10
            left_action_items:
                [['dots-vertical', lambda x: app.root.toggle_nav_drawer()]]

        Widget:
"""


class ToneFlowApp(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Red'

    def build(self):
        self.main_widget = Builder.load_string(main_kv)
        return self.main_widget

    def callback(self, instance, value):
        toast("Pressed item menu %d" % value)

    def on_start(self):
        for i in range(15):
            self.main_widget.ids.nav_drawer.add_widget(
                NavigationDrawerIconButton(
                    icon='checkbox-blank-circle', text="Item menu %d" % i,
                    on_release=lambda x, y=i: self.callback(x, y)))

if __name__ == "__main__":
    ToneFlowApp().run()