from tqdm import trange
import torch
import os
import numpy as np
from torch_geometric.data import Data, DataLoader


class Data:
    def __init__(self, sub_num, dataset_name, dir):
        self.sub_num = sub_num
        self.dataset_name = dataset_name
        
        self.train_data = np.load(os.path.join(dir, f"{self.dataset_name}", f"{self.sub_num}:>02d", "x_train.npy"))
        self.test_data = np.load(os.path.join(dir, f"{self.dataset_name}", f"{self.sub_num}:>02d", "x_test.npy"))
        self.train_label = np.load(os.path.join(dir, f"{self.dataset_name}", f"{self.sub_num}:>02d", "y_train.npy"))
        self.test_label = np.load(os.path.join(dir, f"{self.dataset_name}", f"{self.sub_num}:>02d", "y_test.npy"))

    def get_data(self):
        print(f"generate dataset {self.dataset_name} : No. {self.sub_num:>02d}")
        pass


def gen_data_list(data, label, edge_type='corr', feature_type='psd_group'):
    """
    Generate graph data list from matrix data and label.
    :param data: training or testing data in matrix form, shape: (N, T, C)
    :param label: training or testing label in matrix form, shape: (N, )
    :return: training or testing data list,
             each item in this list is a torch_geometric.data.Data object.
    """
    data_list = []
    for trial in trange(data.shape[0]):
        trial_data = data[trial, ...]
        trial_label = label[trial]

        # generate edge index and node features
        if edge_type == 'corr':
            edge_index, edge_weight = gen_edges_corr(trial_data)
        elif edge_type == 'wpli':
            edge_index, edge_weight = gen_edges_wpli(trial_data)
        elif edge_type == 'plv':
            edge_index, edge_weight = gen_edges_plv(trial_data)
        elif edge_type == 'cg':
            edge_index = gen_edges_cg(trial_data)
            edge_weight = np.zeros((edge_index.shape[-1], 1))

        if feature_type == 'hvg':
            x = gen_features_hvg(trial_data)
        elif feature_type == 'cre':
            x = gen_features_cre(trial_data)
        elif feature_type == 'cre_group':
            x = gen_features_cre_group(trial_data)
        elif feature_type == 'psd_group':
            x = gen_features_psd_group(trial_data)
        elif feature_type == 'wavelet':
            x = gen_features_wavelet(trial_data, wavelet='coif1', level=4)
        elif feature_type == 'raw':
            x = gen_features_raw(trial_data)
        elif feature_type == 'wt_deg':
            x = gen_features_wt_deg(trial_data, level=5)

        edge_index = torch.from_numpy(edge_index).long()
        edge_weight = torch.from_numpy(edge_weight).float()
        x = torch.from_numpy(x).float()

        graph_data = Data(x=x, edge_index=edge_index,
                          y=trial_label, edge_attr=edge_weight)
        data_list.append(graph_data)
    return data_list