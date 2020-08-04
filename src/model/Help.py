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

from kivymd.utils import asynckivy
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.SongEntry import SongEntry
from src.model.CommonUtils import CommonUtils as CU

class Help(Screen):

    app = None
    is_kv_loaded = False
    theme_primary_color = 'Pink'
    theme_accent_color = 'DeepPurple'

    def __init__(self, **kwargs):
        if (not Help.is_kv_loaded):
            # Make sure it's only loaded once:
            Builder.load_file(str(curr_file.parents[1] / "view" / (pl.Path(Help.__name__).with_suffix(".kv")).name))
            Help.is_kv_loaded = True

        super(Help, self).__init__(name=type(self).__name__, **kwargs)

        Help.app = App.get_running_app()
        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a dict of callbacks
        self._context_menus = {"Add Help Location": lambda *args, **kwargs: {self.show_filemanager_add_help_location()},
                               "Clear Input": lambda *args, **kwargs: {self.clear_search_pattern()},
                               "Sort Help": lambda *args, **kwargs: {self.sort_list()},
                               "Refresh": lambda *args, **kwargs: {self.refresh_list(), toast(f"Refreshed")},
                               "Remove Help(s)": lambda *args, **kwargs: toast("TODO: WIP"),
                               "Help": lambda *args, **kwargs: toast("TODO: WIP")}
        # TODO: Implement the other context menus

        # TODO: Can _list not refer directly to listproperty of the widget? self.ids.rv.data
        self._list = list() # ObservableList(None, object, list())

        self._list_additional_help_locations = []

    def get_list(self):
        return self._list

    def set_list(self, list):
        list = CU.safe_cast(list, self._list.__class__, "")
        self._list = list

    def get_context_menus(self):
        return self._context_menus

    list = property(get_list, set_list)
    context_menus = property(get_context_menus)

    def rename_help(self, help_rowview, new_name_help):
        """
        Fires async method to rename a help.
        :param help_rowview:
        :param new_name_help:
        :return:
        """
        asynckivy.start(self.async_rename_help(help_rowview, new_name_help))

    async def async_rename_help(self, help_rowview, new_name_help):
        """
        Actual process to rename a help.
        :param help_rowview:
        :param new_name_help:
        :return:
        """
        # Omit the provided explanation-text in case it was not omitted:
        new_name_help = str(CU.with_consistent_linesep(new_name_help)).replace(f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}{os.linesep}", "")

        # Check the new_name_help by means of a regular expression:
        # Only allow names entirely consisting of alphanumeric characters, dashes and underscores
        help_to_rename = help_rowview.help_entry_obj

        if re.match("^[\w\d_-]+$", str(new_name_help)):
            filename_help = f"{str(new_name_help)}.{help_to_rename.file_path.suffix}"
            if len(list(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['RAW_MIDI_DIR_NAME'].value).glob(filename_help))) > 0:
                toast(f"{new_name_help} already exists")

            elif help_to_rename.file_path.exists():
                old_name = str(help_to_rename.file_path.stem)
                file_path = pl.Path(help_to_rename.file_path.parents[0] / filename_help)
                pl.Path(help_to_rename.file_path).rename(file_path)
                toast(f"{old_name} renamed to {new_name_help}")
            else:
                toast(f"Help {help_to_rename.file_path.stem} not found")
        else:
            toast(f"Name cannot be empty nor contain{os.linesep}non-alphanumeric characters except for \"-_\")")
        await asynckivy.sleep(0)

    def remove_help(self, help_rowview, *args):
        """
        Fires async method to remove a help.
        :param help_rowview:
        :param args:
        :return:
        """
        asynckivy.start(self.async_remove_help(help_rowview, *args))

    async def async_remove_help(self, help_rowview, *args):
        """
        Actual process to remove a help.
        :param help_rowview:
        :param args:
        :return:
        """
        decision = args[0]
        help_to_delete = help_rowview.help_entry_obj

        if (str(decision).lower() == "remove"):
            self._list.remove(help_to_delete)

            file_path_to_delete = help_to_delete.file_path
            if (file_path_to_delete.exists() and file_path_to_delete.is_file()):
                pl.Path(file_path_to_delete).unlink()
            toast(f"{str(help_to_delete.file_path.stem)} successfully removed")
        else:
            toast(f"Canceled removal of {str(help_to_delete.file_path.stem)}")
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

        for help in self._list:
            help_name = str(help.file_path.stem)
            if (len(search_pattern) == 0 or ((len(search_pattern) > 0) and (search_pattern.lower() in help_name.lower()))):

                self.ids.rv.data.append(
                    {
                        "viewclass": "HelpRowView",
                        "list_obj": self,
                        "help_entry_obj": help,
                        "callback": None
                    }
                )
        await asynckivy.sleep(0)

    def refresh_list(self):
        """
        Fires async method to refresh the internal list.
        :return:
        """
        # Clear existing list<HelpEntry>:
        self._list.clear()
        asynckivy.start(self.async_refresh_list())

    async def async_refresh_list(self):
        """
        Scan the workspace-Help folder for help.
        :return:
        """
        pass
        # # Depending on the amount of time it takes to run through the refresh, the spinner will be more/longer visible:
        # for help_folder in [pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['RAW_MIDI_DIR_NAME'].value)] + self._list_additional_help_locations:
        #     for pattern in ["*.mid", "*.midi"]:
        #         for file_path in help_folder.rglob(pattern):
        #             help = SongEntry(file_path=file_path, mute_play_along=True, helplevel_speedfactor=1.0)
        #             self._list.append(help)
        #             await asynckivy.sleep(0)
        #
        # # TODO: Make overscroll easier than it is now, in fact scrollbar should be always visible
        # await self.async_filter_list()
        # self.ids.refresh_layout.refresh_done()

    def show_filemanager_add_help_location(self):
        """
        Show a dialog to ask the name of the new help.
        :return:
        """
        mode = False
        modal_view = ModalView(size_hint=(1, 1), auto_dismiss=False)
        file_manager = MDFileManager(
            exit_manager=lambda *args: self.on_cancel_filemanager(modal_view, *args),
            select_path=lambda *args: self.on_selected_path_filemanager(modal_view, *args),
            previous=mode # Very special naming convention, False means listview-mode, True means Thumbnail mode
        )
        modal_view.add_widget(file_manager)
        file_manager.show(str(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['RAW_MIDI_DIR_NAME'].value)))
        modal_view.open()

    def on_selected_path_filemanager(self, modal_view, *args):
        """It will be called when you click on the file name
        or the catalog selection button.
        :type path: str;
        :param path: path to the selected directory or file;
        """
        path = CU.safe_cast(args[0], pl.Path, None)
        if path.is_file():
            # To make sure that whole parent directory is scanned for additional help-files:
            path = path.parents[0]

        path_found = False
        i = 0

        # On each invocation of this method the default path is prepended because at some point the user might change the tf_workspace_path, and then this change is automatically refreshed.
        scanned_help_locations = [pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['RAW_MIDI_DIR_NAME'].value)] + self._list_additional_help_locations

        # Searching until first occurrence of possible duplicate:
        while not path_found and i < len(scanned_help_locations):
            if path.samefile(scanned_help_locations[i]): # path == scanned_help_locations[i]:
                path_found = True
                toast(f"{os.sep}{path.name}-folder is already searched")
            i = i+1

        if not path_found:
            # If the path is not found yet, it can be added, this whole operation was to avoid duplicates:
            self._list_additional_help_locations.append(path)
            toast(f"{path} added to search scope")

        self.refresh_list()
        modal_view.dismiss()

    def on_cancel_filemanager(self, modal_view, *args):
        """Called when the user reaches the root of the directory tree."""
        modal_view.dismiss()
        toast(f"Canceled")

    def show_dialog_rename_help(self, help_rowview):
        """
        Show a dialog to ask for the new name of the help.
        :param help_rowview:
        :return:
        """
        pass
        # dialog_text = f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}{os.linesep}" \
        #     f"{str(help_rowview.help_entry_obj.file_path.stem)}"
        #
        # CU.show_input_dialog(title=f"Enter New Name for Help",
        #                      hint_text=dialog_text,
        #                      text=dialog_text,
        #                      size_hint=(.7, .4),
        #                      text_button_ok="Update",
        #                      callback=lambda text_button, instance, *args: {self.rename_help(help_rowview, instance.text_field.text), self.refresh_list()})

    def show_dialog_remove_help(self, help_rowview):
        """
        Show a dialog to ask for confirmation of the removal.
        :param help_rowview:
        :return:
        """
        pass
        # dialog_text=f"Are you sure want to remove [color={get_hex_from_color(Help.app.theme_cls.primary_color)}][b]{str(help_rowview.help_entry_obj.file_path.stem)}[/b][/color] from the list? This action cannot be undone."
        #
        # CU.show_ok_cancel_dialog(title=f"Are You Sure?",
        #                          text=dialog_text,
        #                          size_hint=(.7, .4),
        #                          text_button_ok="Remove",
        #                          text_button_cancel="Cancel",
        #                          callback=lambda *args: {self.remove_help(help_rowview, *args), self.refresh_list()})

    def sort_list(self):
        """
        Will sort the internal list in alphabetic order.
        :return:
        """
        self.set_list(sorted(self._list, key=lambda help: str(help.file_path.stem)))
        self.filter_list()
        toast("Help sorted")
