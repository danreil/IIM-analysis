# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:55:54 2020

DC cell count data importing, plot in another routine probably
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


def read_DC_excel(path,sheet):
    """
    import DC cell count data into a pandas dataframe.
    path is absolute path of the DC data, sheet is the sheet number in excel doc.
    return the dataframe
    """
    header_list=[0,1,2]  # which rows to use for multi-index header
    index_col=0
    DC_df=pd.read_excel(path,sheet,header=header_list,index_col=0)
    return DC_df

def find_new_name(old_name):
    """
    For renaming columns in the dataframe, returns '14263' from '14263_IBM' for example
    just manually returning the first 5 characters
    """
    return old_name[0:5]

def write_df_to_excel(path, sheet, df):
    """
    generate a single sheet excel file in directory called filename from the pandas dataframe df
    return: the full path to the file
    Note: Once a workbook has been saved it is not possible write further data without rewriting the whole workbook.
    """
    #path=os.path.join(directory,filename)
    df.to_excel(path,sheet)
    return path

#parameters for loading original DC xlsx file into a dataframe using read_DC_excel
source_dir=r'C:\Users\danre\Documents\UChicago\SciPy_analysis\Excel_Files'
source_file=r'DC_counts.xlsx'
source_path=os.path.join(source_dir,source_file)
sheet_num=1
DC_df=read_DC_excel(source_path,sheet_num) # read DC counts into a dataframe


#rename each biopsy columns name to just biopsy number (so eg. 14263_IBM to 14263)
old_names=[item[0] for item in DC_df.columns]
DC_df.rename(columns={old_name:find_new_name(old_name) for old_name in old_names},inplace=True)

DC_df_long=DC_df.melt()  # convert to long form
DC_df_long.columns=['Biopsy','Disease','Cell Type','Cell Count']  #rename columns

#drop NA rows, then reset indices to columns
DC_df_long_dropna=DC_df_long.dropna() 
DC_df_long=DC_df_long_dropna.reset_index().drop(columns='index')

#groupby disease for long form data
dis_group=DC_df_long.groupby('Disease')
IBM_df=dis_group.get_group('IBM')
DM_df=dis_group.get_group('DM')
"""get number of mDCs and pDCs from each disease. Can change methodology later,
   but for now, mDCs=BDCA1+CD11c+double positive of both
   pDCs=BDCA2+CD123+double positive
"""
#cell_group_IBM=IBM_df.groupby('Cell Type')
#cell_group_DM=DM_df.groupby('Cell Type')

def cell_group_consolidation(df,group,disease=None):
    """input a dataframe (either DM_df or IBM_df, maybe the full DC_df_long)
    and give the cell group type (mDC or pDC) and for convience specify the disease for that df
    return: dataframe specific to that disease with only cell counts for either pDC or mDC
    and rename all values of Cell Type column to mDC or pDC appropriately
    """
    mdc_cells=['BDCA1','CD11c','DB-B1-11c']
    pdc_cells=['BDCA2','CD123','DB-B2-123']
    if group=='mdc':
        mask=(df['Cell Type']=='BDCA1') | (df['Cell Type']=='CD11c') | (df['Cell Type']=='DB-B1-11c')
        df_cell=df[mask]
        df_ret=df_cell.replace(mdc_cells,['mDC','mDC','mDC'])
    elif group=='pdc':
        mask=(df['Cell Type']=='BDCA2') | (df['Cell Type']=='CD123') | (df['Cell Type']=='DB-B2-123')
        df_cell=df[mask]
        df_ret=df_cell.replace(pdc_cells,['pDC','pDC','pDC'])
    return df_ret

#dataframes for the 4 combinations of DM and IBM and pDC and mDC
DM_pdc=cell_group_consolidation(DM_df,'pdc')
DM_mdc=cell_group_consolidation(DM_df,'mdc')
IBM_pdc=cell_group_consolidation(IBM_df,'pdc')
IBM_mdc=cell_group_consolidation(IBM_df,'mdc')

