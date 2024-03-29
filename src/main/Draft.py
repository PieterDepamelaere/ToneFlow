import threading
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

from functools import partial

Builder.load_string("""
<AnimWidget@Widget>:
    canvas:
        Color:
            rgba: 0.7, 0.3, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint: None, None
    size: 400, 30

<ColorTone>:
    tone_color: (1, 1, 1, 1)
    pos_hint: {"x":root.pos_hint_x, "y":root.pos_hint_y}
    canvas:
        Color:
            rgba: self.tone_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            segments: 15
            radius: [15]

<RootWidget>:
    cols: 1
    
    
    but_1: but_1
    lab_1: lab_1
    lab_2: lab_2
    # lab_3: lab_3
    # lab_4: lab_4
    ct_1: ct_1
    ct_2: ct_2
    ct_3: ct_3
    ct_4: ct_4
    ct_5: ct_5
    ct_6: ct_6
    ct_7: ct_7
    ct_8: ct_8
    ct_9: ct_9
    ct_10: ct_10
    ct_11: ct_11
    ct_12: ct_12
    ct_13: ct_13
    ct_14: ct_14
    ct_15: ct_15
    ct_16: ct_16
    ct_17: ct_17
    ct_18: ct_18
    ct_19: ct_19
    

    RelativeLayout:
        id: id_top_foreground
        size_hint: 1.0, None
        

        canvas:
            Color:
                rgba: 0.9, 0.9, 0.9, 1
            Rectangle:
                pos: self.pos
                size: self.size
    
        # anim_box: anim_box
        
        

        Button:
            id: but_1
            font_size: 20
            text: 'Start second thread'
            on_press: root.start_second_thread(lab_2.text)
        # 
        Label:
            id: lab_1
            font_size: 30
            color: 0.6, 0.6, 0.6, 1
            text_size: self.width, None
            # halign: 'center'
    
        # AnchorLayout:
        #     id: anim_box
    
        Label:
            id: lab_2
            font_size: 100
            color: 0.8, 0, 0, 1
            text: '3'
    
        # Label:
        #     id: lab_3
        #     font_size: 100
        #     color: 0.8, 0, 0, 1
        #     text: 'koe'
        # 
        # Label:
        #     id: lab_4
        #     font_size: 100
        #     color: 0.8, 0, 0, 1
        #     text: 'belle'
        
    
        ColorTone:
            id: ct_1
            pos_hint_x: 0.15 
            tone_color: (0.5, 0.4, 0.8, 1)
            pos_hint: {"x":0.2, "y":0.5}
            size_hint: 0.05, 0.3
        
        ColorTone:
            id: ct_2
            pos_hint_x: 0.35
            tone_color: (0.9, 0.4, 0.4, 1)
            pos_hint: {"x":0.35, "y":0.7}
            size_hint: 0.05, 0.6
            
        ColorTone:
            id: ct_3
            pos_hint_x: 0.75
            tone_color: (0.0, 0.6, 0.3, 1)
            pos_hint: {"x":0.75, "y":0.3}
            size_hint: 0.1, 0.2
            
        ColorTone:
            id: ct_4
            pos_hint_x: 0.9
            pos_hint_y: 0.75
            tone_color: (0.0, 0.2, 0.8, 1)
            # pos_hint: {"x":0.75, "y":0.75}
            size_hint: 0.1, 0.4

        ColorTone:
            id: ct_5
            pos_hint_x: 0.2
            pos_hint_y: 0.3
            tone_color: (0.7, 0.1, 0.3, 1)
            # pos_hint: {"x":0.2, "y":0.75}
            size_hint: 0.05, 0.8
            
        ColorTone:
            id: ct_6
            pos_hint_x: 0.35
            pos_hint_y: 0.01
            tone_color: (0.9, 0.4, 0.4, 1)
            size_hint: 0.05, 0.5
            
        ColorTone:
            id: ct_7
            pos_hint_x: 0.75
            pos_hint_y: 1.0
            tone_color: (1.0, 0.0, 0.0, 1)
            # pos_hint: {"x":0.75, "y":0.8}
            size_hint: 0.1, 0.2
            
        ColorTone:
            id: ct_8
            pos_hint_x: 0.9
            pos_hint_y: 0.4
            tone_color: (0.0, 0.2, 0.8, 1)
            # pos_hint: {"x":0.75, "y":0.75}
            size_hint: 0.1, 0.4

        ColorTone:
            id: ct_9
            pos_hint_x: 0.2
            pos_hint_y: 1.6
            tone_color: (0.7, 0.1, 0.3, 1)
            # pos_hint: {"x":0.2, "y":0.75}
            size_hint: 0.05, 0.8
        
        ColorTone:    
            id: ct_10
            pos_hint_x: 0.15
            pos_hint_y: 0.6 
            tone_color: (0.5, 0.4, 0.8, 1)
            # pos_hint: {"x":0.2, "y":0.7}
            size_hint: 0.05, 0.3
            
        ColorTone:
            id: ct_11
            pos_hint_x: 0.15
            pos_hint_y: 1.6  
            tone_color: (0.5, 0.4, 0.8, 1)
            # pos_hint: {"x":0.2, "y":0.5}
            size_hint: 0.05, 0.3
        
        ColorTone:
            id: ct_12
            pos_hint_x: 0.35
            pos_hint_y: 2.3 
            tone_color: (0.9, 0.4, 0.4, 1)
            # pos_hint: {"x":0.35, "y":0.7}
            size_hint: 0.05, 0.6
            
        ColorTone:
            id: ct_13
            pos_hint_x: 0.75
            pos_hint_y: 1.9
            tone_color: (0.0, 0.6, 0.3, 1)
            # pos_hint: {"x":0.75, "y":0.3}
            size_hint: 0.1, 0.2
            
        ColorTone:
            id: ct_14
            pos_hint_x: 0.9
            pos_hint_y: 1.75
            tone_color: (0.0, 0.2, 0.8, 1)
            # pos_hint: {"x":0.75, "y":0.75}
            size_hint: 0.1, 0.4

        ColorTone:
            id: ct_15
            pos_hint_x: 0.2
            pos_hint_y: 0.8
            tone_color: (0.7, 0.1, 0.3, 1)
            # pos_hint: {"x":0.2, "y":0.75}
            size_hint: 0.05, 0.8
            
        ColorTone:
            id: ct_16
            pos_hint_x: 0.35
            pos_hint_y: 2
            tone_color: (0.9, 0.4, 0.4, 1)
            size_hint: 0.05, 0.5
            
        ColorTone:
            id: ct_17
            pos_hint_x: 0.75
            pos_hint_y: 1.6
            tone_color: (1.0, 0.0, 0.0, 1)
            # pos_hint: {"x":0.75, "y":0.8}
            size_hint: 0.1, 0.2
            
        ColorTone:
            id: ct_18
            pos_hint_x: 0.9
            pos_hint_y: 1.2
            tone_color: (0.0, 0.2, 0.8, 1)
            # pos_hint: {"x":0.75, "y":0.75}
            size_hint: 0.1, 0.4

        ColorTone:
            id: ct_19
            pos_hint_x: 0.2
            pos_hint_y: 2.6
            tone_color: (0.7, 0.1, 0.3, 1)
            # pos_hint: {"x":0.2, "y":0.75}
            size_hint: 0.05, 0.8
    
""")

