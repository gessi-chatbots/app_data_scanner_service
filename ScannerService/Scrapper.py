from abc import abstractmethod, ABC


class Scrapper(ABC):

    @abstractmethod
    def scrapWebsite(self, app_list):
        raise NotImplementedError
