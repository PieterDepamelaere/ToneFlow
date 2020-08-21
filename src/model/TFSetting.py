import os
import sys
import pathlib as pl
from kivymd.toast import toast
curr_file = pl.Path(os.path.realpath(__file__))

sys.path.insert(0, str(curr_file.parents[0]))
sys.path.insert(0, str(curr_file.parents[1]))
sys.path.insert(0, str(curr_file.parents[2]))

from src.model.CommonUtils import CommonUtils as CU

class TFSetting:
    def __init__(self, name, value, default_value, description, is_editable=False, callback_on_set=None):

        if (value is None):
            value = default_value

        if (description is None):
            description = ""
            # _description = name

        self._name = name
        self._value = value
        self._default_value = default_value
        self._description = description
        self._is_editable = is_editable
        self._callback_on_set = callback_on_set

    def get_name(self):
        return self._name

    def set_name(self, name):
        name = CU.safe_cast(name, str, "")
        self._name = name

    def get_value(self):
        return self._value

    def set_value(self, value):
        # Check if the type of the new value matches with the type of the default value, try safe_casting:
        if (isinstance(self._default_value, pl.Path)):
            # When it's a pl.Path, then the exportable FILE_SEP_TEXT should be replaced:
            value = str(value).replace(f"{CU.tfs.dic['FILE_SEP_TEXT'].value}", f"{os.sep}")
        if (isinstance(value, str)):
            value = CU.with_consistent_linesep(value)

        # The callback can do some extra checking of the value while its for instance still string, and order of doing the safe cast and calling the callback used to be the other way around, but the pathlib library uses other windows-lineseparator when casting back to string, but then it's not possible to omit an explanation
        if (self._callback_on_set is not None):
            processed_value = self._callback_on_set(value)
        else:
            processed_value = value

        if processed_value is not None:
            self._value = CU.safe_cast(processed_value, type(self._default_value), "")
        else:
            # The previous _value is left unchanged.
            toast(f"Value for setting \"{self.name}\" is not valid{os.linesep}Original value was left unchanged.")


    def get_default_value(self):
        return self._default_value

    def get_description(self):
        return self._description

    def set_description(self, description):
        description = CU.safe_cast(description, str, "")
        self._description = description

    def get_is_editable(self):
        return self._is_editable

    name = property(get_name, set_name)
    value = property(get_value, set_value)
    default_value = property(get_default_value)
    description = property(get_description, set_description)
    is_editable = property(get_is_editable)

    def restore_factory_setting(self):
        self._value = self._default_value

    def to_json(self):
        if (self.is_editable):
            exportable_value = self.value
            if (isinstance(self.value, pl.Path)):
                # The TFSetting indicates a Path-obj:
                # exportable_value = "/FILE_SEP/".join(self.value.parts)

                # Doing it in above more elegant way, sees first '/' of linux path as a solid part, so inevitable extra fileseparator gets prepended
                exportable_value = f"{CU.tfs.dic['FILE_SEP_TEXT'].value}".join(self.value.as_posix().split("/"))

            return dict(name=self.name, value=exportable_value)
        else:
            # This case will theoretically no longer occur given that the export method only serializes a subsection of the
            return None
