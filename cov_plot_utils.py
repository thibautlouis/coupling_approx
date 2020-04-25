import numpy as np, pylab as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
import pixell


def toepliz_plot(plot_dir, corr, name, lsplit):
    pixell.colorize.mpl_setdefault("planck")

    fig2 = plt.figure(constrained_layout=True,figsize=(15,4.5))
    spec2 = gridspec.GridSpec(ncols=3, nrows=2, figure=fig2)
    f2_ax1 = fig2.add_subplot(spec2[0:2, 0:2])
    cax = f2_ax1.matshow(corr, origin = "lower",norm=LogNorm())
    f2_ax1.xaxis.set_ticks_position('bottom')
    fig2.colorbar(cax, aspect=50)
    plt.title(r"$\xi^{%s}(\ell_{1}, \ell_{2})$" % name,fontsize=20)

    plt.xlabel(r"$\ell_{1}$",fontsize=20)
    plt.ylabel(r"$\ell_{2}$",fontsize=20)

    lmin_array=[0, lsplit]
    lmax_array=[lsplit, 10000]
    count = 0
    for lmin, lmax in zip(lmin_array,lmax_array):
        f2_ax2 = fig2.add_subplot(spec2[count, 2])

        ell_range= np.arange(lmin,lmax)
        plt.semilogy()
 
        plt.title(r"$\ell_{1} \in [%d,%d]$"%(lmin,lmax),fontsize=15)
        #plt.xlim(0,3000)
        plt.ylabel(r"$\xi^{%s}_{\ell_{1}, \ell_{1} + \Delta \ell} $" % name ,fontsize=18)
        plt.xlabel(r"$\Delta \ell$",fontsize=20)
        
        if name != "--":
            plt.yticks([1,0.0001,0.00000001])
            plt.ylim(10**-11, 1)
        else:
            plt.yticks([1, 0.01, 0.0001])
            plt.ylim(10**-6, 1)

        for ell in ell_range:
            f2_ax2.plot(corr[ell, ell:], alpha=0.3, c="steelblue")
        count +=1
    plt.savefig("%s/coupling_%s.png" % (plot_dir, name), bbox_inches="tight", dpi=300)
    plt.clf()
    plt.close()