#now combine these (try vertical concat first)
IBM_df_con=pd.concat([IBM_pdc,IBM_mdc]).drop(columns='Biopsy')
DM_df_con=pd.concat([DM_pdc,DM_mdc]).drop(columns='Biopsy')
DC_df_con=pd.concat([IBM_df_con,DM_df_con])

#in case its useful, a numpy array of all cell counts
cell_count_arr=DC_df_con['Cell Count'].to_numpy() 

#try different plotting routines
sns.set(context='paper',style='ticks',font_scale=1.5)
fig,ax1=plt.subplots(1,1,figsize=(8,6))
sns.violinplot(x='Disease',y='Cell Count',hue='Cell Type',data=DC_df_con,legend_out=True)
ax1.set(xlabel='',title='Dendritic Cell Counts')
sns.despine(ax=ax1)
plt.legend(title='Cell Type',loc='upper right')
fig,axes=plt.subplots(1,2,figsize=(12,8))
sns.barplot(x='Disease',y='Cell Count',hue='Cell Type',data=DC_df_con,ax=axes[0])
sns.stripplot(x='Disease',y='Cell Count',hue='Cell Type',data=DC_df_con,ax=axes[1],dodge=True,alpha=.07,jitter=.3)
plt.setp(plt.gcf().get_axes(),xlabel='')
#ax2.set(xlabel='',title='Dendritic Cell Counts')
#sns.despine(ax=ax2)

plt.legend(title='Cell Type',loc='upper right')
#facet grid for histograms (adding a boxplot, from Stackflow-add mean and variability...)
"""try manually making subplots (without boxplot) for 2 rows and 2 columns
def dist_boxplot(x, **kwargs):
    #ax = sns.distplot(x, hist_kws=dict(alpha=0.2))
    #ax2=ax.twinx()
    #sns.boxplot(x=x,ax=ax2)
    f, (ax_box,ax_hist)=plt.subplots(2,sharex=True,gridspec_kw={"height_ratios": (.15, .85)})
    sns.boxplot(x=x,ax=ax_box)
    sns.distplot(x=x,ax=ax_hist)
    ax_box.set(x_label='')
    
g=sns.FacetGrid(DC_df_con,row='Disease',col='Cell Type',margin_titles=True,height=5,aspect=1)
bins=np.linspace(0,8,12)
g.map(dist_boxplot,'Cell Count')
"""
bins=8
f, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
sns.distplot(IBM_pdc['Cell Count'],ax=axes[0,0],bins=bins,axlabel='IBM pDC')
sns.distplot(IBM_mdc['Cell Count'],ax=axes[0,1],bins=bins,axlabel='IBM mDC')
sns.distplot(DM_pdc['Cell Count'],ax=axes[1,0],bins=bins,axlabel='DM pDC')
sns.distplot(DM_mdc['Cell Count'],ax=axes[1,1],bins=bins,axlabel='DM mDC')
f.suptitle('Histogram Grid for Cell Counts',fontsize=24)


#write DC_df_long to excel doc, then read that excel doc into a different dataframe
#save_dir=r'C:\Users\danre\Documents\UChicago\SciPy_analysis\Excel_Files'
#save_file=r'DC_cell_counts_long.xlsx'
#save_path=os.path.join(save_dir,save_file)
#save_sheet=r'longform from python'
#write_df_to_excel(save_path, save_sheet, DC_df_long_dropna)
#DC_df_long1=pd.read_excel(save_path, save_sheet)

"""
#get summary statistics for each cell type for each biopsy
stats=DC_df.describe()
means=stats.loc['mean',:]  #Series object of cell count means for all biopsies and cell types
means=means.to_frame()
mean_counts_groupby_dis=means.groupby(['Disease','Cell Type']).mean() #cell count means over Disease and Type
sem_counts_grouby_dis=means.groupby(['Disease','Cell Type']).sem() #cell count sem's over Disease and Type

#next steps... grouped plots of means and sems (and/or box and whisker plots) with disease as groups
#then, try to do histograms, maybe overlaid... see pandas visualization section on docs

#note:see if plt.hist(histtype='step') looks better than overlaying transperent histograms
"""

 



