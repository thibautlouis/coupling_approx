import pylab as plt, numpy as np
from pspy import so_dict, pspy_utils
import sys
import pickle





d = so_dict.so_dict()
d.read_from_file(sys.argv[1])

plot_dir = "plot"
pspy_utils.create_directory(plot_dir)



run_name = d["run_name"]
id_sim =  d["id_sim"]
lmax = d["lmax"]

this_run = "source"
#this_run = "size"
this_run = "toeplitz"
#this_run = "noise"
this_run = "band"
#this_run = "exact"

l_exact_array = d["l_exact_array"]
l_band_array = d["l_band_array"]
l_toep_array = d["l_toep_array"]
cross ="sim_%03d_split0xsim_%03d_split1"%(id_sim, id_sim)
l_lo, l_hi, lb, delta_l = pspy_utils.read_binning_file( "data/binning.dat", lmax)


result_ps = {}
result_cov = {}

if this_run == "source":
    boost_fac = np.linspace(1, 2.5, 5)
if this_run == "size":
    boost_fac = np.linspace(1, 3, 5)
if this_run == "noise":
    boost_fac = np.linspace(1, 5, 5)
if this_run == "toeplitz":
    boost_fac = np.linspace(2200, 3500, 5).astype(int)
if this_run == "band":
    boost_fac = np.linspace(1000, 2200, 5).astype(int)
if this_run == "exact":
    boost_fac = np.linspace(200, 1000, 5).astype(int)


for count1, boost in enumerate(boost_fac):
    if this_run == "source":
        new_name = "_sourcex%s" % boost
    if this_run == "size":
        new_name = "_sizex%s" % boost
    if this_run == "noise":
        new_name = "_noise%s" % boost
    if this_run == "toeplitz":
        new_name = "_toeplitz%s" % boost
    if this_run == "band":
        new_name = "_band%s" % boost
    if this_run == "exact":
        new_name = "_exact%s" % boost

    
    spectra_dir = "spectra_%s%s" % (run_name, new_name)
    print(spectra_dir)
    test_names = []
    for l_exact, l_band, l_toep in zip(l_exact_array, l_band_array, l_toep_array):

        if (l_exact == None) & (l_toep == None) & (l_band == None):
            test = "exact"
        else:
            if this_run == "toeplitz":
                test = "%d_%d_%d"%(l_exact, l_band, boost)
            elif this_run == "band":
                test = "%d_%d_%d"%(l_exact, boost, l_toep)
            elif this_run == "exact":
                test = "%d_%d_%d"%(boost, l_band, l_toep)

            else:
                test = "%d_%d_%d"%(l_exact, l_band, l_toep)

        pkl_file = open("%s/ps_dict_%s_%03d.pkl" % (spectra_dir, test, d["id_sim"]), "rb")
        ps_dict = pickle.load(pkl_file)
        pkl_file.close()
        
        pkl_file = open("%s/cov_dict_%s_%03d.pkl" % (spectra_dir, test, d["id_sim"]), "rb")
        cov_dict = pickle.load(pkl_file)
        pkl_file.close()

        result_ps[boost, test] = ps_dict
        result_cov[boost, test] = cov_dict
        test_names += [test]
        
    test_names.remove("exact")
    

color_array = ["blue", "orange", "green", "red", "purple", "brown"]
specs = ["TT", "TE", "EE", "BB", "TB", "EB"]
fmt_array = ["-", "--", "-.", ".", "*"]


from matplotlib.patches import Patch
from matplotlib.lines import Line2D


#legend_elements = [Line2D([0], [0], color='black', linestyle="-", label=r"$f^{\rm baseline}_{\rm sky}$ x $1^{2}$"),
#                   Line2D([0], [0], color='black', linestyle="--", label=r"$f^{\rm baseline}_{\rm sky}$ x $1.5^{2}$"),
#                   Line2D([0], [0], color='black', linestyle="-.", label=r"$f^{\rm baseline}_{\rm sky}$ x $2^{2}$"),
#                   Line2D([0], [0], color='black', linestyle="", marker= ".",  label=r"$f^{\rm baseline}_{\rm sky}$ x $2.5^{2}$"),
#                   Line2D([0], [0], color='black', linestyle="", marker= "*", label=r"$f^{\rm baseline}_{\rm sky}$ x $3^{2}$")]
if this_run == "source":
    my_label = [r"$\rho$ x $1$",
                r"$\rho$ x $1.375$",
                r"$\rho$ x $1.75$",
                r"$\rho$ x $2.125$",
                r"$\rho$ x $2.5$"]
if this_run == "size":
    my_label = [r"$f_{\rm sky}$ x $1^{2}$",
                r"$f_{\rm sky}$ x $1.5^{2}$",
                r"$f_{\rm sky}$ x $2^{2}$",
                r"$f_{\rm sky}$ x $2.5^{2}$",
                r"$f_{\rm sky}$ x $3^{2}$"]
if this_run == "toeplitz":
    my_label = [r"$\ell_{\rm toeplitz} = 2200$ (t = 27.3 s)",
                r"$\ell_{\rm toeplitz} = 2525$ (t = 30.5 s)",
                r"$\ell_{\rm toeplitz} = 2850$ (t = 34.2 s)",
                r"$\ell_{\rm toeplitz} = 3125$ (t = 38.2 s)",
                r"$\ell_{\rm toeplitz} = 3500$ (t = 42.6 s)"]
                
