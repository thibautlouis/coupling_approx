import pylab as plt, numpy as np
from pspy import pspy_utils, so_dict, so_map
import ps_tools
import sys
import pickle
import time

d = so_dict.so_dict()
d.read_from_file(sys.argv[1])

sim_dir = "sims"
window_dir = "window"
spectra_dir = "spectra"

pspy_utils.create_directory(spectra_dir)

maps_info_list = []
for i in range(d["n_splits"]):
    name = "sim_%03d_%s%d" % (d["id_sim"], d["name_split"], i)
    maps_info_list += [{"name":"%s/%s.fits" % (sim_dir, name), "data_type":"IQU", "id":name, "cal": None}]


beam = d["beam"]
lmax = d["lmax"]
type = d["type"]
bin_size = d["bin_size"]
compute_T_only = d["compute_T_only"]
binning_file_name = "%s/binning.dat" % spectra_dir
pspy_utils.create_binning_file(bin_size=bin_size, n_bins=1000, file_name=binning_file_name)


window = so_map.read_map("%s/window.fits" % (window_dir))
car_box = np.loadtxt("%s/car_box.dat" % (window_dir))

l_exact_array = d["l_exact_array"]
l_band_array = d["l_band_array"]
l_toep_array = d["l_toep_array"]

for l_exact, l_band, l_toep in zip(l_exact_array, l_band_array, l_toep_array):

    if (l_exact == None) & (l_toep == None) & (l_band == None):
        test = "exact"
    else:
        test = "%d_%d_%d"%(l_exact,l_band, l_toep)
    
    t = time.time()
    
    mbb_inv = ps_tools.compute_mode_coupling(window,
                                             type,
                                             lmax,
                                             binning_file_name,
                                             ps_method="master",
                                             beam = beam,
                                             l_exact=l_exact,
                                             l_band=l_band,
                                             l_toep=l_toep,
                                             compute_T_only=compute_T_only)
                                             
    print ("mbb took %.2f s to compute" % (time.time()-t))

    spectra, spec_name_list, lb, ps_dict = ps_tools.get_spectra(window,
                                                                maps_info_list,
                                                                car_box,
                                                                type,
                                                                lmax,
                                                                binning_file_name,
                                                                ps_method="master",
                                                                mbb_inv=mbb_inv,
                                                                compute_T_only=compute_T_only)
                          
                          
    ps_dict_for_cov = ps_tools.theory_for_covariance(ps_dict,
                                                     spec_name_list,
                                                     spectra,
                                                     lmax,
                                                     beam=beam,
                                                     binning_file=binning_file_name)
                                    

    cov_dict = ps_tools.get_covariance(window,
                                       lmax,
                                       spec_name_list,
                                       ps_dict_for_cov,
                                       binning_file_name,
                                       error_method="master",
                                       l_exact=l_exact,
                                       l_band=l_band,
                                       l_toep=l_toep,
                                       spectra=spectra,
                                       mbb_inv=mbb_inv,
                                       compute_T_only=compute_T_only)

    
    output = open("%s/ps_dict_%s_%03d.pkl" % (spectra_dir, test, d["id_sim"]), "wb")
    pickle.dump(ps_dict, output)
    output.close()

    output = open("%s/cov_dict_%s_%03d.pkl" % (spectra_dir, test, d["id_sim"]), "wb")
    pickle.dump(cov_dict, output)
    output.close()