class ColorTone(Widget):
    pos_hint_x = NumericProperty(0)
    pos_hint_y = NumericProperty(0)
    # pass

class RootWidget(GridLayout):

    stop = threading.Event()

    def start_second_thread(self, l_text):
        threading.Thread(target=self.second_thread, args=(l_text,)).start()

    def second_thread(self, label_text):
        # Remove a widget, update a widget property, create a new widget,
        # add it and animate it in the main thread by scheduling a function
        # call with Clock.
        # Clock.schedule_once(self.start_test, 0)

        # Do some thread blocking operations.
        # time.sleep(5)
        l_text = str(int(label_text) * 3000)

        # Update a widget property in the main thread by decorating the
        # called function with @mainthread.
        self.update_label_text(l_text)

        # Do some more blocking operations.
        time.sleep(0.5)

        # Remove some widgets and update some properties in the main thread
        # by decorating the called function with @mainthread.
        self.stop_test()

        # # Start a new thread with an infinite loop and stop the current one.
        # threading.Thread(target=Clock.schedule_interval(partial(self.shift_x, self.lab_2), 0)).start()
        # print(f'test')
        # threading.Thread(target=Clock.schedule_interval(partial(self.shift_y, self.lab_2), 0)).start()
        #
        # threading.Thread(target=Clock.schedule_interval(partial(self.inverse_shift_x, self.lab_3), 0)).start()
        # threading.Thread(target=Clock.schedule_interval(partial(self.shift_y, self.lab_4), 0)).start()

        # threading.Thread(target=Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_1), 0)).start()
        # threading.Thread(target=Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_2), 0)).start()
        # threading.Thread(target=Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_3), 0)).start()
        # threading.Thread(target=Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_4), 0)).start()
        # threading.Thread(target=Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_5), 0)).start()

        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_1), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_2), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_3), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_4), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_5), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_6), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_7), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_8), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_9), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_10), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_11), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_12), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_13), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_14), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_15), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_16), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_17), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_18), 0)
        Clock.schedule_interval(partial(self.inverse_shift_y, self.ct_19), 0)

        # Clock.schedule_interval(self.combine, 0)

        # Clock.schedule_interval(partial(self.shift_x, self.lab_2), 0)
        # Clock.schedule_interval(partial(self.shift_y, self.lab_2), 0)
        # Clock.schedule_interval(partial(self.inverse_shift_x, self.lab_3), 0)
        # Clock.schedule_interval(partial(self.shift_y, self.lab_4), 0)

        # threading.Thread(target=self.infinite_loop1).start()
        # threading.Thread(target=self.infinite_loop2).start()
        # threading.Thread(target=self.infinite_loop3).start()
        print(f'second infinite thread started')

    def combine(self, *args):
        self.inverse_shift_y(self.ct_1)
        self.inverse_shift_y(self.ct_2)
        self.inverse_shift_y(self.ct_3)
        self.inverse_shift_y(self.ct_4)
        self.inverse_shift_y(self.ct_5)



    def start_test(self, *args):
        # Remove the button.
        self.remove_widget(self.but_1)

        # Update a widget property.
        self.lab_1.text = ('The UI remains responsive while the '
                           'second thread is running.')

        # Create and add a new widget.
        # anim_bar = Factory.AnimWidget()
        # self.anim_box.add_widget(anim_bar)

        # Animate the added widget.
        # anim = Animation(opacity=0.3, width=100, duration=0.6)
        # anim += Animation(opacity=1, width=400, duration=0.8)
        # anim.repeat = True
        # anim.start(anim_bar)

    @mainthread
    def update_label_text(self, new_text):
        self.lab_2.text = new_text

    @mainthread
    def stop_test(self):
        self.lab_1.text = ('Second thread exited, a new thread has started. '
                           'Close the app to exit the new thread and stop '
                           'the main process.')

        self.lab_2.text = str(int(self.lab_2.text) + 1)

        # self.remove_widget(self.anim_box)

    def shift_x(self, widget, *args):
        widget.pos_hint_x -= 0.01

        # widget.x -= 1

    def inverse_shift_x(self, widget, *args):
        widget.x += 1

    def inverse_shift_y(self, widget, *args):
        widget.pos_hint_y -= 0.01

    def shift_y(self, widget, *args):
        widget.y += 1

    def infinite_loop1(self):

        while True:
            if self.stop.is_set():
                # Stop running this thread so the main Python process can exit.
                return

            self.shift_x()


            # if(iteration % 100 == 0):
            #     self.update_label_text(f'the new iteration is {iteration}')
            # print('Infinite loop, iteration {}.'.format(iteration))
            # time.sleep(1)

    def infinite_loop2(self):
        while True:
            if self.stop.is_set():
                return

            self.shift_y()

    def infinite_loop3(self):
        iteration = 0

        while True:
            if self.stop.is_set():
                return

            iteration += 1

            self.lab_2.text = f"{iteration}"

