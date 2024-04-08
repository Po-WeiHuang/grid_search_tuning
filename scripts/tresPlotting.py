import numpy as np
import matplotlib.pyplot as plt

# Path that store the tres
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("iteration", type=str)
#parser.add_argument("parameters", type=str)
#parser.add_argument("-o", help="output directory", type=str)
args = parser.parse_args()

# parameters that need to be changed

outputdir	= "/home/huangp/grid_search_tuning/Plots"
MC_AmBe_Path   = f"/data/snoplus3/weiii/tune_cleaning"
Data_AmBe_Path   = f"/home/huangp/AmBe_tres/AmBe_t_res_RAT7.0.15.npy"


def tres_hist_plot(histarray,fig,ax,color=None,label=None,density=True):
	myhist, xbins = np.histogram(histarray,bins=355,range=[-5.,350.])
	#myhist, xbins = np.histogram(histarray,bins=105,range=[-5.,100.])
	SUM = np.sum(myhist)
	hist, xbins,_ = ax.hist(histarray,bins=355,range=[-5.,350.],fill = False, label =label, color = color,histtype="step", density=density,log=True)
	#hist, xbins,_ = ax.hist(histarray,bins=105,range=[-5.,100.],fill = False, label =label, color = color,histtype="step", density=density,log=False)
	return hist, SUM
def tres_hist(histarray,density = True):
	returnarr,binsx = np.histogram(histarray,bins=355,range=[-5.,350.])
	#returnarr,binsx = np.histogram(histarray,bins=105,range=[-5.,100.])
	returnarr_err = returnarr**0.5
	if density == True: 
		SUM = np.sum(returnarr)
		returnarr_err = returnarr_err/SUM
		returnarr = returnarr/SUM 
	#print(len(returnarr))
	return returnarr, returnarr_err, binsx, SUM

def Plot_1D_error(arr_x,arr_y, fig, ax,xerr,yerr,color,ylogscale = False,label=None):
	ax.errorbar(arr_x, arr_y, xerr=xerr, yerr=yerr,color = color,label=label,linestyle="",marker='o',markersize=1)
	if(ylogscale == True):
		ax.set_yscale('log',nonposy='clip')
def ratiodiff(MC,MC_scale,Data,Data_scale): # calculate and return the ratio diff and its uncertainty(assume poission) of two normalised arrays
	MC_err_norm = (MC*MC_scale)**0.5/(MC_scale); Data_err_norm = (Data*Data_scale)**0.5/(Data_scale)
	#print(np.sqrt( ( (MC_err_norm/MC)**2 )+( (Data_err_norm/Data)**2 ) ) )
	return np.abs(MC/Data), np.sqrt( ( (MC_err_norm/MC)**2 )+( (Data_err_norm/Data)**2 ) )
def opentxt(filename):
	# open a txt file and return a numpy array
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

def GetFile(filedir): #return all of the file(.root) + originalfilename in that dir
	file_addresses = []; name = []
	for filename in os.listdir(filedir):
		file_address = os.path.join(filedir, filename)
		if os.path.isfile(file_address):
			if file_address[-4:] == '.txt':
			#if filename[38:40] == "88": # only rxtrac filename external_water_88 files
			#if filename[35:41] == "300960":
				file_addresses.append(file_address)
				name.append(filename)
				print(filename)
	return file_addresses, name

