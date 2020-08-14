import os
import sys
import re
import aiofiles
import pathlib as pl
from datetime import datetime

from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.utils import get_color_from_hex
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.properties import ObservableList, ListProperty, StringProperty


from kivymd.uix.useranimationcard import MDUserAnimationCard
from kivy.uix.modalview import ModalView
from kivymd.uix.label import MDLabel


from kivymd.utils import asynckivy
from kivymd.toast import toast

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.CommonUtils import CommonUtils as CU
from src.model.MusicTheoryCoreUtils import MusicTheoryCoreUtils as MTCU


# class ToneFlowerProvider:
#
#     tf = None
#
#     def __init__(self, playlist, **kwargs):
#
#         self._playlist = playlist
#
#         # I chose to store the modal view locally when created, so it does not need to be created over and over again:
#         self._modal_view = None
#
#     def get_playlist(self):
#         return self._playlist
#
#     def set_file_path(self, file_path):
#         file_path = CU.safe_cast(file_path, pl.Path, None)
#
#         if self._playlist != file_path:
#             self._playlist = file_path
#             # Reset modal view when the file path changed, just to be sure it's recreated when needed next time:
#             self._modal_view = None
#
#     def get_modal_view(self):
#         if self._modal_view is None:
#             # Create modal view only if asked for (to save computational power):
#             self._modal_view = ToneFlower(self._playlist)
#
#         return self._modal_view
#
#     file_path = property(get_playlist, set_file_path)
#     modal_view = property(get_modal_view)


