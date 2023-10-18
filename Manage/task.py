


class CalculateTask:
    def __init__(self, datasets, subnums, models, scenes):
        self.datasets = datasets
        self.subnums = subnums
        self.models = models
        self.scenes = scenes

    def generate_calculate_task_list(self):
        """
        cal_task_list introduction
        :return: 
                
               [model, dataset, train_sub_id, test_sub_id] 
        """
        # 场景不一样导致的计算任务区别，仅仅体现在训练集和测试集上
        task_list = []
        _cross_exp_flag = False
        for model in self.models:
            for i, dataset in enumerate(self.datasets):
                if dataset == "CAS": _cross_exp_flag = True 
                else: _cross_exp_flag = False
                for scene in self.scenes:
                    if scene == "cross_day" or scene == "subject_d":
                        if not _cross_exp_flag and scene == "cross_day": continue
                        for sub_id in range(1, self.subnums[i]+1):
                            single_task = {"model": model, "dataset": dataset, "train_sub_id": sub_id, "test_sub_id": sub_id}
                            task_list.append(single_task)
                    elif scene == "cross_data": continue
                    elif scene == "subject_i":
                        for sub_id in range(1, self.subnums[i]+1):
                            single_task = {"model": model, "dataset": dataset, "train_sub_id": sub_id, "test_sub_id": (sub_id+1)//self.subnums}
                            task_list.append(single_task)
        if scene == "cross_data":
            pass
        print(task_list)


                    
        



        for scene in self.scenes:
            if scene == "cross_day":
                # 跨时间场景只作用在CAS数据集上
                pass


            if scene == "subject_d":
                self._generate_task_on_dataset()
            elif scene == "subject_i":
                pass

