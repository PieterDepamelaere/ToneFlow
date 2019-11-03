import os
import sys
import pathlib as pl
from kivy.uix.screenmanager import Screen
from kivymd.utils import asynckivy
from kivymd.toast import toast

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.PlayList import PlayList
from src.model.CommonUtils import CommonUtils as CU


class PlayLists(Screen):

    def __init__(self, **kwargs):
        super(PlayLists, self).__init__(name=type(self).__name__, **kwargs)
        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a dict of callbacks
        self._context_menus = {"Clear Input": lambda x: self.clear_search_pattern(),
                               "Sort Playlists": lambda x: self.sort_list(),
                               "Refresh": lambda x: self.refresh_list(),
                               "Rename Playlist(s)": lambda x: toast("TODO: WIP"),
                               "Help": lambda y: toast("TODO: WIP")}
        # TODO: Implement the other context menus

        # TODO: Can _list not refer directly to listproperty of the widget? self.ids.rv.data
        self._list = list() # ObservableList(None, object, list())

    def get_list(self):
        return self._list

    def set_list(self, list):
        list = CU.safe_cast(list, self._list.__class__, "")
        self._list = list

    def get_context_menus(self):
        return self._context_menus

    list = property(get_list, set_list)
    context_menus = property(get_context_menus)

    def clear_search_pattern(self):
        self.ids.search_field.text=""
        # After the filter text is changed, the filter_list() method is automatically triggered.

    def filter_list(self):
        asynckivy.start(self.async_filter_list())

    async def async_filter_list(self):
        search_pattern = CU.safe_cast(self.ids.search_field.text, str, "")
        # print(f"search pattern is {search_pattern}")
        self.ids.rv.data = []

        for playlist in self._list:
            playlist_name = str(playlist.file_path.stem)
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

    async def async_refresh_list(self):
        """
        Scan the workspace for playlists
        :return:
        """
        for file_path in pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).rglob("*.json"):

            playlist = PlayList(file_path)

            # TODO: mechanism to derive exceptions to error popup or so
            # Depending on the amount of time it takes to run through the refresh, the spinner will be more/longer visible:


            self._list.append(playlist)
            await asynckivy.sleep(0)

        # TODO: Make overscroll easier than it is now, in fact scrollbar should be always visible
        await self.async_filter_list()
        self.ids.refresh_layout.refresh_done()

    def sort_list(self):
        self.set_list(sorted(self._list, key=lambda playlist: str(playlist.file_path)))
        self.filter_list()