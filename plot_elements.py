import numpy as np
import pylab as plt
from pspy import so_cov

elements = np.load("coupling/element_computed.npy")



l_toep = 2500
l_band = 2000
l_exact = 800
l_max = 10000

fig2 = plt.figure(figsize=(23,23))
f2_ax1 = fig2.add_subplot()
f2_ax1.matshow(np.log(elements), origin = "lower", cmap="coolwarm", interpolation='nearest')
plt.xlabel(r"$\ell_{1}$",fontsize=35)
plt.ylabel(r"$\ell_{2}$",fontsize=35)

f2_ax1.xaxis.set_ticks_position('bottom')
plt.annotate ('', (l_toep + 40, l_toep), (l_toep +40 , (l_toep+l_band)), arrowprops={'arrowstyle':'<->'})
plt.annotate( r'$\Delta \ell_{\rm band}$', xy=(l_toep + 40, (2*l_toep+l_band)/2), xycoords='data', xytext=(5, 0), textcoords='offset points',fontsize=25)

plt.annotate( r'$\ell_{\rm toepliz}$', xy=(l_toep, l_max), xycoords='data', xytext=(0, 5), textcoords='offset points',fontsize=25)
plt.annotate( r'$\ell_{\rm exact}$', xy=(l_exact, l_max), xycoords='data', xytext=(0, 5), textcoords='offset points',fontsize=25)
f2_ax1.autoscale(False)
#x = np.arange(l_toep, l_max-l_band)
#y= l_band + x
#f2_ax1.plot(x,y,color = "red", alpha = 0.5, linestyle ="--")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)


plt.savefig("elements.png", bbox_inches="tight")
plt.clf()
plt.close()
