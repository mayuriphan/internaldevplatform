from abc import ABC
from abc import abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def provision(
        self,
        resource_name: str,
        parameters: dict,
    ):
        pass

    @abstractmethod
    def deprovision(
        self,
        resource_id: str,
    ):
        pass

    @abstractmethod
    def get_status(
        self,
        resource_id: str,
    ):
        pass