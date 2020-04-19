import pylab as plt, numpy as np
from pspy import pspy_utils, so_map, so_window
import ps_tools
import time

clfile = "data/cosmo_spectra_and_fg.dat"
ra0, ra1, dec0, dec1 = -25, 25, -25, 25
res_arcmin = 0.5
n_splits = 2
rms_uKarcmin_T = 1
#patch = {"patch_type": "Disk", "center": [0,0], "radius": 60}
patch = {"patch_type": "Rectangle", "patch_coordinate": [[-10,-20],[10,20]]}

compute_T_only = False
lmax = 5000
apo_radius_degree = 1
bin_size = 40
type = "Dl"
binning_file_name = "data/binning.dat"
pspy_utils.create_binning_file(bin_size=bin_size, n_bins=500, file_name=binning_file_name)

n_holes = 300
hole_radius_arcmin = 5
apo_radius_degree_pts_source = 0.3

# We will do three test, one without approx, one with l_tres, one with l_tres,
l_tres = 5000
l_toep = 3000
l_thres_array = [None, l_tres, l_tres]
l_toep_array = [None, None, l_toep]
test_names = ["exact", "thres", "thres_toep"]

result_dir = "results"
pspy_utils.create_directory(result_dir)


# First we generate some simulations
print("generate sims")
template_car = so_map.car_template(3, ra0, ra1, dec0, dec1, res_arcmin)
cmb = template_car.synfast(clfile)
maps_info_list = []
for i in range(n_splits):
    name = "split%d"%i
    split = cmb.copy()
    noise = so_map.white_noise(split, rms_uKarcmin_T=rms_uKarcmin_T)
    split.data += noise.data
    split.write_map("%s/%s.fits" % (result_dir, name))
    map_info = {"name":"%s/%s.fits" % (result_dir, name), "data_type":"IQU", "id":name, "cal": None}
    maps_info_list += [map_info]


#  generate a window fonction
print("generate window")
car_box, window = ps_tools.create_window(patch,
                                       maps_info_list,
                                       apo_radius_degree,
                                       res_arcmin,
                                       compute_T_only=compute_T_only)
                                       
#  multiply by an additional source mask
ps_mask = window.copy()
ps_mask.data[:] = 1
ps_mask = so_map.simulate_source_mask(ps_mask, n_holes, hole_radius_arcmin)
ps_mask = so_window.create_apodization(ps_mask, apo_type="C1", apo_radius_degree=apo_radius_degree_pts_source)

window.data *= ps_mask.data

window.write_map("%s/window.fits" % (result_dir))
window.plot(file_name="%s/window"%(result_dir))


result_ps, result_cov = {}, {}
for l_thres, l_toep, name in zip(l_thres_array, l_toep_array, test_names):
    t = time.time()
    mbb_inv = ps_tools.compute_mode_coupling(window,
                                           type,
                                           lmax,
                                           binning_file_name,
                                           ps_method="master",
                                           l_thres=l_thres,
                                           l_toep=l_toep,
                                           compute_T_only=compute_T_only)

    spectra, spec_name_list, lb, ps_dict = ps_tools.get_spectra(window,
                                                              maps_info_list,
                                                              car_box,
                                                              type,
                                                              lmax,
                                                              binning_file_name,
                                                              ps_method="master",
                                                              mbb_inv=mbb_inv,
                                                              compute_T_only=compute_T_only)
                                                         
    cov_dict = ps_tools.get_covariance(window,
                                    lmax,
                                    spec_name_list,
                                    ps_dict,
                                    binning_file_name,
                                    error_method="master",
                                    l_thres=l_thres,
                                    l_toep=l_toep,
                                    spectra=spectra,
                                    mbb_inv=mbb_inv,
                                    compute_T_only=compute_T_only)

    print ("spectra took %.2f s to compute" % (time.time()-t))
    
    result_ps[name] = ps_dict
    result_cov[name] = cov_dict

# Make plots
lth, clth = pspy_utils.ps_lensed_theory_to_dict(clfile, "Dl", lmax=lmax)
cross ="split0xsplit1"
for spec in spectra:
    
    print(spec)
    ps0, sigma0 = result_ps["exact"][cross][spec], np.sqrt(np.diag(result_cov["exact"][cross][spec]))
    ps1, sigma1 = result_ps["thres"][cross][spec], np.sqrt(np.diag(result_cov["thres"][cross][spec]))
    ps2, sigma2 = result_ps["thres_toep"][cross][spec], np.sqrt(np.diag(result_cov["thres_toep"][cross][spec]))

    plt.figure(figsize=(15, 15))
    plt.plot(lth, clth[spec] * lth**2)
    plt.errorbar(lb, ps0 * lb**2, sigma0 * lb**2, fmt=".", label ="exact")
    plt.errorbar(lb + 10, ps1 * lb**2, sigma1 * lb**2, fmt=".", label ="threshold")
    plt.errorbar(lb - 10, ps2 * lb**2, sigma2 * lb**2, fmt=".", label ="threshold_toepliz")
    plt.legend(fontsize=25)
    plt.xlabel(r"$\ell$", fontsize=25)
    plt.ylabel(r"$\ell^{2} D_\ell$", fontsize=25)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig("%s/spectra_%s.png" % (result_dir, spec))
    plt.clf()
    plt.close()
    
    plt.figure(figsize=(15, 15))
    plt.errorbar(lb, 100 * (ps0 - ps1)/sigma0, label = "exact - thres")
    plt.errorbar(lb, 100 * (ps0 - ps2)/sigma0, label = "exact - thres_toepl")
    plt.errorbar(lb, 100 * (ps1 - ps2)/sigma0, label = "thres - thres_toepl")
    plt.legend(fontsize=25)
    plt.xlabel(r"$\ell$", fontsize=25)
    plt.ylabel(r"$\Delta C_\ell/ \sigma_\ell $ (%)", fontsize=25)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig("%s/diff_per_sigma_%s.png" % (result_dir, spec))
    plt.clf()
    plt.close()
    
    plt.figure(figsize=(15, 15))
    plt.plot(lb, 100 * (sigma0/sigma1-1), label = "exact/thres")
    plt.plot(lb, 100 * (sigma0/sigma2-1), label = "exact/thres_toepl")
    plt.plot(lb, 100 * (sigma1/sigma2-1), label = "thres/thres_toepl")
    plt.legend(fontsize=25)
    plt.xlabel(r"$\ell$", fontsize=25)
    plt.ylabel(r"ratio $\sigma_\ell$ (%)", fontsize=25)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig("%s/ratio_error_%s.png" % (result_dir, spec))
    plt.clf()
    plt.close()

