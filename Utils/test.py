import torch 
import dhg

if __name__ == "__main__":
    g = dhg.random.graph_Gnm(5, 8)
    x = torch.rand(5, 3)
    la_mat = g.L_GCN.to_dense()
    features = g.smoothing_with_GCN(x)
    print(features)