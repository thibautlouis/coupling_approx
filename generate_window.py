import numpy as np
from pspy import pspy_utils, so_map, so_window, so_dict
import ps_tools
import sys

d = so_dict.so_dict()
d.read_from_file(sys.argv[1])

window_dir = "window"
pspy_utils.create_directory(window_dir)

ra0, ra1, dec0, dec1 = d["ra0"], d["ra1"], d["dec0"], d["dec1"]

patch = {"patch_type": "Rectangle",
         "patch_coordinate": [[dec0, ra0], [dec1, ra1]]}
         
sim_dir = "sims"
maps_info_list = []
for i in range(d["n_splits"]):
    name = "sim_%03d_%s%d" % (d["id_sim"], d["name_split"], i)
    maps_info_list += [{"name":"%s/%s.fits" % (sim_dir, name), "data_type":"IQU", "id":name, "cal": None}]

print("generate window")
car_box, window = ps_tools.create_window(patch,
                                         maps_info_list,
                                         d["apo_radius_survey_degree"],
                                         d["res_arcmin"],
                                         compute_T_only=d["compute_T_only"])
                                       
#  multiply by an additional source mask

nholes_degsq = d["nholes_degsq"]
hole_radius_arcmin = d["hole_radius_arcmin"]
apo_radius_degree_pts_source = d["apo_radius_degree_pts_source"]


n_holes = int((ra1 - ra0) * (dec1 - dec0) * nholes_degsq)
ps_mask = window.copy()
ps_mask.data[:] = 1
ps_mask = so_map.simulate_source_mask(ps_mask, n_holes, hole_radius_arcmin)
ps_mask = so_window.create_apodization(ps_mask, apo_type="C1", apo_radius_degree=apo_radius_degree_pts_source)
window.data *= ps_mask.data

window.write_map("%s/window.fits" % (window_dir))
window.plot(file_name="%s/window"%(window_dir))
np.savetxt("%s/car_box.dat"%(window_dir), car_box)



