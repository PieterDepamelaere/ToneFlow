import os
import sys
import re
import aiofiles
import pathlib as pl
from datetime import datetime

from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.utils import get_hex_from_color
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.properties import ObservableList, ListProperty, StringProperty
from kivymd.uix.useranimationcard import MDUserAnimationCard
from kivy.uix.modalview import ModalView
from kivymd.uix.label import MDLabel


from kivymd.utils import asynckivy
from kivymd.toast import toast

curr_file = pl.Path(os.path.realpath(__file__))

from src.model.CommonUtils import CommonUtils as CU


class PlayListProvider:
    def __init__(self, file_path, **kwargs):

        self._file_path = CU.safe_cast(file_path, pl.Path, None)

        # I chose to store the modal view locally when created, so it does not need to be created over and over again:
        self._modal_view = None

    def get_file_path(self):
        return self._file_path

    def set_file_path(self, file_path):
        file_path = CU.safe_cast(file_path, pl.Path, None)

        if self._file_path != file_path:
            self._file_path = file_path
            # Reset modal view when the file path changed, just to be sure it's recreated when needed next time:
            self._modal_view = None

    def get_modal_view(self):
        if self._modal_view is None:
            # Create modal view only if asked for (to save computational power):
            self._modal_view = PlayList(self._file_path)

        return self._modal_view

    file_path = property(get_file_path, set_file_path)
    modal_view = property(get_modal_view)


