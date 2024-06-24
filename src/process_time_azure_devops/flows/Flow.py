from abc import ABC, abstractmethod


class Flow(ABC):
    """
    Base interface for different deployment strategy flows
    """
    @abstractmethod
    def calculate_process_time(self):
        pass
    