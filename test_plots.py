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

#this_run = "source"
#this_run = "size"
this_run = "toeplitz"

l_exact_array = d["l_exact_array"]
l_band_array = d["l_band_array"]
l_toep_array = d["l_toep_array"]
cross ="sim_%03d_split0xsim_%03d_split1"%(id_sim, id_sim)
l_lo, l_hi, lb, delta_l = pspy_utils.read_binning_file( "data/binning.dat", lmax)


result_ps = {}
result_cov = {}

if this_run == "source" or this_run == "size":
    boost_fac = np.linspace(1, 3, 5)
else:
    boost_fac = np.linspace(2000, 3500, 5).astype(int)


for count1, boost in enumerate(boost_fac):
    if this_run == "source":
        new_name = "_sourcex%s" % boost
    elif this_run == "size":
        new_name = "_sizex%s" % boost
    elif this_run == "toeplitz":
        new_name = "_toeplitz%s" % boost

    
    spectra_dir = "spectra_%s%s" % (run_name, new_name)
    print(spectra_dir)
    test_names = []
    for l_exact, l_band, l_toep in zip(l_exact_array, l_band_array, l_toep_array):

        if (l_exact == None) & (l_toep == None) & (l_band == None):
            test = "exact"
        else:
            if this_run == "toeplitz":
                test = "%d_%d_%d"%(l_exact, l_band, boost)
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
    

color_array = ["blue", "orange", "green"]
specs = ["TT", "TE", "EE"]
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
                r"$\rho$ x $1.5$",
                r"$\rho$ x $2$",
                r"$\rho$ x $2.5$",
                r"$\rho$ x $3$"]
elif this_run == "size":
    my_label = [r"$f_{\rm sky}$ x $1^{2}$",
                r"$f_{\rm sky}$ x $1.5^{2}$",
                r"$f_{\rm sky}$ x $2^{2}$",
                r"$f_{\rm sky}$ x $2.5^{2}$",
                r"$f_{\rm sky}$ x $3^{2}$"]
elif this_run == "toeplitz":
    my_label = [r"$\ell_{\rm toeplitz} = 2000$ ",
                r"$\ell_{\rm toeplitz} = 2375$ ",
                r"$\ell_{\rm toeplitz} = 2750$ ",
                r"$\ell_{\rm toeplitz} = 3125$ ",
                r"$\ell_{\rm toeplitz} = 3500$ "]




legend_elements = [Line2D([0], [0], color='black', linestyle="-", label=my_label[0]),
                   Line2D([0], [0], color='black', linestyle="--", label=my_label[1]),
                   Line2D([0], [0], color='black', linestyle="-.", label=my_label[2]),
                   Line2D([0], [0], color='black', linestyle="", marker= ".",  label=my_label[3]),
                   Line2D([0], [0], color='black', linestyle="", marker= "*", label=my_label[4])]



# Create the figure
fig, ax = plt.subplots(figsize=(15, 15))


for color,spec in zip(color_array,specs):
    for fmt, boost in zip(fmt_array, boost_fac):

        ps_exact_boost, sigma_exact_boost = result_ps[boost,"exact"][cross][spec], np.sqrt(np.diag(result_cov[boost,"exact"][cross][spec]))
        
        
        
        if this_run == "toeplitz":
            test_names = ["800_2000_%d" % boost]
        for count,test in enumerate(test_names):
            ps_boost, sigma_boost = result_ps[boost,test][cross][spec], np.sqrt(np.diag(result_cov[boost,test][cross][spec]))
            
            frac_boost = np.abs(ps_boost - ps_exact_boost)/sigma_exact_boost

            
            if boost ==1 or boost == 2000:
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


        leg1 = ax.legend(fontsize=30, frameon=False)
        
        
if this_run == "source":
    leg2 = ax.legend(handles=legend_elements, loc='upper left',fontsize=25, frameon=False)
    plt.ylim(0, 0.01)
elif this_run == "size":
    leg2 = ax.legend(handles=legend_elements, loc='upper left',fontsize=25, frameon=False)
    plt.ylim(0, 0.01)
elif this_run == "toeplitz":
    leg2 = ax.legend(handles=legend_elements, loc='upper left',fontsize=22.5, frameon=False)
    plt.ylim(0, 0.03)


ax.add_artist(leg1)
plt.xlabel(r"$\ell$", fontsize=40)
plt.ylabel(r"$|\Delta D_{\ell}|/\sigma(D_{\ell})$", fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
if this_run == "source":
    plt.savefig("%s/sigma_all_test_source.png" % (plot_dir), bbox_inches="tight")
elif this_run == "size":
    plt.savefig("%s/sigma_all_test_size.png" % (plot_dir), bbox_inches="tight")
elif this_run == "toeplitz":
    plt.savefig("%s/sigma_all_test_toeplitz.png" % (plot_dir), bbox_inches="tight")

plt.clf()
plt.close()