if this_run == "band":
    my_label = [r"$\ell_{\rm band} = 1000$ (t = 26.5 s)",
                r"$\ell_{\rm band} = 1300$ (t = 28.3 s)",
                r"$\ell_{\rm band} = 1600$ (t = 30.7 s)",
                r"$\ell_{\rm band} = 1900$ (t = 32.9 s)",
                r"$\ell_{\rm band} = 2200$ (t = 34.9 s)"]
if this_run == "exact":
    my_label = [r"$\ell_{\rm exact} = 200$ (t = 28.0 s)",
                r"$\ell_{\rm exact} = 400$ (t = 28.8 s)",
                r"$\ell_{\rm exact} = 600$ (t = 30.4 s)",
                r"$\ell_{\rm exact} = 800$ (t = 32.9 s)",
                r"$\ell_{\rm exact} = 1000$ (t = 35.6 s)"]
                
if this_run == "noise":
    my_label = [r"$\sigma_{\rm pol} = 1 \mu K \cdot$ arcmin ",
                r"$\sigma_{\rm pol} = 2 \mu K \cdot$ arcmin ",
                r"$\sigma_{\rm pol} = 3 \mu K \cdot$ arcmin ",
                r"$\sigma_{\rm pol} = 4 \mu K \cdot$ arcmin ",
                r"$\sigma_{\rm pol} = 5 \mu K \cdot$ arcmin "]




legend_elements = [Line2D([0], [0], color='black', linestyle="-", label=my_label[0]),
                   Line2D([0], [0], color='black', linestyle="--", label=my_label[1]),
                   Line2D([0], [0], color='black', linestyle="-.", label=my_label[2]),
                   Line2D([0], [0], color='black', linestyle="", marker= ".",  label=my_label[3]),
                   Line2D([0], [0], color='black', linestyle="", marker= "*", label=my_label[4])]



# Create the figure
fig, ax = plt.subplots(figsize=(15, 15))


for color,spec in zip(color_array,specs):
    cc = 0
    for fmt, boost in zip(fmt_array, boost_fac):

        ps_exact_boost, sigma_exact_boost = result_ps[boost,"exact"][cross][spec], np.sqrt(np.diag(result_cov[boost,"exact"][cross][spec]))
        
        
        
        if this_run == "toeplitz":
            test_names = ["800_2000_%d" % boost]
        if this_run == "band":
            test_names = ["800_%d_2750" % boost]
        if this_run == "exact":
            test_names = ["%d_2000_2750" % boost]

        for count,test in enumerate(test_names):
            ps_boost, sigma_boost = result_ps[boost,test][cross][spec], np.sqrt(np.diag(result_cov[boost,test][cross][spec]))
            
            frac_boost = np.abs(ps_boost - ps_exact_boost)/sigma_exact_boost

            
            if cc == 0:
                plt.errorbar(lb,
                            frac_boost,
                            label = "%s" % (spec),
                            color=color,
                            fmt=fmt)
            else:
                plt.errorbar(lb,
                            frac_boost,
                            color=color,
                            fmt=fmt)

            cc += 1
        leg1 = ax.legend(fontsize=30, frameon=False)
        
        
if this_run == "source":
    leg2 = ax.legend(handles=legend_elements, loc='upper left',fontsize=25, frameon=False)
    plt.ylim(0, 0.01)
if this_run == "size":
    leg2 = ax.legend(handles=legend_elements, loc='upper left',fontsize=25, frameon=False)
    plt.ylim(0, 0.01)
if this_run == "toeplitz":
    leg2 = ax.legend(handles=legend_elements, loc='upper left',fontsize=22.5, frameon=False)
    plt.ylim(0, 0.02)
if this_run == "noise":
    leg2 = ax.legend(handles=legend_elements, loc='upper left',fontsize=22.5, frameon=False)
    plt.ylim(0, 0.02)
if this_run == "band":
    leg2 = ax.legend(handles=legend_elements, loc='upper left',fontsize=22.5, frameon=False)
    plt.ylim(0, 0.03)
if this_run == "exact":
    leg2 = ax.legend(handles=legend_elements, loc='upper left',fontsize=22.5, frameon=False)
    plt.ylim(0, 0.02)


ax.add_artist(leg1)
plt.xlabel(r"$\ell$", fontsize=40)
plt.ylabel(r"$|\Delta D_{\ell}|/\sigma(D_{\ell})$", fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
if this_run == "source":
    plt.savefig("%s/StoN_all_test_source.png" % (plot_dir), bbox_inches="tight")
if this_run == "size":
    plt.savefig("%s/StoN_all_test_size.png" % (plot_dir), bbox_inches="tight")
if this_run == "toeplitz":
    plt.savefig("%s/StoN_all_test_toeplitz.png" % (plot_dir), bbox_inches="tight")
if this_run == "band":
    plt.savefig("%s/StoN_all_test_band.png" % (plot_dir), bbox_inches="tight")
if this_run == "exact":
    plt.savefig("%s/StoN_all_test_exact.png" % (plot_dir), bbox_inches="tight")
if this_run == "noise":
    plt.savefig("%s/StoN_all_test_noise.png" % (plot_dir), bbox_inches="tight")

plt.clf()
plt.close()
