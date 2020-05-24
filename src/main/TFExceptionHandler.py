import os
import sys
import traceback

from kivy.app import App
from kivy.utils import get_hex_from_color
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivymd.toast import toast
from kivymd.uix.label import MDLabel

from src.model.CommonUtils import CommonUtils as CU

class TFExceptionHandler(ExceptionHandler):
    def __init__(self):
        super(TFExceptionHandler, self).__init__()
        self._current_exception = None
        self._error_dialog = None
        self._PASS_or_RAISE = ExceptionManager.PASS # PASS==1, RAISE==0

    def handle_exception(self, exception):
        # app = App.get_running_app()

        # If the current problem is cleared, "accept" the next one:
        if self._current_exception is None:
            # In order to make a new dialog, we get rid of a previous one if any:
            self._error_dialog = None
            # While showing the popup to the user with the error's stacktrace, all subsequent calls to handle_exception() should PASS. It turns out that while in error, that his method is constantly triggered!!
            self._PASS_or_RAISE = ExceptionManager.PASS

            if self._error_dialog is None:
                self._current_exception = exception

                bl1 = BoxLayout(orientation='vertical', spacing="12dp", size_hint_y=None)

                # Make sure the height is such that there is something to scroll.
                bl1.bind(minimum_height=bl1.setter('height'))

                mdlbl1 = MDLabel(text = f"[color={get_hex_from_color((1, 0, 0))}][i]{str(self._current_exception)}[/i][/color]{os.linesep}{os.linesep}"
                f"[b]-> Our apologies for the inconvenience, please consult the stack trace below & mail screenshot to pieter.depamelaere@hotmail.com:[/b]"
                f"{os.linesep}{traceback.format_exc()}", size_hint=(1, None), markup=True)

                # TODO: Rather try the .kv alternative also provided at "https://stackoverflow.com/questions/43666381/wrapping-the-text-of-a-kivy-label" and "https://kivy.org/doc/stable/api-kivy.uix.scrollview.html" that will cleaner and more maintainable
                mdlbl1.bind(width=lambda *x, **kwargs: mdlbl1.setter('text_size')(mdlbl1, (mdlbl1.width, None)), texture_size=lambda *x, **kwargs: mdlbl1.setter('height')(mdlbl1,mdlbl1.texture_size[1]))

                bl1.add_widget(mdlbl1)

                content_obj = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint=(1, None), scroll_type=['bars', 'content'])
                content_obj.add_widget(bl1)

                self._error_dialog = CU.show_input_dialog(
                    title=f"{CU.tfs.dic['APP_NAME'].value} Encountered an Error & Needs to Shut Down",
                    content_obj=content_obj,
                    # size_hint=(.8, .6),
                    text_button_ok="Quit",
                    text_button_cancel="Proceed @ Own Risk",
                    ok_callback_set=lambda *args, **kwargs: (self.set_raise_or_pass(ExceptionManager.RAISE)),
                    cancel_callback_set=lambda *args, **kwargs: (toast("Fingers crossed"), self.set_raise_or_pass(ExceptionManager.PASS))
                )

        return self._PASS_or_RAISE

    def set_raise_or_pass(self, decision):

        self._PASS_or_RAISE = decision

        # Reraise in case "QUIT" was clicked for developing purposes:
        if(decision == ExceptionManager.RAISE):
            raise self._current_exception

        # Reset the _current_exception variable so the next one can be handled:
        # This won't be reset in the raise case (throws exception without continuing to execute code), but that doesn't matter:
        self._current_exception = None
