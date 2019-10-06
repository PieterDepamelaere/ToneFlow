import pathlib as pl
from abc import ABC, abstractmethod

class LineupEntry(ABC):

    def __init__(self, entry_type=None, file_path=None, shown_upside_down=False):
        super().__init__()

        self.entry_type = entry_type
        self.file_path = pl.Path(file_path)
        self.shown_upside_down = shown_upside_down

    @abstractmethod
    def test(self):
        pass

    # Normal instance methods
    def set_file_path(self, new_file_path):
        """
        Setter file_path
        :param new_file_path: new_file_path
        :return:
        """
        self.file_path = pl.Path(new_file_path)
        # TODO PDP: Add confirmation via toast that file was found probably rather in main section

    def set_upside_down(self, upside_down):
        """
        Set boolean upside_down, that will make the <LineupEntry> to be shown upside down. (This comes in handy when projecting vertically on the floor facing the audience)
        :param upside_down: bool
        :return:
        """
        self.upside_down = upside_down

    def check_file_exists(self):
        return self.file_path.exists()

    def serialize_json(self):
        pass

    def deserialize_json(self):
        pass
