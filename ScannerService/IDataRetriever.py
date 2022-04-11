import abc


class IDataRetriever(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_data') and
                callable(subclass.get_data))

    @abc.abstractmethod
    def get_data(self, app_name: str):
        raise NotImplementedError
