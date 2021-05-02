import os
import sys
import random
import re
import threading

import aiofiles
import pathlib as pl
from datetime import datetime
import multiprocessing as mp

from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.properties import ObservableList, ListProperty, NumericProperty, StringProperty

from mido import (MidiFile, bpm2tempo, tempo2bpm, tick2second, second2tick,)

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
    # CPU_COUNT = mp.cpu_count()

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
        self.color_white_note_strips = get_color_from_hex('#161616FF') if (CU.tfs.dic['toggle_white_note_strips'].value) else get_color_from_hex('#000000FF')
        self.note_number_to_pos_hint_x = {}
        self.note_number_to_width = {}
        self.note_number_to_color = {}
        self.note_number_to_count = {}
        self.tone_flower_engine = None
        self.black_note_strips = []
        self.color_strips = {}
        self.note_scale_factor = 1

        self.song_position = 1

        # # The start time of the object.
        # time_number
        # # The beats-per-measure (upper number) of the time signature.
        self.time_signature_numerator = 0
        # # The type of beat (lower number) of the time signature.
        # time_signature_denominator
        # # The number of "MIDI clocks" between metronome clicks. There are 24 MIDI clocks in one quarter note.
        # clocks_integer
        # # The number of notated 32nds in 24 MIDI clocks. The default value is 8.
        # 32nds_integer

        self.ppq = 0

        self.color_tones_song = []

        self.pool = None
        self.toneflower_engine_2 = threading.Event()

        # TODO: Playalong platform independently https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python/27978895#27978895
        # TODO: note to freq: https://pages.mtu.edu/~suits/notefreqs.html
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/all_by_myself.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/Movie_Themes_-_2001_-_Also_Sprach_Zarathustra_Richard_Strauss.mid'

        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/ChromaticBasics2.mid'
        self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/InDitHuisje.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/Game_of_Thrones_Easy_piano.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/Ed_Sheeran_-_Perfect_-_Ed_Sheeran.mid'


        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/ChromaticBasics.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/How_Far_Ill_Go.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/How_Far_Ill_Go1Octavev1.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/How_Far_Ill_Go1Octavev2.mid'

        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/LittleSubmarine_TheStarlings1Octave_Preprocessed.mid'



        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/preprocessed-eerste-wals.mid'
        # self.filename = '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/MIDI_Files/preprocessed-melodie-met-kwartnoten.mid'



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

    #     # TODO: Can _list not refer directly to listproperty of the widget? self.ids.rv.data
    #     self._list = list()  # ObservableList(None, object, list())
    #
    #
    # def get_list(self):
    #     return self._list
    #
    # def set_list(self, list):
    #     list = CU.safe_cast(list, self._list.__class__, "")
    #     self._list = list

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

    # list = property(get_list, set_list)
    playlist = property(get_playlist, set_playlist)
    block_close = property(get_block_close, set_block_close)

    def prepare_toneflower_engine(self):

        # Reset the note_number_to_pos_hint_x dictionary:
        self.note_number_to_pos_hint_x = {}
        self.note_number_to_width = {}
        self.note_number_to_color = {}
        self.note_number_to_count = {}

        # Adjust low_pitch_limit and high_pitch_limit, in case the song does not need the entire range:
        low_pitch_limit = MTCU.note_name_to_number(CU.tfs.dic['low_pitch_limit'].value)
        high_pitch_limit = MTCU.note_name_to_number(CU.tfs.dic['high_pitch_limit'].value)

        if (self.filename is not None):
            # Narrow the low_pitch_limit and high_pitch_limit if the song allows it:
            # clip makes sure that no notes would be louder than 127
            midi_file = MidiFile(self.filename, clip=True)

            low_pitch_limit_song = -1
            high_pitch_limit_song = -1

            for track in midi_file.tracks:
                for message in track:

                    if message.type in ["note_on", "note_off"]:

                        # Then it's about notes:
                        if (message.note > high_pitch_limit_song) or (high_pitch_limit_song == -1):
                            high_pitch_limit_song = message.note

                        if ((message.note < low_pitch_limit_song) or (low_pitch_limit_song == -1)):
                            low_pitch_limit_song = message.note

                        # Since some MIDI-files have note_on messages wit velocity==0 to indicate note_off, both events
                        # are counted, will correct afterwards:
                        if message.note in self.note_number_to_count:
                            self.note_number_to_count[message.note] += 1

                        else:
                            self.note_number_to_count[message.note] = 1

            low_pitch_limit = low_pitch_limit_song if low_pitch_limit_song > low_pitch_limit else low_pitch_limit
            high_pitch_limit = high_pitch_limit_song if high_pitch_limit_song < high_pitch_limit else high_pitch_limit

            # Normalize note_number occurrences to show it later in histogram with the color_strip bars
            max_note_number_occurrence = max(self.note_number_to_count.values())

            for note_number in self.note_number_to_count:
                self.note_number_to_count[note_number] /= max_note_number_occurrence

        # Calculate the amount, size and position of the background color_strips:
        amount_white_keys, amount_black_keys = MTCU.note_interval_to_key_range(low_pitch_limit, high_pitch_limit)

        rel_width_black_key = 1.0 / (amount_white_keys * 2 + amount_black_keys)
        rel_width_white_key = 2 * rel_width_black_key

        # Add the black_note_strips as rectangle in the background to the floatlayout:
        # In an earlier version, white_note_strips were added, but it happened to be more efficient (i.e. less objects) if the black strips would be added
        note = low_pitch_limit
        rel_hor_pos = 0.0

        while note <= high_pitch_limit:

            rel_width = 0.0

            if MTCU.is_white_note(note):
                # A white note will be rendered with twice the relative width of a black note.
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
            self.note_number_to_pos_hint_x[note] = rel_hor_pos
            self.note_number_to_width[note] = rel_width
            self.note_number_to_color[note] = MTCU.NOTE_COLORS[MTCU.condense_note_pitch(note)]

            # Before the increment of note, create a color_strip for this note to indicate volume, waiting time etc:
            color_strip = ColorStrip()
            color_strip.strip_color = self.note_number_to_color[note]
            color_strip.pos_hint = {'x': self.note_number_to_pos_hint_x[note], 'y': 0.0}
            color_strip.size_hint = (self.note_number_to_width[note], self.note_number_to_count.get(note, 0))

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
            # self.tone_flower_engine.cancel()
            # self.tone_flower_engine = None
            self.toneflower_engine_2.set()
            toast(f"ToneFlower engine paused")
        else:


            # self.tone_flower_engine = Clock.schedule_interval(self.calculate_frame, 1/60.0)
            self.pool = mp.Pool(processes=self.CPU_COUNT)

            self.toneflower_engine_2.clear()

            self.tone_flower_engine = threading.Thread(target=self.infinite_loop())
            self.tone_flower_engine.daemon = True

            self.tone_flower_engine.start()



            toast(f"ToneFlower engine started")

        # TODO PDP: FPS!!! https://stackoverflow.com/questions/40952038/kivy-animation-works-slowly

    def infinite_loop(self):
        while True:
            if self.toneflower_engine_2.is_set():
                # Stop running this thread so the main Python process can exit.
                return

            self.calculate_frame(0.016667)

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

    @staticmethod
    def on_open_callback(instance):
        """
        Callback fired after the ToneFlower ModalView is opened
        :param instance:
        :return:
        """

        # Remove previous ColorTones if any:
        instance.ids.id_top_foreground.clear_widgets()

        # clip makes sure that no notes would be louder than 127
        midi_file = MidiFile(instance.filename, clip=True)
        midi_file_type = midi_file.type
        length = midi_file.length #In sec
        ticks_per_beat = midi_file.ticks_per_beat

        sec_per_beat = 0
        ns_sec_per_beat = 0
        sec_per_tick = 0
        ns_sec_per_tick = 0

        # type 0 (single track): all messages are saved in one track
        # type 1 (synchronous): all tracks start at the same time
        # type 2 (asynchronous): each track is independent of the others

        print(f"The file type is {midi_file_type} and ticks_per_beat {ticks_per_beat} (=480), length {length} sec")

        # TODO PDP: Revisit this: what if two notes of same note_number simultaneously & how to make link to next note
        note_number_to_start = {}
        elapsed_ticks = 0
        start_time_offset = 0
        start_time_offset_known = False

        for track in midi_file.tracks:
            for message in track:
                if message.is_meta:

                    if message.type == "time_signature":
                        # < meta
                        # message
                        # time_signature
                        # numerator = 1
                        # denominator = 4
                        # clocks_per_click = 24
                        # notated_32nd_notes_per_beat = 8
                        # time = 0 >

                        pass

                    elif message.type == "set_tempo":
                        sec_per_beat = message.tempo * 1e-6
                        ns_sec_per_beat = sec_per_beat * 1e9
                        sec_per_tick = sec_per_beat / ticks_per_beat
                        ns_sec_per_tick = ns_sec_per_beat / ticks_per_beat

                        if not start_time_offset_known:
                            start_time_offset = 8 * sec_per_beat # 8 beats
                            # elapsed_ticks += start_time_offset
                            start_time_offset = True



                elif message.type in ["note_on", "note_off"]:
                    # Then it's about notes:

                    elapsed_ticks += message.time

                    if message.type == "note_on" and message.velocity > 0:
                        # A genuine note_on event:

                        if message.note in note_number_to_start:

                            if note_number_to_start[message.note] == -1:
                                # In this case a note_off event (prior to the currently processed note_one-event) has reset the note:
                                # Store the beginning of the note in dict:

                                note_number_to_start[message.note] = elapsed_ticks

                        else:
                            note_number_to_start[message.note] = elapsed_ticks


                    else:
                        # A note_off event:

                        tone = ColorTone()
                        tone.tone_color = instance.note_number_to_color[message.note]
                        # tone.pos_hint = {'x': instance.note_number_to_pos_hint_x[message.note],
                        #                  'y': (note_number_to_start[message.note] + start_time_offset)}
                        tone.pos_hint_x = instance.note_number_to_pos[message.note]
                        tone.pos_hint_y = (note_number_to_start[message.note])

                        # tone.pos[1] = note_number_to_start[message.note] * instance.note_scale_factor + start_time_offset

                        tone.size_hint = (instance.note_number_to_size[message.note], elapsed_ticks - note_number_to_start[message.note])
                        # tone.size[1] = (elapsed_ticks - note_number_to_start[message.note]) * instance.note_scale_factor

                        # Reset the start for this note_number:
                        note_number_to_start[message.note] = -1

                        # Add ColorTone to collection of song
                        instance.color_tones_song.append(tone)

                        # TODO PDP: move this to thread
                        # instance.ids.id_top_foreground.add_widget(tone, len(instance.ids.id_background.children))


                    # sys.stdout.write('  {!r}\n'.format(message))

        # instance.ids.id_top_foreground.pos_hint["y"] = 0.5

        print(f"the intial size is {instance.ids.id_top_foreground.size}")
        instance.ids.id_top_foreground.size[1] = instance.note_scale_factor * 100

        toast(f"ToneFlower engine ready...{os.linesep}"
              f"         Enjoy playing!")


    def calculate_frame(self, time_passed):
        # print(time_passed)
        self.flow_tones(time_passed)

        # results = self.pool.starmap_async(self.change_height_color_strip, [color_strip for color_strip in self.color_strips.values()]).get()

    def change_height_color_strip(self, color_strip):
        color_strip.size_hint_y = random.gauss(0.5, 0.1666)
        print(color_strip.size_hint_y)

    @mainthread
    def shift_color_tone(self, arg):
        child, delta = arg
        child.pos_hint_y -= delta


    @mainthread
    def flow_tones(self, time_passed):

        # Resize

        # size is the pixel height of the part from the splitter to the top

        # print(self.ids.id_top_foreground.size[1])
        # Statement  below can resize, but better scheduled on less frequently polled thread.
        # self.ids.id_top_foreground.size[1] = self.note_scale_factor * 100



        # print(f"delta {time_passed * 0.5 * self.note_scale_factor}")
        # print(f"song_position {self.song_position}")

        delta = time_passed * CU.tfs.dic['overall_speedfactor'].value

        # for child in self.ids.id_top_foreground.children:
        child = self.ids.id_top_foreground.children[0]
        child.pos_hint_y -= delta
        print(f'done')

        # self.pool = mp.Pool(mp.cpu_count())
        # list_of_results = self.pool.map(self.shift_color_tone , ((child, delta) for child in self.ids.id_top_foreground.children))
        # self.pool.close()
        # self.pool.join()

        # The statement to update the relative layout as a whole does not work together with the note_scale_factor
        # self.ids.id_top_foreground.pos_hint["y"] -= 1


        #############################
        # Original working code with kivy clock:

        # delta = time_passed * CU.tfs.dic['overall_speedfactor'].value
        #
        # # Is this parallellizible?
        # for child in self.ids.id_top_foreground.children:
        #     child.pos_hint_y -= delta

        ###############################"

        # self.ids.id_top_foreground.pos_hint['x'] += 0.01

        # print(f"size {self.ids.id_top_foreground.size[1]}")
        # print(f"pos {self.ids.id_top_foreground.pos[1]}")



        # self.ids.id_top_foreground.size_hint['y'] -= 0.0001

        # for child in self.ids.id_top_foreground.children:
        #     child.y -= time_passed * 50.0

        # for key, value in self.color_tones_song.items():
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
    pos_hint_x = NumericProperty(0)
    pos_hint_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ColorTone, self).__init__(**kwargs)

        self.note_number = -1
        self.start_tick = -1
        self.volume = 1.0
        self.toneflower_engine = None
        self.next_note_link = -1