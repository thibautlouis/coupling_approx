from pspy import so_cov
import numpy as np, pylab as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
import pixell


def toepliz_plot(plot_dir, corr, name, lsplit):
    pixell.colorize.mpl_setdefault("planck")

    fig2 = plt.figure(constrained_layout=True,figsize=(15,4.5))
    spec2 = gridspec.GridSpec(ncols=3, nrows=2, figure=fig2)
    f2_ax1 = fig2.add_subplot(spec2[0:2, 0:2])
    cax = f2_ax1.matshow(corr, norm=LogNorm())
    
    cb = plt.colorbar(cax, aspect=50)
    cb.ax.tick_params(labelsize=16)


  #  fig2.colorbar(cax, aspect=50)
    plt.title(r"$\xi^{%s}(\ell_{1}, \ell_{2})$" % name,fontsize=17, pad=15)

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    plt.xlabel(r"$\ell_{2}$", fontsize=20)
    plt.ylabel(r"$\ell_{1}$", fontsize=20)

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
            
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=14)

        count +=1
    plt.savefig("%s/coupling_%s.png" % (plot_dir, name), bbox_inches="tight", dpi=300)
    plt.clf()
    plt.close()


def residual_plot(plot_dir, coupling_dir, clfile, lmax, vmax):
    pixell.colorize.mpl_setdefault("planck")
    
    def format_toepliz(coupling, l_toep, lmax):
        """take a matrix and apply the toepliz appoximation
        Parameters
        ----------

        toepliz_array: array
        consist of an array where the upper part is the exact matrix and
        the lower part is the diagonal. We will feed the off diagonal
        of the lower part using the measurement of the correlation from the exact computatio
        l_toep: integer
        the l at which we start the approx
        lmax: integer
        the maximum multipole of the array

        """

        toepliz_array = coupling.copy()*0
        diag = np.sqrt(np.diag(coupling))
        corr= so_cov.cov2corr(coupling, remove_diag=False)

        for ell in range(0, l_toep - 2):
            toepliz_array[ell: ell + lmax - (l_toep - 2), ell] = corr[l_toep - 2:lmax, l_toep - 2]
        for ell in range(l_toep - 2, lmax):
            pix = ell - (l_toep - 2)
            toepliz_array[ell:, ell] = corr[l_toep - 2:lmax - pix, l_toep - 2]
    
        toepliz_array = toepliz_array * np.outer(diag, diag)
        toepliz_array = toepliz_array + toepliz_array.T - np.diag(np.diag(toepliz_array))

        return toepliz_array


    def toeplitz(coupling, lmax):
        toepliz_array = coupling.copy() * 0
        diag = np.sqrt(np.diag(coupling))
        corr= so_cov.cov2corr(coupling, remove_diag=False)
        last_column = corr[:, lmax - 1]
    
        for ell in range(lmax):
            toepliz_array[:ell + 1, ell]= last_column[lmax - 1 - ell:lmax]
        
        toepliz_array = toepliz_array * np.outer(diag, diag)
        toepliz_array = toepliz_array + toepliz_array.T - np.diag(np.diag(toepliz_array))
    
        return toepliz_array
    
    cl = {}
    l, cl["TT"], cl["EE"], cl["BB"], cl["TE"] = np.loadtxt(clfile,unpack=True)
    l= l[:lmax]
    spectra = ["TT", "EE", "BB", "TE"]
    
    for spec in spectra:
        cl[spec] = cl[spec][:lmax] * 2 * np.pi / ( l * ( l + 1 ))
        
    coupling_terms = ["00", "++", "++", "02"]
    
    for c_term, spec in zip(coupling_terms,spectra):
    
        coupling = np.load("%s/coupling_exact_%s.npy"%(coupling_dir,c_term))
        coupling = coupling[:lmax,:lmax]
        pseudo_cl = np.dot(coupling, cl[spec] * (2 * l + 1) / (4*np.pi))
        fac_l2 = np.tile(cl[spec] * ((2 * l + 1)) /(4*np.pi), (lmax, 1))
        pseudo_cl1 =  np.transpose(np.tile(pseudo_cl, (lmax, 1)))
        toepliz_array =  toeplitz(coupling, lmax)
        residual = np.abs(coupling - toepliz_array) * fac_l2 / pseudo_cl1
        fig = plt.figure(figsize=(9, 9))
        plt.title(r"$ |\Xi^{%s}_{\rm exact} - \Xi^{%s}_{\rm toeplitz} |_{\ell_{1}\ell_{2}}  (2\ell_{2} + 1) C^{%s}_{\ell_2} /\tilde{C}^{%s}_{\ell_1} $" % (c_term,c_term,spec,spec),
                  fontsize=22, pad= 25)
        ax = fig.gca()
        im = ax.matshow(residual, vmax=vmax, vmin=0, cmap='Greys')
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)

        plt.xlabel(r"$\ell_{2}$", fontsize=22)
        plt.ylabel(r"$\ell_{1}$", fontsize=22)
        
        cb = plt.colorbar(im, pad=0.15, format="%.0e", shrink = 0.8)
        cb.ax.tick_params(labelsize=20)

        #fig.colorbar(im
        plt.savefig("%s/residual_%s.png" % (plot_dir, spec), bbox_inches="tight", dpi=300)
        plt.clf()
        plt.close()

    
