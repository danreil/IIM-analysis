# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:06:42 2020
Code for getting lymphocyte cell counts per ROI 
Similar to analysis_CD68.py but will need to get the ROI cell counts first
from each HistView text file in each ROI subdirectory. Then write those to
a excel file like CD68 is done
see cell_count_plotting for the plotting routines for this data, trying to keep it more modular
@author: danre
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def read_HistView(path):
    """
    path is absolute path of the HistView txt file
    iterate over all ROIs and all biopsys calling this function everytime, put results in dataframe
    return: relevant data from that ROI (just cell counts right now)
    """
    try:                    #catch missing files with try...except
        with open(path) as f:
            data=f.readlines()
            T_area=data[6].split()
            B_area=data[11].split()
            T_area=T_area[2:]
            B_area=B_area[2:]
            T_area=[int(i) for i in T_area]
            B_area=[int(i) for i in B_area]
            T_area_arr=np.array(T_area)
            B_area_arr=np.array(B_area)
            T_area_valid=T_area_arr[(T_area_arr>area_min) & (T_area_arr<area_max)]
            B_area_valid=B_area_arr[(B_area_arr>area_min) & (B_area_arr<area_max)]
            cell_counts=np.array([len(T_area_valid),len(B_area_valid)])
    except OSError:
        cell_counts=np.array([0,0])
    return cell_counts

def write_df_to_excel(directory, filename, sheet, df):
    """
    generate a single sheet excel file in directory called filename from the pandas dataframe df
    return: the full path to the file
    Note: Once a workbook has been saved it is not possible write further data without rewriting the whole workbook.
    """
    path=os.path.join(directory,filename)
    df.to_excel(path,sheet_name=sheet)
    return path


#paramters for write_df_to_excel: where I want to save it, sheet name, filename
save_dir=r'C:\Users\danre\Documents\UChicago\SciPy_analysis'
save_file=r'Lymphocyte_cell_counts.xlsx'
save_sheet=r'CD4_CD8_CD20'


#min and max cell areas           
area_min=175
area_max=3500

source_dir=r'C:\Users\danre\Documents\2HistViewData\Lymphocytes'
DM_biopsies=[13723,14106,13592,14873,14430,15512,14933]
IBM_biopsies=[13633,13871,13690,14162,14595]
Normal_biopsy=[14288]
biopsies=DM_biopsies+IBM_biopsies+Normal_biopsy  #list of all biopsies
disease=7*'DM '.split() + 5*'IBM'.split()+1*'Normal'.split()
DM_ROIs=[47,33,37,50,46,19,44]
IBM_ROIs=[52,48,35,14,50]
Normal_ROI=[50]
ROI_nums=DM_ROIs+IBM_ROIs+Normal_ROI
file_base='2HistViewData_'
cell_type=['_4_20','_8_20']  #change cell type option manually for now

countsCD4_df=pd.DataFrame(columns=['Biopsy','Disease','ROI','CD4','CD20'])
countsCD8_df=pd.DataFrame(columns=['Biopsy','Disease','ROI','CD8','CD20'])
i=0  #biopsy number index
j=0  #cell type index (4 and 20 or 8 and 20)
running_idx=0

for j in range(len(cell_type)):
    i=0 #set i (biopsy index) and running_idx back to 0 for each new cell_type
    running_idx=0
    for biopsy in biopsies:
        biopsy_str=str(biopsy)+cell_type[j]   #biopsy concat cell type for path name
        for ROI in range(1,ROI_nums[i]+1):
            path_base=os.path.join(source_dir,str(biopsy),biopsy_str,str(ROI))
            file_name=file_base+str(ROI)+'.txt'
            file_path=os.path.join(path_base,file_name) #path for read_HistView function
            counts=read_HistView(file_path) #CD4 (or CD8) and CD20 counts 
            #add all data to dataframe, with each biopsy and all its counts info in seperate columns
            if j==0:
                countsCD4_df.loc[running_idx]=list([biopsies[i],disease[i],ROI,counts[0],counts[1]])
                running_idx+=1
            elif j==1:
                countsCD8_df.loc[running_idx]=list([biopsies[i],disease[i],ROI,counts[0],counts[1]])
                running_idx+=1
        i+=1    #iterate over biopsy index

CD8_ser=countsCD8_df.loc[:,'CD8'] 
counts_df=countsCD4_df
counts_df['CD8']=CD8_ser

#call function to save the dataframe into excel file
write_df_to_excel(save_dir,save_file,save_sheet,counts_df)
            
        

            
            
            
        

    
    
    