import numpy as np
import matplotlib.pyplot as plt

Batch3_MCpath   = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/Batch3labppo_2p2_bismsb_Table/"
Batch4_MCpath   = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/Batch4labppo_2p2_bismsb_Table/"
Datapath        = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning/detector_data/"
Low_MCpath   = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/0.1mglabppo_2p2_bismsb_Table/"
Hi_MCpath    = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/50mglabppo_2p2_bismsb_Table/"
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
if __name__ == "__main__":
	
	# load mc(after reconstruction)
	Bitres_batch3 = np.load(f"{Batch3_MCpath}Bi214/5.0.npy")
	Potres_batch3 = np.load(f"{Batch3_MCpath}Po214/4.1.npy")

	Bitres_batch4 = np.load(f"{Batch4_MCpath}Bi214/5.0.npy")
	Potres_batch4 = np.load(f"{Batch4_MCpath}Po214/4.1.npy")

	# load Data
	Bitres_batch3data = np.load(f"{Datapath}Bi214_bismsb_batch3.npy",allow_pickle=True)
	Potres_batch3data = np.load(f"{Datapath}Po214_bismsb_batch3.npy",allow_pickle=True)
	#Bitres_batch3data = np.concatenate(Bitres_batch3data); #Potres_batch3data = np.concatenate(Potres_batch3data)
		
	Bitres_batch4data = np.load(f"{Datapath}bismsb_batch4_bi_4000.0.npy",allow_pickle=True)
	Potres_batch4data = np.load(f"{Datapath}bismsb_batch4_po_4000.0.npy",allow_pickle=True)
	#Bitres_batch4data = np.concatenate(Bitres_batch4data); Potres_batch3data = np.concatenate(Potres_batch4data)

	# load mc truth
	Bitres_batch3_truth = np.load(f"{Batch3_MCpath}Bi214/MC5.0.npy")
	Potres_batch3_truth = np.load(f"{Batch3_MCpath}Po214/MC4.1.npy")

	Bitres_batch4_truth = np.load(f"{Batch4_MCpath}Bi214/MC5.0.npy")
	Potres_batch4_truth = np.load(f"{Batch4_MCpath}Po214/MC4.1.npy")

	Bitres_low_truth = np.load(f"{Low_MCpath}Bi214/MC5.0.npy")
	Bitres_hi_truth  = np.load(f"{Hi_MCpath}Bi214/MC5.0.npy")

	Potres_low_truth = np.load(f"{Low_MCpath}Po214/MC4.1.npy")
	Potres_hi_truth  = np.load(f"{Hi_MCpath}Po214/MC4.1.npy")
	# *************** initial setup for Batch3 plots
	fig, (batch3_Biax, Biax2)  = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)
	fig2, (batch3_Poax, Poax2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)
	
	Bibatch3_hist, SUM1 = tres_hist_plot(Bitres_batch3,fig,batch3_Biax,'blue','MC/Bi/batch3')
	Bibatch3_datahist, Bibatch3_datahisterr, Bibatch3binsx, SUM1_1= tres_hist(Bitres_batch3data)
	Bibatch3binsx = (Bibatch3binsx[1:]+Bibatch3binsx[:-1])/2.
	Plot_1D_error(Bibatch3binsx,Bibatch3_datahist, fig, batch3_Biax,None, Bibatch3_datahisterr,'0',ylogscale = False,label="data/Bi/batch3")
	# calculate the diff between data/MC and plot it
	batch3Bidiff, batch3Bisigma_diff= ratiodiff(Bibatch3_hist,SUM1,Bibatch3_datahist,SUM1_1)
	Plot_1D_error(Bibatch3binsx,batch3Bidiff, fig, Biax2,None, batch3Bisigma_diff,'0',ylogscale = False,label="Batch3 Bi")
	 
	
	Pobatch3_hist,SUM2 = tres_hist_plot(Potres_batch3,fig2,batch3_Poax,'blue','MC/po/batch3')
	Pobatch3_datahist, Pobatch3_datahisterr, Pobatch3binsx, SUM2_2= tres_hist(Potres_batch3data)
	Pobatch3binsx = (Pobatch3binsx[1:]+Pobatch3binsx[:-1])/2.
	Plot_1D_error(Pobatch3binsx,Pobatch3_datahist, fig2, batch3_Poax,None, Pobatch3_datahisterr,'0',ylogscale = False,label="data/Po/batch3")
	# calculate the diff between data/MC and plot it
	batch3Podiff, batch3Posigma_diff= ratiodiff(Pobatch3_hist,SUM2,Pobatch3_datahist,SUM2_2)
	Plot_1D_error(Pobatch3binsx,batch3Podiff, fig2, Poax2,None, batch3Posigma_diff,'0',ylogscale = False,label="Batch3 Po")
	 


	batch3_Biax.legend()
	batch3_Biax.set_xlabel("tres")
	Biax2.legend()
	Biax2.set_xlabel("tres")
	Biax2.set_ylabel("MC/Data")
	batch3_Poax.legend()
	batch3_Poax.set_xlabel("tres")
	Poax2.legend()
	Poax2.set_xlabel("tres")
	Poax2.set_ylabel("MC/Data")
	fig.show()
	fig2.show()
	

	# *************** initial setup for batch4 plot
	fig3, (batch4_Biax, Biax) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)
	fig4, (batch4_Poax, Poax) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)     
	
	Bibatch4_hist, SUM3 = tres_hist_plot(Bitres_batch4,fig3,batch4_Biax,'blue','MC/Bi/batch4')
	Bibatch4_datahist, Bibatch4_datahisterr, Bibatch4binsx, SUM3_2= tres_hist(Bitres_batch4data)
	Bibatch4binsx = (Bibatch4binsx[1:]+Bibatch4binsx[:-1])/2.
	Plot_1D_error(Bibatch4binsx,Bibatch4_datahist, fig3, batch4_Biax,None, Bibatch4_datahisterr,'0',ylogscale = False,label="data/Bi/batch4")
	# calculate the diff between data/MC and plot it
	batch4Bidiff, batch4Bisigma_diff= ratiodiff(Bibatch4_hist,SUM3,Bibatch4_datahist,SUM3_2)
	Plot_1D_error(Bibatch4binsx,batch4Bidiff, fig3, Biax,None, batch4Bisigma_diff,'0',ylogscale = False,label="Batch4 Bi")


	Pobatch4_hist, SUM4 = tres_hist_plot(Potres_batch4,fig4,batch4_Poax,'blue','MC/po/batch4')
	Pobatch4_datahist, Pobatch4_datahisterr, Pobatch4binsx, SUM4_2= tres_hist(Potres_batch4data)
	Pobatch4binsx = (Pobatch4binsx[1:]+Pobatch4binsx[:-1])/2.
	Plot_1D_error(Pobatch4binsx,Pobatch4_datahist, fig4, batch4_Poax,None, Pobatch4_datahisterr,'0',ylogscale = False,label="data/Po/batch4")
	# calculate the diff between data/MC and plot it
	batch4Podiff, batch4Posigma_diff= ratiodiff(Pobatch4_hist,SUM4,Pobatch4_datahist,SUM4_2)
	Plot_1D_error(Pobatch4binsx,batch4Podiff, fig4, Poax,None, batch4Posigma_diff,'0',ylogscale = False,label="Batch4 Po")
	 


	batch4_Biax.legend()
	batch4_Biax.set_xlabel("tres")
	Biax.legend()
	Biax.set_xlabel("tres")
	Biax.set_ylabel("MC/Data")
	batch4_Poax.legend()
	batch4_Poax.set_xlabel("tres")
	Poax.legend()
	Poax.set_xlabel("tres")
	Poax.set_ylabel("MC/Data")
	fig3.show()
	fig4.show()
	
	#  Compare different batch MC
	## fig5: Bi 
	fig5, (axBi5, axBi5_2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)
	Bibatch3_hist, SUM1 = tres_hist_plot(Bitres_batch3_truth,fig5,axBi5,'blue','MC/Bi/batch3')
	Bibatch4_hist, SUM3 = tres_hist_plot(Bitres_batch4_truth,fig5,axBi5,'red', 'MC/Bi/batch4')
	Bidiff, Bisigma_diff= ratiodiff(Bibatch3_hist,SUM1,Bibatch4_hist, SUM3)
	Plot_1D_error(Bibatch4binsx,Bidiff, fig5, axBi5_2,None, Bisigma_diff,'0',ylogscale = False)


	## Po
	fig6, (axPo6, axPo6_2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)
	Pobatch4_hist, SUM4 = tres_hist_plot(Potres_batch4_truth,fig6,axPo6,'blue','MC/po/batch4')
	Pobatch3_hist,SUM2 = tres_hist_plot(Potres_batch3_truth,fig6,axPo6,'red','MC/po/batch3')
	Podiff, Posigma_diff= ratiodiff(Pobatch3_hist,SUM1,Pobatch4_hist, SUM3)
	Plot_1D_error(Pobatch4binsx,Podiff, fig6, axPo6_2,None, Posigma_diff,'0',ylogscale = False)
	
	axBi5.legend()
	axPo6.legend()
	axBi5_2.set_xlabel("tres")
	axBi5_2.set_ylabel("Batch3/Batch4 Bi")
	axPo6_2.set_xlabel("tres")
	axPo6_2.set_ylabel("Batch3/Batch4 Po")
	

	fig5.show()
	fig6.show()

	

	#  Compare 0.1mg bisMSB v.s. 50mg bisMSB MC
	

	## fig7: Bi 
	fig7, (axBi7, axBi7_2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]}, sharex = True)
	Bi_histlow, SUM1 = tres_hist_plot(Bitres_low_truth,fig7,axBi7,'blue','MC/Bi/0.1mg')
	Bi_histhi , SUM3 = tres_hist_plot(Bitres_hi_truth ,fig7,axBi7,'red', 'MC/Bi/50mg')
	Bidifflow_hi, Bisigma_difflow_hi= ratiodiff(Bi_histlow,SUM1,Bi_histhi, SUM3)
	Plot_1D_error(Bibatch4binsx,Bidifflow_hi, fig7, axBi7_2,None, Bisigma_difflow_hi,'0',ylogscale = False)

	## fig8: Po
	fig8, (axPo8, axPo8_2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)
	Po_histlow, SUM1 = tres_hist_plot(Potres_low_truth,fig8,axPo8,'blue','MC/Po/0.1mg')
	Po_histhi , SUM3 = tres_hist_plot(Potres_hi_truth ,fig8,axPo8,'red', 'MC/Po/50mg')
	Podifflow_hi, Posigma_difflow_hi= ratiodiff(Po_histlow,SUM1,Po_histhi, SUM3)
	Plot_1D_error(Pobatch4binsx,Podifflow_hi, fig8, axPo8_2,None, Posigma_difflow_hi,'0',ylogscale = False)

	axBi7.legend()
	axPo8.legend()
	axBi7_2.set_xlabel("tres")
	axBi7_2.set_ylabel("0.1mg/50mg Bi")
	axPo8_2.set_xlabel("tres")
	axPo8_2.set_ylabel("0.1mg/50mg Po")
	

	fig7.show()
	fig8.show()

	#  Compare Batch4 bisMSB v.s. 50mg bisMSB MC
	

	## fig9 Bi 
	fig9, (axBi9, axBi9_2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]}, sharex = True)
	Bi_histbatch4, SUM1 = tres_hist_plot(Bitres_batch4_truth,fig9,axBi9,'blue','MC/Bi/Batch4')
	Bi_histhi , SUM3 = tres_hist_plot(Bitres_hi_truth ,fig9,axBi9,'red', 'MC/Bi/50mg')
	Bidiff4_hi, Bisigma_diff4_hi= ratiodiff(Bi_histbatch4,SUM1,Bi_histhi, SUM3)
	Plot_1D_error(Bibatch4binsx,Bidiff4_hi, fig9, axBi9_2,None, Bisigma_diff4_hi,'0',ylogscale = False)

	## fig10: Po
	fig10, (axPo10, axPo10_2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]},  sharex = True)
	Po_histbatch4, SUM1 = tres_hist_plot(Potres_batch4_truth,fig10,axPo10,'blue','MC/Po/Batch4')
	Po_histhi , SUM3 = tres_hist_plot(Potres_hi_truth ,fig10,axPo10,'red', 'MC/Po/50mg')
	Podiff4_hi, Posigma_diff4_hi= ratiodiff(Po_histbatch4,SUM1,Po_histhi, SUM3)
	Plot_1D_error(Pobatch4binsx,Podiff4_hi, fig10, axPo10_2,None, Posigma_diff4_hi,'0',ylogscale = False)

	axBi9.legend()
	axPo10.legend()
	axBi9_2.set_xlabel("tres")
	axBi9_2.set_ylabel("0.1mg/50mg Bi")
	axPo10_2.set_xlabel("tres")
	axPo10_2.set_ylabel("0.1mg/50mg Po")
	

	fig9.show()
	fig10.show()

	# saving the file
	savepath = "/home/huangp/grid_search_tuning/Plots/Batch34Comparison/"
	fig.savefig( f"{savepath}Batch3Bi_MCData.png")
	fig2.savefig(f"{savepath}Batch3Po_MCData.png")
	fig3.savefig(f"{savepath}Batch4Bi_MCData.png")
	fig4.savefig(f"{savepath}Batch4Po_MCData.png")
	fig5.savefig(f"{savepath}Batch34Bi_MC.png")
	fig6.savefig(f"{savepath}Batch34Po_MC.png")
	fig7.savefig(f"{savepath}0.1vs50Bi_MC.png")
	fig8.savefig(f"{savepath}0.1vs50Po_MC.png")
	fig9.savefig(f"{savepath}Batch4vs50Bi_MC.png")
	fig10.savefig(f"{savepath}Batch4vs50Po_MC.png")

	input()









