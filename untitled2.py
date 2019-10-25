# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 07:41:23 2019

@author: Timothy
"""

# -*- coding: utf-8 -*-
"""
Program Name: graphic_gui3c.py
Created By: Timothy Beggs
Date Created: 9/23/2019

Objective: Produce a gui to quickly graph time series from BDS-LBD release tables

Input Files: BDS-LBD release tables- (see table_dict not limited to list but dependent on variables and categorical
             variables within tables defined by fvariableentry and catliststring). Data should be stored in folder specified by bdsdatadirectorystr
             msacodes_names.csv - MSA and State labeling files. Data should be stored in folder specified by lookupdirectorystr
            
Output Files: All output is stored in specified directory listed in "outdirectorystr"
"""

# -*- coding: utf-8 -*-


import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import argparse
import tkinter as tk
import numpy as np
import sys
import datetime as dt

#directory strings defaulted to app9 locations
bdsdatadirectorystr = '/data/lbd/bitsi/ewdwork/BDS_QA_Release_Tables/'
lookupdirectorystr =  '/data/lbd/bitsi/ewdwork/data/'
outdirectorystr= '/data/lbd/bitsi/ewdwork/output/'
datadirectorystr= '/data/lbd/bitsi/ewdwork/high_level_tables/'
vintagedirectorystr= '/data/lbd/bitsi/ewdwork/datatables2013/'

bdsdatadirectorystr = 'C:/Users/Timothy/Documents/ewdwork/datatables/'
lookupdirectorystr =  'C:/Users/Timothy/Documents/ewdwork/data'
outdirectorystr= 'C:/Users/Timothy/Documents/ewdwork/output/'


#function to pass multiple functions to single object
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

class qaGUI:
    def __init__ (self, window):
        self.window = window
        #to change later
        qaGUI.vdd =tk.StringVar()
        if qaGUI.vdd.get()=="":
            qaGUI.bd = bdsdatadirectorystr
        #qaGUI.bd = bdsdatadirectorystr
        qaGUI.check = 0
        #function to close GUI
        def close_all():
            window.destroy()
           
        #function to ill listboxes
        def fill_listbox(self,list_box, vtable):
            self.len_max = 0
            for i, j in zip(range(len(vtable)), vtable):
                if len(j) > self.len_max:
                    self.len_max = len (j)
                list_box.insert(i,str(j))
               
        #get choices from listboxes
        def get_choices(pwin, listbox, nvariable):
            ndex = listbox.curselection()
            values = [listbox.get(x) for x in ndex]
            setattr(qaGUI, nvariable, values)
           
        #handle closing GUI early and terminate python kernal
        def on_closing(self):
            raise SystemExit
            
        #empty list box
        def clear_list(listbox):
            listbox.delete(0, tk.END)
        
        #edit defualt directory
        def edit_folder(pwin, listbox):
            def close_par(pwin):
                if eod.get() !="":
                    qaGUI.bd=eod.get()
                var_par.withdraw()
                qaGUI.vdd.set(qaGUI.bd)
                clear_list(listbox)
                pwin.deiconify()
                update_dd(self)
                fill_listbox(self, listbox, self.vtable)
            pwin.withdraw()
            var_par = tk.Toplevel()
            var_par.protocol("WM_DELETE_WINDOW", on_closing)
            var_par.grid_columnconfigure(0,weight=1)
            var_par.grid_columnconfigure(1,weight=1)
            var_par.grid_rowconfigure(0,weight=1)
            var_par.grid_rowconfigure(1,weight=1)
            
            lod = tk.Label(var_par, text="Enter New Input Directory:", anchor="w",font="Arial 10")
            lod.grid(row=5,column=0)
            eod = tk.Entry(var_par)
            eod.grid(row=5,column=1, sticky='ew')

            buttonv = tk.Button(var_par, text = "Submit", command = lambda: close_par(pwin))
            buttonv.grid(row=6,column=0, columnspan=2)
        
        #dynamically update table list
        def update_dd(self):
            table_dict=table_dict_base.copy()
            files = [f for f in os.listdir(qaGUI.bd) if os.path.isfile(os.path.join(qaGUI.bd,f))]
            for f in list(table_dict.keys()):
                if f not in files:
                    del table_dict[f]   
            table_dict_values = [table_dict[i][0] for i in table_dict.keys()]
            self.vtable = table_dict_values
        
        #window for table selection
        def table_selection(self, pwin):
            pwin.withdraw()
           
            table_select = tk.Toplevel(window)
           
            update_dd(self)
            
            print(self.vtable)
            
            self.labelt = tk.Label(table_select, text="Select Tables:", anchor="w", font="Arial 12 bold")
            self.s = tk.Scrollbar(table_select)
            self.labelt.grid(row=0,column=0,sticky='nsew')
            self.s.grid(row=2,column=1,sticky='ns')
           
            self.table_list_box = tk.Listbox(table_select, selectmode = "single", listvariable = self.vtable)
            fill_listbox(self, self.table_list_box, self.vtable)
               
            self.table_list_box.grid(row=2, column = 0, sticky = 'nsew')
            qaGUI.e = tk.Entry(table_select, width=self.len_max)
            self.e.grid(row=1,column=0, sticky='nsew')
           
            self.check = tk.Checkbutton(table_select, text = "Plot all selections on one graph", variable = qaGUI.check)
            self.check.grid(row=4, column=0)
           
            self.button1 = tk.Button(table_select, text = "Edit Input Directory", command = lambda: edit_folder(table_select, self.table_list_box))
            self.button1.grid(row=6,column=0)
            self.button = tk.Button(table_select, text = "Next", command = close_all)
            self.button.grid(row=7,column=0)
        
        table_selection(self, window)
   

         
table_dict_base = {    'bds_f_all_release.csv': ['bds_f_all_release', 1]        ,
    'bds_e_all_release.csv': ['bds_e_all_release', 2]        ,
    'bds_f_sic_release.csv': ['bds_f_sic_release', 3]        ,
    'bds_e_sic_release.csv': ['bds_e_sic_release', 4]        ,
    'bds_f_sz_release.csv': ['bds_f_sz_release', 5]        ,
    'bds_e_sz_release.csv': ['bds_e_sz_release', 6]        ,
    'bds_f_isz_release.csv': ['bds_f_isz_release', 7]        ,
    'bds_e_isz_release.csv': ['bds_e_isz_release', 8]        ,
    'bds_f_age_release.csv': ['bds_f_age_release', 9]        ,
    'bds_e_age_release.csv': ['bds_e_age_release', 10]        ,
    'bds_f_st_release.csv': ['bds_f_st_release', 11]        ,
    'bds_e_st_release.csv': ['bds_e_st_release', 12]        ,
    'bds_f_metrononmetro_release.csv': ['bds_f_metrononmetro_release', 13]        ,
    'bds_f_msa_release.csv': ['bds_f_msa_release', 14]        ,
    'bds_e_msa_release.csv': ['bds_e_msa_release', 15]        ,
    'bds_f_agesz_release.csv': ['bds_f_agesz_release', 16]        ,
    'bds_e_agesz_release.csv': ['bds_e_agesz_release', 17]        ,
    'bds_f_ageisz_release.csv': ['bds_f_ageisz_release', 18]        ,
    'bds_e_ageisz_release.csv': ['bds_e_ageisz_release', 19]        ,
    'bds_f_agesic_release.csv': ['bds_f_agesic_release', 20]        ,
    'bds_e_agesic_release.csv': ['bds_e_agesic_release', 21]        ,
    'bds_f_agemetrononmetro_release.csv': ['bds_f_agemetrononmetro_release', 22]        ,
    'bds_f_agemsa_release.csv': ['bds_f_agemsa_release', 23]        ,
    'bds_f_agest_release.csv': ['bds_f_agest_release', 24]        ,
    'bds_e_agest_release.csv': ['bds_e_agest_release', 25]        ,
    'bds_f_szsic_release.csv': ['bds_f_szsic_release', 26]        ,
    'bds_e_szsic_release.csv': ['bds_e_szsic_release', 27]        ,
    'bds_f_szmetrononmetro_release.csv': ['bds_f_szmetrononmetro_release', 28]        ,
    'bds_f_szmsa_release.csv': ['bds_f_szmsa_release', 29]        ,
    'bds_f_szst_release.csv': ['bds_f_szst_release', 30]        ,
    'bds_e_szst_release.csv': ['bds_e_szst_release', 31]        ,
    'bds_f_iszsic_release.csv': ['bds_f_iszsic_release', 32]        ,
    'bds_e_iszsic_release.csv': ['bds_e_iszsic_release', 33]        ,
    'bds_f_iszmetrononmetro_release.csv': ['bds_f_iszmetrononmetro_release', 34]        ,
    'bds_f_iszst_release.csv': ['bds_f_iszst_release', 35]        ,
    'bds_e_iszst_release.csv': ['bds_e_iszst_release', 36]        ,
    'bds_f_agesz_sic_release.csv': ['bds_f_agesz_sic_release', 37]        ,
    'bds_e_agesz_sic_release.csv': ['bds_e_agesz_sic_release', 38]        ,
    'bds_f_agesz_st_release.csv': ['bds_f_agesz_st_release', 39]        ,
    'bds_e_agesz_st_release.csv': ['bds_e_agesz_st_release', 40]        ,
    'bds_f_ageszmetrononmetro_release.csv': ['bds_f_ageszmetrononmetro_release', 41]        ,
    'bds_f_agesz_msa_release.csv': ['bds_f_agesz_msa_release', 42]        ,
    'bds_f_ageisz_sic_release.csv': ['bds_f_ageisz_sic_release', 43]        ,
    'bds_e_ageisz_sic_release.csv': ['bds_e_ageisz_sic_release', 44]        ,
    'bds_f_ageisz_st_release.csv': ['bds_f_ageisz_st_release', 45]        ,
    'bds_e_ageisz_st_release.csv': ['bds_e_ageisz_st_release', 46]        ,
    'bds_f_ageiszmetro_release.csv': ['bds_f_ageiszmetro_release', 47]        ,
    'bds_f_ageszmetro_state_release.csv': ['bds_f_ageszmetro_state_release', 48]        ,
    'bds_f_ageiszmetro_state_release.csv': ['bds_f_ageiszmetro_state_release', 49]        }     

table_dict=table_dict_base.copy()

master = tk.Tk()
window = qaGUI(master)
tk.mainloop()