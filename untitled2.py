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
lookupdirectorystr =  'C:/Users/Timothy/Documents/ewdwork/data/'
outdirectorystr= 'C:/Users/Timothy/Documents/ewdwork/output/'


catlist =["fage4","ifsize","metro","fsize","state","sic1","msa","Fage4","Ifsize","Metro","Fsize","State","Sic1","Msa","age4","Age4","size","Size","isize","Isize"]

fvariable1=["Firms","Estabs","Emp","Denom","Estabs_Entry","Estabs_Exit","Job_Creation","Job_Creation_Births","Job_Creation_Continuers","Job_Destruction","Job_Destruction_Deaths","Job_Destruction_Continuers","Net_Job_Creation","Firmdeath_Firms","Firmdeath_Estabs","Firmdeath_Emp","Estabs_Continuers_Expanding","Estabs_Continuers_Contracting"]
 

#function to pass multiple functions to single object
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

class qaGUI:
    def __init__ (self, window):
        self.window = window
        qaGUI.check=tk.IntVar()
        qaGUI.multi = 0
        qaGUI.cat_selected = []
        qaGUI.cat_selected_match = []
        qaGUI.noselection = 0
        qaGUI.probselection = 0
        qaGUI.catlist = catlist
        #to change later
        qaGUI.vod =tk.StringVar()
        if qaGUI.vod.get()=="":
            qaGUI.od = outdirectorystr
        qaGUI.vod.set(qaGUI.od)
        qaGUI.vdd =tk.StringVar()
        if qaGUI.vdd.get()=="":
            qaGUI.bd = bdsdatadirectorystr
        qaGUI.vld =tk.StringVar()
        if qaGUI.vld.get()=="":
            qaGUI.ld = lookupdirectorystr
        #qaGUI.bd = bdsdatadirectorystr
        #qaGUI.check = 0
        #function to close GUI
        def close_all():
            window.destroy()
        
        #restart program will only work in linux
        def restart():
            python = sys.executable
            os.execl(python, python, * sys.argv)  
        
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
        def on_closing():
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
        
            
            self.labelt = tk.Label(table_select, text="Select One Table:", anchor="w", font="Arial 12 bold")
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
            self.button = tk.Button(table_select, text = "Next", command = lambda:combine_funcs(get_choices(table_select, self.table_list_box, "table_selections"), cat_selection(self, table_select, qaGUI.table_selections)))
            self.button.grid(row=7,column=0)
        
        #to update to new variables
        def var_window(self, pwin):
            #get listbox entries
            var_win = tk.Toplevel()
            var_win.protocol("WM_DELETE_WINDOW", on_closing)
            var_win.grid_columnconfigure(0,weight=1)
            var_win.grid_columnconfigure(1,weight=0)
            var_win.grid_rowconfigure(0,weight=1)
            var_win.grid_rowconfigure(1,weight=1)
            var_win.grid_rowconfigure(2,weight=0)
            var_win.grid_rowconfigure(3,weight=0)
            labelv = tk.Label(var_win, text="Select Variables:", anchor="w",font="Arial 12 bold")
            labelv.grid(row=0,column=0)
            sv = tk.Scrollbar(var_win)
            sv.grid(row=1,column=1,sticky='ns')
            fvariable2 = []
            fvariable4  = []
            for x in fvariable1:
                z = x.upper()
                y = z.lower()
                if x in list(qaGUI.d):
                    fvariable2.append(z)
                if y in list(qaGUI.d):
                    fvariable2.append(y)
            for k in range(0,len(qaGUI.cat_selected)):
                if "Young Incumbent Firms" in qaGUI.cat_selected[k]:
                    if "age" in qaGUI.x:
                        fvariable4 = ["firm_startup_rate", "employment-weighted_startup_rate"]
            if "all" in qaGUI.x:
                fvariable4 = ["firm_death_rate", "employment-weighted_exit_rate"]
            fvariable5 = ["shemp", "shdenom"]
            vvar=['All'] + fvariable2+fvariable4+fvariable5
            self.list_boxv = tk.Listbox(var_win, selectmode="multiple", listvariable=vvar)
            fill_listbox(self, self.list_boxv, vvar)
            self.list_boxv.grid(row=1,column=0,sticky='nsew')
            sv['command'] = self.list_boxv.yview
            self.list_boxv['yscrollcommand'] = sv.set
            self.list_boxv.config(width="0")
            framev = tk.Frame(var_win)
            framev.grid(row=2,column=0)

            
            buttona = tk.Button(var_win, text = "Submit", command = lambda:combine_funcs(get_choices(var_win, self.list_boxv, "selected_variables"), open_confirm(self,var_win)))
            buttona.grid(row=11,column=0, columnspan=1)
            buttonr = tk.Button(var_win, text = "Restart", command = restart)
            buttonr.grid(row=12,column=0, columnspan=1)
        
        def check(self, pwin,x,cat_vars, listboxWidgets):
            qaGUI.noselection = 0
            qaGUI.probselection = 0
            meetlen=len(listboxWidgets)
            check=0

            for q in listboxWidgets:

                ndex = q.curselection()
                selection = [q.get(y) for y in ndex]
                if ndex == ():
                    qaGUI.noselection = 1
                    pwin.destroy()
                    cat_selection(self, 0, qaGUI.table_selections)
                    break
                if "Young" in selection and "Young Incumbent Firms" in selection:
                    qaGUI.probselection += 1
                    if "Young Incumbent Firms" in selection:
                        qaGUI.probselection += 1
                        pwin.destroy()
                        cat_selection(self, 0, qaGUI.table_selections)
                        break
                else:
                    check +=1
            if check == meetlen:
                collection(self, pwin, x,cat_vars, listboxWidgets)
        def collection(self, pwin, x,cat_vars, listboxWidgets):
            for q in listboxWidgets:
                #get_choices(pwin, q, "cat_selected")
                ndex = q.curselection()
                selection = [q.get(y) for y in ndex]
                qaGUI.cat_selected.append(selection)

            for y in cat_vars:
                qaGUI.cat_selected_match.append([x,y])
            pwin.destroy()
            var_window(self, pwin)
        
        
        def cat_list(self, x):
            roll_vars = []
            if "fage4" in x:
                roll_vars = ["Young Incumbent Firms", "Young", "Old"]
            if "fsize" in x:
                roll_vars = ["Small", "Medium", "Large"]
            return roll_vars
        
        def cat_selection(self, pwin, y):
            qaGUI.multi = qaGUI.check.get()
            if pwin != 0:
                pwin.withdraw()
            qaGUI.x = y[0]
            qaGUI.d = pd.read_csv(qaGUI.bd+qaGUI.x+".csv")
           
            labelWidgets=[]
            listboxWidgets=[]
            scrollWidgets=[]

            cat_win = tk.Toplevel()
            cat_win.protocol("WM_DELETE_WINDOW", on_closing)
            
            cat_win.grid_columnconfigure(0,weight=1)
            cat_win.grid_columnconfigure(1,weight=1)
            cat_win.grid_rowconfigure(0,weight=1)
            cat_win.grid_rowconfigure(1,weight=1)
            cat_win.grid_rowconfigure(2,weight=1)
            cat_win.grid_rowconfigure(3,weight=1)
            cat_win.grid_rowconfigure(4,weight=1)

            cat_win.labelt = tk.Label(cat_win, text=str(qaGUI.x), anchor="w", font="Arial 12 bold")
            cat_win.labelt.grid(row=0,column=0,sticky='nsew')
            qaGUI.cat_vars = []
                
            for j in qaGUI.catlist:
                if j in list(qaGUI.d):
                    qaGUI.cat_vars.append(j)
            if qaGUI.cat_vars == []:
                collection(self, cat_win, qaGUI.x, qaGUI.cat_vars, listboxWidgets)
            else:
                for i,y in zip(range(0, len(qaGUI.cat_vars)),qaGUI.cat_vars):
                    u = qaGUI.d[y].unique()
                    cat_options = cat_list(self, y)
                    if qaGUI.cat_vars[i] in ["msa", "Msa"]:
                        qaGUI.lmsa=pd.read_csv(qaGUI.ld+"msacodes_names.csv")
                        qaGUI.lmsa["gui_label"] = qaGUI.lmsa["label"].astype(str)+" ("+qaGUI.lmsa["msa_num"].astype(str)+")"
                        lu = qaGUI.lmsa[qaGUI.lmsa["msa_num"].isin(u)]
                        u = lu["gui_label"]
                    if qaGUI.cat_vars[i] in ["state", "State"]:
                        qaGUI.lstate=pd.read_csv(qaGUI.ld+"state_fips_region_division.csv")
                        qaGUI.lstate["gui_label"] = qaGUI.lstate["state_name"].astype(str)+" ("+qaGUI.lstate["state_fips"].astype(str)+")"
                        lu = qaGUI.lstate[qaGUI.lstate["state_fips"].isin(u)]
                        u = lu["gui_label"]
                    if cat_options == []:
                        cat_options = u
                    labelWidgets.append(tk.Label(cat_win, text = qaGUI.cat_vars[i], anchor="w",font="Arial 10"))
                    listboxWidgets.append(tk.Listbox(cat_win, selectmode="multiple", exportselection=0))
                    scrollWidgets.append(tk.Scrollbar(cat_win))
                    for j,h in zip(range(len(cat_options)),cat_options):
                        listboxWidgets[-1].insert(j,str(h))
                    if i<6:
                        labelWidgets[-1].grid(row=2, column=i+i)
                        listboxWidgets[-1].grid(row=3, column=i+i,sticky='nsew')
                        scrollWidgets[-1].grid(row=3,column=i+i+1,sticky='ns')
                        scrollWidgets[-1]['command'] = listboxWidgets[-1].yview
                        listboxWidgets[-1].config(width="0",height=10)
                    else:
                        labelWidgets[-1].grid(row=4, column=i+i-12)
                        listboxWidgets[-1].grid(row=5, column=i+i-12,sticky='nsew')
                        scrollWidgets[-1].grid(row=5,column=i+i-11,sticky='ns')
                        scrollWidgets[-1]['command'] = listboxWidgets[-1].yview
                        listboxWidgets[-1].config(width="0",height=10)

                buttonb = tk.Button(cat_win, text = "Submit", command = lambda:check(self, cat_win, qaGUI.x,qaGUI.cat_vars, listboxWidgets))
                buttonb.grid(row=6,column=0, columnspan=1)
                buttonc = tk.Button(cat_win, text = "Restart", command = restart)
                buttonc.grid(row=7,column=0, columnspan=1)
                if qaGUI.noselection == 1:
                    labelb = tk.Label(cat_win, text="Please choose at least one option for each variable", anchor="w",font="Arial 12")
                    labelb.grid(row=8,column=0, columnspan =2)
                if qaGUI.probselection == 2:
                    labelb = tk.Label(cat_win, text="Overlapping Categories Chosen", anchor="w",font="Arial 12")
                    labelb.grid(row=9,column=0, columnspan =2)
                window.wait_window(cat_win)
                
            
                
        def open_confirm(self, pwin):
           # ndexv = pwin.list_boxv.curselection()
            #qaGUI.selected_variables=[owindow.list_boxv.get(x) for x in ndexv]
            pwin.withdraw()
            list_params = tk.Toplevel()
            list_params.protocol("WM_DELETE_WINDOW", on_closing)
            list_params.grid_columnconfigure(0,weight=1)
            list_params.grid_columnconfigure(1,weight=1)
            list_params.grid_rowconfigure(0,weight=1)
            list_params.grid_rowconfigure(1,weight=1)
            list_params.grid_rowconfigure(2,weight=1)
            list_params.grid_rowconfigure(3,weight=1)
            list_params.grid_rowconfigure(4,weight=1)
            list_params.grid_rowconfigure(5,weight=1)
            list_params.grid_rowconfigure(6,weight=1)
            list_params.grid_rowconfigure(7,weight=1)
            list_params.grid_rowconfigure(8,weight=1)
            list_params.grid_rowconfigure(9,weight=1)
            
            selected_variables = []
            if selected_variables == []:
                    selected_variables = "All"    
            if 'All' in selected_variables:
                selected_variables = "All"

            vod = tk.StringVar()

            #labelall = tk.Label(list_params, text="Current Selections:", anchor="w",font="Arial 12 bold")
            #labeldd = tk.Label(list_params, text="High Level Data Directory:", anchor="w",font="Arial 10")
            labelod = tk.Label(list_params, text="Out Directory:", anchor="w",font="Arial 10")
            
            #labelhda = tk.Entry(list_params, fg='grey',font="Arial 10",width=len(qaGUI.hdd.get()))
            labeloda = tk.Entry(list_params, fg='grey',font="Arial 10",width=len(qaGUI.vod.get()))
            
            vod.set(qaGUI.od)
            
            #labelall.grid(row=1,column=0)
            #labeldd.grid(row=3,column=0)
            labelod.grid(row=8,column=0)    

            # when typing on box for out directory
            def handle_focus_in(_):
                labeloda.delete(0,tk.END)
                labeloda.config(fg='black')
            # when select awau from box for out directory
            def handle_focus_out(_):
                labeloda.delete(0,tk.END)
                labeloda.config(fg='grey')
                labeloda.insert(0,qaGUI.vod.get())
            # default fill for out directory
            def handle_enter(txt):
                handle_focus_out('example')
                   
            
            labeloda.insert(0,qaGUI.vod.get())
            
            labeloda.bind("<FocusIn>", handle_focus_in)
            labeloda.bind("<FocusOut>", handle_focus_out)
            labeloda.bind("<Return>", handle_enter)
            
            labeloda.grid(row=8,column=1,sticky='we')    
            
            buttona = tk.Button(list_params, text = "Submit", command = close_all)
            buttona.grid(row=9,column=0, columnspan=1)
            buttonr = tk.Button(list_params, text = "Restart", command = restart)
            buttonr.grid(row=9,column=1, columnspan=1)  
        
        table_selection(self, window)
   

   
