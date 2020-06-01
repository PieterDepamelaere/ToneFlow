import os
import sys
import re
import aiofiles
import pathlib as pl
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.utils import get_hex_from_color
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.utils import asynckivy
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.SongEntry import SongEntry
from src.model.CommonUtils import CommonUtils as CU

class Songs(Screen):

    app = None
    is_kv_loaded = False
    theme_primary_color = 'Amber'
    theme_accent_color = 'Gray'  # 'DeepOrange'

    def __init__(self, **kwargs):
        if (not Songs.is_kv_loaded):
            # Make sure it's only loaded once:
            Builder.load_file(str(curr_file.parents[1] / "view" / (pl.Path(Songs.__name__).with_suffix(".kv")).name))
            Songs.is_kv_loaded = True

        super(Songs, self).__init__(name=type(self).__name__, **kwargs)

        Songs.app = App.get_running_app()
        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a dict of callbacks
        self._context_menus = {"Add Song Location": lambda x: {self.show_filemanager_add_songs_location()},
                               "Clear Input": lambda x: {self.clear_search_pattern()},
                               "Sort Songs": lambda x: {self.sort_list()},
                               "Refresh": lambda x: {self.refresh_list(), toast(f"Refreshed")},
                               "Remove Songs(s)": lambda x: toast("TODO: WIP"),
                               "Help": lambda x: toast("TODO: WIP")}
        # TODO: Implement the other context menus

        # TODO: Can _list not refer directly to listproperty of the widget? self.ids.rv.data
        self._list = list() # ObservableList(None, object, list())

        self._list_additional_song_locations = []

    def get_list(self):
        return self._list

    def set_list(self, list):
        list = CU.safe_cast(list, self._list.__class__, "")
        self._list = list

    def get_context_menus(self):
        return self._context_menus

    list = property(get_list, set_list)
    context_menus = property(get_context_menus)

    def rename_song(self, song_rowview, new_name_song):
        """
        Fires async method to rename a song.
        :param song_rowview:
        :param new_name_song:
        :return:
        """
        asynckivy.start(self.async_rename_song(song_rowview, new_name_song))

    async def async_rename_song(self, song_rowview, new_name_song):
        """
        Actual process to rename a song.
        :param song_rowview:
        :param new_name_song:
        :return:
        """

        # Check the new_name_song by means of a regular expression:
        # Only allow names entirely consisting of alphanumeric characters, dashes and underscores
        song_to_rename = song_rowview.song_entry_obj

        if re.match("^[\w\d_-]+$", str(new_name_song)):
            filename_song = f"{str(new_name_song)}{song_to_rename.file_path.suffix}"
            if len(list(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['RAW_MIDI_DIR_NAME'].value).glob(filename_song))) > 0:
                toast(f"{new_name_song} already exists")

            elif song_to_rename.file_path.exists():
                old_name = str(song_to_rename.file_path.stem)
                file_path = pl.Path(song_to_rename.file_path.parents[0] / filename_song)
                pl.Path(song_to_rename.file_path).rename(file_path)
                toast(f"{old_name} renamed to {new_name_song}")
            else:
                toast(f"Song {song_to_rename.file_path.stem} not found")
        else:
            toast(f"Name cannot be empty nor contain{os.linesep}non-alphanumeric characters except for \"-_\")")
        await asynckivy.sleep(0)

    def remove_song(self, song_rowview, *args):
        """
        Fires async method to remove a song.
        :param song_rowview:
        :param args:
        :return:
        """
        asynckivy.start(self.async_remove_song(song_rowview, *args))

    async def async_remove_song(self, song_rowview, *args):
        """
        Actual process to remove a song.
        :param song_rowview:
        :param args:
        :return:
        """
        song_to_delete = song_rowview.song_entry_obj

        self._list.remove(song_to_delete)

        file_path_to_delete = song_to_delete.file_path
        if (file_path_to_delete.exists() and file_path_to_delete.is_file()):
            pl.Path(file_path_to_delete).unlink()
        toast(f"{str(song_to_delete.file_path.stem)} successfully removed")

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

        for song in self._list:
            song_name = str(song.file_path.stem)
            if (len(search_pattern) == 0 or ((len(search_pattern) > 0) and (search_pattern.lower() in song_name.lower()))):

                self.ids.rv.data.append(
                    {
                        "viewclass": "SongRowView",
                        "list_obj": self,
                        "song_entry_obj": song,
                        "callback": None
                    }
                )
        await asynckivy.sleep(0)

    def refresh_list(self):
        """
        Fires async method to refresh the internal list.
        :return:
        """
        # Clear existing list<SongEntry>:
        self._list.clear()
        asynckivy.start(self.async_refresh_list())

    async def async_refresh_list(self):
        """
        Scan the workspace-Songs folder for songs.
        :return:
        """
        # Depending on the amount of time it takes to run through the refresh, the spinner will be more/longer visible:
        for song_folder in [pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['RAW_MIDI_DIR_NAME'].value)] + self._list_additional_song_locations:
            for pattern in ["*" + extension for extension in CU.tfs.dic['MIDI_FILE_EXTENSIONS'].value]:
                for file_path in song_folder.rglob(pattern):
                    song = SongEntry(file_path=file_path, mute_play_along=True, songlevel_speedfactor=1.0)
                    self._list.append(song)
                    await asynckivy.sleep(0)

        # TODO: Make overscroll easier than it is now, in fact scrollbar should be always visible
        await self.async_filter_list()
        self.ids.refresh_layout.refresh_done()

    def show_filemanager_add_songs_location(self):
        """
        Show a dialog to ask the name of the new song.
        :return:
        """
        mode = False
        file_manager = MDFileManager(
            # ext=["mid", "midi"],
            search="all",
            exit_manager=lambda *args, **kwargs: (toast(f"Canceled"), file_manager.close()),
            select_path=lambda *args, **kwargs: (self.on_selected_path_filemanager(args, kwargs), file_manager.close()),
            previous=mode # Very special naming convention, False means listview-mode, True means Thumbnail mode
        )
        file_manager.ext = CU.tfs.dic['MIDI_FILE_EXTENSIONS'].value

        file_manager.show(str(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['RAW_MIDI_DIR_NAME'].value)))

    def on_selected_path_filemanager(self, *args, **kwargs):
        """It will be called when you click on the file name
        or the catalog selection button.
        :type path: str;
        :param path: path to the selected directory or file;
        """

        path = CU.safe_cast(args[0][0], pl.Path, None)
        if path.is_file():
            # To make sure that whole parent directory is scanned for additional song-files:
            path = path.parents[0]

        path_found = False
        i = 0

        # On each invocation of this method the default path is prepended because at some point the user might change the tf_workspace_path, and then this change is automatically refreshed.
        scanned_song_locations = [pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['RAW_MIDI_DIR_NAME'].value)] + self._list_additional_song_locations

        # Searching until first occurrence of possible duplicate:
        while not path_found and i < len(scanned_song_locations):
            if path.samefile(scanned_song_locations[i]): # path == scanned_song_locations[i]:
                path_found = True
                toast(f"{os.sep}{path.name}-folder is already searched")
            i = i+1

        if not path_found:
            # If the path is not found yet, it can be added, this whole operation was to avoid duplicates:
            self._list_additional_song_locations.append(path)
            toast(f"{path} added to search scope")

        self.refresh_list()

    def on_cancel_filemanager(self, modal_view, *args, **kwargs):
        """Called when the user reaches the root of the directory tree."""
        modal_view.dismiss()
        toast(f"Canceled")

    def show_dialog_rename_song(self, song_rowview):
        """
        Show a dialog to ask for the new name of the song.
        :param song_rowview:
        :return:
        """

        text = f"{str(song_rowview.song_entry_obj.file_path.stem)}"
        content_obj = BoxLayout(orientation='vertical', spacing="12dp", size_hint_y=None)

        mdtf1 = MDTextField()
        mdtf1.text = text
        mdtf1.hint_text = f"Name of song"
        mdtf1.helper_text = f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}"
        mdtf1.helper_text_mode = "on_focus"

        content_obj.add_widget(mdtf1)

        CU.show_input_dialog(title=f"Enter New Name for Song",
                             content_obj=content_obj,
                             size_hint=(.7, .4),
                             text_button_ok="Update",
                             text_button_cancel="Cancel",
                             ok_callback_set=lambda *args, **kwargs: {self.rename_song(song_rowview, mdtf1.text), self.refresh_list()})

    def show_dialog_remove_song(self, song_rowview):
        """
        Show a dialog to ask for confirmation of the removal.
        :param song_rowview:
        :return:
        """
        text=f"Are you sure want to remove [color={get_hex_from_color(Songs.app.theme_cls.primary_color)}][b]{str(song_rowview.song_entry_obj.file_path.stem)}[/b][/color] from the list? This action cannot be undone."

        CU.show_ok_cancel_dialog(title=f"Are You Sure?",
                                 text=text,
                                 size_hint=(.7, .4),
                                 text_button_ok="Remove",
                                 text_button_cancel="Cancel",
                                 ok_callback_set=lambda *args, **kwargs: (self.remove_song(song_rowview, args), self.refresh_list()),
                                 cancel_callback_set=lambda *args, **kwargs: (toast(f"Canceled removal of {str(song_rowview.song_entry_obj.file_path.stem)}")))

    def sort_list(self):
        """
        Will sort the internal list in alphabetic order.
        :return:
        """
        self.set_list(sorted(self._list, key=lambda song: str(song.file_path.stem)))
        self.filter_list()
        toast("Songs sorted")
