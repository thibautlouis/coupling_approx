import numpy as np
from pspy import so_dict
import sys, os
from copy import deepcopy

def update_dict2(dict, keys_boost, new_factor, name):

    updated_dict = deepcopy(dict)
    updated_dict[keys_boost] = [new_factor, None]
        
    g = open("global%s.dict" % name , mode="w")
    g.write("run_name = '%s' \n" % (dict["run_name"] + name))
    for key in dict:
        if key == "run_name": continue
        if isinstance(updated_dict[key],str):
            g.write("%s = '%s' \n" % (key, updated_dict[key]))
        else:
            g.write("%s = %s \n" % (key, updated_dict[key]))

    g.close()
    
d = so_dict.so_dict()
d.read_from_file(sys.argv[1])

new_fac = np.linspace(2200, 3500, 5).astype(int)
for boost in new_fac:
    new_name = "_toeplitz%s" % boost
    update_dict2(d, "l_toep_array", boost, name=new_name)
    os.system("python generate_sim.py global%s.dict" % new_name)
    os.system("python generate_window.py global%s.dict" % new_name)
    os.system("python compute_spectra.py global%s.dict" % new_name)
    os.system("python plot_spectra.py global%s.dict" % new_name)
