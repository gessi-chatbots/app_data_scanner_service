from abc import abstractmethod, ABC


class APIScanner(ABC):
    @abstractmethod
    def __init__(self, local_data_source, remote_data_source, keys_to_extract):
        self._local_data_source = local_data_source
        self._remote_data_source = remote_data_source
        self._keys = keys_to_extract

    @abstractmethod
    def scanAppData(self, app_list):
        raise NotImplementedError
