import os
import sys
import random
import re
import threading
import time


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

    # The min_size_hint_y metric imposes an underbound to how small a ColorTone can be depicted while staying visible:
    min_size_hint_y = 0.01
    schedule_engine_freq = 4

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
        self.note_number_to_size_hint_x = {}
        self.note_number_to_color = {}
        self.note_number_to_count = {}
        self.toneflower_time_engine = None
        self.toneflower_schedule_engine = None
        self.elapsed_timer_offset_ns = 0
        self.playback_resume_abs_ns = 0
        self.elapsed_time_ns = 0
        self.elapsed_pos = 0
        self.start_time_offset = -1
        self.note_scale_factor = 1
        self.note_speed_factor = 1
        self.black_note_strips = []
        self.color_strips = {}
        self.note_scale_factor = 1
        self.min_tone_duration_ns = -1
        self.color_tones_song = []
        self.amount_color_tones_song = -1
        self.current_index_color_tones_song = 0
        self.visible_color_tones = {}

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

        # self.pool = None
        # self.toneflower_engine_2 = threading.Event()

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

    @staticmethod
    def on_pre_open_callback(instance):
        """
        Callback fired just before the ToneFlower ModalView is opened
        :param instance:
        :return:
        """
        # Trigger the creation of the white note strips that try to enhance the readability of the flowing tones:
        instance.prepare_toneflower()

    @staticmethod
    def on_open_callback(instance):
        """
        Callback fired after the ToneFlower ModalView is opened
        :param instance:
        :return:
        """

        instance.prepare_song()

    @staticmethod
    def on_pre_dismiss_callback(instance):
        """
        Callback fired on pre-dismissal of the ToneFlower ModalView
        :param instance: the instance of the ModalView itself, a non-static implementation would have passed 'self'
        :return:
        """
        instance.stop_toneflower_engine()

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

    def prepare_toneflower(self):

        # Reset the note_number_to_pos_hint_x dictionary:
        self.note_number_to_pos_hint_x = {}
        self.note_number_to_size_hint_x = {}
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
            self.note_number_to_size_hint_x[note] = rel_width
            self.note_number_to_color[note] = MTCU.NOTE_COLORS[MTCU.condense_note_pitch(note)]

            # Before the increment of note, create a color_strip for this note to indicate volume, waiting time etc:
            color_strip = ColorStrip()
            color_strip.strip_color = self.note_number_to_color[note]
            color_strip.pos_hint = {'x': self.note_number_to_pos_hint_x[note], 'y': 0.0}
            color_strip.size_hint = (self.note_number_to_size_hint_x[note], self.note_number_to_count.get(note, 0))

            self.ids.id_bottom_foreground.add_widget(color_strip)
            self.color_strips[note] = color_strip

            rel_hor_pos += rel_width
            note += 1

    def prepare_song(self):

        # Remove previous ColorTones if any:
        self.ids.id_top_foreground.clear_widgets()

        # clip makes sure that no notes would be louder than 127
        midi_file = MidiFile(self.filename, clip=True)
        midi_file_type = midi_file.type
        length = midi_file.length  # In sec
        ticks_per_beat = midi_file.ticks_per_beat

        note_number_to_index_of_latest = {}
        accumulated_ticks = 0

        sec_per_beat = 0
        sec_per_beat_ns = 0
        sec_per_tick = 0
        sec_per_tick_ns = 0

        # type 0 (single track): all messages are saved in one track
        # type 1 (synchronous): all tracks start at the same time
        # type 2 (asynchronous): each track is independent of the others

        print(f"The file type is \"{midi_file_type}\", has \"{ticks_per_beat} (=480)\" ticks_per_beat and a length of \"{length}\" sec.")

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
                        sec_per_beat_ns = message.tempo * 1e3
                        sec_per_beat = sec_per_beat_ns * 1e-9

                        sec_per_tick_ns = round(sec_per_beat_ns / ticks_per_beat)
                        sec_per_tick = sec_per_beat / ticks_per_beat

                elif message.type in ["note_on", "note_off"]:
                    # Then it's about notes:

                    accumulated_ticks += message.time

                    latest_index_of_note_number = note_number_to_index_of_latest.get(message.note, -1)

                    latest_tone_of_note_number = None

                    if latest_index_of_note_number > -1:
                        latest_tone_of_note_number = self.color_tones_song[latest_index_of_note_number]

                    if message.type == "note_on" and message.velocity > 0:
                        # A genuine note_on event:

                        tone = ColorTone()
                        tone.tf = self
                        tone.tone_color = self.note_number_to_color[message.note]
                        tone.pos_hint_x = self.note_number_to_pos_hint_x[message.note]
                        tone.start_offset_ns = accumulated_ticks * sec_per_tick_ns
                        tone.size_hint_x = self.note_number_to_size_hint_x[message.note]
                        tone.volume = message.velocity / 127

                        # Add ColorTone to collection of song
                        self.color_tones_song.append(tone)

                        current_index_of_note_number = len(self.color_tones_song) - 1

                        if latest_tone_of_note_number is not None:

                            tone.index_previous_note = latest_index_of_note_number

                            # Notify latest color tone of current index:
                            latest_tone_of_note_number.index_next_note = current_index_of_note_number

                            if latest_tone_of_note_number.duration_ns == -1:
                                # This means that the latest_tone_of_note_number has not seen a note_off event yet
                                # Not allowing it to overshadow the current note, it gets trimmed by a 'virtual' note_off event

                                latest_tone_of_note_number.duration_ns = accumulated_ticks - latest_tone_of_note_number.start_offset_ns

                                if self.min_tone_duration_ns == -1 or latest_tone_of_note_number.duration_ns < self.min_tone_duration_ns:
                                    self.min_tone_duration_ns = latest_tone_of_note_number.duration_ns

                        # Reset the start for this note_number:
                        note_number_to_index_of_latest[message.note] = current_index_of_note_number

                    else:
                        # A note_off event:

                        if latest_tone_of_note_number is not None:
                            latest_tone_of_note_number.duration_ns = accumulated_ticks - latest_tone_of_note_number.start_offset_ns

                            if self.min_tone_duration_ns == -1 or latest_tone_of_note_number.duration_ns < self.min_tone_duration_ns:
                                self.min_tone_duration_ns = latest_tone_of_note_number.duration_ns


                    # sys.stdout.write('  {!r}\n'.format(message))

        # Initialize the playback speed and scale factors:
        self.note_speed_factor = CU.tfs.dic['overall_note_speed_factor'].value
        self.note_scale_factor = CU.tfs.dic['overall_note_scale_factor'].value * (ToneFlower.min_size_hint_y / self.min_tone_duration_ns)

        # All ColorTone objects have been created for this song, store the amount for easy reuse by the toneflower_schedule_engine:
        self.amount_color_tones_song = len(self.color_tones_song)

        # Initialize the start_offset_pos and size_hint_y of all the notes now that the initial note_scale_factor is known:
        for color_tone in self.color_tones_song:
            color_tone.start_offset_pos = color_tone.start_offset_ns * self.note_scale_factor
            color_tone.size_hint_y = color_tone.duration_ns * self.note_scale_factor


        print(f"the initial size of the foreground is {self.ids.id_top_foreground.size}")
        # self.ids.id_top_foreground.size[1] = self.note_scale_factor * 100

        toast(f"ToneFlower engine ready...{os.linesep}"
              f"         Enjoy playing!")

    def start_stop_toneflower_engine(self):
        """
        Can start, pause and resume the toneflower_engine
        :return:
        """

        if (self.toneflower_time_engine is not None) or (self.toneflower_schedule_engine is not None):
            self.stop_toneflower_engine()

        else:
            self.start_toneflower_engine()

        # TODO PDP: FPS!!! https://stackoverflow.com/questions/40952038/kivy-animation-works-slowly

    def start_toneflower_engine(self):

        if self.start_time_offset > -1:
            self.elapsed_time_ns -= self.start_time_offset

            # In case of starting with offset somewhere, it's probably better not to show previous notes:
            self.ids.id_top_foreground.clear_widgets()

            # start_time_offset = 8 * sec_per_beat  # 8 beats
            # accumulated_ticks += start_time_offset
            # start_time_offset = True

        self.toneflower_schedule_engine = Clock.schedule_interval(self.tf_schedule_engine_cycle, 1/self.schedule_engine_freq)

        self.playback_resume_abs_ns = time.perf_counter_ns()
        self.toneflower_time_engine = Clock.schedule_interval(self.tf_time_engine_cycle, 0)

        # self.pool = mp.Pool(processes=self.CPU_COUNT)
        #
        # self.toneflower_engine_2.clear()

        # self.toneflower_time_engine = threading.Thread(target=self.infinite_loop())
        # self.toneflower_time_engine.daemon = True
        #
        # self.toneflower_time_engine.start()

        toast(f"ToneFlower engine started")

    def stop_toneflower_engine(self):

        if self.toneflower_time_engine is not None:
            self.toneflower_time_engine.cancel()
            self.toneflower_time_engine = None

        if self.toneflower_schedule_engine is not None:
            self.toneflower_schedule_engine.cancel()
            self.toneflower_schedule_engine = None

        # self.toneflower_engine_2.set()

        toast(f"ToneFlower engine stopped")

    def tf_time_engine_cycle(self, *largs, **kwargs):
        """

        :return:
        """

        self.elapsed_time_ns += (time.perf_counter_ns() - self.playback_resume_abs_ns) * self.note_speed_factor
        self.elapsed_pos = self.elapsed_time_ns * self.note_scale_factor

    def tf_schedule_engine_cycle(self, *largs, **kwargs):
        elapsed_pos_on_top = self.elapsed_pos + 1 + (self.note_scale_factor/ToneFlower.schedule_engine_freq)
        # elapsed_time_ns_on_top = self.elapsed_time_ns + (1 + ToneFlower.schedule_engine_freq)/self.note_scale_factor

        # Initialize color_tone by using a default:
        color_tone = ColorTone()

        while (color_tone.start_offset_pos <= elapsed_pos_on_top) and (self.current_index_color_tones_song < self.amount_color_tones_song):

            color_tone = self.color_tones_song[self.current_index_color_tones_song]

            self.ids.id_top_foreground.add_widget(color_tone, len(self.ids.id_background.children))

            self.visible_color_tones[self.current_index_color_tones_song] = color_tone

            color_tone.start_colortone_engine()

            self.current_index_color_tones_song += 1



    def infinite_loop(self):
        while True:
            if self.toneflower_engine_2.is_set():
                # Stop running this thread so the main Python process can exit.
                return

            self.calculate_frame(0.016667)


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

        delta = time_passed * CU.tfs.dic['overall_note_speed_factor'].value

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

        # delta = time_passed * CU.tfs.dic['overall_note_speed_factor'].value
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


class ColorStrip(Widget):
    pass

class ColorTone(Widget):
    pos_hint_x = NumericProperty(0)
    pos_hint_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ColorTone, self).__init__(**kwargs)

        self.tf = None
        self.note_number = -1
        self.start_offset_ns = -1
        self.start_offset_pos = -1
        self.duration_ns = -1
        self.volume = 1.0
        self.colortone_flow_engine = None

        """Index of next note with same note_number"""
        self.index_next_note = -1

        """Index of previous note with same note_number"""
        self.index_previous_note = -1

    def start_colortone_engine(self):
        self.colortone_flow_engine = Clock.schedule_interval(self.ct_flow_engine_cycle, 0)

    def stop_colortone_engine(self):
        if self.colortone_flow_engine is not None:
            self.colortone_flow_engine.cancel()
            self.colortone_flow_engine = None

    def ct_flow_engine_cycle(self, *largs, **kwargs):
        self.pos_hint_y = self.start_offset_pos - self.tf.elapsed_pos
        print(f"note {(self.index_previous_note + self.index_next_note)*0.5} has position: {self.pos_hint_y}")
