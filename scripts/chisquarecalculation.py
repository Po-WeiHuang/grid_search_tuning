import numpy as np
import rat
from ROOT import RAT 
import argparse
import os
# combined all the simulation results of same tuning time, to calculating chisquare with data

# parameters that need to be changed
t1 = np.arange(2.5,5.1,0.1)
loop = int(input("num of simlation files per runid: "))




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

def chisquarecalc():
	path      = "/data/snoplus3/weiii/tune_cleaning"
	datapath  = "/home/huangp/AmBe_tres/AmBe_t_res_RAT7.0.15.npy"
	outputdir = "/data/snoplus3/weiii/tune_cleaning/chi2"
	binning = np.arange(-5,250,1)
	parameters = np.round(t1,1)
	if(args.isotope == "AmBe"):
		try:
			os.mkdir(f"{outputdir}/{args.iteration}")
			os.chmod(f"{outputdir}/{args.iteration}", 0o0777)
		except:
			print(f"directory:{outputdir}{args.iteration} already exists")
		data_arr  = np.load(datapath, allow_pickle=True)
		for iConst1 in range(len(parameters)):
			MC_arr = []
			for iloop in range(loop):
				try:
					macName = f"{parameters[iConst1]}_{iloop}th_"
					MC_arr    += opentxt(f"{path}/residuals/{args.iteration}/txt/{macName}_{iloop}.txt")
					print("length of MC:", len(MC_arr))
				except:
					print(f"{path}/residuals/{args.iteration}/txt/{macName}_{iloop}.txt doesn't exist!")
			Norm_data_histcounts, Norm_data_histbins = np.histogram(data_arr, bins = binning,density = True)
			Norm_MC_histcounts  , Norm_MC_histbins   = np.histogram(MC_arr, bins = binning, density = True)
			MC_histcounts  , MC_histbins   = np.histogram(MC_arr, bins = binning, density = False) 
			scale = np.sum(MC_histcounts)
			Norm_MC_histcounts_err =  np.sqrt(MC_histcounts)/scale

			MCindex = np.where(Norm_MC_histcounts<0.000001)[0][0]	
			#print(( data_histcounts[:MCindex-1] - MC_histcounts[MCindex-1] )**2/MC_histcounts[MCindex-1])
			#diffs = np.sum(( data_histcounts[:MCindex-1] - MC_histcounts[:MCindex-1] )**2 )
			diffs = np.sum(( Norm_data_histcounts[:MCindex-1] - Norm_MC_histcounts[:MCindex-1] )**2/Norm_MC_histcounts_err[:MCindex-1]**2  )
			print("chisquare",diffs)

			np.save(f"{outputdir}/{args.iteration}/{parameters[iConst1]}.npy",diffs)
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-iteration", type=str)
	parser.add_argument("-isotope",type=str)
	#parser.add_argument("-parameters",type=str)
	args = parser.parse_args()
	chisquarecalc()
