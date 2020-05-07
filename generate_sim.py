from pspy import  so_dict, so_map, pspy_utils
import numpy as np
import sys

d = so_dict.so_dict()
d.read_from_file(sys.argv[1])

n_sims = d["n_sims"]
beamed_clfile = d["beamed_clfile"]
res_arcmin = d["res_arcmin"]
name_split = d["name_split"]
n_splits = d["n_splits"]
rms_uKarcmin_T = d["rms_uKarcmin_T"] * np.sqrt(n_splits)
ra0, ra1, dec0, dec1 = d["ra0"], d["ra1"], d["dec0"], d["dec1"]
run_name = d["run_name"]

sim_dir = "sims_%s" % run_name
pspy_utils.create_directory(sim_dir)

eps = 1
template_car = so_map.car_template(3, ra0 - eps, ra1 + eps, dec0 - eps, dec1 + eps, res_arcmin)

for iii in range(n_sims):
    print("generate sim %03d"%iii)
    cmb = template_car.synfast(beamed_clfile)
    for i in range(n_splits):
        name = "sim_%03d_%s%d" % (iii, name_split, i)
        split = cmb.copy()
        noise = so_map.white_noise(split, rms_uKarcmin_T=rms_uKarcmin_T)
        split.data += noise.data
        split.write_map("%s/%s.fits" % (sim_dir, name))
        split.plot(file_name="%s/%s" % (sim_dir, name))

    
