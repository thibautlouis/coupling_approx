import pylab as plt, numpy as np
from pspy import pspy_utils, so_dict, so_map
import ps_tools
import sys
import pickle
import time
import spectra_plot_utils

d = so_dict.so_dict()
d.read_from_file(sys.argv[1])
run_name = d["run_name"]

spectra_dir = "spectra_%s" % run_name
plot_dir = "plot_%s" % run_name

pspy_utils.create_directory(spectra_dir)
pspy_utils.create_directory(plot_dir)

lmax = d["lmax"]
type = d["type"]
clfile = d["clfile"]
l_exact_array = d["l_exact_array"]
l_band_array = d["l_band_array"]
l_toep_array = d["l_toep_array"]
compute_T_only = d["compute_T_only"]
l_lo, l_hi, lb, delta_l = pspy_utils.read_binning_file( "data/binning.dat", lmax)


id_sim =  d["id_sim"]
result_ps = {}
result_cov = {}

test_names = []
for l_exact, l_band, l_toep in zip(l_exact_array, l_band_array, l_toep_array):

    if (l_exact == None) & (l_toep == None) & (l_band == None):
        test = "exact"
    else:
        test = "%d_%d_%d"%(l_exact, l_band, l_toep)
    
    print (test)
    t = time.time()
    
    pkl_file = open("%s/ps_dict_%s_%03d.pkl" % (spectra_dir, test, d["id_sim"]), "rb")
    ps_dict = pickle.load(pkl_file)
    pkl_file.close()
    
    pkl_file = open("%s/cov_dict_%s_%03d.pkl" % (spectra_dir, test, d["id_sim"]), "rb")
    cov_dict = pickle.load(pkl_file)
    pkl_file.close()

    result_ps[test] = ps_dict
    result_cov[test] = cov_dict
    
    test_names += [test]
    
if compute_T_only == True:
    spectra = ["TT"]
else:
    spectra = ["TT", "TE", "TB", "ET", "BT", "EE", "EB", "BE", "BB"]
    
test_names.remove("exact")
# Make plots
lth, clth = pspy_utils.ps_lensed_theory_to_dict(clfile, type, lmax=lmax)
cross ="sim_%03d_split0xsim_%03d_split1"%(id_sim, id_sim)


spectra_plot_utils.plot_spectra_comparison(lb, result_ps, result_cov, cross, ["TT","TE","EE"], test_names, plot_dir, lth, clth)
spectra_plot_utils.plot_spectra_comparison(lb, result_ps, result_cov, cross, ["TB","EB","BB"], test_names, plot_dir, lth, clth)

spectra_plot_utils.delta_Cl_over_sigma(lb, result_ps, result_cov, cross, spectra, test_names, plot_dir)

spectra_plot_utils.cov_plot(lb,  result_cov, cross, spectra, test_names, plot_dir)

for spec in spectra:
    for count,test in enumerate(test_names):
        ps, sigma = result_ps[test][cross][spec], np.sqrt(np.diag(result_cov[test][cross][spec]))
        print(ps)
        
    
 #   plt.figure(figsize=(15, 15))
 #   for count,test in enumerate(test_names):
 #       ps, sigma = result_ps[test][cross][spec], np.sqrt(np.diag(result_cov[test][cross][spec]))
 #       l_exact, l_band, l_toep = test.split("_")
 #       plt.errorbar(lb,
 #                    100 * (ps / ps_exact - 1),
 ##                    label = r"$\ell_{\rm exact}=$%s, $\ell_{\rm band}=$%s, $\ell_{\rm toep}=$%s"% (l_exact,l_band, l_toep))

   # plt.legend(fontsize=25)
   # plt.xlabel(r"$\ell$", fontsize=25)
   # plt.ylabel(r"ratio $C_\ell$ (%)", fontsize=25)
   # plt.xticks(fontsize=20)
   ## plt.yticks(fontsize=20)
   # plt.savefig("%s/ratio_ps_%s.png" % (plot_dir, spec))
   # plt.clf()
   # plt.close()