class ThreadedApp(App):

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    ThreadedApp().run()

##############################################################

# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.lang import Builder
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.properties import ListProperty
#
# kv_string = '''
# #:import get_color_from_hex kivy.utils.get_color_from_hex
#
# <ColorStrip>:
#     pos_hint: {'x': 0.75, 'y': 0.25}
#     size_hint: 0.1, 0.8
#     canvas:
#         Color:
#             rgba: get_color_from_hex('#111111FF')
#         Rectangle:
#             size: self.size
#             pos: self.pos
#
# <MyWidget>:
#     FloatLayout:
#         id: id_background
# '''
#
# Builder.load_string(kv_string)
#
#
# class MyWidget(FloatLayout):
#
#     # def __init__(self):
#     #     super(MyWidget, self).__init__()
#
#     def create_strips(self):
#         # with self.ids.id_background.canvas.before:
#         #     ColorStrip()
#
#         w = ColorStrip()
#
#         self.ids.id_background.add_widget(w)
#
#     pass
#
#
# class ColorStrip(Widget):
#     r_size = ListProperty([0, 0])
#
#
# class TestApp(App):
#     def build(self):
#         m = MyWidget()
#         m.create_strips()
#
#         return m
#
# if __name__ == '__main__':
#     TestApp().run()

#
# from kivy.app import App
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.lang import Builder
# from kivy.uix.widget import Widget
#
# kv_string = '''
#
# #:import get_color_from_hex kivy.utils.get_color_from_hex
#
# <ColorStrip@Widget>:
#     pos_hint: {'x': 0.75, 'y': 0.25}
#     size_hint: 0.1, 0.8
#
#     canvas:
#         Color:
#             rgba: get_color_from_hex('#111111FF')
#         Rectangle:
#             size: self.size
#             pos: self.pos
#
# <MyWidget>:
#     id: id_background
#
#
#     # Widget:
#     #     pos_hint: {'center_y': 0.5, 'center_x': 0.2}
#     #     size_hint: 0.2, 0.2
#     #     canvas:
#     #         Color:
#     #             rgb: 0.1, 0.6, 0.3
#     #         Rectangle:
#     #             size: self.size
#     #             pos: self.pos
#     # Widget:
#     #     pos_hint: {'center_y': 0.5, 'center_x': 0.8}
#     #     size_hint: 0.2, 0.2
#     #     canvas:
#     #         Color:
#     #             rgb: 0.1, 0.6, 0.3
#     #         Rectangle:
#     #             size: self.size
#     #             pos: self.pos
#     # Widget:
#     #     pos_hint: {'center_y': 0.2, 'center_x': 0.5}
#     #     size_hint: 0.2, 0.2
#     #     canvas:
#     #         Color:
#     #             rgb: 0.1, 0.6, 0.3
#     #         Rectangle:
#     #             size: self.size
#     #             pos: self.pos
#     # Widget:
#     #     pos_hint: {'center_y': 0.8, 'center_x': 0.5}
#     #     size_hint: 0.2, 0.2
#     #     canvas:
#     #         Color:
#     #             rgb: 0.1, 0.6, 0.3
#     #         Rectangle:
#     #             size: self.size
#     #             pos: self.pos
# '''
#
# Builder.load_string(kv_string)
#
# class ColorStrip(Widget):
#     pass
#
# class MyWidget(FloatLayout):
#
#     def __init__(self):
#         super(MyWidget, self).__init__()
#
#     def create_strips(self):
#         with self.ids.id_background.canvas.before:
#             ColorStrip()
#
# class TestApp(App):
#
#     def build(self):
#         m = MyWidget()
#
#         m.create_strips()
#         return m
#
# if __name__ == '__main__':
#
#     t = TestApp()
#
#     t.run()

