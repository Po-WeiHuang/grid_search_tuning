import numpy as np
import rat
from ROOT import RAT 
import argparse
import os


path      = "/data/snoplus3/weiii/tune_cleaning/MC/"
datapath  = "/home/huangp/AmBe_tres/AmBe_t_res_RAT7.0.15.npy"
outputdir = "/data/snoplus3/weiii/tune_cleaning/chi2/"
binning = np.arange(-5,250,1)

def opentxt(filename):
	try:
		return_list = []
		with open(filename, 'r') as file:
			numbers_str = file.read().strip()
			
			numbers_list = numbers_str.split(",")
			for i in range(len(numbers_list)-1):
				return_list.append(float(numbers_list[i]))
			#print("Numbers:", return_list)
			return return_list

	except FileNotFoundError:
		print(f"Error: File`{filename}` not found. ")
	except Exception as e:
		print(f"Error: {e}")
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-iteration", type=str)
	parser.add_argument("-isotope",type=str)
	parser.add_argument("-parameters",type=str)
	args = parser.parse_args()

	if(args.isotope == "AmBe"):
		data_arr  = np.load(datapath, allow_pickle=True)
		
		MC_arr    = opentxt(f"{path}{args.iteration}/AfterCutAmBe/{args.parameters}.txt")
		#print(MC_arr)
		data_histcounts, data_histbins = np.histogram(data_arr, bins = binning,density = True)
		MC_histcounts  , MC_histbins   = np.histogram(MC_arr, bins = binning, density = True) 

		MCindex = np.where(MC_histcounts<0.000001)[0][0]	
		#print(( data_histcounts[:MCindex-1] - MC_histcounts[MCindex-1] )**2/MC_histcounts[MCindex-1])
		diffs = np.sum(( data_histcounts[:MCindex-1] - MC_histcounts[MCindex-1] )**2/MC_histcounts[MCindex-1]  )
		print("chisquare",diffs)

		np.save(f"{outputdir}{args.iteration}/{args.parameters}.npy",diffs)
		

