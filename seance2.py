import pandas as pd
import matplotlib.pyplot as plt

xlsx_path = 'TP Data 2024 - FISA/activites.xlsx'
db_path = 'tache2/db_full.csv'

base = pd.read_csv(db_path, sep=',')
base['Time'] = pd.to_datetime(base['Time']).dt.tz_convert('UTC+01:00')

print(base.dtypes)

# DF segmentation
print("Reading excel file...")
df_excel = pd.read_excel(xlsx_path, sheet_name='Done so far')
print("Done reading excel file !")


print("Dropping columns from Excel sheet...")
df_excel = df_excel.drop(columns=df_excel.columns[df_excel.columns.str.contains('^Unnamed|Comments')], errors="ignored")
print("Done dropping columns from Excel sheet !")
print(df_excel.dtypes)

print("Converting Excel sheet dates...")
df_excel['Started'] = pd.to_datetime(df_excel['Started']).dt.tz_localize('UTC').dt.tz_convert('UTC+01:00')
df_excel['Ended'] = pd.to_datetime(df_excel['Ended']).dt.tz_localize('UTC').dt.tz_convert('UTC+01:00')
print("Done converting Excel sheet dates !")

print("Dropping N/A from Excel...")
df_excel = df_excel.dropna().reset_index(drop=True)
print("Done dropping N/A from Excel !")

print(df_excel)

instances = {}

# as1_instances = []
# len_as1 = 0

# nett_instances = []
# len_nett = 0


for idact, act in enumerate(df_excel['activity']):
    start = df_excel['Started'][idact]
    end = df_excel['Ended'][idact]

    new_instance = base[(base['Time'] >= start) & (base['Time'] <= end)].reset_index(drop=True).sort_values(by='Time').drop(columns='Time')
    if not act in instances:
        instances[act] = [new_instance]
    else :
        instances[act].append(new_instance)

# for idact, act in enumerate(df_excel['activity']):
#     start = df_excel['Started'][idact]
#     end = df_excel['Ended'][idact]
#     print(act)

#     # AS1
#     if act == 'AS1':
#         as1new = base[(base['Time'] >= start) & (base['Time'] <= end)].reset_index(drop=True).sort_values(by='Time').drop(columns='Time')
#         len_as1 += len(as1new)
#         as1_instances.append(as1new)


def averageSignature(instances):

    df_avg = pd.DataFrame(instances[0])

    for i in range(1, len(instances)): 

        current_instance = instances[i] 
        min_rows = min(current_instance.shape[0], df_avg.shape[0])

        for row in range(min_rows):
            avg_row = df_avg.iloc[row]
            current_avg_row = current_instance.iloc[row]

            df_avg.iloc[row] = (avg_row + current_avg_row) / 2
    print(df_avg)

    df_avg = df_avg.dropna()

    return df_avg
avgAS1 = averageSignature(instances['AS1'])
avgOeuf = averageSignature(instances['Oeuf'])

# Plotting the average signature for AS1
fig = plt.figure(figsize=(10, 6))
print(avgAS1)

i = 0

for activity in instances.keys():
    i+= 1
    plt.subplot(5,2,i)
    # plt.subplots_adjust(top=1)
    avg = averageSignature(instances[activity])
    for column in avg.columns:
        plt.plot(avg.index, avg[column])


    plt.title(f'Average signature of {activity}')
    plt.xlabel('Number of Samples')
    plt.ylabel('Sensor Measurements')
# for column in avgAS1.columns:
#     plt.plot(avgAS1.index, avgAS1[column])
# plt.grid(True)


fig.tight_layout()
plt.show()
    # aligned_instances = pd.DataFrame()
    
    # for instance in instances:
    #     instance['Time'] = instance.index - instance.index[0]
    #     instance = instance.set_index('Time')
    #     aligned_instances = aligned_instances.add(instance, fill_value=0)
    
    # aligned_instances.interpolate(method='linear', inplace=True)
    
    # avg_signature = aligned_instances.mean(axis=4)
    
    # avg_signature *= (average_length / len(aligned_instances))
    
    # return avg_signature


# avgAS1 = averageSignature(as1_instances, len_as1)

# def average_activity_across_instances(instances, length):
#     df_full = pd.DataFrame()

#     for instance in instances:
#         df_full = pd.concat((df_full, instance))
#     by_row_index = df_full.groupby(df_full.index)
#     df_means = by_row_index.mean()

#     print(df_means)
# print(average_activity_across_instances(as1_instances, len_as1))

# def averageSignature(instances, average_length):
#     print(instances)
# avgAS1 = averageSignature(as1_instances, len_as1)

