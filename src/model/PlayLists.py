import os
import sys
import pathlib as pl
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.properties import ObservableList, ListProperty
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
        self._list = list() # ObservableList(None, object, list())

    def get_list(self):
        return self._list

    def set_list(self, list):
        list = CU.safe_cast(list, self._list.__class__, "")
        self._list = list

    list = property(get_list, set_list)
    # a = ListProperty().

    def filter_list(self, search_pattern):
        self.ids.rv.data = []

        asynckivy.start(self.async_filter_list(search_pattern))

    async def async_filter_list(self, search_pattern):
        search_pattern = CU.safe_cast(search_pattern, str, "")
        print(f"search pattern is {search_pattern}")
        playlist_name = None
        self.ids.rv.data = []

        for playlist in self._list:
            playlist_name = str(playlist.stem)
            if (len(search_pattern) == 0 or ((len(search_pattern) > 0) and (search_pattern.lower() in playlist_name.lower()))):

                self.ids.rv.data.append(
                    {
                        "viewclass": "PlayListRowView",
                        "icon": "playlist-music",
                        "text": playlist_name,
                        "callback": None
                    }
                )
        await asynckivy.sleep(0)

    def refresh_list(self):

        # Clear existing list<PlayList>:
        self._list.clear()

        asynckivy.start(self.async_refresh_list())
        # for i in range(1000000):
        #     print(i)

    async def async_refresh_list(self):
        """
        Scan the workspace for playlists
        :return:
        """


        for file_name in pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).rglob("*.json"):

            # playlist = await Playlist()
            # await self.append_item to list()
            # TODO: Remove all the thread sleeps and as much print out, this makes thins slower. + mechanism to derive exceptions to error popup or so
            # Depending on the amount of time it takes to run through the refresh, the spinner will be more/longer visible:
            await asynckivy.sleep(0)
            print(f">> Refresh taking place of {file_name}")
            self._list.append(file_name)

        await self.async_filter_list(self.ids.search_field.text)
        self.ids.refresh_layout.refresh_done()

class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass
