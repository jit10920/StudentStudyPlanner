from strategies.task_sort_strategy import TaskSortStrategy


class DeadlineStrategy(TaskSortStrategy):
    def sort(self, tasks):
        return sorted(
            tasks,
            key=lambda task: (
                not task["deadline"],
                task["deadline"] or ""
            )
        )
