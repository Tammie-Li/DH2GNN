


class CalculateTask:
    def __init__(self, dataset, model, scene):
        self.dataset = dataset
        self.model = model
        self.scene = scene

    def generate_calculate_task_list(self):
        """
        cal_task_list introduction
        :return: normalized node features, shape: (C, F)
                C denotes the number of nodes,
                F denotes the number of node features.
        """
        pass