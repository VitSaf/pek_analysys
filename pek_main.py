#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pek_ns as ns
import lims_merger_pek as lm

col_112_useless_data = ['25_SKS_Column_112_001.RAB', '25_SKS_Column_112_002.RAB', '25_SKN_Column_112_003.RAB', '25_SKS_Column_112_004.RAB', '25_SKS_Column_112_005.RAB']
date_and_time = ['Дата и время']

ROOT_DIR = './'
print("Ready!")


# In[3]:


df = pd.read_excel(os.path.join(ROOT_DIR, 'свод тэгов мес по ПЭК.xlsx'), sheet_name = 'Лист1')
correct_names = pd.read_excel(os.path.join(ROOT_DIR, 'свод тэгов мес по ПЭК.xlsx'), sheet_name = 'Лист2')
print(correct_names)
df.info()
dates = df['Дата и время']

#lims1_df, lims2_df, lims3_df = lm.get_all_lims_data()
lims = lm.get_all_lims_data()
lims.info()
print("Steady!")


# In[4]:


col_112_3_latex_t = pd.read_excel(os.path.join(ROOT_DIR, 'Уср. Выгрузка по 122-3.xlsx'), sheet_name = 'Sheet1')
col_112_4_latex_t = pd.read_excel(os.path.join(ROOT_DIR, 'Уср. Выгрузка по 122-4.xlsx'), sheet_name = 'Sheet1')
print('+')


# In[44]:


def get_smena_full_data(start, addition):
    return df.iloc[start:start+addition], start+addition


def get_data_by_tags(row_start, row_end, tags):
    tmp = ['Дата и время']
    for i in tags:
        tmp.append(i)
    tmp_return = df[tmp].iloc[row_start:row_end]
    #print(tmp_return.shape, tags)
    return tmp_return

#def get_line_info(ns_jour, count_of_sm, sm_n):#журнал н.с. за день, количество смен, номер нужной смены
def get_line_info(ns_jour, sm_n):#журнал н.с. за день, номер нужной смены(0,3,5)
    tmp_battery = []
    tmp_112_smena = []
    tmp_41_smena = []
    isWorking = True
    #собираем инфу по батарее
    if ns_jour[sm_n][3] != '0' :#
        tmp_battery.append(ns_jour[sm_n][3])
    else:
        isWorking = False
    if ns_jour[sm_n+1][3] != '0' :
        tmp_battery.append(ns_jour[sm_n+1][3])
    if ns_jour[sm_n+2][3] != '0' :
        tmp_battery.append(ns_jour[sm_n+2][3])   
    #Собираем инфу по 112    
    if ns_jour[sm_n][4] != '0' :#
        tmp_112_smena.append(ns_jour[sm_n][4]) 
    else:
        isWorking = False
    if ns_jour[sm_n+1][4] != '0' :
        tmp_112_smena.append(ns_jour[sm_n+1][4]) 
    if ns_jour[sm_n+2][4] != '0' :
        tmp_112_smena.append(ns_jour[sm_n+2][4])    
    #Собираем инфу по 41
    if ns_jour[sm_n][5] != '0' :#
        tmp_41_smena.append(ns_jour[sm_n][5])
    else:
        isWorking = False
    if ns_jour[sm_n+1][5] != '0' :
        tmp_41_smena.append(ns_jour[sm_n][5])
    if ns_jour[sm_n+2][5] != '0' :
        tmp_41_smena.append(ns_jour[sm_n][5])  
    return tmp_battery, tmp_112_smena, tmp_41_smena, isWorking
    

#журнал нач смены
#собирать новый большой датафрейм из маленьких append'amи(добавление строк)
#т.е. отдельные фреймы: дата за смены, 112, 41, бат
#взять все данные, дропнуть 112,41,bat

#даты в журнал нс

def save_merge(df1, df2):
    c1 = df1.columns.to_list()
    c2 = df2.columns.to_list()
    list_on = []
    for i in c2:
        try:
            list_on.append(c1[c1.index(i)])
        except (ValueError):
            continue
    #print(c1, c2, list_on)
        return df1.merge(df2 ,on = list_on)


