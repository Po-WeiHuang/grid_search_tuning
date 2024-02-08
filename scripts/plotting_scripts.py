import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm

def setup_plot_style():
    matplotlib.rcParams.update({'font.size': 12})
    matplotlib.rcParams.update({'font.style': "normal", 'font.family': 'serif'})
    matplotlib.rcParams['xtick.major.size'] = 10
    matplotlib.rcParams['xtick.major.width'] = 2
    matplotlib.rcParams['xtick.minor.size'] = 5
    matplotlib.rcParams['xtick.minor.width'] = 1
    matplotlib.rcParams['ytick.major.size'] = 10
    matplotlib.rcParams['ytick.major.width'] = 2
    matplotlib.rcParams['ytick.minor.size'] = 5
    matplotlib.rcParams['ytick.minor.width'] = 1
    matplotlib.rcParams['axes.linewidth'] = 2  # set the value globally
    matplotlib.rcParams['figure.facecolor'] = 'white'
    matplotlib.rcParams['figure.figsize'] = 18, 10
    matplotlib.rcParams['xtick.major.pad'] = '12'
    matplotlib.rcParams['ytick.major.pad'] = '12'
    font_filepath = "/home/hunt-stokes/LiberationSerif-Regular.ttf"

    return fm.FontProperties(fname=font_filepath, size=28)
#prop_font = setup_plot_style()

