import pandas as pd
import os

folder = 'TP Data 2024 - FISA'
output = 'tache1'

def chercher_fichiers_identiques(input_folder):
    # Dictionnaire pour stocker les fichiers identiques
    fichiers_identiques = {}

    # Parcourir récursivement les sous-dossiers
    for root, dirs, files in os.walk(input_folder):
        for file_name in files:
            # Construction du chemin complet du fichier
            file_path = os.path.join(root, file_name)


            # Ajouter le chemin du fichier au dictionnaire
            if file_name not in fichiers_identiques:
                fichiers_identiques[file_name] = [file_path]
            else:
                fichiers_identiques[file_name].append(file_path)

    return fichiers_identiques

resultat = chercher_fichiers_identiques(folder)

# Traiter les fichiers identiques
for nom_fichier, chemins in resultat.items():
    if len(chemins) > 1 :
        output_file_path = os.path.join(output, nom_fichier)
        print(output_file_path)
           # Vérifier si le fichier de sortie existe déjà
        if os.path.exists(output_file_path):
            print(f"Le fichier '{output_file_path}' existe déjà.")
        else:
            print(f"Traitement des fichiers pour '{nom_fichier}':")
            dfs = [] 
            if nom_fichier.endswith(".csv"):
                for chemin in chemins:
                    df = pd.read_csv(chemin,comment="#")
                    dfs.append(df)
                concatenated_df = pd.concat(dfs, ignore_index=True)
                print(concatenated_df.info())
                try:
                    # Vérifier les échantillons en double
                    duplicates = concatenated_df.duplicated()

                    # Afficher les échantillons en double
                    print("Échantillons en double :")
                    print(concatenated_df[duplicates])

                    # Compter le nombre d'échantillons en double
                    nombre_doublons = duplicates.sum()
                    print(f"Nombre total d'échantillons en double : {nombre_doublons}")
                    # Supprimer les échantillons en double
                    concatenated_df.drop_duplicates(inplace=True)
                    print("Echantillons en double ont été supprimé")
                    # Trier par date
                    concatenated_df['date'] = pd.to_datetime(concatenated_df['date'])
                    concatenated_df = concatenated_df.sort_values(by='date')
                    print("trié :D ")
                except Exception as e :
                    print(f"Error has occured {e}")
                # Enregistrer le DataFrame résultant dans un nouveau fichier CSV
                concatenated_df.to_csv(output_file_path, index=False)
                print(f"Fichier '{output_file_path}' créé avec succès.")

