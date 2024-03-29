import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import os

folder = 'TP Data 2024 - FISA'
output = 'tache1'

def chercher_fichiers_identiques(input_folder):
    # Dictionnaire pour stocker les fichiers identiques
    fichiers_identiques = {
            'MOD1.txt': [],
            'MOD2.txt': [],
            'POD 200085.csv': [],
            'POD 200086.csv': [],
            'POD 200088.csv': [],
            'PICO.csv': [],
            'THICK.csv': [],
            'THIN.csv': [],
            }

    # Parcourir récursivement les sous-dossiers
    for root, dirs, files in os.walk(input_folder):
        for file_name in files:
            # Construction du chemin complet du fichier
            file_path = os.path.join(root, file_name)

            file_name_upper: str = file_name.upper()
            if "MOD1" in file_name_upper:
                fichiers_identiques["MOD1.txt"].append(file_path)
            if "MOD2" in file_name_upper:
                fichiers_identiques["MOD2.txt"].append(file_path)
            elif "POD 200085" in file_name_upper:
                fichiers_identiques["POD 200085.csv"].append(file_path)
            elif "POD 200086" in file_name_upper:
                fichiers_identiques["POD 200086.csv"].append(file_path)
            elif "POD 200088" in file_name_upper:
                fichiers_identiques["POD 200088.csv"].append(file_path)
            elif "PICO" in file_name_upper:
                fichiers_identiques["PICO.csv"].append(file_path)
            elif "THICK" in file_name_upper:
                fichiers_identiques["THICK.csv"].append(file_path)
            elif "THIN" in file_name_upper:
                fichiers_identiques["THIN.csv"].append(file_path)

    return fichiers_identiques


### CLEANING PART ###

# - Cleanup text files -
def cleanup_text_files(files_paths):

    # First merge all related files
    df_full = pd.DataFrame()
    print("Cleaning up TXT file...")

    for txt in files_paths:
        newDf = pd.read_csv(txt, sep="\t",header=None, names=("Time","RH","Temperature","TGS4161","MICS2714","TGS2442","MICS5524","TGS2602","TGS2620"))
        df_full = pd.concat([ df_full, newDf ])

    # Then cleanup junk
    print("Editing localization...")

    df_full["Time"] = pd.to_datetime(df_full['Time']).dt.tz_localize('UTC+01:00',ambiguous='infer')

    print("Done editing localization !")

    print("Dropping duplicates...")

    df_full.drop_duplicates()

    print("Done dropping duplicates !")

    print(df_full)

    print("Done cleaning up TXT file !")

    return df_full


# - Cleaning csv files -

def cleanup_pod_df(df: pd.DataFrame):
    print("Extra cleanup for POD file...")
    df = df.drop(columns=df.columns[df.columns.str.contains('aqi|element|^Unnamed')], errors="ignored")

    df = df.rename(columns={'date': 'Time'})
    df['Time'] = pd.to_datetime(df['Time'])

    print("Done extra cleanup for POD file !")
    return df


def cleanup_pico_df(df: pd.DataFrame):
    print("Extra cleanup for PICO file...")
    df = df.drop(columns=df.columns[df.columns.str.contains('aqi|qai|iaq|element|^Unnamed')], errors='ignored')

    df = df.rename(columns={'date': 'Time'})
    df['Time'] = pd.to_datetime(df['Time'])

    print("Done extra cleanup for PICO file !")
    return df


def cleanup_thick_df(df: pd.DataFrame):
    print("Extra cleanup for THICK file...")
    df = df.drop(columns=df.columns[df.columns.str.contains('element|^Unnamed')], errors="ignored")

    df = df.rename(columns={'date': 'Time'})
    df['Time'] = pd.to_datetime(df['Time'])

    print("Done extra cleanup for THICK file !")
    return df


def cleanup_thin_df(df: pd.DataFrame):
    print("Extra cleanup for THIN file...")
    df = df.drop(columns=df.columns[df.columns.str.contains('element|^Unnamed')])

    df = df.rename(columns={'date': 'Time'})
    df['Time'] = pd.to_datetime(df['Time'])

    print("Done extra cleanup for THIN file !")
    return df

