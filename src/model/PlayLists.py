import os
import sys
import pathlib as pl
from kivy.uix.screenmanager import Screen

curr_file = pl.Path(os.path.realpath(__file__))

from src.model import CommonUtils as CU


class PlayLists(Screen):

    def __init__(self, **kwargs):
        super().__init__(name=type(self).__name__, **kwargs)
        self._list = list()
        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a list of callbacks
        self._context_menus = list()

    def get_list(self):
        return self._list

    def set_list(self, list):
        list = CU.safe_cast(list, self._list.__class__, "")
        self._list = list

    list = property(get_list, set_list)

    async def scan_workspace_for_playlists(self):
        pass

    def refresh_playlists(self):
        pass