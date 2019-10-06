import pathlib as pl
from abc import ABC, abstractmethod

class LineupEntry(ABC):

    def __init__(self, entry_type=None, file_path=None, **kwargs):
        super().__init__(**kwargs)

        # Entry type will be handy when deserializing from JSON-files + to know which icon has to be shown
        self._entry_type = entry_type
        self._file_path = pl.Path(file_path)

    @abstractmethod
    def test(self):
        pass

    # Normal instance methods
    def set_file_path(self, file_path):
        """
        Setter _file_path
        :param file_path: file_path
        :return:
        """
        self._file_path = pl.Path(file_path)
        # TODO: Add confirmation via toast that file was found probably rather in main section

    def check_file_exists(self):
        return self._file_path.exists()

    def serialize_json(self):
        # TODO: Watch out that _file_path is serialized relatively and in platform indep way. ie, as list of separate segments, while omitting the fileseparator
        pass

    def deserialize_json(self):
        pass
