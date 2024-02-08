import numpy as np 
import rat 
from ROOT import RAT
import argparse
import os 

def extractAnalysis(parameters, iteration, isotope, FV_CUT, zOffset, ENERGY_LOW, ENERGY_HIGH):
    """
    INPUTS: These inputs define the MC file to load in:

            1 ) emission time parameters STRING
            2 ) iteration name           STRING
            3 ) isotope simulated        STRING
            
            Inputs define cuts to apply to MC:

            1 ) FV_CUT                   FLOAT
            2 ) zOffset                  FLOAT
            3) ENERGY_LOW                FLOAT
            4) ENERGY_HIGH               FLOAT

    OUTPUT: time residuals               ARRAY
    """ 

    # OUTPUTS
    residualsRECON = []
    COUNTER        = 0 
    #iteration = "initial_config"
    if iteration == "1" and isotope == "Po214":
        # Doubled the stats by adding additional file which has {parameters}2.root suffix 
        fname = f"/data/snoplus3/hunt-stokes/tune_cleaning/MC/{isotope}/{iteration}/{parameters}*.root"
    elif iteration == "bismsb_comparison":
        fname = f"/data/snoplus3/hunt-stokes/tune_cleaning/MC/{iteration}/{isotope}/{parameters}.root"
    else:
        fname          = f"/data/snoplus3/hunt-stokes/tune_cleaning/MC/{isotope}/{iteration}/{parameters}.root"
    # fname = f"/data/snoplus3/hunt-stokes/tune_cleaning/MC/{isotope}/{iteration}/{parameters}*.root"
    print(fname)
    # fname          = f"MC/{isotope}/{iteration}/*.root"
    ds = RAT.DU.DSReader(fname)
        
    for ientry, _ in rat.dsreader(fname):
        # light path calculator and point3D stuff loaded after ratds constructor
        # timeResCalc = rat.utility().GetTimeResidualCalculator()
        PMTCalStatus = RAT.DU.Utility.Get().GetPMTCalStatus()
        light_path = rat.utility().GetLightPathCalculator()
        group_velocity = rat.utility().GetGroupVelocity()
        pmt_info = rat.utility().GetPMTInfo()
        psup_system_id = RAT.DU.Point3D.GetSystemId("innerPMT")
        av_system_id = RAT.DU.Point3D.GetSystemId("av")
        
        # entry = ds.GetEntry(i)
        if ientry.GetEVCount() == 0:
            continue

        #### RECONSTRUCTION INFORMATION EXTRACTED ####
        reconEvent = ientry.GetEV(0)
        
        # did event get reconstructed correctly?
        fit_name = reconEvent.GetDefaultFitName()
        if not reconEvent.FitResultExists(fit_name):
            continue

        vertex = reconEvent.GetFitResult(fit_name).GetVertex(0)
        if (not vertex.ContainsPosition() or
            not vertex.ContainsTime() or
            not vertex.ValidPosition() or
            not vertex.ValidTime() or
            not vertex.ContainsEnergy() or
            not vertex.ValidEnergy()):
            continue
        # print("Reconstruction checks PASSED!")
        # reconstruction valid so get reconstructed position and energy
        reconPosition  = vertex.GetPosition() # returns in PSUP coordinates
        reconEnergy    = vertex.GetEnergy()        
        reconEventTime = vertex.GetTime()
        
        # apply AV offset to position
        event_point = RAT.DU.Point3D(psup_system_id, reconPosition)
        event_point.SetCoordinateSystem(av_system_id)
        if event_point.Mag() > FV_CUT:
            continue
        # convert back to PSUP coordinates
        event_point.SetCoordinateSystem(psup_system_id)

        # apply energy tagging cuts the same as that in data
        if reconEnergy < ENERGY_LOW or reconEnergy > ENERGY_HIGH:
            continue
        
        # event has passed all the cuts so we can extract the time residuals
        calibratedPMTs = reconEvent.GetCalPMTs()
        pmtCalStatus = rat.utility().GetPMTCalStatus()
        for j in range(calibratedPMTs.GetCount()):
            pmt = calibratedPMTs.GetPMT(j)
            if pmtCalStatus.GetHitStatus(pmt) != 0:
                continue
            
            # residual_recon = timeResCalc.CalcTimeResidual(pmt, reconPosition, reconEventTime, True)
            pmt_point = RAT.DU.Point3D(psup_system_id, pmt_info.GetPosition(pmt.GetID()))
            light_path.CalcByPosition(event_point, pmt_point)
            inner_av_distance = light_path.GetDistInInnerAV()
            av_distance = light_path.GetDistInAV()
            water_distance = light_path.GetDistInWater()
            transit_time = group_velocity.CalcByDistance(inner_av_distance, av_distance, water_distance)
            residual_recon = pmt.GetTime() - transit_time - reconEventTime
            
            residualsRECON.append(residual_recon)
        
        COUNTER += 1
        if COUNTER % 1 == 0:
            print("COMPLETED {} / {}".format(COUNTER, ds.GetEntryCount()))
    return residualsRECON
            
