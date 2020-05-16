import numpy as np
import pylab as plt
from pspy import so_cov
import pixell
import matplotlib
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


pixell.colorize.mpl_setdefault("planck")

elements = np.load("coupling_baseline/element_computed.npy")
approx = np.load("coupling_baseline/coupling_800_2000_2750_00.npy")

myelements = elements.copy()
myelements = myelements*0+1
id = np.where(elements == 0)
myelements[id] =-1

top = cm.get_cmap('Oranges_r', 128)
bottom = cm.get_cmap('Blues', 128)

newcolors = np.vstack((top(np.linspace(0.8, 1, 128)),
                       bottom(np.linspace(0, 0.6, 128))))
newcmp = ListedColormap(newcolors, name='OrangeBlue')


l_toep = 2750
l_band = 2000
l_exact = 800
l_max = 10000

fig2 = plt.figure(figsize=(23,23))
f2_ax1 = fig2.add_subplot()
f2_ax1.matshow(myelements, interpolation='nearest',cmap=newcmp)
plt.xlabel(r"$\ell_{2}$",fontsize=50)
plt.ylabel(r"$\ell_{1}$",fontsize=50)

plt.annotate ('', (l_toep + 40, l_toep), (l_toep +40 , (l_toep+l_band)), arrowprops={'arrowstyle':'<->'})
plt.annotate( r'$\Delta \ell_{\rm band}$', xy=(l_toep + 40, (2*l_toep+l_band)/2), xycoords='data', xytext=(5, 0), textcoords='offset points',fontsize=50)

plt.annotate( r'$\ell_{\rm toepliz}$', xy=(l_toep, l_max), xycoords='data', xytext=(10, 10), textcoords='offset points',fontsize=50)
plt.annotate( r'$\ell_{\rm exact}$', xy=(l_exact, l_max), xycoords='data', xytext=(10, 10), textcoords='offset points',fontsize=50)
f2_ax1.autoscale(False)
#x = np.arange(l_toep, l_max-l_band)
#y= l_band + x
#f2_ax1.plot(x,y,color = "red", alpha = 0.5, linestyle ="--")
plt.xticks(fontsize=50)
plt.yticks(fontsize=50)

#plt.show()
plt.savefig("elements.png", bbox_inches="tight")
plt.clf()
plt.close()