def get_df_for_smena(row_start, addition, ns_jour, sm):#sm = 0,3,5
    tmp_bat,tmp_112,tmp_41,tmpBool = get_line_info(ns_jour, sm)
    tmp1 = pd.DataFrame()
    tmp1 = get_data_by_tags(row_start, row_start+addition,[])
    on_tmp = ['Дата и время']
    
    #x = on_tmp[:]  
    for i in tmp_bat:#merg'ы добавляют дубликаты. ФИКСИ!ФИКСИ!ФИКСИ!ФИКСИ!ФИКСИ!ФИКСИ!ФИКСИ!
        data =get_data_by_tags(row_start, row_start+addition, ns.bat[i])
        #tmp1 = tmp1.merge(data, on = x)
        tmp1 = save_merge(tmp1, data)

 
    for i in tmp_112:
        #tmp1 = tmp1.merge(get_data_by_tags(row_start, row_start+addition, col_112[i]), on = x)
        data =get_data_by_tags(row_start, row_start+addition, ns.col_112[i])
        tmp1 = save_merge(tmp1, data)

    for i in tmp_41:
        #tmp1 = tmp1.merge(get_data_by_tags(row_start, row_start+addition, col_41[i]), on = x)
        data =get_data_by_tags(row_start, row_start+addition, ns.col_41[i])
        tmp1 = save_merge(tmp1, data)
       
    return tmp1

#В итоге собран df за одну смену
def add_lims_data(df):
    df = df.merge(lims, how = 'left' ,on = 'Дата и время')
    return df.fillna('-')

def add_rest_of_data(df_with_lims):
    x = all_tags
    x.extend(col_112_useless_data)
    #df.drop(columns = x).to_excel('drop.xlsx')
    df_dropped = df.drop(columns = x)
    return df_with_lims.merge(df_dropped, how = 'left', on = 'Дата и время')

def init_all():
    all_t = []
    for i in ns.col_112.values():
        #for j in i:
        all_t.extend(i)
    for i in ns.col_41.values():
        all_t.extend(i)
    for i in ns.bat.values():
        all_t.extend(i)
    #all_t.append(date_and_time[0])
    return all_t

def get_dict_of_names():
    tags = df.columns.to_list()
    new_names = {}
    for i in tags:
        counter = 0
        for j in correct_names['Тэг']:
            if i == j:
                new_names.update({str(i):str(correct_names.iloc[counter, 1])})
            counter += 1
    return new_names

def add_iot_t(x):
    x = x.merge(col_112_3_latex_t, how = 'left', on = 'Дата и время')
    return x.merge(col_112_4_latex_t, how = 'left', on = 'Дата и время')


#Этот блок в инициализацию
sm_number_8h = [0, 3, 6]
sm_numer_12h = [0, 3]
all_tags = init_all()
result = get_data_by_tags(0, 0, all_tags)
td_ns_day = timedelta(days = 1)
td_hour = timedelta(hours = 1)
day_ns_jour_date = datetime(day = 1, month = 1, year = 2017)
row_start = 0

print('Its Done')


# In[47]:


#Основной цикл
FINAL_DATE = datetime(year = 2020, month = 6, day = 23, hour = 0,minute = 0 )
j = 0
#for j in range(365): 
while day_ns_jour_date < FINAL_DATE:
    ns_jour, isExist = ns.get_actual_tl(day_ns_jour_date)
    if (isExist):
        print(day_ns_jour_date, df.iloc[row_start, 0], j)
        j += 1
        
        #if j%300 == 0:#темповое сохранение, убрать
        #    result.to_excel(str(j) + '.xlsx')
        
        if len(ns_jour) == 9:
            sm_counter = sm_number_8h
            addition = 8
        if len(ns_jour) == 6:
            sm_counter = sm_number_12h
            addition = 12

        for i in sm_counter:
            smena_df = get_df_for_smena(row_start, addition, ns_jour, i)
            result = result.append(smena_df, ignore_index = True)
            #result = result.merge(smena_df, how = 'outer' ,on = x)
            row_start += addition
        day_ns_jour_date += td_ns_day
    else:
        row_start += 24
        day_ns_jour_date += td_ns_day
#print(result)
print('Finish step 1')
result = add_lims_data(result)
result = add_rest_of_data(result)
result = result.rename(columns = get_dict_of_names())
print('Finish step 2')
result = add_iot_t(result)
result.to_excel('load.xlsx')
print('FINALLY!')




