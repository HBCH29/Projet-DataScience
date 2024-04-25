import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from scipy.sparse import coo_matrix

# Path to your custom CSV dataset
csv_file = "tache3/labels.csv"

# Charger les données à partir d'un fichier CSV
data = pd.read_csv(csv_file, sep=";")

data = data.dropna()

X = data.drop('label', axis=1)  # Features
y = data['label']  # Labels


X_sparse = coo_matrix(X)

X, X_sparse, y = shuffle(X, X_sparse, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


knn = KNeighborsClassifier(n_neighbors=5)  # You can adjust the number of neighbors as needed
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

scores = cross_validate(knn, X, y, cv=5, scoring='f1_macro', return_train_score=True)

print("Training Scores:", scores['train_score'])
print("Testing Scores:", scores['test_score'])

print("Cross-Validation Scores:", scores)


print("-------------------")

data_scaled = scaler.transform(data.drop('label', axis=1))
p = knn.predict(data_scaled)

# for i in range(data.shape[0]):
#     print(f"{data.iloc[i]['label']} -> {p[i]}")


# WIP
# Calculer la matrice de corrélation
# corr_matrix = data.corr().corr(method='pearson')
# Définir un seuil de corrélation élevée
# threshold = 0.2

# Parcourir les colonnes et supprimer les colonnes redondantes
# redundant_columns = []

# print(corr_matrix)
    # for j in range(i+1, len(corr_matrix.columns)):

    #     if abs(corr_matrix.iloc[i, j]) <= threshold :
    #         print(abs(corr_matrix.iloc[i, j]))
    #         redundant_columns.append(corr_matrix.columns[j])

# Supprimer les colonnes redondantes du jeu de données
# data = data.drop(redundant_columns, axis=1)
# import seaborn as sns
# fig, ax = plt.subplots()
# sns.heatmap(data.corr(), annot=True)
# plt.show()

# Create an instance of your custom dataset
# custom_dataset = CustomDataset(csv_file)
 

