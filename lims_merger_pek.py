#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
ROOT_DIR = './'

print("Ready!")


# In[7]:


df_lims1 = pd.read_excel(os.path.join(ROOT_DIR, 'лимс стирол1.xlsx'), sheet_name = 'Sheet1')
df_lims2 = pd.read_excel(os.path.join(ROOT_DIR, 'лимс стирол2.xlsx'), sheet_name = 'Лист1')
df_lims3 = pd.read_excel(os.path.join(ROOT_DIR, 'лимс стирол3.xlsx'), sheet_name = 'Лист1')
df_lims1.info()

print('Steady!')


# In[8]:


#15.01.2017 17:56
#strptime(str,"%d.%m.%Y %H:%M")  = df_lims['Дата и время отбора']
#print(datetime.strptime('15.01.2017 17:56', "%d.%m.%Y %H:%M") )
#x = pd.to_datetime(df_lims['Дата и время отбора'],format = "%d.%m.%Y %H:%M")
#year, month, day, hour=0, minute=0, second=0
def round_dt(dt):
    if dt.minute > 30:#date.replace(minute = 0, hour = 0)
        if dt.hour == 23:
            return dt.replace(minute = 0, hour = 0)
        else:
            return dt.replace(minute = 0, hour = dt.hour + 1) 
    else:
        return dt.replace(minute = 0)

#f'201{x}') for x in ['7', '8', '9']
def normalize(df):
    tmp_df = df[['Дата и время отбора', 'Массовая доля остаточного стирола, %.1', 'Место отбора']].dropna()
    tmp_df['Дата и время отбора'] = pd.to_datetime(tmp_df['Дата и время отбора'],format = "%d.%m.%Y %H:%M").apply(round_dt)
    #tmp_df.rename(columns = {'Дата и время отбора':'Дата и время'})
    return tmp_df.rename(columns = {'Дата и время отбора':'Дата и время', 'Массовая доля остаточного стирола, %.1':'Остаточный стирол, %'})

def get_all_lims_data():
    return pd.concat([normalize(df_lims1), normalize(df_lims2), normalize(df_lims3)], ignore_index=True)

#for i in get_all_lims_data():
#    print(i.shape, i)



# In[14]:





# In[ ]:




