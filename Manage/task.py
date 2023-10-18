


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
                
               [model, dataset, scene, train_sub_id, test_sub_id] 
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
                        if not _cross_exp_flag and scene == "subject_d": continue
                        for sub_id in range(1, self.subnums[i]+1):
                            single_task = {"model": model, "dataset": dataset, "scene": scene, "train_sub_id": sub_id, "test_sub_id": sub_id}
                            task_list.append(single_task)
                    elif scene == "cross_data": continue
                    elif scene == "subject_i":
                        for sub_id in range(self.subnums[i]):
                            single_task = {"model": model, "dataset": dataset, "scene": scene, "train_sub_id": sub_id+1, "test_sub_id": 1+(sub_id+1)%(self.subnums[i])}
                            task_list.append(single_task)
        if scene == "cross_data":
            # 多种情况（A. THU to CAS  B. THU to GIST  C. CAS to THU  
            #          D. CAS to GIST E. GIST to THU  F. GIST to CAS）
            # A. THU to CAS
            pass
        for i in range(len(task_list)):
            print(task_list[i], end='\n')
            with open("task_list.txt", "a+") as f:
                f.writelines(task_list[i]["model"] + "\t" +
                             task_list[i]["dataset"] + "\t" +
                             task_list[i]["scene"] + "\t" +
                             str(task_list[i]["train_sub_id"]) + "\t" +
                             str(task_list[i]["test_sub_id"]) + "\t" + "\n")
            
        


                    
        



