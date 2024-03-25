import numpy as np
import matplotlib.pyplot as plt

# Path that store the tres
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("iteration", type=str)
parser.add_argument("parameters", type=str)
#parser.add_argument("-o", help="output directory", type=str)
args = parser.parse_args()

MC_AmBe_Path   = f"/data/snoplus3/weiii/tune_cleaning/MC/{args.iteration}/AfterCutAmBe/"
Data_AmBe_Path   = f"/home/huangp/AmBe_tres/AmBe_t_res_RAT7.0.15.npy"


def tres_hist_plot(histarray,fig,ax,color=None,label=None,density=True):
	#myhist, xbins = np.histogram(histarray,bins=355,range=[-5.,350.])
	myhist, xbins = np.histogram(histarray,bins=105,range=[-5.,100.])
	SUM = np.sum(myhist)
	#hist, xbins,_ = ax.hist(histarray,bins=355,range=[-5.,350.],fill = False, label =label, color = color,histtype="step", density=density,log=True)
	hist, xbins,_ = ax.hist(histarray,bins=105,range=[-5.,100.],fill = False, label =label, color = color,histtype="step", density=density,log=False)
	return hist, SUM
def tres_hist(histarray,density = True):
	#returnarr,binsx = np.histogram(histarray,bins=355,range=[-5.,350.])
	returnarr,binsx = np.histogram(histarray,bins=105,range=[-5.,100.])
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
			return np.array(return_list)

	except FileNotFoundError:
		print(f"Error: File`{filename}` not found. ")
	except Exception as e:
		print(f"Error: {e}")

if __name__ == "__main__":
	
	# load mc(after reconstruction)
	MC = opentxt(f"{MC_AmBe_Path}{args.parameters}.txt")
	Data = np.load(f"{Data_AmBe_Path}")
	
	# *************** initial setup for Batch3 plots
	fig, (ax, ax2)  = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)
	
	MC_hist, MC_histerr, MCbinsx,SUM1 = tres_hist(MC)#,fig,ax,'blue',f'MC:{args.parameters}[ns]')
	Datahist, Datahisterr, binsx, SUM1_1= tres_hist(Data)
	binsx = (binsx[1:]+binsx[:-1])/2.
	Plot_1D_error(binsx,MC_hist, fig, ax,None, MC_histerr,'blue',ylogscale = False,label=f'MC:{args.parameters}[ns]')
	Plot_1D_error(binsx,Datahist, fig, ax,None, Datahisterr,'0',ylogscale = False,label="Data")
	# calculate the diff between data/MC and plot it
	diff, sigma_diff= ratiodiff(MC_hist,SUM1,Datahist,SUM1_1)
	Plot_1D_error(binsx,diff, fig, ax2,None, sigma_diff,'0',ylogscale = True)
	 
	

	ax.legend()
	ax2.legend()
	ax2.set_xlabel("tres")
	ax2.set_ylabel("MC/Data")
	plt.savefig(f"/home/huangp/grid_search_tuning/Plots/{args.iteration}/{args.parameters}_tres.png")
	fig.show()
	

	#input()









