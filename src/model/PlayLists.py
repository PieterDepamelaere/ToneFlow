import os
import sys
import re
import aiofiles
import pathlib as pl
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.utils import get_hex_from_color
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty

from kivymd.utils import asynckivy
from kivymd.toast import toast

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.PlayList import PlayList
from src.model.CommonUtils import CommonUtils as CU

class PlayLists(Screen):

    app = None

    def __init__(self, **kwargs):
        super(PlayLists, self).__init__(name=type(self).__name__, **kwargs)
        PlayLists.app = App.get_running_app()
        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a dict of callbacks
        self._context_menus = {"Add Playlist": lambda x: {self.show_dialog_add_playlist()},
                               "Clear Input": lambda x: {self.clear_search_pattern()},
                               "Sort Playlists": lambda x: {self.sort_list()},
                               "Refresh": lambda x: {self.refresh_list(), toast(f"Refreshed")},
                               "Remove Playlist(s)": lambda x: toast("TODO: WIP"),
                               "Help": lambda x: toast("TODO: WIP")}
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

    def add_playlist(self, name_new_playlist):
        """
        Fires async method to add a playlist.
        :param name_new_playlist:
        :return:
        """
        asynckivy.start(self.async_add_playlist(name_new_playlist))

    async def async_add_playlist(self, name_new_playlist):
        """
        Actual process to add a playlist.
        :param name_new_playlist:
        :return:
        """
        # Omit the provided explanation-text in case it was not omitted:
        name_new_playlist = str(name_new_playlist).replace(f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}", "")

        # Check the name_new_playlist by means of a regular expression:
        # Only allow names entirely consisting of alphanumeric characters, dashes and underscores
        if re.match("^[\w\d_-]+$", str(name_new_playlist)):
            filename_playlist = f"{str(name_new_playlist)}.json"
            if len(list(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).glob(filename_playlist))) > 0:
                toast(f"{name_new_playlist} already exists")
            else:
                file_path = pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value / filename_playlist)
                with open(str(file_path), "w") as json_file:
                    json_file.write("")

                # TODO: async option doesn't work in combination with asynckivy.start() error is TypeError: '_asyncio.Future' object is not callable
                # async with open(str(file_path), 'w') as json_file:
                #     await json_file.write("")

                toast(f"{name_new_playlist} added")
        else:
            toast(f"Name cannot be empty nor contain{os.linesep}non-alphanumeric characters except for \"-_\")")
        await asynckivy.sleep(0)

    def rename_playlist(self, playlist_rowview, new_name_playlist):
        """
        Fires async method to rename a playlist.
        :param playlist_rowview:
        :param new_name_playlist:
        :return:
        """
        asynckivy.start(self.async_rename_playlist(playlist_rowview, new_name_playlist))

    async def async_rename_playlist(self, playlist_rowview, new_name_playlist):
        """
        Actual process to rename a playlist.
        :param playlist_rowview:
        :param new_name_playlist:
        :return:
        """
        # Omit the provided explanation-text in case it was not omitted:
        new_name_playlist = str(new_name_playlist).replace(f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}", "")

        # Check the new_name_playlist by means of a regular expression:
        # Only allow names entirely consisting of alphanumeric characters, dashes and underscores
        playlist_to_rename = playlist_rowview.playlist_obj

        if re.match("^[\w\d_-]+$", str(new_name_playlist)):
            filename_playlist = f"{str(new_name_playlist)}.json"
            if len(list(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).glob(filename_playlist))) > 0:
                toast(f"{new_name_playlist} already exists")

            elif playlist_to_rename.file_path.exists():
                old_name = str(playlist_to_rename.file_path.stem)
                file_path = pl.Path(playlist_to_rename.file_path.parents[0] / filename_playlist)
                pl.Path(playlist_to_rename.file_path).rename(file_path)
                toast(f"{old_name} renamed to {new_name_playlist}")
            else:
                toast(f"Playlist {playlist_to_rename.file_path.stem} not found")
        else:
            toast(f"Name cannot be empty nor contain{os.linesep}non-alphanumeric characters except for \"-_\")")
        await asynckivy.sleep(0)

    def remove_playlist(self, playlist_rowview, *args):
        """
        Fires async method to remove a playlist.
        :param playlist_rowview:
        :param args:
        :return:
        """
        asynckivy.start(self.async_remove_playlist(playlist_rowview, *args))

    async def async_remove_playlist(self, playlist_rowview, *args):
        """
        Actual process to remove a playlist.
        :param playlist_rowview:
        :param args:
        :return:
        """
        decision = args[0]
        playlist_to_delete = playlist_rowview.playlist_obj

        if (str(decision).lower() == "remove"):
            self._list.remove(playlist_to_delete)

            file_path_to_delete = playlist_to_delete.file_path
            if (file_path_to_delete.exists() and file_path_to_delete.is_file()):
                pl.Path(file_path_to_delete).unlink()
            toast(f"{str(playlist_to_delete.file_path.stem)} successfully removed")
        else:
            toast(f"Canceled removal of {str(playlist_to_delete.file_path.stem)}")
        await asynckivy.sleep(0)

    def clear_search_pattern(self):
        """
        Clear the search pattern in the filter.
        :return:
        """
        self.ids.search_field.text=""
        toast("Input cleared")
        # After the filter text is changed, the filter_list() method is automatically triggered.

    def filter_list(self):
        """
        Fires async method to filter the visual list.
        :return:
        """
        asynckivy.start(self.async_filter_list())

    async def async_filter_list(self):
        """
        Filter the visual list on the provided search pattern.
        :return:
        """
        search_pattern = CU.safe_cast(self.ids.search_field.text, str, "")
        # print(f"search pattern is {search_pattern}")
        self.ids.rv.data = []

        for playlist in self._list:
            playlist_name = str(playlist.file_path.stem)
            if (len(search_pattern) == 0 or ((len(search_pattern) > 0) and (search_pattern.lower() in playlist_name.lower()))):

                self.ids.rv.data.append(
                    {
                        "viewclass": "PlayListRowView",
                        "list_obj": self,
                        "playlist_obj": playlist,
                        "callback": None
                    }
                )
        await asynckivy.sleep(0)

    def refresh_list(self):
        """
        Fires async method to refresh the internal list.
        :return:
        """
        # Clear existing list<PlayList>:
        self._list.clear()

        asynckivy.start(self.async_refresh_list())

    async def async_refresh_list(self):
        """
        Scan the workspace-Playlists folder for playlists.
        :return:
        """
        # Depending on the amount of time it takes to run through the refresh, the spinner will be more/longer visible:
        for file_path in pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).rglob("*.json"):

            playlist = PlayList(file_path)

            self._list.append(playlist)
            await asynckivy.sleep(0)

        # TODO: Make overscroll easier than it is now, in fact scrollbar should be always visible
        await self.async_filter_list()
        self.ids.refresh_layout.refresh_done()

    def show_dialog_add_playlist(self):
        """
        Show a dialog to ask the name of the new playlist.
        :return:
        """
        creation_time = datetime.now()

        dialog_text = f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}" \
            f"Concert_{creation_time.year}{creation_time.month}{creation_time.day}-{creation_time.hour}{creation_time.minute}{creation_time.second}"

        CU.show_input_dialog(title=f"Enter Name of New Playlist",
                             hint_text=dialog_text,
                             text=dialog_text,
                             size_hint=(.7, .4),
                             text_button_ok="Add",
                             callback=lambda text_button, instance, *args: {self.add_playlist(instance.text_field.text), self.refresh_list()})

    def show_dialog_rename_playlist(self, playlist_rowview):
        """
        Show a dialog to ask for the new name of the playlist.
        :param playlist_rowview:
        :return:
        """
        dialog_text = f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}" \
            f"{str(playlist_rowview.playlist_obj.file_path.stem)}"

        CU.show_input_dialog(title=f"Enter New Name for Playlist",
                             hint_text=dialog_text,
                             text=dialog_text,
                             size_hint=(.7, .4),
                             text_button_ok="Update",
                             callback=lambda text_button, instance, *args: {self.rename_playlist(playlist_rowview, instance.text_field.text), self.refresh_list()})

    def show_dialog_remove_playlist(self, playlist_rowview):
        """
        Show a dialog to ask for confirmation of the removal.
        :param playlist_rowview:
        :return:
        """
        dialog_text=f"Are you sure want to remove [color={get_hex_from_color(PlayLists.app.theme_cls.primary_color)}][b]{str(playlist_rowview.playlist_obj.file_path.stem)}[/b][/color] from the list? This action cannot be undone."

        CU.show_ok_cancel_dialog(title=f"Are You Sure?",
                                 text=dialog_text,
                                 size_hint=(.7, .4),
                                 text_button_ok="Remove",
                                 text_button_cancel="Cancel",
                                 callback=lambda *args: {self.remove_playlist(playlist_rowview, *args), self.refresh_list()})

    def sort_list(self):
        """
        Will sort the internal list in alphabetic order.
        :return:
        """
        self.set_list(sorted(self._list, key=lambda playlist: str(playlist.file_path.stem)))
        self.filter_list()
        toast("Playlists sorted")