if __name__ == "__main__":

    """
    Given a combination of timing parameters and which iteration of tuning it is, extract residuals 
    from the relavent .root MC file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("iteration", type=str)
    parser.add_argument("isotope", type=str)
    # parser.add_argument("T1", type=str)
    # parser.add_argument("T2", type=str)
    # parser.add_argument("A1", type=str)
    # parser.add_argument("A2", type=str)
    parser.add_argument("parameters", type=str)
    parser.add_argument("zOffset", type=float)
    parser.add_argument("FV_CUT", type=float)
    parser.add_argument("E_LOW", type=float)
    parser.add_argument("E_HIGH", type=float)
    parser.add_argument("domain_low", type=float)
    parser.add_argument("domain_high", type=float)
    args = parser.parse_args()
    
    # convert inputs to rounded floats
    # T1 = round(float(args.T1), 3)
    # T2 = round(float(args.T2), 3)
    # A1 = round(float(args.A1), 3)
    # A2 = round(float(args.A2), 3)
    # parameters = f"{T1}_{T2}_{A1}_{A2}"

    residuals  = extractAnalysis(args.parameters, args.iteration, args.isotope, args.FV_CUT, args.zOffset, args.E_LOW, args.E_HIGH)
    
    if args.iteration == "bismsb_comparison":
        np.save(f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/{args.iteration}/{args.isotope}/{args.parameters}.npy", residuals)
    else:
        np.save(f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/{args.isotope}/{args.iteration}/{args.parameters}.npy", residuals)
    print("saved residuals!", f"/data/snoplus3/hunt-stokes/tune_cleaning/residuals/{args.isotope}/{args.iteration}/{args.parameters}.npy")
    # np.save(f"{args.isotope}214_MC_residuals/{args.iteration}/{parameters}.npy", residuals)
    
    # COMPUTE THE SQUARED DIFFERENCES BETWEEN THIS AND THE DATA
    #binning = np.arange(args.domain_low, args.domain_high, 1)
    # actually due to changing normalisation conditions, need to bin over the entire range

    if args.iteration != "bismsb_comparsion":
        binning = np.arange(-5, 250, 1)
        if args.isotope == "init_Po214" or args.isotope == "init_Bi214":
            data = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/detector_data/{args.isotope[5:]}_data_{args.FV_CUT}mmFV_{args.E_LOW}MeV_{args.E_HIGH}MeV_residuals.npy", allow_pickle=True)
        else:
            # data = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/detector_data/{args.isotope}_{args.FV_CUT}mmFV_{args.E_LOW}MeV_{args.E_HIGH}MeV_residuals.npy")
            data = np.load(f"/data/snoplus3/hunt-stokes/tune_cleaning/detector_data/po_FV4000.0_goldList_REPROC.npy", allow_pickle=True)
        data = np.concatenate(data)
        data_hist_counts, data_hist_bin_edges = np.histogram(data, bins = binning, density = True)
        model_hist_counts, model_hist_bin_edges = np.histogram(residuals, bins = binning, density = True)

        # find the bin idx from -5 ns --> 40 ns to compute the chi2
        binIdxLow = np.where(binning == int(args.domain_low))[0][0]
        binIdxHigh = np.where(binning == int(args.domain_high))[0][0]
        # print(binIdxLow[0])
        # print(type(binIdxLow[0]))
        # compute diffs of each bin counts 
        diffs = np.sum(( data_hist_counts[binIdxLow:binIdxHigh] - model_hist_counts[binIdxLow:binIdxHigh] ) **2 )

        # save this number
        np.save(f"/data/snoplus3/hunt-stokes/tune_cleaning/chi2/{args.isotope}/{args.iteration}/{args.parameters}.npy", diffs)
        # np.save(f"{args.isotope}214_chi2/{args.iteration}/{parameters}.npy", diffs)
