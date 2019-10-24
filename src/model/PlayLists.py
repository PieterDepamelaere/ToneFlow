import os
import sys
import pathlib as pl
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.properties import ObservableList
from kivymd.utils import asynckivy
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import ILeftBodyTouch

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.CommonUtils import CommonUtils as CU


class PlayLists(Screen):

    def __init__(self, **kwargs):
        super().__init__(name=type(self).__name__, **kwargs)
        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a list of callbacks
        self._context_menus = list()

        # TODO: Can _list not refer directly to listproperty of the widget? self.ids.rv.data
        self._list = list()


    def get_list(self):
        return self._list

    def set_list(self, list):
        list = CU.safe_cast(list, self._list.__class__, "")
        self._list = list

    list = property(get_list, set_list)

    async def filter_list(self, search_pattern):
        pass

    def refresh_list(self):
        # It is an ObservableList
        # a: RecycleView  = self.ids.rv
        # self.ids.rv.refresh_from_data()

        # self.ids.rv.
        # self.ids.rv.data.clear()

        asynckivy.start(self.async_refresh_list())
        # for i in range(1000000):
        #     print(i)

    async def async_refresh_list(self):
        """
        Scan the workspace for playlists
        :return:
        """
        # Clear existing Playlists:
        self.set_list(list())

        # async self.set_list([file_name for file_name in pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).rglob("*.json")])
        # yield pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).rglob("*.json")

        for file_name in pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).rglob("*.json"):

            # playlist = await Playlist()
            # await self.append_item to list()
            await asynckivy.sleep(0.75)

            self.ids.rv.data.append(
            {
                "viewclass": "MDIconItemForMdIconsList",
                "icon": "playlist-music",
                "text": str(file_name.stem),
                "callback": None
            }
        )

        self.ids.refresh_layout.refresh_done()

class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass
