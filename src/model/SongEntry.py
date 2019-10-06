import os
import sys
import pathlib as pl
curr_file = pl.Path(os.path.realpath(__file__))
curr_file_dir = curr_file.parents[0]

sys.path.insert(0, str(curr_file.parents[0]))
sys.path.insert(0, str(curr_file.parents[1]))
sys.path.insert(0, str(curr_file.parents[2]))

from src.model import LineupEntry as LE


class SongEntry(LE.LineupEntry):

    def __init__(self, file_path=None, mute_play_along=True, songlevel_speedfactor=1.0, **kwargs):
        super().__init__(self, entry_type=SongEntry, file_path=file_path, **kwargs)
        self._mute_play_along = mute_play_along
        self._songlevel_speedfactor = songlevel_speedfactor

    def test(self):
        print("test")

    def set_mute_play_along(self, mute_play_along):
        """
        Set boolean _mute_play_along, to toggle whether syntetic MIDI file sound will be played out loud in concertmode.
        :param mute_play_along: bool
        :return:
        """
        self._mute_play_along = mute_play_along

    def set_songlevel_speedfactor(self, songlevel_speedfactor):
        """
        Set float _songlevel_speedfactor, to override the default overall_speed_factor inside the TF_Settigns at song level here.
        :param songlevel_speedfactor: bool
        :return:
        """
        self._songlevel_speedfactor = songlevel_speedfactor