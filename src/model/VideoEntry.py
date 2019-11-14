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


class VideoEntry(LineupEntry):

    def __init__(self, file_path=None, show_upside_down=False, mute_audio=False, loop_repeat=False, **kwargs):
        super().__init__(self, entry_type=VideoEntry, file_path=file_path, **kwargs)
        self._show_upside_down = show_upside_down
        self._mute_audio = mute_audio
        self._loop_repeat = loop_repeat

    def test(self):
        print("test")

    def get_show_upside_down(self):
        """
        Get boolean _show_upside_down, that will make the <LineupEntry> to be shown upside down. (This comes in handy when projecting vertically on the floor, so the image or clip to announce the next music-piece faces the audience)
        :param show_upside_down: bool
        :return:
        """
        return self._show_upside_down

    def set_show_upside_down(self, show_upside_down):
        """
        Set boolean _show_upside_down, that will make the <LineupEntry> to be shown upside down. (This comes in handy when projecting vertically on the floor, so the image or clip to announce the next music-piece faces the audience)
        :param show_upside_down: bool
        :return:
        """
        show_upside_down = CU.safe_cast(show_upside_down, bool, False)
        self._show_upside_down = show_upside_down

    def get_mute_audio(self):
        """
        To mute the sound of a movie clip during playback.
        :return:
        """
        return self._mute_audio

    def set_mute_audio(self, mute_audio):
        """
        To mute the sound of a movie clip during playback.
        :param mute_audio:
        :return:
        """
        mute_audio = CU.safe_cast(mute_audio, bool, False)
        self._mute_audio = mute_audio

    def get_repeat(self):
        """
        Loop repeat option comes in very handy when you e.g. turn a sponsor-slideshow into a movie-file which should repeat at some points in the concert.
        :return:
        """
        return self._loop_repeat

    def set_repeat(self, loop_repeat):
        """
        Loop repeat option comes in very handy when you e.g. turn a sponsor-slideshow into a movie-file which should repeat at some points in the concert.
        :param loop_repeat:
        :return:
        """
        loop_repeat = CU.safe_cast(loop_repeat, bool, False)
        self._loop_repeat = loop_repeat

    show_upside_down = property(get_show_upside_down, set_show_upside_down)
    mute_audio = property(get_mute_audio, set_mute_audio)
    loop_repeat = property(get_repeat, set_repeat)


