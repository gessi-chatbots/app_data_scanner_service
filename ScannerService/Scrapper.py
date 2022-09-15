from abc import abstractmethod, ABC


class Scrapper(ABC):

    @abstractmethod
    def scrapWebsite(self, app, context):
        raise NotImplementedError
