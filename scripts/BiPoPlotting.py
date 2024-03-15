import numpy as np
import matplotlib.pyplot as plt

Batch3_MCpath   = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/Batch3labppo_2p2_bismsb_Table/"
Batch4_MCpath   = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning/residuals/Batch4labppo_2p2_bismsb_Table/"
Datapath        = "/data/snoplus2/weiiiii/BiPo214_tune_cleaning/detector_data/"
def tres_hist_plot(histarray,fig,ax,color=None,density=True,label=None):
	myhist, xbins = np.histogram(histarray,bins=355,range=[-5.,350.])
	SUM = np.sum(myhist)
	hist, xbins,_ = ax.hist(histarray,bins=355,range=[-5.,350.],fill = False, label =label, color = color,histtype="step", density=density,log=True)
	return hist, SUM
def tres_hist(histarray,density = True):
	returnarr,binsx = np.histogram(histarray,bins=355,range=[-5.,350.])
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
	print(np.sqrt( ( (MC_err_norm/MC)**2 )+( (Data_err_norm/Data)**2 ) ) )
	return np.abs(MC/Data), np.sqrt( ( (MC_err_norm/MC)**2 )+( (Data_err_norm/Data)**2 ) )
if __name__ == "__main__":
	
	Bitres_batch3 = np.load(f"{Batch3_MCpath}Bi214/5.0.npy")
	Potres_batch3 = np.load(f"{Batch3_MCpath}Po214/4.1.npy")

	Bitres_batch3data = np.load(f"{Datapath}Bi214_bismsb_batch3.npy",allow_pickle=True)
	Potres_batch3data = np.load(f"{Datapath}Po214_bismsb_batch3.npy",allow_pickle=True)
	#Bitres_batch3data = np.concatenate(Bitres_batch3data); #Potres_batch3data = np.concatenate(Potres_batch3data)


	Bitres_batch4 = np.load(f"{Batch3_MCpath}Bi214/5.0.npy")
	Potres_batch4 = np.load(f"{Batch3_MCpath}Po214/4.1.npy")
	
	Bitres_batch4data = np.load(f"{Datapath}bismsb_batch4_bi_4000.0.npy",allow_pickle=True)
	Potres_batch4data = np.load(f"{Datapath}bismsb_batch4_po_4000.0.npy",allow_pickle=True)
	#Bitres_batch4data = np.concatenate(Bitres_batch4data); Potres_batch3data = np.concatenate(Potres_batch4data)

	# *************** initial setup for Batch3 plots
	fig, (batch3_Biax, Biax2)  = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]})
	fig2, (batch3_Poax, Poax2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]})
	
	Bibatch3_hist, SUM1 = tres_hist_plot(Bitres_batch3,fig,batch3_Biax,'blue','MC/Bi/batch3')
	Bibatch3_datahist, Bibatch3_datahisterr, Bibatch3binsx, SUM1_1= tres_hist(Bitres_batch3data)
	Bibatch3binsx = (Bibatch3binsx[1:]+Bibatch3binsx[:-1])/2.
	Plot_1D_error(Bibatch3binsx,Bibatch3_datahist, fig, batch3_Biax,None, Bibatch3_datahisterr,'0',ylogscale = True,label="data/Bi/batch3")
	# calculate the diff between data/MC and plot it
	batch3Bidiff, batch3Bisigma_diff= ratiodiff(Bibatch3_hist,SUM1,Bibatch3_datahist,SUM1_1)
	Plot_1D_error(Bibatch3binsx,batch3Bidiff, fig, Biax2,None, batch3Bisigma_diff,'0',ylogscale = True,label="Batch3 Bi")
	 
	
	Pobatch3_hist,SUM2 = tres_hist_plot(Potres_batch3,fig2,batch3_Poax,'blue','MC/po/batch3')
	Pobatch3_datahist, Pobatch3_datahisterr, Pobatch3binsx, SUM2_2= tres_hist(Potres_batch3data)
	Pobatch3binsx = (Pobatch3binsx[1:]+Pobatch3binsx[:-1])/2.
	Plot_1D_error(Pobatch3binsx,Pobatch3_datahist, fig2, batch3_Poax,None, Pobatch3_datahisterr,'0',ylogscale = True,label="data/Po/batch3")
	# calculate the diff between data/MC and plot it
	batch3Podiff, batch3Posigma_diff= ratiodiff(Pobatch3_hist,SUM2,Pobatch3_datahist,SUM2_2)
	Plot_1D_error(Pobatch3binsx,batch3Podiff, fig2, Poax2,None, batch3Posigma_diff,'0',ylogscale = True,label="Batch3 Po")
	 


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
	fig3, (batch4_Biax, Biax) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]})
	fig4, (batch4_Poax, Poax) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]})     
	
	Bibatch4_hist, SUM3 = tres_hist_plot(Bitres_batch4,fig3,batch4_Biax,'blue','MC/Bi/batch4')
	Bibatch4_datahist, Bibatch4_datahisterr, Bibatch4binsx, SUM3_2= tres_hist(Bitres_batch4data)
	Bibatch4binsx = (Bibatch4binsx[1:]+Bibatch4binsx[:-1])/2.
	Plot_1D_error(Bibatch4binsx,Bibatch4_datahist, fig3, batch4_Biax,None, Bibatch4_datahisterr,'0',ylogscale = True,label="data/Bi/batch4")
	# calculate the diff between data/MC and plot it
	batch4Bidiff, batch4Bisigma_diff= ratiodiff(Bibatch4_hist,SUM3,Bibatch4_datahist,SUM3_2)
	Plot_1D_error(Bibatch4binsx,batch4Bidiff, fig3, Biax,None, batch4Bisigma_diff,'0',ylogscale = True,label="Batch4 Bi")


	Pobatch4_hist, SUM4 = tres_hist_plot(Potres_batch4,fig4,batch4_Poax,'blue','MC/po/batch4')
	Pobatch4_datahist, Pobatch4_datahisterr, Pobatch4binsx, SUM4_2= tres_hist(Potres_batch4data)
	Pobatch4binsx = (Pobatch4binsx[1:]+Pobatch4binsx[:-1])/2.
	Plot_1D_error(Pobatch4binsx,Pobatch4_datahist, fig4, batch4_Poax,None, Pobatch4_datahisterr,'0',ylogscale = True,label="data/Po/batch4")
	# calculate the diff between data/MC and plot it
	batch4Podiff, batch4Posigma_diff= ratiodiff(Pobatch4_hist,SUM4,Pobatch4_datahist,SUM4_2)
	Plot_1D_error(Pobatch4binsx,batch4Podiff, fig4, Poax,None, batch4Posigma_diff,'0',ylogscale = True,label="Batch4 Po")
	 


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
	fig5, (axBi5, axBi5_2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]})
	Bibatch3_hist, SUM1 = tres_hist_plot(Bitres_batch3,fig5,axBi5,'blue','MC/Bi/batch3')
	Bibatch4_hist, SUM3 = tres_hist_plot(Bitres_batch4,fig,batch4_Biax,'blue','MC/Bi/batch4')
	


	## Po
	fig6, (axPo6, axPo6_2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [3, 1]})
	Pobatch4_hist, SUM4 = tres_hist_plot(Potres_batch4,fig4,batch4_Poax,'blue','MC/po/batch4')
	Pobatch3_hist,SUM2 = tres_hist_plot(Potres_batch3,fig2,batch3_Poax,'blue','MC/po/batch3')
	
	input()









