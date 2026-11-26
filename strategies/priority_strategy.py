from strategies.task_sort_strategy import TaskSortStrategy


class PriorityStrategy(TaskSortStrategy):
    def sort(self, tasks):
        priority_order = {
            "High": 1,
            "Medium": 2,
            "Low": 3
        }

        return sorted(
            tasks,
            key=lambda task: priority_order.get(task["priority"], 4)
        )
