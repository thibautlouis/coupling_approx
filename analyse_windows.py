from pspy import so_map, so_window, so_mcm, sph_tools, pspy_utils, so_cov
import numpy as np, pylab as plt
import time

ra0, ra1, dec0, dec1 = -25, 25, -25, 25
res_arcmin = 0.5
apo_radius_degree = 1
apo_type_surey = "C1"
niter = 0
n_holes = 300
hole_radius_arcmin = 5
pts_apo_radius_degree = 0.3
pts_apo_type = "C1"
lmax = 4000


binary = so_map.car_template(1, ra0, ra1, dec0, dec1, res_arcmin)
binary.data[:] = 0
binary.data[1:-1, 1:-1] = 1
window = so_window.create_apodization(binary,
                                      apo_type=apo_type_surey,
                                      apo_radius_degree=apo_radius_degree)

#  multiply by an additional source mask
ps_mask = window.copy()
ps_mask.data[:] = 1
ps_mask = so_map.simulate_source_mask(ps_mask,
                                      n_holes,
                                      hole_radius_arcmin)
                                      
ps_mask = so_window.create_apodization(ps_mask,
                                       apo_type=pts_apo_type,
                                       apo_radius_degree=pts_apo_radius_degree)

window.data *= ps_mask.data

mcm_list = so_mcm.mcm_and_bbl_spin0and2((window, window),
                                        binning_file= "data/binning.dat",
                                        lmax=lmax,
                                        niter=niter,
                                        return_coupling_only=True)

name_list =["00", "+0", "++", "--"]
id_list = [0, 1, 3, 4]
mcm_dict = {}
for id_mcm, name in zip(id_list, name_list):
    mcm_dict[name] = mcm_list[id_mcm]
    corr = so_cov.cov2corr(mcm_dict[name], remove_diag=False)
    plt.matshow(np.log(corr))
    plt.title(name)
    plt.show()
    
    ell_range= np.arange(2000,4000)
    plt.semilogy()
    for ell in ell_range:
        plt.plot(corr[ell,ell:])
    plt.show()

    
mcm_pol = np.block([[mcm_dict["++"], mcm_dict["--"]], [mcm_dict["--"], mcm_dict["++"]]])
corr = so_cov.cov2corr(mcm_pol, remove_diag=False)
plt.matshow(np.log(corr))
plt.title(name)
plt.show()


plt.semilogy()
for ell in ell_range:
    plt.plot(corr[ell,ell:])
plt.show()
