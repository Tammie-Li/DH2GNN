"""从数据集中加载数据, 以不同的方式构图, 返回图数据集"""
import numpy as np
import matplotlib.mlab as mlab
from scipy.signal import hilbert


def gen_edges_corr(x, weighted=True):
    """
    Generate weighted(optional) edges based on channel correlation coefficient
    :param x: (T, C)
    :param weighted: True or False
    :return: edge_index: (2, num_edges)
             edge_weight:(num_edges, 1)
    """
    adj = np.corrcoef(x.T)
    adj[range(adj.shape[0]), range(adj.shape[0])] = 0
    avg = np.sum(adj) / (adj.shape[0] * adj.shape[0] - adj.shape[0])
    zeros_index = np.argwhere(adj <= avg)
    adj[zeros_index[:, 0], zeros_index[:, 1]] = 0

    edge_index = np.argwhere(adj != 0).T

    if weighted:
        edge_weight = adj[edge_index[0, :], edge_index[1, :]].reshape(-1, 1)
        return edge_index, edge_weight
    else:
        return edge_index


def gen_edges_wpli(x, fs=256, weighted=True):
    """
    Generate weighted(optional) edges based on weighted phase lax index
    :param x: (T, C)
    :param weighted: True or False
    :return: edge_index: (2, num_edges)
             edge_weight:(num_edges, 1)
    """
    x = x.T
    channels, samples = x.shape
    wpli = np.zeros((channels, channels))

    pairs = [(i, j) for i in range(channels) for j in range(channels)]

    for pair in pairs:
        ch1, ch2 = x[pair,]
        csdxy, _ = mlab.csd(ch1, ch2, Fs=fs, scale_by_freq=True,
                            sides='onesided')

        i_xy = np.imag(csdxy)
        num = np.nansum(np.abs(i_xy) * np.sign(i_xy))
        denom = np.nansum(np.abs(i_xy))

        wpli[pair] = np.abs(num / denom)

    adj = wpli
    adj[range(adj.shape[0]), range(adj.shape[0])] = 0
    avg = np.sum(adj) / (adj.shape[0] * adj.shape[0] - adj.shape[0])
    zeros_index = np.argwhere(adj <= avg)
    adj[zeros_index[:, 0], zeros_index[:, 1]] = 0

    edge_index = np.argwhere(adj != 0).T

    if weighted:
        edge_weight = adj[edge_index[0, :], edge_index[1, :]].reshape(-1, 1)
        return edge_index, edge_weight
    else:
        return edge_index


def gen_edges_plv(x, weighted=True):
    """
    Generate weighted(optional) edges based on phase locking value
    :param x: (T, C)
    :param weighted: True or False
    :return: edge_index: (2, num_edges)
             edge_weight:(num_edges, 1)
    """
    x = x.T
    channels, samples = x.shape
    x_h = hilbert(x)
    phase = np.unwrap(np.angle(x_h))

    Q = np.exp(1j * phase)
    Q = np.matrix(Q)
    W = np.abs(Q @ Q.conj().transpose()) / np.float32(samples)

    adj = W
    adj[range(adj.shape[0]), range(adj.shape[0])] = 0
    avg = np.sum(adj) / (adj.shape[0] * adj.shape[0] - adj.shape[0])
    zeros_index = np.argwhere(adj <= avg)
    adj[zeros_index[:, 0], zeros_index[:, 1]] = 0

    edge_index = np.argwhere(adj != 0).T

    if weighted:
        edge_weight = adj[edge_index[0, :], edge_index[1, :]].reshape(-1, 1)
        return edge_index, edge_weight
    else:
        return edge_index


def gen_edges_cg(x):
    """
    Generate edges based on complete graph
    :param x: (T, C)
    :return: edge_index: (2, C * C - C)
    """
    samples, channels = x.shape
    edge_index = [[i, j] for i in range(channels) for j in range(channels)
                  if i != j]
    edge_index = np.asarray(edge_index).T
    return edge_index

def gen_hvg_edges(nodes):
    """
    Generate edges from the horizontal visibility graph.
    :param nodes: time series of the specific node
    :return: edges list
    """
    edges = []
    for i in range(len(nodes) - 1):
        a_idx, a_val = nodes[i]
        b_idx, b_val = nodes[i + 1]
        edges.append([a_idx, b_idx])

    for i in range(0, len(nodes) - 1):
        a_idx, a_val = nodes[i]
        for j in range(i + 2, len(nodes)):
            b_idx, b_val = nodes[j]
            visible = True
            for c_idx, c_val in nodes:
                if c_idx > a_idx and c_idx < b_idx:
                    if c_val > a_val or c_val > b_val:
                        visible = False
                        break
            if visible:
                edges.append([a_idx, b_idx])
    return edges