def plot_varyingt1():
	t1 			= [100.0]#np.arange(50.0,120.0,2.0)#np.arange(2.5,5.1,0.1)
	loop 		= int(input("num of simlation files per runid: "))
	parameters = np.round(t1,1)
	try:
		os.mkdir(f"{outputdir}/{args.iteration}")
		os.chmod(f"{outputdir}/{args.iteration}", 0o0777)
	except:
		print(f"directory:{outputdir}{args.iteration} already exists")
	Data = np.load(f"{Data_AmBe_Path}")
	for iConst1 in range(len(parameters)):
		MC = []
		for iloop in range(loop):
			try:
				macName = f"{parameters[iConst1]}_{iloop}th_"
				print(f"Ready to process {MC_AmBe_Path}/residuals/{args.iteration}/txt/{macName}_{iloop}.txt")
				MC    += opentxt(f"{MC_AmBe_Path}/residuals/{args.iteration}/txt/{macName}_{iloop}.txt")
				#print(MC)
				print("length of MC:", len(MC))
			except:
				print(f"{MC_AmBe_Path}/residuals/{args.iteration}/txt/{macName}_{iloop}.txt doesn't exist!")

		# *************** initial setup for Batch3 plots
		fig, (ax, ax2)  = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)
		
		MC_hist, MC_histerr, MCbinsx,SUM1 = tres_hist(MC)#,fig,ax,'blue',f'MC:{args.parameters}[ns]')
		Datahist, Datahisterr, binsx, SUM1_1= tres_hist(Data)
		binsx = (binsx[1:]+binsx[:-1])/2.
		Plot_1D_error(binsx,MC_hist, fig, ax,None, MC_histerr,'blue',ylogscale = True,label=f'MC:{parameters[iConst1]}[ns]')
		Plot_1D_error(binsx,Datahist, fig, ax,None, Datahisterr,'0',ylogscale = True,label="Data")
		# calculate the diff between data/MC and plot it
		diff, sigma_diff= ratiodiff(MC_hist,SUM1,Datahist,SUM1_1)
		Plot_1D_error(binsx,diff, fig, ax2,None, sigma_diff,'0',ylogscale = False)
		
		

		ax.legend()
		ax2.legend()
		ax2.set_xlabel("tres")
		ax2.set_ylabel("MC/Data")
		ax2.set_ylim(0.6,1.2)
		#plt.savefig(f"{outputdir}/{args.iteration}/{parameters[iConst1]}_tres.png")
		plt.savefig(f"{outputdir}/{args.iteration}/log{parameters[iConst1]}_tres.png")
		#fig.show()
		#input()
	
def plot_genericmc_data():
	try:
		os.mkdir(f"{outputdir}/{args.iteration}")
		os.chmod(f"{outputdir}/{args.iteration}", 0o0777)
	except:
		print(f"directory:{outputdir}{args.iteration} already exists")
	Data = np.load(f"{Data_AmBe_Path}")
	mcfilepath, filename = GetFile(f"{MC_AmBe_Path}/residuals/{args.iteration}/txt")
	MC = []
	for i in range(len(mcfilepath)):
		MC    += opentxt(f"{MC_AmBe_Path}/residuals/{args.iteration}/txt/{filename[i]}")
		# *************** initial setup for Batch3 plots
	fig, (ax, ax2)  = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)
		
	MC_hist, MC_histerr, MCbinsx,SUM1 = tres_hist(MC)#,fig,ax,'blue',f'MC:{args.parameters}[ns]')
	Datahist, Datahisterr, binsx, SUM1_1= tres_hist(Data)
	binsx = (binsx[1:]+binsx[:-1])/2.
	Plot_1D_error(binsx,MC_hist, fig, ax,None, MC_histerr,'blue',ylogscale = True,label=f'MC')
	Plot_1D_error(binsx,Datahist, fig, ax,None, Datahisterr,'0',ylogscale = True,label="Data")
	# calculate the diff between data/MC and plot it
	diff, sigma_diff= ratiodiff(MC_hist,SUM1,Datahist,SUM1_1)
	Plot_1D_error(binsx,diff, fig, ax2,None, sigma_diff,'0',ylogscale = False)
	
	

	ax.legend()
	ax2.legend()
	ax2.set_xlabel("tres")
	ax2.set_ylabel("MC/Data")
	ax2.set_ylim(0.6,1.2)
	#plt.savefig(f"{outputdir}/{args.iteration}/GenericMc_Data_tres.png")
	plt.savefig(f"{outputdir}/{args.iteration}/logGenericMc_Data_tres.png")
	#fig.show()

	
if __name__ == "__main__":

	plot_varyingt1()
	#plot_genericmc_data()
	#input()








