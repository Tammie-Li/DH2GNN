import os
import torch
import numpy as np
from Manage.task import *

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
dataset_list = ["THU", "GIST", "CAS"]
dataset_sub_nums = [64, 55, 14]
model_list = ["GCN", "HGNN", "DHGNN", "DH2GNN"]
scene_list = ["subject_d", "subject_i", "cross_data", "cross_day"]

if __name__ == "__main__":
    # generate all tasks need to train and evaluate
    tasks = CalculateTask(dataset_list, model_list, scene_list)
    single_task_set = tasks.generate_calculate_task_list()

    

