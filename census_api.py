# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 09:23:26 2019

@author: Timothy
playing with census api
"""

import pandas as pd
import seaborn as sb
import tkinter as tk

from census import Census

from us import states

#c = Census("7db67c2f72a14f9f2c0138b925d00cb7dbd4061b")
#df = c.acs.get(('NAME', 'B25034_010E'), {'for': 'state:%s' % states.MD.fips})
#print(df)

#for st in states.STATES:
#    print(st)

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

class apiGUI:
    def __init__(self, window):
        self.window = window
        apiGUI.state_selections = []
        
        def close_all():
            window.destroy()
        
        def fill_listbox(self,list_box,vtable):
            self.len_max=0
            for i, j in zip(range(len(vtable)),vtable):
                if len(j) > self.len_max:
                    self.len_max = len(j)
                list_box.insert(i,str(j))
        
        def get_choices(pwin, listbox, nvariable):
            ndex = listbox.curselection()
            values = [listbox.get(x) for x in ndex]
            setattr(apiGUI, nvariable, values)
        
        def on_closing(self):
            raise SystemExit
            
        def state_selection(self,pwin):
            pwin.withdraw()
            state_win = tk.Toplevel(window)
            #state_win.protocol("WM_DELETE_WINDOW", on_closing(self))
            self.len_max=0
            self.vtable=[str(st) for st in states.STATES]
            self.state_list_box = tk.Listbox(state_win, selectmode="multiple", listvariable=self.vtable)
            fill_listbox(self,self.state_list_box,self.vtable)

            self.state_list_box.grid(row=0,column=0,sticky='nsew')
            
            self.ss = tk.Scrollbar(state_win)
            self.ss.grid(row=0,column=1,sticky='ns')
            
            self.var_button = tk.Button(state_win, text = "Next",command = lambda:combine_funcs(get_choices(state_win, self.state_list_box, "state_selections"), var_selection(self,state_win)))
            self.var_button.grid(row=1,column=0, columnspan=2)
            
        def var_selection(self, pwin):
            pwin.withdraw()
            var_win = tk.Toplevel(window)
            #state_win.protocol("WM_DELETE_WINDOW", on_closing(self))
            self.len_max=0
            self.vtable=[str(st) for st in range(0,10)]
            self.var_list_box = tk.Listbox(var_win, selectmode="multiple", listvariable=self.vtable)
            fill_listbox(self,self.var_list_box,self.vtable)
            self.var_list_box.grid(row=0,column=0,sticky='nsew')
            
            self.ss = tk.Scrollbar(var_win)
            self.ss.grid(row=0,column=1,sticky='ns')
            
            self.var_button = tk.Button(var_win, text = "Next", command = lambda:combine_funcs(get_choices(var_win, self.var_list_box, "var_selections"), close_all()))
            self.var_button.grid(row=1,column=0, columnspan=2)
        
        #apiGUI.state_selection = get_choices(state_selection.state_win.state_list_box)
        
        state_selection(self, window) 
        






master = tk.Tk()
window = apiGUI(master)
tk.mainloop()

print(apiGUI.state_selections)
print(apiGUI.var_selections)