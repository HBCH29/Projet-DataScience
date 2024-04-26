import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from sklearn.feature_selection import SelectKBest, f_classif
from scipy.sparse import coo_matrix
import numpy as np


# Path to your custom CSV dataset
csv_file = "tache3/labels.csv"

# Charger les données à partir d'un fichier CSV
data = pd.read_csv(csv_file, sep=";")

data = data.dropna()

X = data.drop('label', axis=1)  # Features

y = data['label']  # Labels

k = 53
print(f"K: {k}")
# Feature selection
selector = SelectKBest(score_func=f_classif, k=k)  # Find k features to drop
X_selected = selector.fit_transform(X, y)
mask = selector.get_support()

dropped_features = X.columns[~mask]
print(f"Dropped columns {dropped_features}")

# Shuffle and split data
X_selected_sparse = coo_matrix(X_selected)
X_selected, X_selected_sparse, y = shuffle(X_selected, X_selected_sparse, y)
X_train, X_test, y_train_selected, y_test_selected = train_test_split(X_selected, y, test_size=0.2)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Classifier
knn = KNeighborsClassifier(n_neighbors=4)  # You can adjust the number of neighbors as needed
knn.fit(X_train, y_train_selected)

# Prediction
y_pred = knn.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test_selected, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test_selected, y_pred))

# Cross-validation
scores = cross_validate(knn, X_selected, y, cv=5, scoring='f1_macro', return_train_score=True)

print("Training Scores:", scores['train_score'])
print("Testing Scores:", scores['test_score'])

print("Cross-Validation Scores:", scores)
print(f"Average F1 : {np.average(scores['test_score'])}")
print("-------------------")

# Uncomment if you want to test model's predictions

# test_dataset = data.drop([*dropped_features,'label'], axis=1)

# data_scaled = scaler.transform(test_dataset)
# p = knn.predict(data_scaled)

# for i in range(data.shape[0]):
#     print(f"{data.iloc[i]['label']} -> {p[i]}")