def initial_comparison(isotope, FV, E_LOW, E_HIGH):
    """
    Compare initial RAT configuration for a given ISOTOPE and the tagged Bi214 or Po214 residuals.
    """

    #data = np.load(f"detector_data/{isotope}_{FV}mmFV_{E_LOW}MeV_{E_HIGH}MeV_data_residuals3.npy")
    data = np.load("/data/snoplus3/hunt-stokes/2p2gL_optics/results/bi214_4m_residuals.npy")
    #mc = np.load(f"residuals/Po214/1/4.0_15.0_0.5_0.5.npy")
    mc = np.load("/data/snoplus3/hunt-stokes/2p2gL_optics/beta_tuning2/tRes/t4_1/425_residualsRECON.npy")
    num_data_events = print(f"Num in Data: {len(data)}")
    #data = np.concatenate(data) # data generated event by event so need to roll into 1
    # mc   = np.load(f"residuals/init_{isotope}/1/init_config.npy")

    print(f"Num tres in Data: {len(data)}\nNum tRes in MC: {len(mc)}")
    # mc2  = np.load(f"residuals/init_{isotope}/1/init_config2.npy")
    # mc = mc.tolist() + mc2.tolist()
    binWidth = 2
    binning = np.arange(-5, 100, binWidth)
    plt.hist(data, bins = binning, density = True, histtype = "step", label = f"Data | FV: {FV/1000} m | {isotope}", color = "black")
    plt.hist(mc, bins = binning, density = True, histtype = "step", label = f"RAT 7.0.8 | FV: {FV/1000} m | {isotope}", color = "blue")

    # errors on histogram
    counts_data, _    = np.histogram(data, bins = binning)
    counts_mc, _      = np.histogram(mc, bins = binning)
    bin_mids          = binning[1:] - np.diff(binning)[0] / 2
    integral_data     = np.sum(counts_data * binWidth)
    integral_mc       = np.sum(counts_mc * binWidth)

    err_data    = np.sqrt(counts_data) / integral_data
    err_mc      = np.sqrt(counts_mc) / integral_mc

    scaled_data = counts_data / integral_data
    scaled_mc   = counts_mc / integral_mc

    plt.errorbar(bin_mids, scaled_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    plt.errorbar(bin_mids, scaled_mc, yerr = err_mc, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")

    plt.legend()
    plt.xlabel('Time Residual [ns]')
    plt.ylabel(f'Normalised Counts per {binWidth} ns Bin')
    #plt.title(f"Initial Comparison of RAT 7.0.8 vs {isotope} Data", fontproperties=prop_font)
    # plt.xlim((-5, 40))
    #plt.yscale("log")
    plt.savefig("../plots/daniel_old_tuning_250Cut_2ns.pdf")

def createSubtraction(isotope, iteration, combination):
    """
    Function creates comparison plot showing the subtraction from data
    and a given MC combination.
    """
    
    data    = np.load(f"{isotope}214_data_residuals/{isotope}214_data_residuals_4m.npy") 
    best_mc = np.load(f"{isotope}214_MC_residuals/{iteration}/{combination}.npy") 

    fig, axes = plt.subplots(2,3, sharex="col")
    
    binWidth  = 1
    binning   = np.arange(-5, 15, binWidth)
    axes[0,0].hist(data, bins = binning, density = True, histtype = "step", label = "Data", color = "black")
    axes[0,0].hist(best_mc, bins = binning, density = True, histtype = "step", label = f"Best MC | {combination}", color = "blue")

    # errors on histogram
    counts_data, _    = np.histogram(data, bins = binning)
    counts_bestMC, _  = np.histogram(best_mc, bins = binning)
    bin_mids          = binning[1:] - np.diff(binning)[0] / 2
    integral_data     = np.sum(counts_data * binWidth)
    integral_bestMC   = np.sum(counts_bestMC * binWidth)

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC

    scaled_data = counts_data / integral_data
    scaled_MC   = counts_bestMC / integral_bestMC

    axes[0,0].errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    axes[0,0].errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    
    # create residual subtraction showing bin-by-bin variation as % change
    # create residual subtraction showing bin-by-bin variation as % change
    delta     = ( (scaled_data ) - ( scaled_MC) )/ (scaled_data)
    err_delta = np.sqrt( (scaled_MC / scaled_data**2)**2 * err_data**2 + (1 / scaled_data)**2 * err_bestMC**2)
    axes[1, 0].errorbar(bin_mids, 100 * delta , yerr = 100 * err_delta, linestyle = "", marker = "o", linewidth = 1, markersize = 1, capsize =0, color = "black")

    # axes[1, 0].set_ylim((-100, 100))


    binWidth  = 1
    binning   = np.arange(-5, 50, binWidth)
    axes[0,1].hist(data, bins = binning, density = True, histtype = "step", label = "Data", color = "black")
    axes[0,1].hist(best_mc, bins = binning, density = True, histtype = "step", label = f"Best MC | {combination}", color = "blue")

    # errors on histogram
    counts_data, _    = np.histogram(data, bins = binning)
    counts_bestMC, _  = np.histogram(best_mc, bins = binning)
    bin_mids          = binning[1:] - np.diff(binning)[0] / 2
    integral_data     = np.sum(counts_data * binWidth)
    integral_bestMC   = np.sum(counts_bestMC * binWidth)

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC

    scaled_data = counts_data / integral_data
    scaled_MC   = counts_bestMC / integral_bestMC

    axes[0,1].errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    axes[0,1].errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    
    # create residual subtraction showing bin-by-bin variation as % change
    delta     = ( (scaled_data ) - ( scaled_MC) )/ (scaled_data)
    err_delta = np.sqrt( (scaled_MC / scaled_data**2)**2 * err_data**2 + (1 / scaled_data)**2 * err_bestMC**2)
    axes[1, 1].errorbar(bin_mids, 100 * delta , yerr = 100 * err_delta, linestyle = "", marker = "o", linewidth = 1, markersize = 1, capsize =0, color = "black")
    # axes[1, 1].set_ylim((-2, 2))
   
    binWidth  = 1
    binning   = np.arange(-5, 250, binWidth)
    axes[0,2].hist(data, bins = binning, density = True, histtype = "step", label = "Data", color = "black")
    axes[0,2].hist(best_mc, bins = binning, density = True, histtype = "step", label = f"Best MC | {combination}", color = "blue")
    # axes[0,2].hist(best_mc, bins = binning, density = True, histtype = "step", label = f"RAT 7.0.8", color = "blue")

    axes[0,2].set_yscale("log")
    
    # errors on histogram
    counts_data, _    = np.histogram(data, bins = binning)
    counts_bestMC, _  = np.histogram(best_mc, bins = binning)
    bin_mids          = binning[1:] - np.diff(binning)[0] / 2
    integral_data     = np.sum(counts_data) * binWidth
    integral_bestMC   = np.sum(counts_bestMC) * binWidth

    err_data    = np.sqrt(counts_data) / integral_data
    err_bestMC  = np.sqrt(counts_bestMC) / integral_bestMC

    scaled_data = counts_data / integral_data
    scaled_MC   = counts_bestMC / integral_bestMC

    axes[0,2].errorbar(bin_mids, counts_data / integral_data, yerr = err_data, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
    axes[0,2].errorbar(bin_mids, counts_bestMC / integral_bestMC, yerr = err_bestMC, marker = "o", markersize = 2, capsize = 2, color = "blue", linestyle = "")
    delta     = ( (scaled_data ) - ( scaled_MC) )/ (scaled_data)
    err_delta = np.sqrt( (scaled_MC / scaled_data**2)**2 * err_data**2 + (1 / scaled_data)**2 * err_bestMC**2)
    print(counts_data[10], counts_bestMC[10], integral_data, integral_bestMC, err_delta[10] *100)

    axes[1, 2].errorbar(bin_mids, 100 * delta , yerr = 100 * err_delta, linestyle = "", marker = "o", linewidth = 1, markersize = 1, capsize =0, color = "black")
    # axes[1, 2].set_ylim((-2, 2))
    axes[1, 2].set_xlim((-5, 250))
    
    axes[1,0].set_xlabel("Time Residual (ns)", fontsize = 7)
    axes[1,1].set_xlabel("Time Residual (ns)", fontsize = 7)
    axes[1,2].set_xlabel("Time Residual (ns)", fontsize = 7)
    axes[1,0].set_ylabel(r"$\frac{N_{data} - N_{MC}}{N_{data}}$ (%)")
    axes[0,2].legend(fontsize = 7)
    # axes[0,1].set_title("FV = 4.0 m")
    fig.tight_layout()
    # plt.show()
    # print("saving")
    
    plt.savefig(f"subtraction_{isotope}_{iteration}_{combination}.pdf")

# createSubtraction("bi", "initial_config_5p5m", "7.25_5.45_117.5_425.0")
initial_comparison("Bi214", 4000.0, 0.7, 1.1)
