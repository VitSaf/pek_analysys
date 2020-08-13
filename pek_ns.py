import pandas as pd
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

Column_112_001 = ['25_SKS_Column_112_001.P1', '25_SKS_Column_112_001.T1', '25_SKS_Column_112_001.T2', '25_SKS_Column_112_001.F1', '25_SKS_Column_112_001.F2']
Column_112_002 = ['25_SKS_Column_112_002.P1', '25_SKS_Column_112_002.T1', '25_SKS_Column_112_002.T2', '25_SKS_Column_112_002.F1', '25_SKS_Column_112_002.F2']
Column_112_003 = ['25_SKN_Column_112_003.P1', '25_SKN_Column_112_003.T1', '25_SKN_Column_112_003.T2', '25_SKN_Column_112_003.F1', '25_SKN_Column_112_003.F2']
Column_112_004 = ['25_SKS_Column_112_004.P1', '25_SKS_Column_112_004.T1', '25_SKS_Column_112_004.T2', '25_SKS_Column_112_004.F1', '25_SKS_Column_112_004.F2']
Column_112_005 = ['25_SKS_Column_112_005.P1', '25_SKS_Column_112_005.T1', '25_SKS_Column_112_005.T2', '25_SKS_Column_112_005.F1', '25_SKS_Column_112_005.F2']



Column_41_001 = ['25_SKS_Column_41_001.F1', '25_SKS_Column_41_001.F2', '25_SKS_Column_41_001.F3', '25_SKS_Column_41_001.F3.T_sat', '25_SKS_Column_41_001.L1_1', '25_SKS_Column_41_001.L1_2', '25_SKS_Column_41_001.P1', '25_SKS_Column_41_001.P2', '25_SKS_Column_41_001.P3', '25_SKS_Column_41_001.P4', '25_SKS_Column_41_001.RAB', '25_SKS_Column_41_001.T4', '25_SKS_Column_41_001.T5', '25_SKS_Column_41_001.T6', '25_SKS_Column_41_001.T7', '25_SKS_Column_41_001.T8']
Column_41_002 = ['25_SKS_Column_41_002.F1', '25_SKS_Column_41_002.F2', '25_SKS_Column_41_002.F3', '25_SKS_Column_41_002.F3.T_sat', '25_SKS_Column_41_002.L1_1', '25_SKS_Column_41_002.L1_2', '25_SKS_Column_41_002.P1', '25_SKS_Column_41_002.P2', '25_SKS_Column_41_002.P3', '25_SKS_Column_41_002.P4', '25_SKS_Column_41_002.RAB', '25_SKS_Column_41_002.T4', '25_SKS_Column_41_002.T5', '25_SKS_Column_41_002.T6', '25_SKS_Column_41_002.T7', '25_SKS_Column_41_002.T8']
Column_41_003 = ['25_SKS_Column_41_003.F1', '25_SKS_Column_41_003.F2', '25_SKS_Column_41_003.F3', '25_SKS_Column_41_003.F3.T_sat', '25_SKS_Column_41_003.L1_1', '25_SKS_Column_41_003.L1_2', '25_SKS_Column_41_003.P1', '25_SKS_Column_41_003.P2', '25_SKS_Column_41_003.P3', '25_SKS_Column_41_003.P4', '25_SKS_Column_41_003.RAB', '25_SKS_Column_41_003.T4', '25_SKS_Column_41_003.T5', '25_SKS_Column_41_003.T6', '25_SKS_Column_41_003.T7', '25_SKS_Column_41_003.T8']
Column_41_004 = ['25_SKN_Column_41_004.F1', '25_SKN_Column_41_004.F2', '25_SKN_Column_41_004.F3', '25_SKN_Column_41_004.F3.T_sat', '25_SKN_Column_41_004.L1_1', '25_SKN_Column_41_004.L1_2', '25_SKN_Column_41_004.P1', '25_SKN_Column_41_004.P2', '25_SKN_Column_41_004.P3', '25_SKN_Column_41_004.P4', '25_SKN_Column_41_004.RAB', '25_SKN_Column_41_004.T4', '25_SKN_Column_41_004.T5', '25_SKN_Column_41_004.T6', '25_SKN_Column_41_004.T7', '25_SKN_Column_41_004.T8']



Battery_001 = ['25_SKS_Battery_001.KONV']
Battery_002 = ['25_SKS_Battery_002.KONV']
#Battery_003 = ['25_SKS_Battery_003.KONV']
Battery_004 = ['25_SKS_Battery_004.KONV']
#Battery_005 = ['25_SKS_Battery_005.KONV']
#Battery_006 = ['25_SKN_Battery_006.KONV']
#Battery_007 = ['25_SKS_Battery_007.KONV']
Battery_008 = ['25_SKS_Battery_008.KONV']


