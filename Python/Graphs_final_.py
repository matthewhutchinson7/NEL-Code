"""
Created on Wed Nov 24 11:23:50 2021

@author: HutchinsonM
"""
#-------------------------------------------------------------------------

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as tkr
from palettable.matplotlib import Inferno_5 as i5

#-------------------------------------------------------------------------

# shows attendances for each financial year plotted on the same axes
def fyears_overlayed(axes, data, labels):
   axes.set_xlabel('Month',fontweight='bold')
   axes.set_ylabel('Hospital Attendances',fontweight='bold')
   i=1
   for d in data:
       d.loc[:,'Month'] = pd.Categorical(d['Month'],['04','05','06','07',
                                                    '08','09','10','11',
                                                    '12','01','02','03'])
       d = d.groupby('Month',as_index=False).count()
       d = d.sort_values('Month')
       axes.plot(d['Month'],d['SK_EncounterID'],color=i5.mpl_colors[i],
             label=labels[i-1])
       i += 1
    
   axes.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=3, mode="expand", borderaxespad=0.)
   axes.spines['right'].set_visible(False)
   axes.spines['top'].set_visible(False)
   axes.yaxis.set_ticks_position('left')
   axes.xaxis.set_ticks_position('bottom')
   axes.set_xticklabels(['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov',
                       'Dec','Jan','Feb','Mar'])
   axes.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x,
                                                p: format(int(x), ',')))
   return
    
    
# plots a time series of attendances for the whole time range    
def time_series(axes,data):
    monthly = data.groupby('YearMonth',as_index=False).count()
    monthly = monthly.sort_values('YearMonth')
    
    axes.plot(monthly['YearMonth'],monthly['SK_EncounterID'],
         color=i5.mpl_colors[2])
    axes.set_ylabel('Hospital Attendances',fontweight='bold')
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.yaxis.set_ticks_position('left')
    axes.xaxis.set_ticks_position('bottom')
    axes.get_yaxis().set_major_formatter(tkr.FuncFormatter(lambda x,
                                                p: format(int(x), ',')))
    axes.set_xticks([0,12,24,35])
    axes.set_xticklabels(['Apr 2018',' Apr 2019','Apr 2020','Mar 2021'])
    return


#-------------------------------------------------------------------------    

if __name__ == "__main__":
   
    sns.set_theme(style='whitegrid')
    ip = pd.read_excel('RandomDataIP.xlsx')
    ae = pd.read_excel('RandomDataAE.xlsx')

    f1,ax1=plt.subplots()
    f2,ax2=plt.subplots()
    f3,ax3=plt.subplots()
    f4,ax4=plt.subplots()
    
    # create month, year, and yearmonth columns for the data
    ae = ae.loc[ae['DiagnosisNumber']==1,:]
    ae.loc[:,'Month'] = ae['StartDate'].dt.month.astype(str)    
    ae.loc[:,'Month'] = ae['Month'].str.zfill(2)
    ae.loc[:,'Year'] = ae['StartDate'].dt.year.astype(str)
    ae.loc[:,'YearMonth'] = ae['Year'] + ' ' + ae['Month']
    ip = ip.loc[ip['DiagnosisNumber']==1,:]
    ip.loc[:,'Month'] = ip['AdmissionDate'].dt.month.astype(str)
    ip.loc[:,'Month'] = ip['Month'].str.zfill(2)
    ip.loc[:,'Year'] = ip['AdmissionDate'].dt.year.astype(str)
    ip.loc[:,'YearMonth'] = ip['Year'] + ' ' + ip['Month']

    #split data into financial years
    three_months = ['01','02','03']
    nine_months = ['04','05','06','07','08','09','10','11','12']
    ae_2018_19 = ae[(ae['Year'] == '2018') | ((ae['Year']=='2019') & 
                                (ae['Month'].isin(['01','02','03'])))]
    ae_2019_20 = ae[((ae['Year'] == '2019') & 
                (ae['Month'].isin(nine_months)))| ((ae['Year']=='2020') & 
                (ae['Month'].isin(three_months)))]
    ae_2020_21 = ae[((ae['Year'] == '2020') & 
                (ae['Month'].isin(nine_months)))
                 | ((ae['Year']=='2021') & 
                (ae['Month'].isin(three_months)))]
    ip_2019_20 = ip[((ip['Year'] == '2019') & 
                (ip['Month'].isin(nine_months))) | 
                ((ip['Year']=='2020') & (ip['Month'].isin(three_months)))]
    ip_2020_21 = ip[((ip['Year'] == '2020') & 
                (ip['Month'].isin(nine_months))) | ((ip['Year']=='2021') 
                & (ip['Month'].isin(three_months)))]

    #add the years to lists to iterate over in the graph creating functions
    ae_yr = [ae_2018_19,ae_2019_20,ae_2020_21]
    labels_ae = ['2018/19','2019/20','2020/21']
    ip_yr = [ip_2019_20,ip_2020_21]
    labels_ip = ['2019/20','2020/21']
    ip_after_2019 = pd.concat(ip_yr,ignore_index=True)

    #plot the graphs
    fyears_overlayed(ax1,ae_yr,labels_ae)
    fyears_overlayed(ax2,ip_yr,labels_ip)
    time_series(ax3,ae)
    time_series(ax4,ip_after_2019)

    plt.show()

