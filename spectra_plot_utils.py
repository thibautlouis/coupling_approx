import numpy as np, pylab as plt


def plot_spectra_comparison(lb, result_ps, result_cov, cross, spectra, test_names, plot_dir, lth, clth, lmid=6000):

    plt.figure(figsize=(25, 20))

    count = 1
    
    spectra_names = "spectra"
    for spec in spectra:
    
        spectra_names += "_%s"%spec

        ps_exact, sigma_exact = result_ps["exact"][cross][spec], np.sqrt(np.diag(result_cov["exact"][cross][spec]))
 
        lmin_array = [0, lmid]
        lmax_array = [lmid, 10000]
        label_array = ["low_ell", "high_ell" ]
        if spec == "TT" or spec == "TE":
            fac_array = [2, 0]
        elif spec == "BB":
            fac_array = [0, 0]
        elif spec == "EE":
            fac_array = [1, 0]
        else:
            fac_array = [0, 0]
 
        for lmin, lmax, label, fac in zip(lmin_array, lmax_array, label_array, fac_array):
            clth_select = clth[spec].copy()[lmin:lmax]
            lth_select = lth.copy()[lmin:lmax]
     
            id = np.where((lb > lmin) & (lb < lmax))
     
            lb_select = lb.copy()[id]
            ps_exact_select = ps_exact.copy()[id]
            sigma_exact_select = sigma_exact.copy()[id]

            plt.subplot(3, 2, count)
            
            if count == 1:
                plt.title("$\ell$ < %d" % lmid, fontsize=30)
            elif count == 2:
                 plt.title("$\ell$ > %d" % lmid, fontsize=30)

            if label == "high_ell":
                plt.xticks([6000,7000,8000,9000,10000])
            plt.plot(lth_select, clth_select * lth_select**fac, color = "grey")
     
     
            plt.errorbar(lb_select - 15,
                         ps_exact_select * lb_select**fac,
                         sigma_exact_select * lb_select**fac,
                         fmt=".",
                         label ="exact",
                         color = "darkorange")
                         
            for test in test_names:
                ps, sigma = result_ps[test][cross][spec], np.sqrt(np.diag(result_cov[test][cross][spec]))
                ps_select = ps.copy()[id]
                sigma_select = sigma.copy()[id]

                l_exact, l_band, l_toep = test.split("_")
         
                plt.errorbar(lb_select +  15,
                            ps_select * lb_select**fac,
                            sigma_select * lb_select**fac,
                            fmt=".",
                            label = "Toeplitz approximation",
                            color = "steelblue")
     
                if count >4:
                    plt.xlabel(r"$\ell$", fontsize=35)
                plt.ylabel(r"$\ell^{%d} D^{%s}_\ell [\mu K]^{2}$"  % (fac,spec), fontsize=35)
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
            if count==2:
                plt.legend(fontsize=25, loc = "upper left", frameon = False)
            count += 1

    plt.savefig("%s/%s.pdf" % (plot_dir, spectra_names), bbox_inches="tight")
    plt.clf()
    plt.close()
    


def delta_Cl_over_sigma(lb, result_ps, result_cov, cross, spectra, test_names, plot_dir):

    plt.figure(figsize=(15, 15))
    plt.semilogy()
    for spec in ["TT", "TE", "EE", "BB", "TB", "EB"]:
        ps_exact, sigma_exact = result_ps["exact"][cross][spec], np.sqrt(np.diag(result_cov["exact"][cross][spec]))


        for count,test in enumerate(test_names):
            ps, sigma = result_ps[test][cross][spec], np.sqrt(np.diag(result_cov[test][cross][spec]))
            l_exact, l_band, l_toep = test.split("_")
            plt.errorbar(lb,
                         np.abs(ps - ps_exact)/sigma_exact,
                         label = "%s" % spec)

    plt.ylim(10**-6, 1)
    plt.legend(fontsize=30, frameon=False)
    plt.xlabel(r"$\ell$", fontsize=40)
    plt.ylabel(r"$|\Delta D_{\ell}|/\sigma(D_{\ell})$", fontsize=40)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig("%s/diff_per_sigma_all.png" % (plot_dir), bbox_inches="tight")
    plt.clf()
    plt.close()


def cov_plot(lb,  result_cov, cross, spectra, test_names, plot_dir):

    plt.figure(figsize=(15, 15))
    plt.semilogy()
    for spec in ["TT", "TE", "EE", "BB", "TB", "EB"]:
        cov_exact  =  result_cov["exact"][cross][spec]
        std_exact = np.sqrt(np.diag(cov_exact))

        for count,test in enumerate(test_names):
            cov = result_cov[test][cross][spec]
            std = np.sqrt(np.diag(cov))

            plt.errorbar(lb,
                        np.abs(std - std_exact)/std_exact,
                        label = "%s" % spec)

    plt.legend(fontsize=30, frameon=False)
    plt.xlabel(r"$\ell$", fontsize=40)
    plt.ylabel(r"$|\Delta \sigma(D_{\ell})|/\sigma(D_{\ell})$", fontsize=40)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.ylim(10**-5, 0.1)

    plt.savefig("%s/sigma_all.png" % (plot_dir), bbox_inches="tight")
    plt.clf()
    plt.close()