class ToneFlower(ModalView):
    app = None
    is_kv_loaded = False

    def __init__(self, playlist, **kwargs):
        if (not ToneFlower.is_kv_loaded):
            # Make sure it's only loaded once:
            Builder.load_file(str(curr_file.parents[1] / "view" / (pl.Path(ToneFlower.__name__).with_suffix(".kv")).name))
            ToneFlower.app = App.get_running_app()
            ToneFlower.is_kv_loaded = True
        super(ToneFlower, self).__init__(**kwargs)

        # Initializing properties of ModalView:
        self.size_hint = (1, 1)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.background_color = (0, 0, 0, 0)
        self.white_note_strips = []
        self.render_width_black_key = 10.0
        self.note_number_to_pos = {}


        # When auto_dismiss==True, then you can escape the modal view with [ESC]
        self.auto_dismiss = True
        # can be argument in ModalView Constructor border = (16, 16, 16, 16)

        # Binding events that come with the ModalView ('on_pre_open', 'on_open', 'on_pre_dismiss', 'on_dismiss') to
        # their respective static methods:
        self.bind(on_pre_open=ToneFlower.on_pre_open_callback)
        self.bind(on_open=ToneFlower.on_open_callback)
        self.bind(on_pre_dismiss=ToneFlower.on_pre_dismiss_callback)
        self.bind(on_dismiss=ToneFlower.on_dismiss_callback)

        # Initializing custom properties:pipe
        self._block_close = False
        self._playlist = playlist


        self._former_primary_palette, self._former_accent_palette = ToneFlower.app.theme_cls.primary_palette, ToneFlower.app.theme_cls.accent_palette
        self._former_context_menus = ToneFlower.app.context_menus

        # TODO: Can _list not refer directly to listproperty of the widget? self.ids.rv.data
        self._list = list()  # ObservableList(None, object, list())


    def get_list(self):
        return self._list

    def set_list(self, list):
        list = CU.safe_cast(list, self._list.__class__, "")
        self._list = list

    def get_context_menus(self):
        return self._context_menus

    def get_playlist(self):
        return self._playlist

    def set_playlist(self, playlist):
        self._playlist = playlist

    def get_block_close(self):
        return self._block_close

    def set_block_close(self, block_close):
        self._block_close = block_close

    list = property(get_list, set_list)
    playlist = property(get_playlist, set_playlist)
    block_close = property(get_block_close, set_block_close)

    def create_white_note_strips(self):

        # Reset the note_number_to_pos dictionary:
        self.note_number_to_pos = {}

        # Only proceed if these white note strips are required by the TFSettings:
        if (CU.tfs.dic['toggle_white_note_strips'].value):

            low_pitch_limit = MTCU.note_name_to_number(CU.tfs.dic['low_pitch_limit'].value)
            high_pitch_limit = MTCU.note_name_to_number(CU.tfs.dic['high_pitch_limit'].value)

            amount_white_keys, amount_black_keys = MTCU.note_interval_to_key_range(low_pitch_limit, high_pitch_limit)

            self.render_width_black_key = Window.width / (amount_white_keys * 2 + amount_black_keys)

            white_strip_position = self.pos

            # A call to the clear method would erase everything that has been drawn so far on the canvas:
            # self.ids.id_background.canvas.before.clear()

            # Add to the canvas the white_note_strips as rectangle in the background:
            with self.ids.id_background.canvas.before:

                Color(rgba=get_color_from_hex("#111111FF"))

                note = low_pitch_limit
                while note <= high_pitch_limit:

                    if MTCU.is_white_note(note):
                        # A white note will be rendered with twice the width of a black note, two adjacent white notes 4 times that size:

                        # TODO: https://blog.kivy.org/2014/10/updating-canvas-instructions-declared-in-python/


                        if MTCU.is_white_note(note + 1):
                            # In case of adjacent E, F or B, C, one white_strip can be saved by drawing a wider one instead.
                            # This might be good for performance
                            rect = Rectangle(pos=white_strip_position, size=(self.render_width_black_key * 4, self.height))
                            self.white_note_strips.append(rect)

                            # Increment the current note, because we draw two at once:
                            note += 1

                        else:
                            rect = Rectangle(pos=white_strip_position, size=(self.render_width_black_key * 2, self.height))
                            self.white_note_strips.append(rect)

                        white_strip_position[0] += rect.size[0]

                    else:
                        white_strip_position[0] += self.render_width_black_key
                        # Callback(self.my_callback)

                    note += 1

            self.bind(pos=self.update_rect, size=self.update_rect)

                # pipe.size_hint = (None, None)
                # pipe.pos = (Window.width + i * distance_between_pipes, 96)
                # pipe.size = (64, self.root.height - 96)
                #
                # self.pipes.append(pipe)
                # self.root.add_widget(pipe)

    def update_rect(self, *args):
        for white_note_strip in self.white_note_strips:
            # white_note_strip.pos = self.pos
            white_note_strip.size = white_note_strip.size[0], self.height

    def load_from_json(self):
        # TODO
        pass

    def save_to_json(self):
        # TODO
        pass

    @staticmethod
    def on_pre_open_callback(instance):
        """
        Callback fired just before the ToneFlower ModalView is opened
        :param instance:
        :return:
        """
        # Trigger the creation of the white note strips that try to enhance the readability of the flowing tones:
        instance.create_white_note_strips()

        # Override needed overscroll to refresh the screen to the bare minimum:
        # refresh_layout.effect_cls.min_scroll_to_reload = -dp(1)


    @staticmethod
    def on_open_callback(instance):
        """
        Callback fired after the ToneFlower ModalView is opened
        :param instance:
        :return:
        """
        # self.refresh_list()
        toast(f"ToneFlower engine ready...{os.linesep}"
              f"    Enjoy playing!")

    @staticmethod
    def on_pre_dismiss_callback(instance):
        """
        Callback fired on pre-dismissal of the ToneFlower ModalView
        :param instance: the instance of the ModalView itself, a non-static implementation would have passed 'self'
        :return:
        """
        # TODO: Warn display popup not to leave with unsaved progress:
        pass

    @staticmethod
    def on_dismiss_callback(instance):
        """
        Callback fired on dismissal of the ToneFlower ModalView
        :param instance: the instance of the ModalView itself, a non-static implementation would have passed 'self'
        :return: True prevents the modal view from closing
        """
        if instance.block_close:
            toast(f"Blocked closing")
        else:
            pass

        return instance.block_close