
from abc import ABC, abstractmethod


class Assistant(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        pass


class BaseCache(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def put(self, *args, **kwargs):
        pass
