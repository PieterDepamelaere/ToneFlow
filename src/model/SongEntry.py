import os
import sys
import pathlib as pl
curr_file = pl.Path(os.path.realpath(__file__))
curr_file_dir = curr_file.parents[0]

sys.path.insert(0, str(curr_file.parents[0]))
sys.path.insert(0, str(curr_file.parents[1]))
sys.path.insert(0, str(curr_file.parents[2]))

from src.model.LineupEntry import LineupEntry
from src.model.CommonUtils import CommonUtils as CU

class SongEntry(LineupEntry):

    def __init__(self, file_path=None, mute_play_along=True, songlevel_speedfactor=1.0, **kwargs):
        super().__init__(entry_type=SongEntry, file_path=file_path, **kwargs)
        self._mute_play_along = mute_play_along
        self._songlevel_speedfactor = songlevel_speedfactor

    def test(self):
        print("test")

    def get_mute_play_along(self):
        """
        Get boolean _mute_play_along, to toggle whether synthetic MIDI file sound will be played out loud in concertmode.
        :return:
        """
        return self._mute_play_along

    def set_mute_play_along(self, mute_play_along):
        """
        Set boolean _mute_play_along, to toggle whether synthetic MIDI file sound will be played out loud in concertmode.
        :param mute_play_along: bool
        :return:
        """
        mute_play_along = CU.safe_cast(mute_play_along, bool, True)
        self._mute_play_along = mute_play_along

    def get_songlevel_speedfactor(self):
        """
        Get float _songlevel_speedfactor, to override the default overall_speed_factor inside the TF_Settigns at song level here.
        :return:
        """
        return self._songlevel_speedfactor

    def set_songlevel_speedfactor(self, songlevel_speedfactor):
        """
        Set float _songlevel_speedfactor, to override the default overall_speed_factor inside the TF_Settigns at song level here.
        :param songlevel_speedfactor: bool
        :return:
        """
        songlevel_speedfactor = CU.safe_cast(songlevel_speedfactor, float, 1.0)
        self._songlevel_speedfactor = songlevel_speedfactor

    mute_play_along = property(get_mute_play_along, set_mute_play_along)
    songlevel_speedfactor = property(get_songlevel_speedfactor, set_songlevel_speedfactor)