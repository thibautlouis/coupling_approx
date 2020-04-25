from pspy import so_dict, so_cov, pspy_utils
import cov_plot_utils
import numpy as np
import sys


plot_dir = "plot"

pspy_utils.create_directory(plot_dir)


coupling_dir = "coupling"

name_list =["00", "02", "20", "++", "--"]
mcm_dict = {}

for id_mcm, name in enumerate(name_list):
    coupling = np.load("%s/coupling_exact_%s.npy" % (coupling_dir, name))
    corr = so_cov.cov2corr(coupling, remove_diag=False)
    cov_plot_utils.toepliz_plot(plot_dir, corr, name, lsplit=2500)
 
