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
            # Extraction du nom du fichier sans l'extension
            base_name, _ = os.path.splitext(file_name)

            # Ajouter le chemin du fichier au dictionnaire
            if base_name not in fichiers_identiques:
                fichiers_identiques[base_name] = [file_path]
            else:
                fichiers_identiques[base_name].append(file_path)

    return fichiers_identiques
def fusionner_fichiers(dataframes):
    # Fusionner les DataFrames dans une liste
    merged_data = pd.concat(dataframes)
    # Organiser chronologiquement
    merged_data.sort_values(by='date', inplace=True)  # Remplacez 'date_colonne' par le nom de votre colonne de date
    # Supprimer les doublons
    merged_data.drop_duplicates(inplace=True)
    
    return merged_data
def lire_fichier(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == '.csv':
        return pd.read_csv(file_path)
    elif ext == '.txt':
        return pd.read_csv(file_path, delimiter='\t')  # Adapter le délimiteur selon vos besoins pour les fichiers texte
    else:
        raise ValueError(f"Extension de fichier non prise en charge : {ext}")
# Liste pour stocker les DataFrames fusionnés
merged_dfs = []
resultat = chercher_fichiers_identiques(folder)
n=0
# Afficher le résultat
for nom_fichier, chemins in resultat.items():
    if len(chemins) > 2:
        # Liste pour stocker les DataFrames de chaque fichier identique
        dfs = []
        print(f"Fichiers identiques pour '{nom_fichier}':")
        for chemin in chemins:
            print(chemin)
            df = lire_fichier(chemin)
            dfs.append(df)
          # Fusionner les DataFrames et ajouter au résultat final
        merged_df = fusionner_fichiers(dfs)
        merged_dfs.append(merged_df)


# Fusionner tous les DataFrames
final_merged_df = pd.concat(merged_dfs)

# Enregistrer le résultat dans un fichier unique
final_merged_df.to_csv(os.path.join(output, 'resultat_final.csv'), index=False)  # Modifier le chemin selon vos besoins

print("Fusion et enregistrement terminés.")