import numpy as np
import rat
from ROOT import RAT 
import argparse
import os
# combined all the simulation results of same tuning time, to calculating chisquare with data

# parameters that need to be changed
t1 = np.arange(10.0,30.0,0.2)#np.arange(15.0,35.0,0.2)






def chisquarecalc():
	isotope = args.isotope
	path      = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning"
	datapath  = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning/detector_data/"
	datafilename = "bismsb_batch4_bi_4000.0.npy" if isotope == "Bi214" else "bismsb_batch4_po_4000.0.npy"
	outputdir = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning/chi2"
	binning = np.arange(-5,350,1)
	parameters = np.round(t1,1)
	if(args.isotope == "Bi214" or args.isotope == "Po214"):
		try:
			os.mkdir(f"{outputdir}/{args.iteration}")
			os.chmod(f"{outputdir}/{args.iteration}", 0o0777)
		except:
			print(f"directory:{outputdir}{args.iteration} already exists")
		try:
			os.mkdir(f"{outputdir}/{args.iteration}/{isotope}")
			os.chmod(f"{outputdir}/{args.iteration}/{isotope}", 0o0777)
		except:
			print(f"directory:{outputdir}{args.iteration}/{isotope} already exists")
		data_arr  = np.load(datapath+datafilename, allow_pickle=True)
		for iConst1 in range(len(parameters)):
			MC_arr = []
			try:
				macName = f"{parameters[iConst1]}"
				MC_arr    = np.load(f"{path}/residuals/{args.iteration}/{isotope}/{macName}.npy")
				print("length of MC:", len(MC_arr))
			except:
				print(f"{path}/residuals/{args.iteration}/{isotope}/{macName}.npy not exists")
			Norm_data_histcounts, Norm_data_histbins = np.histogram(data_arr, bins = binning,density = True)
			Norm_MC_histcounts  , Norm_MC_histbins   = np.histogram(MC_arr, bins = binning, density = True)
			MC_histcounts  , 		   MC_histbins   = np.histogram(MC_arr, bins = binning, density = False)
			Data_histcounts  , 		 Data_histbins   = np.histogram(MC_arr, bins = binning, density = False) 
			scale = np.sum(MC_histcounts); scale_data = np.sum(Data_histcounts)
			Norm_MC_histcounts_err =  np.sqrt(MC_histcounts)/scale; Norm_Data_histcounts_err =  np.sqrt(Data_histcounts)/scale 
			#print(( MC_histcounts))
			
			MCindex = np.where(Norm_MC_histcounts<0.00001)[0][0]	
			#print(( data_histcounts[:MCindex-1] - MC_histcounts[MCindex-1] )**2/MC_histcounts[MCindex-1])
			#diffs = np.sum(( Norm_data_histcounts[:MCindex-1] - Norm_MC_histcounts[:MCindex-1] )**2/ Norm_MC_histcounts[:MCindex-1])
			diffs = np.sum(( Norm_data_histcounts[:MCindex-1] - Norm_MC_histcounts[:MCindex-1] )**2/((Norm_MC_histcounts_err[:MCindex-1]**2 + Norm_Data_histcounts_err[:MCindex-1]**2)  ))
			print("chisquare",diffs)

			np.save(f"{outputdir}/{args.iteration}/{isotope}/{parameters[iConst1]}.npy",diffs)
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("iteration", type=str)
	parser.add_argument("isotope",type=str)
	#parser.add_argument("-parameters",type=str)
	args = parser.parse_args()
	chisquarecalc()