##########################################################

# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.lang import Builder
# from kivy.properties import ListProperty
#
# kv_string = '''
# <ColorStrip>:
#     pos_hint: {'center_y': 0.5, 'center_x': 0.5}
#     size_hint: 0.2, 0.2
#     canvas:
#         Color:
#             rgb: 0.1, 0.6, 0.3
#         Rectangle:
#             size: self.size
#             pos: self.pos
#
# <MyWidget>:
#     FloatLayout:
#         id: id_background
#         canvas.after:
#             Color:
#                 rgb: 0.9, 0.6, 0.3
#
# '''
#
# Builder.load_string(kv_string)
#
#
# class ColorStrip(Widget):
#     r_size = ListProperty([0, 0])
#
#
# class MyWidget(Widget):
#
#     def create_strips(self):
#         # with self.ids.id_background.canvas.before:
#         #     ColorStrip()
#         w = ColorStrip()
#         w.r_size = [20,40]
#         self.ids.id_background.add_widget(w)
#
# class TestApp(App):
#     def build(self):
#         m = MyWidget()
#         m.create_strips()
#         return m
#
# if __name__ == '__main__':
#     TestApp().run()


#########################################################"

# from kivy.lang import Builder
#
# from kivymd.app import MDApp
# from kivymd.uix.menu import MDDropdownMenu
#
# import kivy
# # kivy.require('1.0.5')
#
# from kivy.uix.floatlayout import FloatLayout
# from kivy.app import App
# from kivy.graphics import Rectangle
# from kivy.properties import ObjectProperty, StringProperty, NumericProperty
#
# KV = '''
# #:import get_color_from_hex kivy.utils.get_color_from_hex
# <ColorStrip>:
#     rectangle: id_rectangle
#     FloatLayout:
#         canvas:
#             Color:
#                 rgba: get_color_from_hex('#FF1111FF')
#
#             Rectangle:
#                 id: id_rectangle
#                 pos: root.proportional_horizontal_size, 0
#                 size: root.proportional_horizontal_size, root.height
#
# <Controlller>:
#     label_wid: my_custom_label
#
#     BoxLayout:
#         orientation: 'vertical'
#         padding: 20
#
#         Button:
#             text: 'My controller info is: ' + root.info
#             on_press: root.do_action()
#
#         Label:
#             id: my_custom_label
#             text: 'My label before button press'
#
#         Label:
#             text: f'One higher than favorite number: {root.favorite_number + 1}'
# '''


