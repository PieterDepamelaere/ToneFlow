import os
import sys
import pathlib as pl
curr_file = pl.Path(os.path.realpath(__file__))
curr_file_dir = curr_file.parents[0]

sys.path.insert(0, str(curr_file.parents[0]))
sys.path.insert(0, str(curr_file.parents[1]))
sys.path.insert(0, str(curr_file.parents[2]))

from src.model import LineupEntry as LE


class ImageEntry(LE.LineupEntry):

    def __init__(self, file_path=None, show_upside_down=False, **kwargs):
        super().__init__(self, entry_type=ImageEntry, file_path=file_path, **kwargs)
        self._show_upside_down = show_upside_down

    def test(self):
        print("test")

    def set_show_upside_down(self, show_upside_down):
        """
        Set boolean _show_upside_down, that will make the <LineupEntry> to be shown upside down. (This comes in handy when projecting vertically on the floor, so the image or clip to announce the next music-piece faces the audience)
        :param show_upside_down: bool
        :return:
        """
        self._show_upside_down = show_upside_down