import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from scipy.sparse import coo_matrix
import numpy as np

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

knn = KNeighborsClassifier(n_neighbors=4)  # You can adjust the number of neighbors as needed
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

scores = cross_validate(knn, X, y, cv=5, scoring='f1_macro', return_train_score=True)

print("Training Scores:", scores['train_score'])
print("Testing Scores:", scores['test_score'])

print("Cross-Validation Scores:", scores)
print(f"Mean F1 : { np.mean(scores['test_score']) }")

# print("-------------------")

# data_scaled = scaler.transform(data.drop('label', axis=1))
# p = knn.predict([ data_scaled[0] ])

