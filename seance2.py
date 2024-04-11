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

for idact, act in enumerate(df_excel['activity']):
    start = df_excel['Started'][idact]
    end = df_excel['Ended'][idact]

    new_instance = base[(base['Time'] >= start) & (base['Time'] <= end)].reset_index(drop=True).sort_values(by='Time').drop(columns='Time')
    if not act in instances:
        instances[act] = [new_instance]
    else :
        instances[act].append(new_instance)

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
    avg = averageSignature(instances[activity])
    for column in avg.columns:
        plt.plot(avg.index, avg[column])


    plt.title(f'Average signature of {activity}')
    plt.xlabel('Number of Samples')
    plt.ylabel('Sensor Measurements')

fig.tight_layout()
plt.show()