#initialization
if __name__=="__main__":
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
    
    
    bdsdirectory = bdsdatadirectorystr
    #    ddirectory = args.datadirectory
    ldirectory = lookupdirectorystr
    odirectory= outdirectorystr
    
    try: window.od
    except AttributeError: window.od = None
    if window.od != None:
        if str(window.od) !="":
           odirectory  = str(window.od)    
    if not odirectory.endswith("/"):
        odirectory= odirectory + "/"
        
    try: window.bd
    except AttributeError: window.bd = None
    if window.bd != None:
        if str(window.bd) !="":
           bdsdirectory  = str(window.bd)
           
    
    def plotting_multi(table,keymatch, keymatchpos, namestring):
            if len(keymatchpos) == 0:
                plotx=[]
                ploty=[]
                labell=[]
                for i in fvariable3:
                    xa = table["year2"]
                    ya = table[i]
                    plotx.append(xa)
                    ploty.append(ya)
                    labell.append(i)
                for x,y,z in zip(plotx,ploty,labell):
                    plt.plot(x,y,marker = 'o', markersize=3, label=z)
                fig = plt.gcf()
                fi = len(plotx)*.25
                fig.set_size_inches(6, 3.75+float(fi))
                plttitle ="Table: "+str(table.name)+"""
    """+str(min(plt.gca().get_xlim())+2)[:4]+"-"+str(max(plt.gca().get_xlim())-1)[:4] 
                plt.title(plttitle,loc='center')
                #plt.ylabel(str(i).capitalize())
                plt.xlabel("Year")
                plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2))
                plt.tight_layout()
                filestring = str(odirectory)+str(table.name)+namestring+".png"
                filestring = filestring.replace(" ","_").replace(")","").replace("(","")
                plt.savefig(filestring, bbox_inches="tight", pad_inches=.2)
                print("Writing "+filestring)
                plt.clf()
            if len(keymatchpos) == 1:
                plotx=[]
                ploty=[]
                labell=[]
                for i in fvariable3:
                    for k,l in zip(range(0,len(qaGUI.cat_selected[keymatchpos[0]])),qaGUI.cat_selected[keymatchpos[0]]):
                        xa = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)), "year2"]
                        ya = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)), i]
                        plotx.append(xa)
                        ploty.append(ya)
                        j = str(i)+" | "+str(keymatch[0][1])+": "+str(l)
                        labell.append(j)
                for x,y,z in zip(plotx,ploty,labell):
                    plt.plot(x,y,marker = 'o', markersize=3, label=z)
                fig = plt.gcf()
                fi = len(plotx)*.25
                fig.set_size_inches(6, 3.75+float(fi))
                plttitle ="Table: "+str(table.name)+"""
    """+str(min(plt.gca().get_xlim())+2)[:4]+"-"+str(max(plt.gca().get_xlim())-1)[:4] 
                plt.title(plttitle,loc='center')
                #plt.ylabel(str(i).capitalize())
                plt.xlabel("Year")
                plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2))
                plt.tight_layout()
                filestring = str(odirectory)+str(table.name)+namestring+".png"
                filestring = filestring.replace(" ","_").replace(")","").replace("(","")
                plt.savefig(filestring, bbox_inches="tight", pad_inches=.2)
                print("Writing "+filestring)
                plt.clf()
            if len(keymatchpos) == 2:
                plotx=[]
                ploty=[]
                labell=[]
                for i in fvariable3:
                    for k,l in zip(range(0,len(qaGUI.cat_selected[keymatchpos[0]])),qaGUI.cat_selected[keymatchpos[0]]):
                        for m,n in zip(range(0,len(qaGUI.cat_selected[keymatchpos[1]])),qaGUI.cat_selected[keymatchpos[1]]):
                            xa = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)), "year2"]
                            ya = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)), i]
                            plotx.append(xa)
                            ploty.append(ya)
                            j = str(i)+" | "+str(keymatch[0][1])+": "+str(l)+" | "+str(keymatch[1][1])+": "+str(n)
                            labell.append(j)
                for x,y,z in zip(plotx,ploty,labell):
                    plt.plot(x,y,marker = 'o', markersize=3, label=z)
                fig = plt.gcf()
                fi = len(plotx)*.25
                fig.set_size_inches(6, 3.75+float(fi))
                plttitle ="Table: "+str(table.name)+"""
    """+str(min(plt.gca().get_xlim())+2)[:4]+"-"+str(max(plt.gca().get_xlim())-1)[:4] 
                plt.title(plttitle,loc='center')
                #plt.ylabel(str(i).capitalize())
                plt.xlabel("Year")
                plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2))
                plt.tight_layout()
                filestring = str(odirectory)+str(table.name)+namestring+".png"
                filestring = filestring.replace(" ","_").replace(")","").replace("(","")
                plt.savefig(filestring, bbox_inches="tight", pad_inches=.2)
                print("Writing "+filestring)
                plt.clf()
            if len(keymatchpos) == 3:
                plotx=[]
                ploty=[]
                labell=[]
                for i in fvariable3:
                    for k,l in zip(range(0,len(qaGUI.cat_selected[keymatchpos[0]])),qaGUI.cat_selected[keymatchpos[0]]):
                        for m,n in zip(range(0,len(qaGUI.cat_selected[keymatchpos[1]])),qaGUI.cat_selected[keymatchpos[1]]):
                            for o,p in zip(range(0,len(qaGUI.cat_selected[keymatchpos[2]])),qaGUI.cat_selected[keymatchpos[2]]):
                                xa = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)) & (table[str(keymatch[2][1])].astype(str)==str(p)), "year2"]
                                ya = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)) & (table[str(keymatch[2][1])].astype(str)==str(p)), i]
                                plotx.append(xa)
                                ploty.append(ya)
                                j = str(i)+" | "+str(keymatch[0][1])+": "+str(l)+" | "+str(keymatch[1][1])+": "+str(n)+" | "+str(keymatch[2][1])+": "+str(p)
                                labell.append(j)
                for x,y,z in zip(plotx,ploty,labell):
                    plt.plot(x,y,marker = 'o', markersize=3, label=z)
                fig = plt.gcf()
                fi = len(plotx)*.25
                fig.set_size_inches(6, 3.75+float(fi))
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2))
                plttitle ="Table: "+str(table.name)+"""
    """+str(min(plt.gca().get_xlim())+2)[:4]+"-"+str(max(plt.gca().get_xlim())-1)[:4] 
                plt.title(plttitle,loc='center')
                #plt.ylabel(str(i).capitalize())
                plt.xlabel("Year")
                plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
                plt.tight_layout()
                filestring = str(odirectory)+str(table.name)+namestring+".png"
                filestring = filestring.replace(" ","_").replace(")","").replace("(","")
                plt.savefig(filestring, bbox_inches="tight", pad_inches=.2)
                print("Writing "+filestring)
                plt.clf()
            if len(keymatchpos) == 4:
                plotx=[]
                ploty=[]
                labell=[]
                for i in fvariable3:
                    for k,l in zip(range(0,len(qaGUI.cat_selected[keymatchpos[0]])),qaGUI.cat_selected[keymatchpos[0]]):
                        for m,n in zip(range(0,len(qaGUI.cat_selected[keymatchpos[1]])),qaGUI.cat_selected[keymatchpos[1]]):
                            for o,p in zip(range(0,len(qaGUI.cat_selected[keymatchpos[2]])),qaGUI.cat_selected[keymatchpos[2]]):
                                for q,r in zip(range(0,len(qaGUI.cat_selected[keymatchpos[3]])),qaGUI.cat_selected[keymatchpos[3]]):
                                    xa = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)) & (table[str(keymatch[2][1])].astype(str)==str(p)) & (table[str(keymatch[3][1])].astype(str)==str(r)), "year2"]
                                    ya = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)) & (table[str(keymatch[2][1])].astype(str)==str(p)) & (table[str(keymatch[3][1])].astype(str)==str(r)), i]
                                    plotx.append(xa)
                                    ploty.append(ya)
                                    j = str(i)+" | "+str(keymatch[0][1])+": "+str(l)+" | "+str(keymatch[1][1])+": "+str(n)+" | "+str(keymatch[2][1])+": "+str(p)
                                    labell.append(j)
                for x,y,z in zip(plotx,ploty,labell):
                    plt.plot(x,y,marker = 'o', markersize=3, label=z)
                fig = plt.gcf()
                fi = len(plotx)*.25
                fig.set_size_inches(6, 3.75+float(fi))
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2))
                plttitle ="Table: "+str(table.name)+"""
    """+str(min(plt.gca().get_xlim())+2)[:4]+"-"+str(max(plt.gca().get_xlim())-1)[:4] 
                plt.title(plttitle,loc='center')
                #plt.ylabel(str(i).capitalize())
                plt.xlabel("Year")
                plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
                plt.tight_layout()
                filestring = str(odirectory)+str(table.name)+namestring+".png"
                filestring = filestring.replace(" ","_").replace(")","").replace("(","")
                plt.savefig(filestring, bbox_inches="tight", pad_inches=.2)
                print("Writing "+filestring)
                plt.clf()
    
    
    def plotting(table,keymatch, keymatchpos):
        if len(keymatchpos) == 0:
            for i in fvariable3:
                    plttitle = """Graphic Gui Output
                        """+"Table: "+str(table.name)
                    x = table["year2"]
                    y = table[i]
                    plt.plot(x,y, marker ='o', markersize=3)
                    plt.title(plttitle,loc='center')
                    plt.legend()
                    plt.tight_layout()
                    filestring = str(odirectory)+str(table.name)+"_"+str(i)+".png"
                    filestring = filestring.replace(" ","_").replace(")","")
                    plt.savefig(filestring)
                    print("Writing "+filestring)
                    plt.clf()
        if len(keymatchpos) == 1:
            for i in fvariable3:
                for k,l in zip(range(0,len(qaGUI.cat_selected[keymatchpos[0]])),qaGUI.cat_selected[keymatchpos[0]]):
                        plttitle = """Graphic Gui Output
                        """+"Table: "+str(table.name)+"""
            """+str(keymatch[0][1])+": "+str(l)
                        x = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)), "year2"]
                        y = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)), i]
                        plt.plot(x,y, marker ='o', markersize=3)
                        plt.title(plttitle,loc='center')
                        plt.legend()
                        plt.tight_layout()
                        filestring = str(odirectory)+str(table.name)+"_"+str(i)+"_"+str(l)+".png"
                        filestring = filestring.replace(" ","_").replace(")","")
                        plt.savefig(filestring)
                        print("Writing "+filestring)
                        plt.clf()
        if len(keymatchpos) == 2:
            for i in fvariable3:
                for k,l in zip(range(0,len(qaGUI.cat_selected[keymatchpos[0]])),qaGUI.cat_selected[keymatchpos[0]]):
                    for m,n in zip(range(0,len(qaGUI.cat_selected[keymatchpos[1]])),qaGUI.cat_selected[keymatchpos[1]]):
                        plttitle = """Graphic Gui Output
                        """+"Table: "+str(table.name)+"""
            """+str(keymatch[0][1])+": "+str(l)+"""
            """+str(keymatch[1][1])+": "+str(n)
                        x = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)), "year2"]
                        y = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)), i]
                        plt.plot(x,y, marker ='o', markersize=3)
                        plt.title(plttitle,loc='center')
                        plt.legend()
                        plt.tight_layout()
                        filestring = str(odirectory)+str(table.name)+"_"+str(i)+"_"+str(l)+"_"+str(n)+".png"
                        filestring = filestring.replace(" ","_").replace(")","")
                        plt.savefig(filestring)
                        print("Writing "+filestring)
                        plt.clf()
        if len(keymatchpos) == 3:
            for i in fvariable3:
                for k,l in zip(range(0,len(qaGUI.cat_selected[keymatchpos[0]])),qaGUI.cat_selected[keymatchpos[0]]):
                    for m,n in zip(range(0,len(qaGUI.cat_selected[keymatchpos[1]])),qaGUI.cat_selected[keymatchpos[1]]):
                        for o,p in zip(range(0,len(qaGUI.cat_selected[keymatchpos[2]])),qaGUI.cat_selected[keymatchpos[2]]):
                            plttitle = """Graphic Gui Output
                        """+"Table: "+str(table.name)+"""
            """+str(keymatch[0][1])+": "+str(l)+"""
            """+str(keymatch[1][1])+": "+str(n)+"""
            """+str(keymatch[2][1])+": "+str(p)
                            x = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)) & (table[str(keymatch[2][1])].astype(str)==str(p)), "year2"]
                            y = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)) & (table[str(keymatch[2][1])].astype(str)==str(p)), i]
                            plt.plot(x,y, marker ='o', markersize=3)
                            plt.title(plttitle,loc='center')
                            plt.legend()
                            plt.tight_layout()
                            filestring = str(odirectory)+str(table.name)+"_"+str(i)+"_"+str(l)+"_"+str(n)+"_"+str(p)+".png"
                            filestring = filestring.replace(" ","_").replace(")","")
                            plt.savefig(filestring)
                            print("Writing "+filestring)
                            plt.clf()
        if len(keymatchpos) == 4:
            for i in fvariable3:
                for k,l in zip(range(0,len(qaGUI.cat_selected[keymatchpos[0]])),qaGUI.cat_selected[keymatchpos[0]]):
                    for m,n in zip(range(0,len(qaGUI.cat_selected[keymatchpos[1]])),qaGUI.cat_selected[keymatchpos[1]]):
                        for o,p in zip(range(0,len(qaGUI.cat_selected[keymatchpos[2]])),qaGUI.cat_selected[keymatchpos[2]]):
                            for q,r in zip(range(0,len(qaGUI.cat_selected[keymatchpos[3]])),qaGUI.cat_selected[keymatchpos[3]]):
                                plttitle = """Graphic Gui Output
                        """+"Table: "+str(table.name)+"""
                """+str(keymatch[0][1])+": "+str(l)+"""
                """+str(keymatch[1][1])+": "+str(n)+"""
                """+str(keymatch[2][1])+": "+str(p)+"""
                """+str(keymatch[3][1])+": "+str(r)
                                x = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)) & (table[str(keymatch[2][1])].astype(str)==str(p)) & (table[str(keymatch[3][1])].astype(str)==str(r)), "year2"]
                                y = table.loc[(table[str(keymatch[0][1])].astype(str)==str(l)) & (table[str(keymatch[1][1])].astype(str)==str(n)) & (table[str(keymatch[2][1])].astype(str)==str(p)) & (table[str(keymatch[3][1])].astype(str)==str(r)), i]
                                plt.plot(x,y, marker ='o', markersize=3)
                                plt.title(plttitle,loc='center')
                                plt.legend()
                                plt.tight_layout()
                                filestring = str(odirectory)+str(table.name)+"_"+str(i)+"_"+str(l)+"_"+str(n)+"_"+str(p)+".png"
                                filestring = filestring.replace(" ","_").replace(")","")
                                plt.savefig(filestring)
                                print("Writing "+filestring)
                                plt.clf()
    
    
    for i in qaGUI.table_selections:
            bdsdatas = qaGUI.d
            #bdsdatas.name = i
            keymatch = [s for s in qaGUI.cat_selected_match if i in s[0]]
            keymatchpos = [p for p, c in enumerate(qaGUI.cat_selected_match) if c[0] == i]
            fvariable3=[item.lower() for item in qaGUI.selected_variables]
