from pspy import so_map, so_dict, sph_tools, so_mcm, pspy_utils
import numpy as np, healpy as hp
import sys, time

d = so_dict.so_dict()
d.read_from_file(sys.argv[1])

l_exact_array = d["l_exact_array"]
l_band_array = d["l_band_array"]
l_toep_array = d["l_toep_array"]
lmax = d["lmax"]
niter = 0

coupling_dir = "coupling"
pspy_utils.create_directory(coupling_dir)

window_dir = "window"
window = so_map.read_map("%s/window.fits" % (window_dir))

win_alm = sph_tools.map2alm(window, niter=niter, lmax=lmax)
wcl = hp.alm2cl(win_alm, win_alm)

for l_exact, l_band, l_toep in zip(l_exact_array, l_band_array, l_toep_array):

    if (l_exact == None) & (l_toep == None) & (l_band == None):
        test = "exact"
    else:
        test = "%d_%d_%d"%(l_exact, l_band, l_toep)

    t = time.time()
    mcm_list = so_mcm.mcm_and_bbl_spin0and2((win_alm, win_alm),
                                            input_alm=True,
                                            binning_file= "data/binning.dat",
                                            lmax=lmax,
                                            niter=niter,
                                            l_exact=l_exact,
                                            l_band=l_band,
                                            l_toep=l_toep,
                                            return_coupling_only=True)
                                            
    print("time to compute coupling: %0.2f s"%(time.time()-t))
    
    name_list =["00", "02", "20", "++", "--"]
    for id_mcm, name in enumerate(name_list):
        np.save("%s/coupling_%s_%s.npy" % (coupling_dir, test, name), mcm_list[id_mcm])