col_112 = {'112/1':Column_112_001, '112/2':Column_112_002, '112/3':Column_112_003, '112/4':Column_112_004, '112/5':Column_112_005}
col_41 = {'41/1':Column_41_001, '41/2':Column_41_002, '41/3':Column_41_003, '41/4':Column_41_004}
#bat = {'1 бат':Battery_001, '2 бат':Battery_002, '3 бат':Battery_003, '4 бат':Battery_004, '5 бат':Battery_005, '6 бат':Battery_006, '7 бат':Battery_007, '8 бат':Battery_008}
bat = {'1 бат':Battery_001, '2 бат':Battery_002, '4 бат': Battery_004, '8 бат': Battery_008}

ROOT_DIR = './'
MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
YEARS = [2017, 2018, 2019, 2020]
YEAR_STR = {2017:'2017', 2018:'2018', 2019:'2019', 2020:'2020'}

#Ищет ячейку с заголовком "Действующая технологическая линия" на странице в журнале начальника смены
#Возвращает координаты ячейки вида № столбоца, № строки
#print('41/1' in col_41.keys())
def is_valid(data):
    return data in col_112.keys() or data in col_41.keys() or data in bat.keys()

def find_table(d, m, y):
	df, isExist = get_ns_journal_by_date(d,m,y)
	if(isExist):
		x = df.shape[1]#запоминаем количество столбцов в датасете
		i = 0
	#В цикле обходим все столбцы
		while i < x:
			tmp = df.iloc[:,i]#Выбираем полностью стобец номер i
			i += 1
			counter = 0
			for j in tmp:#по всем ячейкам
				if j == 'Действующая технологическая линия':#, пока не встретим ячейку со значением "Действующая технологическая линия"
					#return i -1  , counter
					column = i - 1
					row = counter
					return df.iloc[row+1:row+10,column:column+8], True
				counter += 1
	else:
		print('Нет данных')
		return [] ,False

#0-8	11/1	35а/3	1 бат	112/2	41/1	37/3	11 л/л
#def get_actual_tl(d, m, y):
def get_actual_tl(date):
	d = date.day
	m = date.month
	y = date.year
	
	table,isExist = find_table(d,m,y)
	SMENA_TMP = ("0","0","0","0","0","0","0","0")
	RESULT = []
	if (isExist == False):
		return [],isExist
	#print(table)
	for row in range(table.shape[0]):
		SMENA = list(SMENA_TMP)
		for column in range(table.shape[1]):
			data = table.iloc[row, column]
			#print(pd.isna(data) and column != 0) or (not is_valid(data))
			if (pd.isna(data) and column != 0) or (not is_valid(data)):#!!!!!!!!!!!!
				continue
			else:
				try:
					#print(str(data))
					hour = str(data).split('-')
					#08.01.2017 08:52 - даты из лимс(остаточный стирол)
					#01.01.17 0:00:00 - мес
					dt = []
					dt.append(datetime(day = d,month = m,year = y, hour = int(hour[0]), minute = 0,second = 0).strftime("%d.%m.%y %H:%M:%S"))
					if(int(hour[1]) == 24): 
						hour[1] = 0
					dt.append(datetime(day = d,month = m,year = y, hour = int(hour[1]), minute = 0,second = 0).strftime("%d.%m.%y %H:%M:%S"))
					SMENA[column] = dt
				except ValueError:
					#print(type(e))
					if (column == 0):#NB!!!!!!!!!!
						tmp = RESULT[-1]
						SMENA[column] = tmp[column]
					else:
						SMENA[column] = data
		#if (SMENA[1] == "0" and SMENA[2] == "0" and SMENA[3] == "0" and SMENA[4] == "0" and SMENA[5] == "0"):
		RESULT.append(SMENA)
	return RESULT, isExist

#date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
	#print(table)#Выбираем подтаблицу с содержимым таблицы "Действующая технологическая линия"
	#return df_tmp, df_tmp.shape[0]#Возвращаем содержимое и количество линий в работе (соответствует количеству строк в таблице)


def parse_all():
	for y in YEARS:
		for m in MONTHS:
			for d in range(31):
				print(m, MONTHS.index(m))
				df, isExist = get_ns_journal_by_date(d,MONTHS.index(m), y)
				if (isExist):
					print(find_table(df))
					print(get_actual_tl_in_3sm(df))
				else:
					break


def get_ns_journal_by_date(d, m, y):
#def get_ns_journal_by_date(date):
	m -= 1
	journal_name = MONTHS[m] + ' ' + YEAR_STR[y] + ".xlsx"
	print(journal_name)
	try:
		return pd.read_excel(os.path.join(ROOT_DIR, journal_name), sheet_name = str(d)), True #d+1 было
	except FileNotFoundError as e:
		print(e)
		return np.nan ,False

print('Hello')
#tmp = get_actual_tl(25,12,2017)
#for i in tmp:
#	print(i)