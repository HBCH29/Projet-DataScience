import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
# Define your custom dataset class
class CustomDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file, sep=";")  # Read CSV file into DataFrame

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data.iloc[idx, :]  # Get row at index 'idx'
        # sample = torch.tensor(sample.values.astype(float))
        return sample

# Path to your custom CSV dataset
csv_file = "tache3/labels.csv"

# Charger les données à partir d'un fichier CSV
data = pd.read_csv(csv_file, sep=";")

print(data.columns.shape)
# Calculer la matrice de corrélation
corr_matrix = data.corr().corr(method='pearson')
# Définir un seuil de corrélation élevée
threshold = 0.7

# Parcourir les colonnes et supprimer les colonnes redondantes
redundant_columns = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) >= threshold :
            print(abs(corr_matrix.iloc[i, j]))
            redundant_columns.append(corr_matrix.columns[j])

# Supprimer les colonnes redondantes du jeu de données
data = data.drop(redundant_columns, axis=1)
import seaborn as sns
fig, ax = plt.subplots()
sns.heatmap(data.corr(), annot=True)
plt.show()
# Create an instance of your custom dataset
custom_dataset = CustomDataset(csv_file)


# Create a dataloader for your data
train_loader = DataLoader(dataset=custom_dataset, batch_size=50, shuffle=True)

print(train_loader.dataset[0]['label'])