class PlayList(ModalView):
    app = None
    is_kv_loaded = False
    theme_primary_color = 'Indigo'
    theme_accent_color = 'Gray'

    add_options = {
        "music-note-plus": "Add song",
        "image-plus": "Add image",
        "video-plus": "Add movie"
    }

    def __init__(self, file_path, **kwargs):
        if (not PlayList.is_kv_loaded):
            # Make sure it's only loaded once:
            Builder.load_file(str(curr_file.parents[1] / "view" / (pl.Path(PlayList.__name__).with_suffix(".kv")).name))
            PlayList.app = App.get_running_app()
            PlayList.is_kv_loaded = True
        super(PlayList, self).__init__(**kwargs)

        # Initializing properties of ModalView:
        self.size_hint = (1, 1)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.background_color = (1, 1, 1, 1)
        # When auto_dismiss==True, then you can escape the modal view with [ESC]
        self.auto_dismiss = True
        # can be argument in ModalView Constructor border = (16, 16, 16, 16)

        # Binding events that come with the ModalView ('on_pre_open', 'on_open', 'on_pre_dismiss', 'on_dismiss') to
        # their respective static methods:
        self.bind(on_pre_open=PlayList.on_pre_open_callback)
        self.bind(on_open=PlayList.on_open_callback)
        self.bind(on_pre_dismiss=PlayList.on_pre_dismiss_callback)
        self.bind(on_dismiss=PlayList.on_dismiss_callback)

        # These are the right action item menu's possible at the '3-vertical dots' menu. This can become a dict of callbacks
        self._context_menus = {"Clear Input": lambda x: self.clear_search_pattern(),
                               "Refresh": lambda x: self.refresh_list(),
                               "Help": lambda x: toast("TODO: WIP"),
                               "Save Playlist": lambda x: toast("TODO: WIP")}
        # TODO: Implement the other context menus

        # Initializing custom properties:
        self._block_close = False
        self._file_path = file_path

        self._former_primary_palette, self._former_accent_palette = PlayList.app.theme_cls.primary_palette, PlayList.app.theme_cls.accent_palette
        self._former_context_menus = PlayList.app.context_menus

        # TODO: Can _list not refer directly to listproperty of the widget? self.ids.rv.data
        self._list = list()  # ObservableList(None, object, list())


    def get_list(self):
        return self._list

    def set_list(self, list):
        list = CU.safe_cast(list, self._list.__class__, "")
        self._list = list

    def get_context_menus(self):
        return self._context_menus

    def get_file_path(self):
        return self._file_path

    def get_block_close(self):
        return self._block_close

    def set_block_close(self, block_close):
        self._block_close = block_close

    list = property(get_list, set_list)
    context_menus = property(get_context_menus)
    file_path = property(get_file_path)
    block_close = property(get_block_close, set_block_close)

    def load_from_json(self):
        # TODO
        pass

    def save_to_json(self):
        # TODO
        pass

    def add_lineup_entry(self, name_new_lineup_entry):
        """
        Fires async method to add a lineup_entry.
        :param name_new_lineup_entry:
        :return:
        """
        asynckivy.start(self.async_add_lineup_entry(name_new_lineup_entry))

    async def async_add_lineup_entry(self, name_new_lineup_entry):
        """
        Actual process to add a lineup_entry.
        :param name_new_lineup_entry:
        :return:
        """
        # Omit the provided explanation-text in case it was not omitted:
        name_new_lineup_entry = str(CU.with_consistent_linesep(name_new_lineup_entry)).replace(f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}{os.linesep}", "")

        # Check the name_new_lineup_entry by means of a regular expression:
        # Only allow names entirely consisting of alphanumeric characters, dashes and underscores
        if re.match("^[\w\d_-]+$", str(name_new_lineup_entry)):
            filename_lineup_entry = f"{str(name_new_lineup_entry)}.json"
            if len(list(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).glob(filename_lineup_entry))) > 0:
                toast(f"{name_new_lineup_entry} already exists")
            else:
                file_path = pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value / filename_lineup_entry)
                with open(str(file_path), "w") as json_file:
                    json_file.write("")

                # TODO: async option doesn't work in combination with asynckivy.start() error is TypeError: '_asyncio.Future' object is not callable
                # async with open(str(file_path), 'w') as json_file:
                #     await json_file.write("")

                toast(f"{name_new_lineup_entry} added")
        else:
            toast(f"Name cannot be empty nor contain{os.linesep}non-alphanumeric characters except for \"-_\")")
        await asynckivy.sleep(0)



    # def rename_lineup_entry(self, lineup_entry_rowview, new_name_lineup_entry):
    #     """
    #     Fires async method to rename a lineup_entry.
    #     :param lineup_entry_rowview:
    #     :param new_name_lineup_entry:
    #     :return:
    #     """
    #     asynckivy.start(self.async_rename_lineup_entry(lineup_entry_rowview, new_name_lineup_entry))
    #
    # async def async_rename_lineup_entry(self, lineup_entry_rowview, new_name_lineup_entry):
    #     """
    #     Actual process to rename a lineup_entry.
    #     :param lineup_entry_rowview:
    #     :param new_name_lineup_entry:
    #     :return:
    #     """
    #     # Omit the provided explanation-text in case it was not omitted:
    #     new_name_lineup_entry = str(CU.with_consistent_linesep(new_name_lineup_entry)).replace(f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}{os.linesep}", "")
    #
    #     # Check the new_name_lineup_entry by means of a regular expression:
    #     # Only allow names entirely consisting of alphanumeric characters, dashes and underscores
    #     lineup_entry_to_rename = lineup_entry_rowview.lineup_entry_obj
    #
    #     if re.match("^[\w\d_-]+$", str(new_name_lineup_entry)):
    #         filename_lineup_entry = f"{str(new_name_lineup_entry)}.json"
    #         if len(list(pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).glob(filename_lineup_entry))) > 0:
    #             toast(f"{new_name_lineup_entry} already exists")
    #
    #         elif lineup_entry_to_rename.file_path.exists():
    #             old_name = str(lineup_entry_to_rename.file_path.stem)
    #             file_path = pl.Path(lineup_entry_to_rename.file_path.parents[0] / filename_lineup_entry)
    #             pl.Path(lineup_entry_to_rename.file_path).rename(file_path)
    #             toast(f"{old_name} renamed to {new_name_lineup_entry}")
    #         else:
    #             toast(f"Playlist {lineup_entry_to_rename.file_path.stem} not found")
    #     else:
    #         toast(f"Name cannot be empty nor contain{os.linesep}non-alphanumeric characters except for \"-_\")")
    #     await asynckivy.sleep(0)

    def remove_lineup_entry(self, lineup_entry_rowview, *args):
        """
        Fires async method to remove a lineup_entry.
        :param lineup_entry_rowview:
        :param args:
        :return:
        """
        asynckivy.start(self.async_remove_lineup_entry(lineup_entry_rowview, *args))

    async def async_remove_lineup_entry(self, lineup_entry_rowview, *args):
        """
        Actual process to remove a lineup_entry.
        :param lineup_entry_rowview:
        :param args:
        :return:
        """
        decision = args[0]
        lineup_entry_to_delete = lineup_entry_rowview.lineup_entry_obj

        if (str(decision).lower() == "remove"):
            self._list.remove(lineup_entry_to_delete)

            file_path_to_delete = lineup_entry_to_delete.file_path
            if (file_path_to_delete.exists() and file_path_to_delete.is_file()):
                pl.Path(file_path_to_delete).unlink()
            toast(f"{str(lineup_entry_to_delete.file_path.stem)} successfully removed")
        else:
            toast(f"Canceled removal of {str(lineup_entry_to_delete.file_path.stem)}")
        await asynckivy.sleep(0)

    # def clear_search_pattern(self):
    #     """
    #     Clear the search pattern in the filter.
    #     :return:
    #     """
    #     self.ids.search_field.text=""
    #     toast("Input cleared")
    #     # After the filter text is changed, the filter_list() method is automatically triggered.
    #
    # def filter_list(self):
    #     """
    #     Fires async method to filter the visual list.
    #     :return:
    #     """
    #     asynckivy.start(self.async_filter_list())
    #
    # async def async_filter_list(self):
    #     """
    #     Filter the visual list on the provided search pattern.
    #     :return:
    #     """
    #     search_pattern = CU.safe_cast(self.ids.search_field.text, str, "")
    #     # print(f"search pattern is {search_pattern}")
    #     self.ids.rv.data = []
    #
    #     for lineup_entry in self._list:
    #         lineup_entry_name = str(lineup_entry.file_path.stem)
    #         if (len(search_pattern) == 0 or ((len(search_pattern) > 0) and (search_pattern.lower() in lineup_entry_name.lower()))):
    #
    #             self.ids.rv.data.append(
    #                 {
    #                     "viewclass": "PlayListRowView",
    #                     "list_obj": self,
    #                     "lineup_entry_obj": lineup_entry,
    #                     "callback": None
    #                 }
    #             )
    #     await asynckivy.sleep(0)

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
        Scan the workspace-Playlists folder for lineup_entries.
        :return:
        """
        # Depending on the amount of time it takes to run through the refresh, the spinner will be more/longer visible:
        for file_path in pl.Path(CU.tfs.dic['tf_workspace_path'].value / CU.tfs.dic['PLAYLISTS_DIR_NAME'].value).rglob("*.json"):

            lineup_entry = PlayList(file_path)

            self._list.append(lineup_entry)
            await asynckivy.sleep(0)

        # TODO: Make overscroll easier than it is now, in fact scrollbar should be always visible
        await self.async_filter_list()
        self.ids.refresh_layout.refresh_done()

    def restore_former_theme_context_menus(self):
        """
        Restoring the former theme_cls and context_menus, so the modal-calling-screen gets its proper look/functionality
        :return:
        """
        PlayList.app.set_theme_toolbar(self._former_primary_palette, self._former_accent_palette)
        PlayList.app.context_menus = self._former_context_menus

    def show_dialog_add_lineup_entry(self):
        """
        Show a dialog to ask the name of the new lineup_entry.
        :return:
        """
        creation_time = datetime.now().strftime("%Y%m%d-%H%M%S")

        dialog_text = f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}{os.linesep}Concert_{creation_time}"

        CU.show_input_dialog(title=f"Enter Name of New Playlist",
                             hint_text=dialog_text,
                             text=dialog_text,
                             size_hint=(.7, .4),
                             text_button_ok="Add",
                             callback=lambda text_button, instance, *args: {self.add_lineup_entry(instance.text_field.text), self.refresh_list()})

    def show_dialog_rename_lineup_entry(self, lineup_entry_rowview):
        """
        Show a dialog to ask for the new name of the lineup_entry.
        :param lineup_entry_rowview:
        :return:
        """
        dialog_text = f"{CU.tfs.dic['EXPLANATION_PLAYLIST_SONG_NAME'].value}{os.linesep}" \
            f"{str(lineup_entry_rowview.lineup_entry_obj.file_path.stem)}"

        CU.show_input_dialog(title=f"Enter New Name for Playlist",
                             hint_text=dialog_text,
                             text=dialog_text,
                             size_hint=(.7, .4),
                             text_button_ok="Update",
                             callback=lambda text_button, instance, *args: {self.rename_lineup_entry(lineup_entry_rowview, instance.text_field.text), self.refresh_list()})

    def show_dialog_remove_lineup_entry(self, lineup_entry_rowview):
        """
        Show a dialog to ask for confirmation of the removal.
        :param lineup_entry_rowview:
        :return:
        """
        dialog_text=f"Are you sure want to remove [color={get_hex_from_color(PlayList.app.theme_cls.primary_color)}][b]{str(lineup_entry_rowview.lineup_entry_obj.file_path.stem)}[/b][/color] from the list? This action cannot be undone."

        CU.show_ok_cancel_dialog(title=f"Are You Sure?",
                                 text=dialog_text,
                                 size_hint=(.7, .4),
                                 text_button_ok="Remove",
                                 text_button_cancel="Cancel",
                                 callback=lambda *args: {self.remove_lineup_entry(lineup_entry_rowview, *args), self.refresh_list()})

    def sort_list(self):
        """
        Will sort the internal list in alphabetic order.
        :return:
        """
        self.set_list(sorted(self._list, key=lambda lineup_entry: str(lineup_entry.file_path.stem)))
        self.filter_list()
        toast("Playlists sorted")

    @staticmethod
    def on_pre_open_callback(instance):
        """
        Callback fired just before the PlayList ModalView is opened
        :param instance:
        :return:
        """
        # KivyProperties must made at class level/kv-rule not within __init__()-method. On pre open the title is updated:
        instance.playlist_name = '<Title not available>' if instance.file_path is None else instance.file_path.stem

        PlayList.app.set_theme_toolbar(PlayList.theme_primary_color, PlayList.theme_accent_color)
        PlayList.app.convert_dict_to_context_menus(instance.context_menus)

        # Override needed overscroll to refresh the screen to the bare minimum:
        # refresh_layout.effect_cls.min_scroll_to_reload = -dp(1)


    @staticmethod
    def on_open_callback(instance):
        """
        Callback fired after the PlayList ModalView is opened
        :param instance:
        :return:
        """
        # self.refresh_list()
        toast(f"{type(instance).__name__}")

    @staticmethod
    def on_pre_dismiss_callback(instance):
        """
        Callback fired on pre-dismissal of the PlayList ModalView
        :param instance: the instance of the ModalView itself, a non-static implementation would have passed 'self'
        :return:
        """
        # TODO: Warn display popup not to leave with unsaved progress:
        pass

    @staticmethod
    def on_dismiss_callback(instance):
        """
        Callback fired on dismissal of the PlayList ModalView
        :param instance: the instance of the ModalView itself, a non-static implementation would have passed 'self'
        :return: True prevents the modal view from closing
        """
        if instance.block_close:
            toast(f"Blocked closing")
        else:
            instance.restore_former_theme_context_menus()

        return instance.block_close

