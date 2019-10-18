# -*- coding: utf-8 -*-

import time
from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivymd.utils import asynckivy as ak


class TestApp(App):

    def build(self):
        return Label(text='Hello', markup=True, font_size='80sp',
                     outline_width=2,
                     outline_color=get_color_from_hex('#FFFFFF'),
                     color=get_color_from_hex('#000000'),
                     )

    def on_start(self):
        # async def animate(label):
        #     await ak.sleep(1.5)
        #     while True:
        #         label.outline_color = get_color_from_hex('#FFFFFF')
        #         label.text = 'Do'
        #         await ak.sleep(.5)
        #         label.text = 'you'
        #         await ak.sleep(.5)
        #         label.text = 'like'
        #         await ak.sleep(.5)
        #         label.text = 'Kivy?'
        #         await ak.sleep(2)
        #
        #         label.outline_color = get_color_from_hex('#FF5555')
        #         label.text = 'Answer me!'
        #         await ak.sleep(2)
        #
        #         label.outline_color = get_color_from_hex('#FFFF00')
        #         label.text = 'Left-click to replay'
        #         while True:
        #             args, kwargs = await ak.event(label, 'on_touch_down')
        #             touch = args[1]
        #             if touch.button == 'left':
        #                 break

        def animate(label):
            print("Got here 1")
            time.sleep(1.5)
            print("Got here 2")
            for i in [0,2]:
                label.outline_color = get_color_from_hex('#FFFFFF')
                label.text = 'Do'
                print("Got here 3")
                time.sleep(.5)
                label.text = 'you'
                print("Got here 4")
                time.sleep(.5)
                label.text = 'like'
                print("Got here 5")
                time.sleep(.5)
                label.text = 'Kivy?'
                print("Got here 6")
                time.sleep(2)

                label.outline_color = get_color_from_hex('#FF5555')
                label.text = 'Answer me!'
                print("Got here 7")
                time.sleep(2)

                label.outline_color = get_color_from_hex('#FFFF00')
                label.text = 'Left-click to replay'
                # while True:
                #     args, kwargs = ak.event(label, 'on_touch_down')
                #     touch = args[1]
                #     if touch.button == 'left':
                #         break
                print("Got here 8")
        animate(self.root)


if __name__ == '__main__':
    TestApp().run()

# from kivy.app import App
# from kivy.lang import Builder
# from kivy.factory import Factory
# from kivy.utils import get_hex_from_color
#
# from kivymd.uix.dialog import MDInputDialog, MDDialog
# from kivymd.theming import ThemeManager
#
#
# Builder.load_string('''
# <ExampleDialogs@BoxLayout>
#     orientation: 'vertical'
#     spacing: dp(5)
#
#     MDToolbar:
#         id: toolbar
#         title: app.title
#         left_action_items: [['menu', lambda x: None]]
#         elevation: 10
#         md_bg_color: app.theme_cls.primary_color
#
#     FloatLayout:
#         MDRectangleFlatButton:
#             text: "Open input dialog"
#             pos_hint: {'center_x': .5, 'center_y': .7}
#             opposite_colors: True
#             on_release: app.show_example_input_dialog()
#
#         MDRectangleFlatButton:
#             text: "Open Ok Cancel dialog"
#             pos_hint: {'center_x': .5, 'center_y': .5}
#             opposite_colors: True
#             on_release: app.show_example_okcancel_dialog()
# ''')
#
#
# class Example(App):
#     theme_cls = ThemeManager()
#     theme_cls.primary_palette = 'Teal'
#     title = "Dialogs"
#
#     def build(self):
#         return Factory.ExampleDialogs()
#
#     def on_start(self):
#         self.icon = "/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/ToneFlow/img/ToneFlow_Logo_Filled.png"
#         print("its me " +  str(self.get_application_icon()))
#         self.show_example_input_dialog()
#
#     def on_title(self, instance, title):
#         self.title = "owksy"
#
#     def callback_for_menu_items(self, *args):
#         from kivymd.toast.kivytoast import toast
#         toast(args[0])
#
#     def show_example_input_dialog(self):
#         dialog = MDInputDialog(
#             title='Enter path to workspace folder', hint_text="Where is the hint text", size_hint=(.8, .4),
#             text_button_ok='Confirm',
#             events_callback=self.callback_for_menu_items)
#         dialog.open()
#
#     def show_example_okcancel_dialog(self):
#         dialog = MDDialog(
#             title='Title', size_hint=(.8, .3), text_button_ok='Yes',
#             text="Your [color=%s][b]text[/b][/color] dialog" % get_hex_from_color(
#                 self.theme_cls.primary_color),
#             text_button_cancel='Cancel',
#             events_callback=self.callback_for_menu_items)
#         dialog.open()
#
#
# if __name__ == "__main__":
#     # a = InputDiagTest()
#     # a.show_example_input_dialog()
#     a = Example()
#     # a.show_example_input_dialog()
#     a.run()
#
