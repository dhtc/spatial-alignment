import torch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import seaborn as sns
import sys
from os.path import join as pjoin
import scanpy as sc
import anndata
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.patches as patches

sys.path.append("../../..")
sys.path.append("../../../data")
from plotting.callbacks import callback_oned, callback_twod

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, RBF, Matern
from sklearn.model_selection import KFold

import matplotlib

font = {"size": 30}
matplotlib.rc("font", **font)
matplotlib.rcParams["text.usetex"] = True
matplotlib.rcParams["xtick.labelsize"] = 10
matplotlib.rcParams["ytick.labelsize"] = 10

aligned_coords_expression = pd.read_csv(
    "./out/multimodal/aligned_coords_expression_visium.csv", index_col=0
).values
aligned_coords_histology = pd.read_csv(
    "./out/multimodal/aligned_coords_histology_visium.csv", index_col=0
).values

view_idx_expression = pd.read_csv(
    "./out/multimodal/view_idx_expression_visium.csv", index_col=0
).values
view_idx_histology = pd.read_csv(
    "./out/multimodal/view_idx_histology_visium.csv", index_col=0
).values

X_expression = pd.read_csv(
    "./out/multimodal/X_expression_visium.csv", index_col=0
).values
X_histology = pd.read_csv("./out/multimodal/X_histology_visium.csv", index_col=0).values

Y_expression = pd.read_csv(
    "./out/multimodal/Y_expression_visium.csv", index_col=0
).values
Y_histology = pd.read_csv("./out/multimodal/Y_histology_rgb_visium.csv", index_col=0).values

data = sc.read_h5ad("./out/data_visium.h5")


plt.figure(figsize=(10, 5))
for vv in range(2):
    plt.subplot(1, 2, vv + 1)
    plt.scatter(
        aligned_coords_histology[view_idx_histology[vv]][:, 0],
        aligned_coords_histology[view_idx_histology[vv]][:, 1],
        c=Y_histology[view_idx_histology[vv]],
        s=8
    )
plt.show()

import ipdb

ipdb.set_trace()

view_idx = []
for vv in range(2):
    view_idx.append(np.where(data.obs.batch.values == str(vv))[0])

n_genes = 3
# plt.figure(figsize=(n_genes * 5 + 5, 10), gridspec_kw={'width_ratios': [2., 1, 1, 1]})
fig, ax = plt.subplots(
    2,
    n_genes + 1,
    figsize=(n_genes * 5 + 5, 8),
    gridspec_kw={"width_ratios": [1.1, 1, 1, 1]},
)

# plt.subplot(2, n_genes + 1, 1)
plt.sca(ax[0, 0])
for vv in range(len(data.obs.batch.unique())):
    plt.scatter(
        X[view_idx[vv], 0], X[view_idx[vv], 1], s=1, label="View {}".format(vv + 1)
    )
lgnd = plt.legend(loc="center right", bbox_to_anchor=(-0.05, 0.5))
for handle in lgnd.legendHandles:
    handle.set_sizes([60])
plt.tight_layout()
plt.axis("off")

# plt.subplot(2, n_genes + 1, 5)
plt.sca(ax[1, 0])
for vv in range(len(data.obs.batch.unique())):
    plt.scatter(
        aligned_coords[view_idx[vv], 0],
        aligned_coords[view_idx[vv], 1],
        s=1,
    )
plt.axis("off")


for gg in range(n_genes):

    # plt.subplot(2, n_genes + 1, gg + 2)
    plt.sca(ax[0, gg + 1])
    for vv in range(len(data.obs.batch.unique())):
        plt.scatter(
            X[view_idx[vv], 0],
            X[view_idx[vv], 1],
            c=Y[view_idx[vv]][:, gg],
            s=1,
        )
    plt.title(r"$\emph{" + data.var.gene_ids.values[gg] + "}$")
    plt.axis("off")

    # plt.subplot(2, n_genes + 1, gg + (n_genes + 2) + 1)
    plt.sca(ax[1, gg + 1])
    for vv in range(len(data.obs.batch.unique())):
        plt.scatter(
            aligned_coords[view_idx[vv], 0],
            aligned_coords[view_idx[vv], 1],
            c=Y[view_idx[vv]][:, gg],
            s=1,
        )
    # plt.title(r"$\emph{" + data.var.gene_ids.values[gg] + "}$")
    plt.axis("off")

plt.savefig("./out/slideseq_alignment_per_gene.png")
plt.show()


import ipdb

ipdb.set_trace()