# class Test(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.screen = Builder.load_string(KV)
#         menu_items = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
#         self.menu = MDDropdownMenu(
#             caller=self.screen.ids.button, items=menu_items, width_mult=4
#         )
#
#     def build(self):
#         return self.screen


# class Controlller(FloatLayout):
#     '''Create a controller that receives a custom widget from the kv lang file.
#
#     Add an action to be called from the kv lang file.
#     '''
#     label_wid = ObjectProperty()
#     info = StringProperty()
#     favorite_number = NumericProperty(0)
#
#     def do_action(self):
#         self.label_wid.text = 'My label after button press'
#         self.info = 'New info text'
#
# class ColorStrip(FloatLayout):
#     proportional_horizontal_pos = NumericProperty(20)
#     proportional_horizontal_size = NumericProperty(20)
#
# class ControllerApp(App):
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.screen = Builder.load_string(KV)
#         # menu_items = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
#         # self.menu = MDDropdownMenu(
#         #     caller=self.screen.ids.button, items=menu_items, width_mult=4
#         # )
#
#     def build(self):
#         c = Controlller(info='Hello world', favorite_number=3)
#         c.add_widget(ColorStrip(proportional_horizontal_pos=20, proportional_horizontal_size=40))
#         return c
#
#
# if __name__ == '__main__':
#     ControllerApp().run()


#######################################################

# from kivy.lang import Builder
#
# from kivymd.app import MDApp
# from kivymd.uix.menu import MDDropdownMenu
# from kivymd.theming import ThemableBehavior
# from kivymd.uix.behaviors import RectangularElevationBehavior
# from kivymd.uix.boxlayout import MDBoxLayout
#
# KV = '''
# <CustomToolbar>:
#     size_hint_y: None
#     height: self.theme_cls.standard_increment
#     padding: "5dp"
#     spacing: "12dp"
#
#     MDIconButton:
#         id: button_1
#         icon: "menu"
#         pos_hint: {"center_y": .5}
#         on_release: app.menu_1.open()
#
#     MDLabel:
#         text: "MDDropdownMenu"
#         pos_hint: {"center_y": .5}
#         size_hint_x: None
#         width: self.texture_size[0]
#         text_size: None, None
#         font_style: 'H6'
#
#     Widget:
#
#     MDIconButton:
#         id: button_2
#         icon: "dots-vertical"
#         pos_hint: {"center_y": .5}
#         on_release: app.context_menu.open()
#
#
# Screen:
#
#     CustomToolbar:
#         id: toolbar
#         elevation: 10
#         pos_hint: {"top": 1}
# '''
#
#
# class CustomToolbar(
#     ThemableBehavior, RectangularElevationBehavior, MDBoxLayout,
# ):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.md_bg_color = self.theme_cls.primary_color
#
#
# class Test(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.screen = Builder.load_string(KV)
#         self.menu_1 = self.create_menu(
#             "Button menu", self.screen.ids.toolbar.ids.button_1
#         )
#         self.context_menu = self.create_menu(
#             "Button dots", self.screen.ids.toolbar.ids.button_2
#         )
#
#     def create_menu(self, text, instance):
#         menu_items = [{"icon": "android", "divider": None, "text": text} for i in range(5)]
#         return MDDropdownMenu(caller=instance, items=menu_items, width_mult=5)
#
#     def build(self):
#         return self.screen
#
#
# Test().run()
#

#######################################################

# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
# from kivy.properties import StringProperty
#
# from kivymd.app import MDApp
# from kivymd.uix.button import MDFlatButton
# from kivymd.uix.dialog import MDDialog
# from src.model.CommonUtils import CommonUtils as CU
# from kivymd.toast import toast
# from kivymd.uix.label import MDLabel
# from kivymd.uix.textfield import MDTextField
# from kivymd.uix.textfield import MDTextFieldRound
#
# KV = '''
# <NewDraftContent>
#     id: id_content
#     orientation: "vertical"
#     spacing: "12dp"
#     size_hint_y: None
#     height: "120dp"
#
#     MDTextField:
#         id: city_field
#         hint_text: "City"
#
#     MDTextField:
#         id: street_field
#         hint_text: "Street"
#
#
# FloatLayout:
#
#     MDFlatButton:
#         text: "ALERT DIALOG"
#         pos_hint: {'center_x': .5, 'center_y': .5}
#         on_release: app.show_confirmation_dialog()
# '''
#
# class NewDraftContent(BoxLayout):
#     pass
#
# class Example(MDApp):
#     dialog = None
#
#     def build(self):
#         return Builder.load_string(KV)
#
#     def callback_like_never_before(self, content_obj, *args, **kwargs):
#         print(f"callback fires")
#         # print(content_obj[0].ids['city_field'].text)
#
#         # content_obj[0][0].text
#         print("printing args")
#         print(args[0])
#
#
#     def show_confirmation_dialog(self):
#
#         dialog_text=f"foo bar"
#         content_obj = BoxLayout(orientation='vertical', spacing="12dp", size_hint_y=None, height="120dp")
#
#         mdlbl1 = MDLabel(text=f"This is explanation label")
#
#         mdtf1 = MDTextField()
#
#         mdtf1.hint_text="override"
#         mdtf1.helper_text = "wqsdf"
#         mdtf1.helper_text_mode = "on_focus"
#
#         content_obj.add_widget(mdlbl1)
#         content_obj.add_widget(mdtf1)
#
#         # CU.show_input_dialog(title="Please Enter", content_obj=content_obj, size_hint=(.8, .4),
#           #                    text_button_ok="OK", text_button_cancel="CANCEL", ok_callback_set=lambda *args, **kwargs: (print(f'wow outside {args[0]}'), self.callback_like_never_before(args, kwargs)))
#
#         CU.show_ok_cancel_dialog(f"This is the title", "Do you agree with this", size_hint=(.8, .4), text_button_ok="Yes", text_button_cancel="No", ok_callback_set=lambda *args, **kwargs: self.callback_like_never_before(args, kwargs))
#
#         print(f"from outside after dialog call")
#
#
# Example().run()

########################################"

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

#############################################################

# import mido
# import pygame
#
#
# def play_with_pygame(song):
#     # https://gist.github.com/naotokui/29073690279056e9354e6259efbf8f30
#     # https://stackoverflow.com/questions/27279864/generate-midi-file-and-play-it-without-saving-it-to-disk
#     pygame.init()
#     freq = 44100  # audio CD quality
#     bitsize = -16  # unsigned 16 bit
#     channels = 2  # 1 is mono, 2 is stereo
#     buffer = 1024  # number of samples
#     pygame.mixer.init(freq, bitsize, channels, buffer)
#     # optional volume 0 to 1.0
#     pygame.mixer.music.set_volume(0.8)
#
#     pygame.mixer.music.load(song)
#     length = pygame.time.get_ticks()
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.wait(length)
#
#
#
#
# if __name__ == '__main__':
#     main()

#############################################################
#
# import sys
# from mido import MidiFile
#
# if __name__ == '__main__':
#     # filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/all_by_myself.mid'
#     # filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/Movie_Themes_-_2001_-_Also_Sprach_Zarathustra_Richard_Strauss.mid'
#     filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/ChromaticBasics.mid'
#     # filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/ChromaticBasics2.mid'
#
#     # clip makes sure that no notes would be louder than 127
#     midi_file = MidiFile(filename, clip=True)
#     midi_file_type = midi_file.type
#     ticks_per_beat = midi_file.ticks_per_beat
#     length = midi_file.length
#
#     # type 0 (single track): all messages are saved in one track
#     # type 1 (synchronous): all tracks start at the same time
#     # type 2 (asynchronous): each track is independent of the others
#
#     print(f"The file type is {midi_file_type}")
#
#
#     for i, track in enumerate(midi_file.tracks):
#         sys.stdout.write('=== Track {}\n'.format(i))
#         for message in track:
#             if not message.is_meta:
#                 # Then it's about notes:
#
#                 sys.stdout.write('  {!r}\n'.format(message))
#
#
#     for msg in midi_file.play():
#         print(f"Test PDP: {msg}")

#############################################################

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
