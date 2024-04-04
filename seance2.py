import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

xlsx_path = 'TP Data 2024 - FISA/activites.xlsx'
db_path = 'tache2/db_full.csv'

base = pd.read_csv(db_path, sep=',')
base['Time'] = pd.to_datetime(base['Time']).dt.tz_convert('UTC+01:00')

print(base.dtypes)

# DF segmentation
print("Reading excel file...")
df = pd.read_excel(xlsx_path, sheet_name='Done so far')
print("Done reading excel file !")


print("Dropping N/A from Excel...")
df = df.dropna()
print("Done dropping N/A from Excel !")

print("Types :")

calendar = df.drop(columns=df.columns[df.columns.str.contains('^Unnamed')], errors="ignored")
print(calendar)

# as1_instances = []

# for idact, act in enumerate(calendar['activity']):

#     start = calendar['Started'][idact].tz_convert('UTC+01:00')
#     end = calendar['Ended'][idact].tz_convert('UTC+01:00')

#     # AS1
#     if act == 'AS1':
#         as1new = base[(base['Time'] >= start) & (base['Time'] <= end)].reset_index(drop=True).sort_values(by='Time').drop(columns='Time')
#         len_as1 = len_as1 + len(as1new)
#         as1_instances.append(as1new)

# len_as1 = len(as1_instances)
# print(as1_instances)
# # def averageSignature(instances, avg_len):
# #     # interpolate the instances
# #     instances = instances.interpolate()

# #     # calculate the average signature
# #     avg_sig = instances.mean(axis=1)

# #     return avg_sig

# # # AS1
# # avgAS1 = averageSignature(as1_instances, len_as1)

# # print(avgAS1)
