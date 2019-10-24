import os
import sys
import pathlib as pl
from kivy.uix.screenmanager import Screen

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.CommonUtils import CommonUtils as CU


class Songs(Screen):

    def __init__(self, **kwargs):
        super().__init__(name=type(self).__name__, **kwargs)
        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a list of callbacks
        self._context_menus = list()

        self._list = list()

    def get_list(self):
        return self._list

    def set_list(self, list):
        list = CU.safe_cast(list, self._list.__class__, "")
        self._list = list

    list = property(get_list, set_list)

    async def scan_workspace_for_songs(self):
        pass

    def refresh_songs(self):
        pass