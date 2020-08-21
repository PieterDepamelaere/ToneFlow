import mido
from mido import MidiFile
from src.model.CommonUtils import CommonUtils as CU

all_mid = ['major-scale.mid']


class MusicTheoryCoreUtils:

    # Inspiration from https://stackoverflow.com/questions/59571840/why-is-clean-midi-file-playing-differently-with-mido
    # https://www.twilio.com/blog/working-with-midi-data-in-python-using-mido
    # https://mido.readthedocs.io/en/latest/midi_files.html

    # https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies

    NOTE_SYSTEM = {0: 'C', 1: 'C#/Db', 2: 'D', 3: 'D#/Eb', 4: 'E', 5: 'F', 6: 'F#/Gb', 7: 'G', 8: 'G#/Ab', 9: 'A', 10: 'A#/Bb', 11: 'B'}
    AMOUNT_DISTINCT_NOTES = len(NOTE_SYSTEM)
    WHITE_NOTES = {0, 2, 4, 5, 7, 9, 11} # Made this a set for efficient lookups. (White/black notes refer to piano keys)
    NOTE_COLORS = {0: [1, 1, 1, 1], 1: [1, 1, 1, 1], 2: [1, 1, 1, 1], 3: [1, 1, 1, 1], 4: [1, 1, 1, 1], 5: [1, 1, 1, 1], 
                   6: [1, 1, 1, 1], 7: [1, 1, 1, 1], 8: [1, 1, 1, 1], 9: [1, 1, 1, 1], 10: [1, 1, 1, 1], 11: [1, 1, 1, 1]}

    @staticmethod
    def condense_note_pitch(note_number):
        """
        Returns the note pitch where a given note_number boils down to, regardless of the octave
        :param note_number: 'uncondensed' note_number (i.e. note_number which may be > 11).
        :return: the corresponding note_number < 11
        """
        note_number = CU.safe_cast(note_number, int, 0)
        return note_number % MusicTheoryCoreUtils.AMOUNT_DISTINCT_NOTES

    @staticmethod
    def is_white_note(note_number):
        """
        Check whether the pitch of a note is a white piano key, return false in the other case.
        :param note_number: uncondensed note number, i.e. the note_number may still be > 11.
        :return: bool
        """
        condensed_pitch = MusicTheoryCoreUtils.condense_note_pitch(note_number)
        return condensed_pitch in MusicTheoryCoreUtils.WHITE_NOTES

    @staticmethod
    def note_number_to_name(note_number):
        """
        Maps a MIDI-encoded note_number to its human-readable form
        :param note_number: note_number
        :return: human-readable note_name
        """
        # The reason why 1 is subtracted is only to meet the MIDI-standard. Apparently, an octave -1 is foreseen:
        octave = (note_number / MusicTheoryCoreUtils.AMOUNT_DISTINCT_NOTES) -1

        # Add the octave number at the end, and also before the slash in case of black notes.
        note_name = f"{MusicTheoryCoreUtils.NOTE_SYSTEM[MusicTheoryCoreUtils.condense_note_pitch(note_number)]}{octave}"
        note_name.replace("/", f"{octave}/")

        return note_name

    @staticmethod
    def note_name_to_number(note_name):
        """
        Maps a human-readable note to its MIDI-encoded form. Supplied note_name should be formatted as {'C4', 'C#4/Db4', 'Db4/C#4', 'C#4', 'Db4', 'C#/Db4', 'Db/C#4'}.
        In other words, last character(s) must be devoted to denoting the octave. Midi now supports 10 octaves [0..9]
        :param note_name: string describing a note
        :return: MIDI-encoded note_number
        """
        note_name = CU.safe_cast(note_name, str, "")

        # Split on '/' to tell apart possible redundant namings:
        note_names = note_name.split("/")

        # Possible redundant namings are ignored by considering the last/default one:
        note_name = note_names[len(note_names) - 1]

        note_pitch_text, octave_text = CU.split_letters_from_digits(note_name)
        octave = CU.safe_cast(octave_text, int, 0)

        note_number = '-1'

        # Determine whether the note that has to be parsed is a black note or not.
        is_black_note = any((char in set('#b')) for char in note_pitch_text)

        # Save work in the next loop over the key-value pairs (parsing the note_pitch_text) by filtering the note_System:
        subdict_whites_or_blacks = {key: value for (key, value) in MusicTheoryCoreUtils.NOTE_SYSTEM.items() if ((key in MusicTheoryCoreUtils.WHITE_NOTES) == (not is_black_note))}

        # Map the retrieved note_pitch_text to a condensed_note_number:
        for key, value in subdict_whites_or_blacks.items():

            # As soon as the note is parsed exit the for loop:
            if note_pitch_text in value:
                note_number = key
                break

        if note_number != -1:
            # The reason why octave + 1 is multiplied with the amount of distinct notes rather than just octave is to meet the MIDI-standard. Apparently, an octave -1 is foreseen:
            note_number += MusicTheoryCoreUtils.AMOUNT_DISTINCT_NOTES * (octave + 1)

        return note_number

    @staticmethod
    def note_interval_to_delta(from_note, to_note):
        """
        Calculates the amount of half tone steps that fit in the supplied interval.
        An rising interval is an interval where the note-number of the to_note > from_note, and similarly for a dropping interval. 0 means no pitch difference.
        :param from_note:
        :param to_note:
        :return: delta_pitch = the difference in pitch (expressed in halve steps)
        """

        return to_note - from_note

    @staticmethod
    def note_interval_to_key_range(from_note, to_note):
        """
        Calculates how many keys have to be drawn on ToneFlow's keyboard layout to visualize a particular note_interval
        :param from_note:
        :param to_note:
        :return: delta_white_keys = the amount of white keys needed, delta_black_keys = the amount of black keys needed
        """

        delta_white_keys = 0
        delta_black_keys = 0

        delta_pitch_halve_steps = MusicTheoryCoreUtils.note_interval_to_delta(from_note, to_note)

        # Correction in case of dropping interval:
        if (delta_pitch_halve_steps < 0):

            # Switch from_note and to_note:
            temp_note = to_note
            to_note = from_note
            from_note = temp_note

            # Invert the delta_pitch_halve_steps:
            delta_pitch_halve_steps *= -1


        for delta in range(0, delta_pitch_halve_steps + 1):

            if MusicTheoryCoreUtils.is_white_note(from_note + delta):
                delta_white_keys += 1
            else:
                delta_black_keys += 1

        return delta_white_keys, delta_black_keys

    # Unlike music, tempo in MIDI is not given as beats per minute, but rather in microseconds per beat.

    # check is midi file is type 2 (and removes if so) - this is unlikely but can happen on old sites
    @staticmethod
    def remove_type_2(midi):
        return True if midi.type == 2 else False

    # removes unnecessary meta data types
    @staticmethod
    def filter_meta_type(msg):
        accept = ["set_tempo", "time_signature", "key_signature"]
        return True if msg.type in accept else False

    @staticmethod
    def remove_duplicate_tracks(cv1):
        message_numbers = []
        duplicates = []

        for track in cv1.tracks:
            if len(track) in message_numbers:
                duplicates.append(track)
            else:
                message_numbers.append(len(track))

        for track in duplicates:
            cv1.tracks.remove(track)

    # removes tempo duplicates and only keeps the last tempo stated for a particular cumulative time
    @staticmethod
    def remove_extra_tempo(msg, msgwithtempos, current_time):
        if not msgwithtempos:  # if the list is empty
            msgwithtempos.append([msg, current_time])
        else:
            for i in range(len(msgwithtempos)):
                msgwithtempo = msgwithtempos[i]
                if msgwithtempo[1] == current_time:  # this checks duplicates
                    msgwithtempos.remove(msgwithtempo)
            msgwithtempos.append([msg, current_time])
        return msgwithtempos

    @staticmethod
    def do_shit(mid_file):  # for each track (then message) do the following
        all_messages = []
        msgwithtempos = []
        for i, track in enumerate(mid_file.tracks):
            current_time = 0
            print(f"Track {i}: {track.name}")
            for msg in track:
                current_time += msg.time
                if msg.type == "sysex data":
                    pass
                elif msg.is_meta:
                    #if filter_meta_type(msg):
                    if msg.type == "set_tempo":
                        msgwithtempos = MusicTheoryCoreUtils.remove_extra_tempo(msg, msgwithtempos, current_time)
                    else:
                        all_messages.append([msg, current_time])
                else:
                    all_messages.append([msg, current_time])
        return all_messages, msgwithtempos

    @staticmethod
    def preprocess_midi_file(midi_file):  # for each midi file do the following
        final_messages = None
        midi_file = MidiFile(midi_file)
        if not MusicTheoryCoreUtils.remove_type_2(midi_file):
            all_messages, msgwithtempos = MusicTheoryCoreUtils.do_shit(midi_file)
            final_messages = all_messages + msgwithtempos
            final_messages = sorted(final_messages, key=lambda x: x[1])
        # print(final_messages)
        return final_messages

    @staticmethod
    def preprocess_midi_files(midi_files):
        for midi_file in midi_files:
            MusicTheoryCoreUtils.preprocess_midi_file(midi_file)

