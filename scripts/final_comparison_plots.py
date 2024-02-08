import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import glob

"""
Script duplicates a lot of code, but produces the final plots for the 2.2 g/L time residual tuning.

Time residual agreement graphs for Bi214 and Po214 are produced, for a range of different FVs.
"""

FVs      = [4000.0]#[6000.0, 5500.0, 5000.0, 4500.0, 4000.0, 3500.0, 3000.0]
isotopes = ["po"]

def create_data_vs_mc_plots(FVs, isotopes):
    for i in range(len(FVs)):
        for j in range(len(isotopes)):

            """
            For a given FV and isotope, create the following graphs: 
            1. -5 --> 100 ns peak region
            2. -5 --> 100 ns peak region (log scale)
            3. -5 --> 350 ns tails region (log scale)
            4. -5 --> 350 ns full range
            5. -5 --> 350 ns full range (log scale)

            For the following cases:
                A: OLD RECOORDINATED MC
                B: NEW TIMING MC

            Additionally, make:
                1. alpha vs beta timing before and after updated timing + recoordination (i.e. just showing MC)
            """
            # load up the dataset
            data            = np.load(f"../detector_data/{isotopes[j]}_FV{FVs[i]}_goldList.npy")
            num_data_events = data.size
            data            = np.concatenate(data)

            data_new            = np.load(f"../detector_data/{isotopes[j]}_FV{FVs[i]}_goldList_REPROC.npy")
            num_data_events_new = data_new.size
            data_new            = np.concatenate(data_new)

            # load up the MC 
            MC            = np.load(f"/data/snoplus3/hunt-stokes/clean_bipo/new_extracted_residuals/{isotopes[j]}_old_mc/{isotopes[j]}_{FVs[i]}_highStats.npy")
            num_mc_events = MC.size
            MC            = np.concatenate(MC) 
            
            MC_recoord    = np.load(f"/data/snoplus3/hunt-stokes/clean_bipo/new_extracted_residuals/{isotopes[j]}_new_mc/{isotopes[j]}_{FVs[i]}_combined2.npy")
            num_new_mc    = MC_recoord.size
            MC_recoord    = np.concatenate(MC_recoord)

            # create the binning schemes for each plot
            binwidth      = 2
            binning_peak  = np.arange(-5, 100, binwidth)
            binning_tails = np.arange(-5, 350, binwidth)
            
            if isotopes[j] == "bi":
                name = "Bi214"
            else:
                name = "Po214"
            
            # work out the error on each bin for MC and data
            counts_data_peak, _    = np.histogram(data, bins = binning_peak)
            counts_data_peak_new, _    = np.histogram(data_new, bins = binning_peak)
            counts_mc_peak,   _    = np.histogram(MC, bins = binning_peak)
            counts_mc_peak_new, _  = np.histogram(MC_recoord, bins = binning_peak)

            bin_mids_peak = binning_peak[1:] - np.diff(binning_peak)[0] / 2

            integral_data_peak   = np.sum(counts_data_peak) * binwidth
            integral_data_peak_new   = np.sum(counts_data_peak_new) * binwidth
            integral_mc_peak     = np.sum(counts_mc_peak)   * binwidth
            integral_mc_peak_new = np.sum(counts_mc_peak_new)   * binwidth

            err_data_peak      = np.sqrt(counts_data_peak) / integral_data_peak
            err_data_peak_new      = np.sqrt(counts_data_peak_new) / integral_data_peak_new
            err_mc_peak        = np.sqrt(counts_mc_peak)   / integral_mc_peak
            err_mc_peak_new    = np.sqrt(counts_mc_peak_new)   / integral_mc_peak_new

            # tails #
            counts_data_tails, _    = np.histogram(data, bins = binning_tails)
            counts_data_tails_new, _    = np.histogram(data_new, bins = binning_tails)
            counts_mc_tails,   _    = np.histogram(MC, bins = binning_tails)
            counts_mc_tails_new, _  = np.histogram(MC_recoord, bins = binning_tails)

            bin_mids_tails = binning_tails[1:] - np.diff(binning_tails)[0] / 2

            integral_data_tails    = np.sum(counts_data_tails) * binwidth
            integral_data_tails_new    = np.sum(counts_data_tails_new) * binwidth
            integral_mc_tails      = np.sum(counts_mc_tails)   * binwidth
            integral_mc_tails_new  = np.sum(counts_mc_tails_new)   * binwidth

            err_data_tails      = np.sqrt(counts_data_tails) / integral_data_tails
            err_data_tails_new      = np.sqrt(counts_data_tails_new) / integral_data_tails_new
            err_mc_tails        = np.sqrt(counts_mc_tails)   / integral_mc_tails
            err_mc_tails_new    = np.sqrt(counts_mc_tails_new)   / integral_mc_tails_new
            
            fig, axes = plt.subplots(nrows =1, ncols = 2, figsize = (10, 4))
            """
            Peak Histogram.
            """
            # plt.figure()
            # axes[0,0].hist(data, density = True, bins = binning_peak, histtype = "step", color = "black", label = f"Data | 7.0.8 | Num EVs: {num_data_events}")
            # axes[0,0].hist(MC, density = True, bins = binning_peak, histtype = "step", linestyle = "dashed", color = "red", label = f"MC   | 7.0.8 | Num EVs: {num_mc_events}")
            # axes[0,0].set_title(f"{name} | {int(FVs[i]) / 1000} m FV")
            # axes[0,0].set_xlabel("Time Residual (ns)")
            # axes[0,0].set_ylabel(f"Normalised Counts per {binwidth} ns Bin")
            # axes[0,0].legend()

            # axes[0,0].errorbar(bin_mids_peak, counts_data_peak / integral_data_peak, yerr = err_data_peak, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
            # axes[0,0].errorbar(bin_mids_peak, counts_mc_peak / integral_mc_peak, yerr = err_mc_peak, marker = "o", markersize = 2, capsize = 2, color = "red", linestyle = "")
            # plt.savefig(f"../official_plots/plots_for_slides/{isotopes[j]}_{FVs[i]}_peak_old.pdf")
            # plt.close()

            # plt.figure()
            axes[0].hist(data_new, density = True, bins = binning_peak, histtype = "step", color = "black", label = f"Data | ReCoord + ReProcessed\nNum EVs: {num_data_events_new}")
            axes[0].hist(MC_recoord, density = True, bins = binning_peak, histtype = "step", linestyle = "dotted", color = "red", label = f"MC   | ReCoord | Num EVs: {num_new_mc}")
            axes[0].set_title(f"{name} | {int(FVs[i]) / 1000} m FV | ReCoordinated and ReProcessed")
            axes[0].set_xlabel("Time Residual (ns)")
            axes[0].set_ylabel(f"Normalised Counts per {binwidth} ns Bin")
            axes[0].legend()

            axes[0].errorbar(bin_mids_peak, counts_data_peak_new / integral_data_peak_new, yerr = err_data_peak_new, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
            axes[0].errorbar(bin_mids_peak, counts_mc_peak_new / integral_mc_peak_new, yerr = err_mc_peak_new, marker = "o", markersize = 2, capsize = 2, color = "red", linestyle = "")
            # plt.savefig(f"../official_plots/plots_for_slides/{isotopes[j]}_{FVs[i]}_peak_new.pdf")
            # plt.close()

            """
            Tails Histogram.
            """
            # plt.figure()
            # axes[1,0].hist(data, density = True, bins = binning_tails, histtype = "step", color = "black", label = f"Data | 7.0.8 | Num EVs: {num_data_events}")
            # axes[1,0].hist(MC, density = True, bins = binning_tails, histtype = "step", linestyle = "dashed", color = "red", label = f"MC   | 7.0.8 | Num EVs: {num_mc_events}")
            # axes[1,0].set_title(f"{name} | {int(FVs[i]) / 1000} m FV")
            # axes[1,0].set_xlabel("Time Residual (ns)")
            # axes[1,0].set_ylabel(f"Normalised Counts per {binwidth} ns Bin")
            # axes[1,0].legend()

            # axes[1,0].errorbar(bin_mids_tails, counts_data_tails / integral_data_tails, yerr = err_data_tails, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
            # axes[1,0].errorbar(bin_mids_tails, counts_mc_tails / integral_mc_tails, yerr = err_mc_tails, marker = "o", markersize = 2, capsize = 2, color = "red", linestyle = "")
            # axes[1,0].set_yscale("log")
            # plt.savefig(f"../official_plots/plots_for_slides/{isotopes[j]}_{FVs[i]}_tails_old.pdf")
            # plt.close()

            # plt.figure()
            axes[1].hist(data_new, density = True, bins = binning_tails, histtype = "step", color = "black", label = f"Data | ReCoord + ReProcess\nNum EVs: {num_data_events}")
            axes[1].hist(MC_recoord, density = True, bins = binning_tails, histtype = "step", linestyle = "dashed", color = "red", label = f"MC   | ReCoord | Num EVs: {num_mc_events}")
            axes[1].set_title(f"{name} | {int(FVs[i]) / 1000} m FV | ReCoordinated and ReProcessed")
            axes[1].set_xlabel("Time Residual (ns)")
            axes[1].set_ylabel(f"Normalised Counts per {binwidth} ns Bin")
            axes[1].legend()

            axes[1].errorbar(bin_mids_tails, counts_data_tails_new / integral_data_tails_new, yerr = err_data_tails_new, marker = "o", markersize = 2, capsize = 2, color = "black", linestyle = "")
            axes[1].errorbar(bin_mids_tails, counts_mc_tails_new / integral_mc_tails_new, yerr = err_mc_tails_new, marker = "o", markersize = 2, capsize = 2, color = "red", linestyle = "")
            axes[1].set_yscale("log")
            fig.tight_layout()
            plt.savefig(f"../official_plots/plots_for_slides/{isotopes[j]}_{FVs[i]}_combined.pdf")
            plt.close()

def create_recoordianted_mc_tres_dists():
    """
    Load up the time residual distributions generated from the run-by-run MC and combine them to make
    a single time residual distribution for each FV.
    """

    FVs      = [6000.0, 5500.0, 5000.0, 4500.0, 4000.0, 3500.0, 3000.0]
    isotopes = ["po"]

    for i in range(len(FVs)):
        for j in range(len(isotopes)):
            combined_residuals = []

            run_by_run_files = glob.glob(f"/data/snoplus3/hunt-stokes/clean_bipo/new_extracted_residuals/{isotopes[j]}_mc_REPROC/*{FVs[i]}.npy")
            print(run_by_run_files)
            for ifile in range(len(run_by_run_files)):
                run_residuals = np.load(run_by_run_files[ifile]).tolist()
                combined_residuals += run_residuals
                print("Combined ", ifile)
            # save this array
            np.save(f"/data/snoplus3/hunt-stokes/clean_bipo/new_extracted_residuals/{isotopes[j]}_new_mc/{isotopes[j]}_{FVs[i]}_combined2.npy", combined_residuals)
            print(f"Completed: {isotopes[j]} {FVs[i]}.")

def reprocessing_data_comparison():
    """
    Comparing the time residual distributions of Bi214 data in each FV before and 
    after Will's reprocessing with improved reconstruction bias.
    """

    # create a plot for each FV
    FVs   = [3000.0, 3500.0, 4000.0, 4500.0, 5000.0, 5500.0, 6000.0]
    width = 1
    binning_tails = np.arange(-5, 350, width)
    binning_peak  = np.arange(-5, 80, width)

    for iFV in FVs:

        data_old = np.load(f"../detector_data/bi_FV{iFV}_goldList_REPROC.npy")
        data_new = np.load(f"../detector_data/bi_FV{iFV}_goldList_REPROC_WILL.npy")
        
        data_old = np.concatenate(data_old)
        data_new = np.concatenate(data_new)

        plt.figure()
        plt.hist(data_old, bins = binning_peak, density = True, histtype = "step", color = "black", label = "ASCII Reprocessed")
        plt.hist(data_new, bins = binning_peak, density = True, histtype = "step", color = "red", label = "WP Reprocessed")
        plt.legend()
        plt.title("Impact of Will's Recoordination on Bi214 Time Residuals")
        plt.xlabel("Time Residual (ns)")
        plt.ylabel(f"Normalised Counts per {width} ns Bin")
        plt.savefig(f"../official_plots/reproc_impacts/peak_bi_{iFV}.pdf")
        plt.close()

        plt.figure()
        plt.hist(data_old, bins = binning_tails, density = True, histtype = "step", color = "black", label = "ASCII Reprocessed")
        plt.hist(data_new, bins = binning_tails, density = True, histtype = "step", color = "red", label = "WP Reprocessed")
        plt.legend()
        plt.yscale("log")
        plt.title("Impact of Will's Recoordination on Bi214 Time Residuals")
        plt.xlabel("Time Residual (ns)")
        plt.ylabel(f"Normalised Counts per {width} ns Bin")
        plt.savefig(f"../official_plots/reproc_impacts/tails_bi_{iFV}.pdf")
        plt.close()

# reprocessing_data_comparison()
# create_recoordianted_mc_tres_dists()
create_data_vs_mc_plots([3000.0, 3500.0, 4000.0, 4500.0, 5000.0, 5500.0, 6000.0], ["po"])