#            selected_variables1 = [item.lower() for item in qaGUI.selected_variables]
#            for h,j in zip(qaGUI.selected_variables, selected_variables1):
#                if h in list(bdsdatas):
#                    fvariable3.append(h)
#                if j in list(bdsdatas):
#                    fvariable3.append(j)
                
     
    
    listcat=qaGUI.cat_vars + ["year2"]
    for k in range(0,len(qaGUI.cat_selected)):
        if "Young Incumbent Firms" in qaGUI.cat_selected[k]:
            for age in ['fage4', 'Fage4']:
                if age in list(bdsdatas):
                    bdsdatas.loc[bdsdatas[age] == "b) 1", age] = "Young Incumbent Firms"
                    bdsdatas.loc[bdsdatas[age] == "c) 2", age] = "Young Incumbent Firms"
                    bdsdatas.loc[bdsdatas[age] == "d) 3", age] = "Young Incumbent Firms"
                    bdsdatas.loc[bdsdatas[age] == "e) 4", age] = "Young Incumbent Firms"
                    bdsdatas.loc[bdsdatas[age] == "f) 5", age] = "Young Incumbent Firms"
                    bdsdatas = bdsdatas.groupby(listcat).sum().reset_index()
        if "Young" in qaGUI.cat_selected[k]:
            for age in ['fage4', 'Fage4']:
                if age in list(bdsdatas):
                    bdsdatas.loc[bdsdatas[age] == "a) 0", age] = "Young"
                    bdsdatas.loc[bdsdatas[age] == "b) 1", age] = "Young"
                    bdsdatas.loc[bdsdatas[age] == "c) 2", age] = "Young"
                    bdsdatas.loc[bdsdatas[age] == "d) 3", age] = "Young"
                    bdsdatas.loc[bdsdatas[age] == "e) 4", age] = "Young"
                    bdsdatas = bdsdatas.groupby(listcat).sum().reset_index()
        if "Old" in qaGUI.cat_selected[k]:
            for age in ['fage4', 'Fage4']:
                if age in list(bdsdatas):
                    bdsdatas.loc[bdsdatas[age] == "f) 5", age] = "Old"
                    bdsdatas.loc[bdsdatas[age] == "g) 6 to 10", age] = "Old"
                    bdsdatas.loc[bdsdatas[age] == "h) 11 to 15", age] = "Old"
                    bdsdatas.loc[bdsdatas[age] == "i) 16 to 20", age] = "Old"
                    bdsdatas.loc[bdsdatas[age] == "j) 21 to 25", age] = "Old"
                    bdsdatas.loc[bdsdatas[age] == "k) 26+", age] = "Old"
                    bdsdatas = bdsdatas.groupby(listcat).sum().reset_index()
        if "Small" in qaGUI.cat_selected[k]:
            for size in ['fsize', 'ifsize', 'Fsize', 'Ifsize']:
                if size in list(bdsdatas):
                    bdsdatas.loc[bdsdatas[size] == "a) 1 to 4", size] = "Small"
                    bdsdatas.loc[bdsdatas[size] == "g) b) 5 to 9", size] = "Small"
                    bdsdatas.loc[bdsdatas[size] == "c) 10 to 19", size] = "Small"
                    bdsdatas = bdsdatas.groupby(listcat).sum().reset_index()
        if "Medium" in qaGUI.cat_selected[k]:
            for size in ['fsize', 'ifsize', 'Fsize', 'Ifsize']:
                if size in list(bdsdatas):
                    bdsdatas.loc[bdsdatas[size] == "d) 20 to 49", size] = "Medium"
                    bdsdatas.loc[bdsdatas[size] == "e) 50 to 99", size] = "Medium"
                    bdsdatas.loc[bdsdatas[size] == "f) 100 to 249", size] = "Medium"
                    bdsdatas.loc[bdsdatas[size] == "g) 250 to 499", size] = "Medium"
            bdsdatas = bdsdatas.groupby(listcat).sum().reset_index()
        if "Large" in qaGUI.cat_selected[k]:
            for size in ['fsize', 'ifsize', 'Fsize', 'Ifsize']:
                if size in list(bdsdatas):
                    bdsdatas.loc[bdsdatas[size] == "h) 500 to 999", size] = "Large"
                    bdsdatas.loc[bdsdatas[size] == "i) 1000 to 2499", size] = "Large"
                    bdsdatas.loc[bdsdatas[size] == "j) 2500 to 4999", size] = "Large"
                    bdsdatas.loc[bdsdatas[size] == "k) 5000 to 9999", size] = "Large"
                    bdsdatas.loc[bdsdatas[size] == "l) 10000+", size] = "Large"
                    bdsdatas = bdsdatas.groupby(listcat).sum().reset_index()
    if "firm_startup_rate" in fvariable3:
        bdsdatas['sumall'] = bdsdatas.groupby(["year2"]).sum().reset_index()["firms"]
        bdsdatas["firm_startup_rate"] = bdsdatas["firms"]/bdsdatas['sumall']
    if "employment-weighted_startup_rate" in fvariable3:
        bdsdatas['sumall'] = bdsdatas.groupby(["year2"]).sum().reset_index()["emp"]
        bdsdatas["employment-weighted_startup_rate"] = bdsdatas["job_creation"]/bdsdatas["sumall"]
    if "firm_death_rate" in fvariable3:
        bdsdatas['sumall'] = bdsdatas.groupby(["year2"]).sum().reset_index()["firms"]
        bdsdatas["firm_death_rate"] =  bdsdatas["Firmdeath_Firms"]/bdsdatas['sumall']
        
    if "employment-weighted_exit rate" in fvariable3:
        bdsdatas['sumall'] = bdsdatas.groupby(["year2"]).sum().reset_index()["emp"]
        bdsdatas["firm_death_rate"] =  bdsdatas["Firmdeath_emp"]/bdsdatas['sumall']
    if "shemp" in fvariable3:
        bdsdatas['sumall'] = bdsdatas.groupby(["year2"]).sum().reset_index()["emp"]
        bdsdatas["shemp"] =  bdsdatas["emp"]/bdsdatas['sumall']
    if "shdenom" in fvariable3:
        bdsdatas['sumall'] = bdsdatas.groupby(["year2"]).sum().reset_index()["denom"]
        bdsdatas["shdenom"] =  bdsdatas["denom"]/bdsdatas['sumall']

                
    
    
    if len(keymatchpos) != 0:
        listcheck = []
        for p in (0,len(keymatch)-1):
            listcheck.append(keymatch[p][1])
    
        if "msa" in listcheck:
            bdsdatas1=bdsdatas.merge(qaGUI.lmsa, left_on="msa", right_on="msa_num")
            bdsdatas1["msa"] = bdsdatas1["gui_label"]
            bdsdatas=bdsdatas1
    
        if "Msa" in listcheck:
            bdsdatas=bdsdatas.merge(qaGUI.lmsa, left_on="Msa", right_on="msa_num")
            bdsdatas["Msa"] = bdsdatas["gui_label"]
        if "state" in listcheck:
            bdsdatas=bdsdatas.merge(qaGUI.lstate, left_on="state", right_on="state_fips")
            bdsdatas["state"] = bdsdatas["gui_label"]
    
        if "State" in listcheck:
            bdsdatas=bdsdatas.merge(qaGUI.lstate, left_on="State", right_on="state_fips")
            bdsdatas["State"] = bdsdatas["gui_label"] 
    
    bdsdatas.name = i
    if qaGUI.multi == 1:
        namestring = "_multi_variable"
        plotting_multi(bdsdatas,keymatch,keymatchpos, namestring)
    else:
        plotting(bdsdatas,keymatch,keymatchpos)