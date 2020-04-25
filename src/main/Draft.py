# import sys
# import json
# import mido
#
#
# def midifile_to_dict(mid):
#     tracks = []
#     for track in mid.tracks:
#         tracks.append([vars(msg).copy() for msg in track])
#
#     return {
#         'ticks_per_beat': mid.ticks_per_beat,
#         'tracks': tracks,
#     }
#
#
# mid = mido.MidiFile('/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/all_by_myself.mid')
#
# print(json.dumps(midifile_to_dict(mid), indent=2))

#############################################################"

import sys
from mido import MidiFile

if __name__ == '__main__':
    # filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/all_by_myself.mid'
    # filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/Movie_Themes_-_2001_-_Also_Sprach_Zarathustra_Richard_Strauss.mid'
    filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/ChromaticBasics.mid'

    midi_file = MidiFile(filename)


    for i, track in enumerate(midi_file.tracks):
        sys.stdout.write('=== Track {}\n'.format(i))
        for message in track:
            sys.stdout.write('  {!r}\n'.format(message))


    for msg in midi_file.play():
        print(f"Test PDP: {msg}")



# from kivy.uix.boxlayout import BoxLayout
#
# from kivymd.app import MDApp
# from kivy.lang import Builder
# from kivy.properties import StringProperty
#
# from kivymd.uix.list import OneLineAvatarListItem
#
# KV = '''
# #:import IconLeftWidget kivymd.uix.list.IconLeftWidget
# #:import images_path kivymd.images_path
#
#
# <NavigationItemWithDivider@OneLineAvatarListItem>
#     theme_text_color: 'Custom'
#     divider: 'Full'
#     icon: 'checkbox-blank-circle'
#
#     IconLeftWidget:
#         icon: root.icon
#
#
# <NavigationItem@OneLineAvatarListItem>
#     theme_text_color: 'Custom'
#     divider: None
#     icon: 'checkbox-blank-circle'
#
#     IconLeftWidget:
#         icon: root.icon
#
# <NavigationDrawerDivider@canvas>
#     Color:
#         rgba: self.theme_cls.divider_color
#     Line:
#         points: root.x, root.y + dp(8), root.x + self.width, root.y + dp(8)
#
# <NavigationDrawerSubheader@OneLineListItem>
#     disabled: True
#     divider: None
#     theme_text_color: "Secondary"
#
# <ContentNavigationDrawer@BoxLayout>
#
#     BoxLayout:
#         orientation: 'vertical'
#
#         FloatLayout:
#             size_hint_y: None
#             height: "200dp"
#
#             canvas:
#                 Color:
#                     rgba: app.theme_cls.primary_color
#                 Rectangle:
#                     pos: self.pos
#                     size: self.size
#
#             BoxLayout:
#                 id: top_box
#                 size_hint_y: None
#                 height: "200dp"
#                 #padding: "10dp"
#                 x: root.parent.x
#                 pos_hint: {"top": 1}
#
#                 FitImage:
#                     source: f"{images_path}kivymd_alpha.png"
#
#             MDIconButton:
#                 icon: "close"
#                 x: root.parent.x + dp(10)
#                 pos_hint: {"top": 1}
#                 on_release: root.parent.toggle_nav_drawer()
#
#             MDLabel:
#                 markup: True
#                 text: "[b]KivyMD[/b]\\nVersion: 0.103.0"
#                 #pos_hint: {'center_y': .5}
#                 x: root.parent.x + dp(10)
#                 y: root.height - top_box.height + dp(10)
#                 size_hint_y: None
#                 height: self.texture_size[1]
#
#         ScrollView:
#             pos_hint: {"top": 1}
#
#             GridLayout:
#                 id: box_item
#                 cols: 1
#                 size_hint_y: None
#                 height: self.minimum_height
#
#                 NavigationItem:
#                     text: 'help'
#                     icon: 'home'
#
#                 # NavigationDrawerDivider
#
#                 NavigationDrawerSubheader:
#                     text: 'Menus:'
#
#                 NavigationItem:
#                     text: 'help'
#                     icon: 'list'
#
#                 NavigationItemWithDivider:
#                     text: 'help'
#                     icon: 'settings'
#
#                 NavigationItem:
#                     text: 'help'
#                     icon: 'list'
#
#
#
#
#
# Screen:
#
#     NavigationLayout:
#
#         ScreenManager:
#
#             Screen:
#
#                 BoxLayout:
#                     orientation: 'vertical'
#
#                     MDToolbar:
#                         title: "Navigation Drawer"
#                         md_bg_color: app.theme_cls.primary_color
#                         elevation: 10
#                         left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
#
#                     Widget:
#
#
#         MDNavigationDrawer:
#             id: nav_drawer
#
#             ContentNavigationDrawer:
#                 id: content_drawer
#
# '''
#
#
# # class ContentNavigationDrawer(BoxLayout):
# #     pass
#
#
# # class NavigationItem(OneLineAvatarListItem):
# #     icon = StringProperty()
#
#
# class TestNavigationDrawer(MDApp):
#     def build(self):
#         return Builder.load_string(KV)
#
#     def on_start(self):
#         pass
#         # for items in {
#         #     "home-circle-outline": "Home",
#         #     "update": "Check for Update",
#         #     "settings-outline": "Settings",
#         #     "exit-to-app": "Exit",
#         # }.items():
#         #     self.root.ids.content_drawer.ids.box_item.add_widget(
#         #         NavigationItem(
#         #             text=items[1],
#         #             icon=items[0],
#         #         )
#
# TestNavigationDrawer().run()
#
# # from kivy.app import App
# # from kivy.lang import Builder
# # from kivy.factory import Factory
# #
# # from kivymd.toast import toast
# # from kivymd.theming import ThemeManager
# # from kivymd.uix.stackfloatingbutton import MDStackFloatingButtons
# #
# #
# # Builder.load_string('''
# #
# #
# # <ExampleFloatingButtons@BoxLayout>:
# #     orientation: 'vertical'
# #
# #     MDToolbar:
# #         title: 'Stack Floating Buttons'
# #         md_bg_color: app.theme_cls.primary_color
# #         elevation: 10
# #         left_action_items: [['menu', lambda x: None]]
# #
# # ''')
# #
# #
# # class Example(App):
# #     theme_cls = ThemeManager()
# #     theme_cls.primary_palette = 'Teal'
# #     title = "Example Stack Floating Buttons"
# #     create_stack_floating_buttons = False
# #     floating_data = {
# #         'Python': 'language-python',
# #         'Php': 'language-php',
# #         'C++': 'language-cpp'}
# #
# #     def set_my_language(self, instance_button):
# #         toast(instance_button.icon)
# #
# #     def build(self):
# #         screen = Factory.ExampleFloatingButtons()
# #         # Use this condition otherwise the stack will be created each time.
# #         if not self.create_stack_floating_buttons:
# #             screen.add_widget(MDStackFloatingButtons(
# #                 icon='lead-pencil',
# #                 # floating_data=self.floating_data,
# #                 floating_data={
# #                     'Python': None,
# #                     'Php': 'language-php',
# #                     'C++': 'language-cpp'},
# #                 # floating_data={'a': 'b', 'c': 'd'},
# #                 callback=self.set_my_language))
# #             self.create_stack_floating_buttons = True
# #         return screen
# #
# #
# # Example().run()
# #
# # #
# # #
# # # # -*- coding: utf-8 -*-
# # #
# # # import time
# # # from kivy.app import App
# # # from kivy.uix.label import Label
# # # from kivy.utils import get_color_from_hex
# # # from kivymd.utils import asynckivy as ak
# # #
# # #
# # # class TestApp(App):
# # #
# # #     def build(self):
# # #         return Label(text='Hello', markup=True, font_size='80sp',
# # #                      outline_width=2,
# # #                      outline_color=get_color_from_hex('#FFFFFF'),
# # #                      color=get_color_from_hex('#000000'),
# # #                      )
# # #
# # #     def on_start(self):
# # #         # async def animate(label):
# # #         #     await ak.sleep(1.5)
# # #         #     while True:
# # #         #         label.outline_color = get_color_from_hex('#FFFFFF')
# # #         #         label.text = 'Do'
# # #         #         await ak.sleep(.5)
# # #         #         label.text = 'you'
# # #         #         await ak.sleep(.5)
# # #         #         label.text = 'like'
# # #         #         await ak.sleep(.5)
# # #         #         label.text = 'Kivy?'
# # #         #         await ak.sleep(2)
# # #         #
# # #         #         label.outline_color = get_color_from_hex('#FF5555')
# # #         #         label.text = 'Answer me!'
# # #         #         await ak.sleep(2)
# # #         #
# # #         #         label.outline_color = get_color_from_hex('#FFFF00')
# # #         #         label.text = 'Left-click to replay'
# # #         #         while True:
# # #         #             args, kwargs = await ak.event(label, 'on_touch_down')
# # #         #             touch = args[1]
# # #         #             if touch.button == 'left':
# # #         #                 break
# # #
# # #         def animate(label):
# # #             print("Got here 1")
# # #             time.sleep(1.5)
# # #             print("Got here 2")
# # #             for i in [0,2]:
# # #                 label.outline_color = get_color_from_hex('#FFFFFF')
# # #                 label.text = 'Do'
# # #                 print("Got here 3")
# # #                 time.sleep(.5)
# # #                 label.text = 'you'
# # #                 print("Got here 4")
# # #                 time.sleep(.5)
# # #                 label.text = 'like'
# # #                 print("Got here 5")
# # #                 time.sleep(.5)
# # #                 label.text = 'Kivy?'
# # #                 print("Got here 6")
# # #                 time.sleep(2)
# # #
# # #                 label.outline_color = get_color_from_hex('#FF5555')
# # #                 label.text = 'Answer me!'
# # #                 print("Got here 7")
# # #                 time.sleep(2)
# # #
# # #                 label.outline_color = get_color_from_hex('#FFFF00')
# # #                 label.text = 'Left-click to replay'
# # #                 # while True:
# # #                 #     args, kwargs = ak.event(label, 'on_touch_down')
# # #                 #     touch = args[1]
# # #                 #     if touch.button == 'left':
# # #                 #         break
# # #                 print("Got here 8")
# # #         animate(self.root)
# # #
# # #
# # # if __name__ == '__main__':
# # #     TestApp().run()
# #
# # # from kivy.app import App
# # # from kivy.lang import Builder
# # # from kivy.factory import Factory
# # # from kivy.utils import get_hex_from_color
# # #
# # # from kivymd.uix.dialog import MDInputDialog, MDDialog
# # # from kivymd.theming import ThemeManager
# # #
# # #
# # # Builder.load_string('''
# # # <ExampleDialogs@BoxLayout>
# # #     orientation: 'vertical'
# # #     spacing: dp(5)
# # #
# # #     MDToolbar:
# # #         id: toolbar
# # #         title: app.title
# # #         left_action_items: [['menu', lambda x: None]]
# # #         elevation: 10
# # #         md_bg_color: app.theme_cls.primary_color
# # #
# # #     FloatLayout:
# # #         MDRectangleFlatButton:
# # #             text: "Open input dialog"
# # #             pos_hint: {'center_x': .5, 'center_y': .7}
# # #             opposite_colors: True
# # #             on_release: app.show_input_dialog()
# # #
# # #         MDRectangleFlatButton:
# # #             text: "Open Ok Cancel dialog"
# # #             pos_hint: {'center_x': .5, 'center_y': .5}
# # #             opposite_colors: True
# # #             on_release: app.show_example_okcancel_dialog()
# # # ''')
# # #
# # #
# # # class Example(App):
# # #     theme_cls = ThemeManager()
# # #     theme_cls.primary_palette = 'Teal'
# # #     title = "Dialogs"
# # #
# # #     def build(self):
# # #         return Factory.ExampleDialogs()
# # #
# # #     def on_start(self):
# # #         self.icon = "/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/ToneFlow/img/ToneFlow_Logo_Filled.png"
# # #         print("its me " +  str(self.get_application_icon()))
# # #         self.show_input_dialog()
# # #
# # #     def on_title(self, instance, title):
# # #         self.title = "owksy"
# # #
# # #     def callback_for_menu_items(self, *args):
# # #         from kivymd.toast.kivytoast import toast
# # #         toast(args[0])
# # #
# # #     def show_input_dialog(self):
# # #         dialog = MDInputDialog(
# # #             title='Enter path to workspace folder', hint_text="Where is the hint text", size_hint=(.8, .4),
# # #             text_button_ok='Confirm',
# # #             events_callback=self.callback_for_menu_items)
# # #         dialog.open()
# # #
# # #     def show_example_okcancel_dialog(self):
# # #         dialog = MDDialog(
# # #             title='Title', size_hint=(.8, .3), text_button_ok='Yes',
# # #             text="Your [color=%s][b]text[/b][/color] dialog" % get_hex_from_color(
# # #                 self.theme_cls.primary_color),
# # #             text_button_cancel='Cancel',
# # #             events_callback=self.callback_for_menu_items)
# # #         dialog.open()
# # #
# # #
# # # if __name__ == "__main__":
# # #     # a = InputDiagTest()
# # #     # a.show_input_dialog()
# # #     a = Example()
# # #     # a.show_input_dialog()
# # #     a.run()
# # #
