from strategies.task_sort_strategy import TaskSortStrategy


class DefaultStrategy(TaskSortStrategy):
    def sort(self, tasks):
        return list(tasks)
