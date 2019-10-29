import os
import sys
import pathlib as pl
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.properties import ObservableList, ListProperty
from kivymd.utils import asynckivy
from kivymd.toast import toast

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.CommonUtils import CommonUtils as CU

class PlayList(Screen):
    def __init__(self, file_path, **kwargs):
        super(PlayList, self).__init__(name=type(self).__name__, **kwargs)

        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a dict of callbacks
        self._context_menus = {"Clear Input": lambda x: self.clear_search_pattern(),
                               "Refresh": lambda x: self.refresh_list(),
                               "Help": lambda y: toast("TODO: WIP")}
        # TODO: Implement the other context menus

        self.file_path = CU.safe_cast(file_path, pl.Path, None)
        # TODO: Can _list not refer directly to listproperty of the widget? self.ids.rv.data
        self._list = list()  # ObservableList(None, object, list())

    def parse_from_json(self):
        pass

    def save_to_json(self):
        pass

    # TODO: In order to get sorted in the playlists overview a comparator method should be overridden somehow