def cleanup_csv_files(filename:str, files_paths):
    print("Cleaning up CSV file...")

    filename = filename.upper()
    df_full = pd.DataFrame()
    for csv in files_paths:
        newDf = pd.read_csv(csv,comment="#", sep=";", skiprows=(1,2,3,4))
        df_full = pd.concat([ df_full, newDf ])

    # Then cleanup junk

    if "POD" in filename:
        df_full = cleanup_pod_df(df_full)
    elif "PICO" in filename:
        df_full = cleanup_pico_df(df_full)
    elif "THICK" in filename:
        df_full = cleanup_thick_df(df_full)
    elif "THIN" in filename:
        df_full = cleanup_thin_df(df_full)

    print("Dropping duplicates...")

    df_full.drop_duplicates()

    print("Done dropping duplicates !")

    print(df_full)

    print("Done cleaning up CSV file !")
    return df_full

# - Cleaning entrypoint -
def cleanup_by_files_type(filename ,files_paths):
    df = pd.DataFrame()

    if(filename.endswith('.csv')):
        df = cleanup_csv_files(filename, files_paths)

    elif(filename.endswith('.txt')):
        df = cleanup_text_files(files_paths)

    return df

# Main function to clean files
def cleanup_files(input_files):

    dfs = dict()
    print("Scanning for files to cleanup...")
    # Traiter les fichiers identiques
    for nom_fichier, chemins in input_files.items():
        filename, ext = os.path.splitext( nom_fichier)
        print(f"{'-' * 10} {nom_fichier} {'-' * 10}")
        if len(chemins) > 1 :
            output_file_path = os.path.join(output, f"{filename}.csv")
               # Vérifier si le fichier de sortie existe déjà
            if os.path.exists(output_file_path):
                print(f"Le fichier '{output_file_path}' existe déjà.")
                # TODO : debug matplotlib hanging
                # print("Saving df to memory...")
                # df = pd.read_csv(output_file_path,sep=",")
                # dfs[filename.lower()] = df
                # print("Done saving df to memory !")
            else:
                df = cleanup_by_files_type(nom_fichier, chemins)
                print("Saving df to memory...")

                dfs[filename.lower()] = df

                print("Done saving df to memory !")

                print("Saving df to file...")

                df.to_csv(output_file_path, index=False)

                print("Done saving file !")
        print("-" * 20)

    print("Done cleaning up files !")
    return dfs

files_to_clean = chercher_fichiers_identiques(folder)
files_clean = cleanup_files(files_to_clean)
print(files_clean)
plt.figure(figsize=(10, 2))  # Plot overview of the files
date_format = mdates.DateFormatter('%d-%b')

plt.subplot(3,2,1) # MOD1
plt.subplots_adjust(top=8)
plt.title("MOD1 (Temperature x Time)")
print("Plotting mod1...")
plt.plot(files_clean['mod1']['Time'],files_clean['mod1']['Temperature'])
plt.gca().xaxis.set_major_formatter(date_format)
print("Done Plotting mod1 !")

plt.xticks(rotation=45)

plt.subplot(3,2,2) # MOD2
plt.subplots_adjust(top=8)
plt.title("MOD2 (Temperature x Time)")

print("Plotting mod2...")
plt.plot(files_clean['mod2']['Time'],files_clean['mod2']['Temperature'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)
print("Done plotting mod2 !")

plt.subplot(3,2,3) # POD 200085
plt.subplots_adjust(top=8)
plt.title("POD 200085 (Temperature x Time)")
print("Plotting pod 200085...")
plt.plot(files_clean['pod 200085']['Time'],files_clean['pod 200085']['temperature'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)
print("Done plotting pod 200085 !")

plt.subplot(3,2,4) # Piano PICO
plt.subplots_adjust(top=8)
plt.title("PICO (Temperature x Time)")
print("Plotting pico...")
plt.plot(files_clean['pico']['Time'],files_clean['pico']['bme68x_temp'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)
print("Done plotting pico !")

plt.subplot(3,2,5) # Piano Thick
plt.subplots_adjust(top=8)
plt.title("THICK (TGS2620 x Time)")
plt.plot(files_clean['thick']['Time'], files_clean['thick']['piano_TGS2620I00'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

plt.subplot(3,2,6) # Piano Thin
plt.subplots_adjust(top=8)
plt.title("THIN (GM102B x Time)")
plt.plot(files_clean['thin']['Time'],files_clean['thin']['piano_GM102BI00'])
plt.gca().xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45)

plt.subplots_adjust(left=0.1, bottom=0.06, right=0.9, top=0.96, wspace=0.2, hspace=0.2)
plt.savefig("plot.png")
plt.show()


