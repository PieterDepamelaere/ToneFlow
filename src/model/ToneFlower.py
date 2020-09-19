import os
import sys
import random
import re
import aiofiles
import pathlib as pl
from datetime import datetime

from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.properties import ObservableList, ListProperty, NumericProperty, StringProperty

from mido import MidiFile

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
        self.pos_hint = {'x': 0, 'y': 0}
        self.background_color = (0, 0, 0, 0)
        self.color_white_note_strips = get_color_from_hex('#111111FF') if (CU.tfs.dic['toggle_white_note_strips'].value) else get_color_from_hex('#000000FF')
        self.note_number_to_pos = {}
        self.note_number_to_size = {}
        self.note_number_to_color = {}
        self.tone_flower_engine = None
        self.black_note_strips = []
        self.color_strips = {}

        # TODO PDP: note_number mappen op queue<SoortToneObject> hier?
        self.color_tones = {}

        # TODO: Playalong platform independently https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python/27978895#27978895
        # TODO: note to freq: https://pages.mtu.edu/~suits/notefreqs.html
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/all_by_myself.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/Movie_Themes_-_2001_-_Also_Sprach_Zarathustra_Richard_Strauss.mid'

        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/ChromaticBasics2.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/InDitHuisje.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/Game_of_Thrones_Easy_piano.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/Ed_Sheeran_-_Perfect_-_Ed_Sheeran.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/LittleSubmarine_TheStarlings1Octave_Preprocessed.mid'

        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/ChromaticBasics.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/How_Far_Ill_Go.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/How_Far_Ill_Go1Octavev1.mid'
        self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/How_Far_Ill_Go1Octavev2.mid'


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

    def prepare_toneflower_engine(self):

        # Reset the note_number_to_pos dictionary:
        self.note_number_to_pos = {}
        self.note_number_to_size = {}
        self.note_number_to_color = {}

        low_pitch_limit = MTCU.note_name_to_number(CU.tfs.dic['low_pitch_limit'].value)
        high_pitch_limit = MTCU.note_name_to_number(CU.tfs.dic['high_pitch_limit'].value)

        if (self.filename is not None):
            # Narrow the low_pitch_limit and high_pitch_limit if the song allows it:
            # clip makes sure that no notes would be louder than 127
            midi_file = MidiFile(self.filename, clip=True)

            low_pitch_limit_song = -1
            high_pitch_limit_song = -1

            for i, track in enumerate(midi_file.tracks):
                # sys.stdout.write('=== Track {}\n'.format(i))
                for message in track:
                    if message.type in ["note_on", "note_off"]:
                        # Then it's about notes:
                        if (message.note > high_pitch_limit_song) or (high_pitch_limit_song == -1):
                            high_pitch_limit_song = message.note
                        if ((message.note < low_pitch_limit_song) or (low_pitch_limit_song == -1)):
                            low_pitch_limit_song = message.note

            low_pitch_limit = low_pitch_limit_song if low_pitch_limit_song > low_pitch_limit else low_pitch_limit
            high_pitch_limit = high_pitch_limit_song if high_pitch_limit_song < high_pitch_limit else high_pitch_limit




        # Adjust low_pitch_limit and high_pitch_limit, in case the song does not need the entire range:
        # TODO: implement

        amount_white_keys, amount_black_keys = MTCU.note_interval_to_key_range(low_pitch_limit, high_pitch_limit)

        rel_width_black_key = 1.0 / (amount_white_keys * 2 + amount_black_keys)
        rel_width_white_key = 2 * rel_width_black_key

        # Add the black_note_strips as rectangle in the background to the floatlayout:

        note = low_pitch_limit
        rel_hor_pos = 0.0

        while note <= high_pitch_limit:

            rel_width = 0.0

            if MTCU.is_white_note(note):
                # A white note will be rendered with twice the white_strip_width of a black note.
                rel_width = rel_width_white_key

            else:
                # Add black note strip:
                rel_width = rel_width_black_key

                if (CU.tfs.dic['toggle_white_note_strips'].value):
                    black_note_strip = ColorStrip()
                    black_note_strip.strip_color = get_color_from_hex('#000000FF')
                    black_note_strip.pos_hint = {'x': rel_hor_pos, 'y': 0.0}
                    black_note_strip.size_hint = (rel_width, 1.0)

                    self.ids.id_background.add_widget(black_note_strip, len(self.ids.id_background.children))
                    self.black_note_strips.append(black_note_strip)

            # Before this increment of note, store correct rel_hor_pos, rel_width and color in resp. dicts:
            self.note_number_to_pos[note] = rel_hor_pos
            self.note_number_to_size[note] = rel_width
            self.note_number_to_color[note] = MTCU.NOTE_COLORS[MTCU.condense_note_pitch(note)]

            # Before the increment of note, create a color_strip for this note to indicate volume, waiting time etc:
            color_strip = ColorStrip()
            color_strip.strip_color = self.note_number_to_color[note]
            color_strip.pos_hint = {'x': self.note_number_to_pos[note], 'y': 0.0}
            color_strip.size_hint = (self.note_number_to_size[note], 0.25 + 0.5 * random.uniform(0, 1))

            self.ids.id_bottom_foreground.add_widget(color_strip)
            self.color_strips[note] = color_strip

            rel_hor_pos += rel_width
            note += 1

    def start_stop_toneflower_engine(self):
        """
        Can start, pause and resume the toneflower_engine
        :return:
        """

        if self.tone_flower_engine is not None:
            self.tone_flower_engine.cancel()
            self.tone_flower_engine = None
            toast(f"ToneFlower engine paused")
        else:
            self.tone_flower_engine = Clock.schedule_interval(self.calculate_frame, 1 / 60.0)
            toast(f"ToneFlower engine started")


        # TODO PDP: FPS!!! https://stackoverflow.com/questions/40952038/kivy-animation-works-slowly



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
        instance.prepare_toneflower_engine()

        # Override needed overscroll to refresh the screen to the bare minimum:
        # refresh_layout.effect_cls.min_scroll_to_reload = -dp(1)


    @staticmethod
    def on_open_callback(instance):
        """
        Callback fired after the ToneFlower ModalView is opened
        :param instance:
        :return:
        """

        # clip makes sure that no notes would be louder than 127
        midi_file = MidiFile(instance.filename, clip=True)
        midi_file_type = midi_file.type
        ticks_per_beat = midi_file.ticks_per_beat
        length = midi_file.length

        # type 0 (single track): all messages are saved in one track
        # type 1 (synchronous): all tracks start at the same time
        # type 2 (asynchronous): each track is independent of the others

        print(f"The file type is {midi_file_type}")

        note_number_pos = {}
        elapsed_ticks = 0
        vert_pos_offset = 300

        for i, track in enumerate(midi_file.tracks):
            # sys.stdout.write('=== Track {}\n'.format(i))
            for message in track:
                if message.is_meta:
                    pass

                elif message.type in ["note_on", "note_off"]:
                    # Then it's about notes:

                    if message.type == "note_on" and message.velocity > 0:
                        # A genuine note_on event:
                        # Store the beginning of the note in dict:
                        elapsed_ticks += (message.time * 0.1)
                        note_number_pos[message.note] = elapsed_ticks

                    else:
                        # A note_off event:
                        elapsed_ticks += (message.time * 0.1)

                        tone = ColorTone()
                        tone.tone_color = instance.note_number_to_color[message.note]
                        tone.pos_hint = {'x': instance.note_number_to_pos[message.note]}
                        tone.pos[1] = note_number_pos[message.note] *2 + vert_pos_offset
                        tone.size_hint = (instance.note_number_to_size[message.note], None)
                        tone.size[1] = (elapsed_ticks - note_number_pos[message.note]) *2

                        instance.ids.id_top_foreground.add_widget(tone, len(instance.ids.id_background.children))


                    # sys.stdout.write('  {!r}\n'.format(message))

        toast(f"ToneFlower engine ready...{os.linesep}"
              f"         Enjoy playing!")


        #
        # tone2 = ColorTone()
        # tone2.tone_color = instance.note_number_to_color[67]
        # tone2.pos_hint = {'x': instance.note_number_to_pos[67]}
        # tone2.pos[1] = 600
        # tone2.size_hint = (instance.note_number_to_size[67], None)
        # tone2.size[1] = 45
        #
        #
        # instance.ids.id_top_foreground.add_widget(tone2, len(instance.ids.id_background.children))
        #
        # instance.color_tones[60] = [tone]
        # instance.color_tones[67] = [tone2]
        #

    def calculate_frame(self, time_passed):
        # print(time_passed)
        self.flow_tones(time_passed)

    def flow_tones(self, time_passed):

        self.ids.id_top_foreground.pos[1] -= time_passed * 50.0 * 2

        # self.ids.id_top_foreground.size_hint['y'] -= 0.0001

        # for child in self.ids.id_top_foreground.children:
        #     child.y -= time_passed * 50.0

        # for key, value in self.color_tones.items():
            # for tone in value:
            #     tone.y -= time_passed *50.0
                # tone.pos_hint['y'] -= time_passed/10.0

    @staticmethod
    def on_pre_dismiss_callback(instance):
        """
        Callback fired on pre-dismissal of the ToneFlower ModalView
        :param instance: the instance of the ModalView itself, a non-static implementation would have passed 'self'
        :return:
        """
        if instance.tone_flower_engine is not None:
            instance.tone_flower_engine.cancel()
            instance.tone_flower_engine = None

    @staticmethod
    def on_dismiss_callback(instance):
        """
        Callback fired on dismissal of the ToneFlower ModalView
        :param instance: the instance of the ModalView itself, a non-static implementation would have passed 'self'
        :return: True prevents the modal view from closing
        """
        if instance.block_close:
            toast(f"Blocked closing")

        return instance.block_close


class ColorStrip(Widget):
    pass

class ColorTone(Widget):
    pass