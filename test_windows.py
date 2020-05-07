import numpy as np
from pspy import so_dict
import sys, os
from copy import deepcopy

def update_dict(dict, keys_boost, boost_factor, name):
    updated_dict = deepcopy(dict)
    for key in dict:
        if key in keys_boost:
            updated_dict[key] *= boost_factor
        
    g = open("global%s.dict" % name , mode="w")
    g.write("run_name = %s \n" % (dict["run_name"] + name))
    for key in dict:
        if key == "run_name": continue
        g.write("%s = %s \n" % (key,updated_dict[key]))
    g.close()

    
d = so_dict.so_dict()
d.read_from_file(sys.argv[1])

boost_fac = np.linspace(1, 3, 5)
for boost in boost_fac:
    new_name = "_sizex%s" % boost
    update_dict(d, ["ra0","ra1","dec0","dec1"], boost, name=new_name)
    os.system("python generate_sim.py global%s.dict" % new_name)
    os.system("python generate_window.py global%s.dict" % new_name)
    os.system("python compute_spectra.py global%s.dict" % new_name)
    os.system("python plot_spectra.py global%s.dict" % new_name)
