# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 09:23:26 2019

@author: Timothy
"""

import pandas as pd
import seaborn as sb
import tkinter as tk

from census import Census

from us import states

c = Census("7db67c2f72a14f9f2c0138b925d00cb7dbd4061b")
df = c.acs.get(('NAME', 'B25034_010E'), {'for': 'state:%s' % states.MD.fips})
print(df)