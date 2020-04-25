import numpy as np, pylab as plt


l, bl =np.loadtxt("beam_LAT_93.dat", unpack=True)
clth = {}
lth, clth["TT"], clth["EE"], clth["BB"], clth["TE"] = np.loadtxt("cosmo_spectra_and_fg.dat", unpack=True)
bl = bl[2:len(lth)+2]

fields = ["TT", "EE", "BB", "TE"]
for field in fields:
    clth[field] *= bl**2

np.savetxt("cosmo_spectra_and_fg_beam_LAT93.dat", np.transpose([lth,  clth["TT"], clth["EE"], clth["BB"], clth["TE"]]))
