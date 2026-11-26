from abc import ABC, abstractmethod


class TaskSortStrategy(ABC):
    @abstractmethod
    def sort(self, tasks):
        pass
