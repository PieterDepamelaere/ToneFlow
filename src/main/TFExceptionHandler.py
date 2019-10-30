import os
import sys
import traceback

from kivy.app import App
from kivy.utils import get_hex_from_color
from kivy.base import ExceptionHandler, ExceptionManager

from kivymd.toast import toast

from src.model.CommonUtils import CommonUtils as CU

class TFExceptionHandler(ExceptionHandler):
    def __init__(self):
        super(TFExceptionHandler, self).__init__()
        self._current_exception = None
        self._error_dialog = None
        self._PASS_or_RAISE = ExceptionManager.PASS # PASS==1, RAISE==0

    def handle_exception(self, exception):
        app = App.get_running_app()

        # If the current problem is cleared, "accept" the next one:
        if self._current_exception is None:
            # In order to make a new dialog, we get rid of a previous one if any:
            self._error_dialog = None
            # While showing the popup to the user with the error's stacktrace, all subsequent calls to handle_exception() should PASS. It turns out that while in error, that his method is constantly triggerd!!
            self._PASS_or_RAISE = ExceptionManager.PASS

            if self._error_dialog is None:
                self._current_exception = exception
                self._error_dialog = app.show_ok_cancel_dialog(
                    # title=f"{CU.tfs.dic['APP_NAME'].value} Encountered an Error & Needs to Shut Down",
                    title=f"{CU.tfs.dic['APP_NAME'].value} Encountered an Error & Needs to Shut Down",
                    text=f"[color={get_hex_from_color((1, 0, 0))}][i]{str(self._current_exception)}[/i][/color]{os.linesep}{os.linesep}"
                    f"[b]-> Our apologies for the inconvenience, please consult the stack trace below:[/b]{os.linesep}"
                    f"{traceback.format_exc()}",
                    size_hint=(.8, .6),
                    text_button_ok="Quit",
                    text_button_cancel="Proceed @ Own Risk",
                    callback=lambda *args: self.decide_raise_or_pass(*args)
                )

        return self._PASS_or_RAISE


    def decide_raise_or_pass(self, *args):

        # Interpret user's choice:
        if args[0] is not None:
            if (CU.safe_cast(args[0], str, "")).lower() == "quit":
                self._PASS_or_RAISE = ExceptionManager.RAISE
                raise self._current_exception
            else:
                # Proceed @ own risk case:
                toast("Fingers crossed")
                self._PASS_or_RAISE = ExceptionManager.PASS
        else:
            self._PASS_or_RAISE = ExceptionManager.RAISE

        # Reset the _current_exception variable so the next one can be handled. This won't be reset in the raise case, but that doesn't matter.
        self._current_exception = None
