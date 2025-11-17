import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# On génère un dataset propre
X, y = make_classification(
    n_samples=2000,
    n_features=2,        # 2 features pour visualiser
    n_informative=2,
    n_redundant=0,
    class_sep=1.8,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)


# On empoisonne nos données en modifiant les features mais pas les labels

def clean_label_poison(X, y, target_class=0, shift_strength=0.8, poison_fraction=0.15):
    X_poison = X.copy()
    y_poison = y.copy()

    # indices de la classe cible
    idx_target = np.where(y == target_class)[0]
    n_poison = int(len(idx_target) * poison_fraction)

    # sélection des échantillons à empoisonner
    poison_idx = np.random.choice(idx_target, n_poison, replace=False)

    # On calcule le centre de l’autre classe
    center_other = X[y != target_class].mean(axis=0)

    # On déplace les points choisis vers le centre de la classe ennemie
    for i in poison_idx:
        direction = center_other - X[i]
        X_poison[i] = X[i] + shift_strength * direction

    return X_poison, y_poison, poison_idx


# On créé notre dataset empoisonné

X_train_poison, y_train_poison, poison_idx = clean_label_poison(
    X_train, y_train,
    target_class=0,
    shift_strength=0.9,
    poison_fraction=0.20
)

# On entraine notre model clean

model_clean = LogisticRegression()
model_clean.fit(X_train, y_train)

acc_clean = accuracy_score(y_test, model_clean.predict(X_test))
print("Accuracy CLEAN :", acc_clean)


# Et notre model empoisonné 

model_poison = LogisticRegression()
model_poison.fit(X_train_poison, y_train_poison)

acc_poison = accuracy_score(y_test, model_poison.predict(X_test))
print("Accuracy POISON clean-label :", acc_poison)


# On visualise les résultats

plt.figure(figsize=(7,6))

# Données propres
plt.scatter(X_train[:,0], X_train[:,1], c=y_train, cmap="coolwarm", s=10, label="Clean")

# Points empoisonnés
plt.scatter(
    X_train_poison[poison_idx,0],
    X_train_poison[poison_idx,1],
    c="green", edgecolors="black", s=50, marker="X",
    label="Poisoned (clean-label)"
)

plt.title("Clean-Label Poisoning Visualization")
plt.legend()
plt.show()
