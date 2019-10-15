import os
import sys
import pathlib as pl
curr_file = pl.Path(os.path.realpath(__file__))

sys.path.insert(0, str(curr_file.parents[0]))
sys.path.insert(0, str(curr_file.parents[1]))
sys.path.insert(0, str(curr_file.parents[2]))

from src.model.CommonUtils import CommonUtils as CU

class TFSetting:
    def __init__(self, name, value, default_value, description, is_editable=False):

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

    def get_name(self):
        return self._name

    def set_name(self, name):
        name = CU.safe_cast(name, str, "")
        self._name = name

    def get_value(self):
        return self._value

    def set_value(self, value):
        # if (value < 18):
        #     raise ValueError("Sorry you age is below eligibility criteria")
        self._value = value

    def get_description(self):
        return self._description

    def set_description(self, description):
        description = CU.safe_cast(description, str, "")
        self._description = description

    def get_is_editable(self):
        return self._is_editable

    name = property(get_name, set_name)
    value = property(get_value, set_value)
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
