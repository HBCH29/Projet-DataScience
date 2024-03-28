import pandas as pd
import os

folder = 'TP Data 2024 - FISA'
output = 'tache1'

def chercher_fichiers_identiques(input_folder):
    # Dictionnaire pour stocker les fichiers identiques
    fichiers_identiques = {
            'MOD1.txt': [],
            'MOD2.txt': [],
            'POD.csv': [],
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
            elif "POD" in file_name_upper:
                fichiers_identiques["POD.csv"].append(file_path)
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
        newDf = pd.read_csv(csv,comment="#", sep=";")
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

# def cleanup_file(file_path):



# Main function to clean files
def cleanup_files(input_files):

    print("Scanning for files to cleanup...")
    # Traiter les fichiers identiques
    for nom_fichier, chemins in input_files.items():

        print(f"{'-' * 10} {nom_fichier} {'-' * 10}")
        if len(chemins) > 1 :
            output_file_path = os.path.join(output, nom_fichier)
               # Vérifier si le fichier de sortie existe déjà
            if os.path.exists(output_file_path):
                print(f"Le fichier '{output_file_path}' existe déjà.")
            else:
                df = cleanup_by_files_type(nom_fichier, chemins)
                print("Saving file...")
                df.to_csv(output_file_path, index=False)

                print("Done saving file !")
        print("-" * 20)

    print("Done cleaning up files !")
        # else:
        #     print(f"Traitement des fichiers pour '{nom_fichier}':")
        #     dfs = [] 
        #     if nom_fichier.endswith(".csv"):
        #         for chemin in chemins:
        #             df = pd.read_csv(chemin,comment="#")
        #             dfs.append(df)
        #         concatenated_df = pd.concat(dfs, ignore_index=True)
        #         print(concatenated_df.info())
        #         try:
        #             # Vérifier les échantillons en double
        #             duplicates = concatenated_df.duplicated()

        #             # Afficher les échantillons en double
        #             print("Échantillons en double :")
        #             print(concatenated_df[duplicates])

        #             # Compter le nombre d'échantillons en double
        #             nombre_doublons = duplicates.sum()
        #             print(f"Nombre total d'échantillons en double : {nombre_doublons}")
        #             # Supprimer les échantillons en double
        #             concatenated_df.drop_duplicates(inplace=True)
        #             print("Echantillons en double ont été supprimé")
        #             # Trier par date
        #             concatenated_df['date'] = pd.to_datetime(concatenated_df['date'])
        #             concatenated_df = concatenated_df.sort_values(by='date')
        #             print("trié :D ")
        #         except Exception as e :
        #             print(f"Error has occured {e}")
        #         # Enregistrer le DataFrame résultant dans un nouveau fichier CSV
        #         concatenated_df.to_csv(output_file_path, index=False)
        #         print(f"Fichier '{output_file_path}' créé avec succès.")

files_to_clean = chercher_fichiers_identiques(folder)
cleanup_files(files_to_clean)
