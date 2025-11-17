import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# On génère notre dataset propre
X, y = make_classification(
    n_samples=2000,
    n_features=5,
    n_informative=3,
    n_redundant=0,
    n_clusters_per_class=1,
    flip_y=0.0,
    class_sep=1.5,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)


##################### On génère des données malveillantes #####################

"""
Pour générer nos données malveillantes, on échange les classes de certaines données
"""

def poison_label_flipping(X, y, poison_fraction=0.2):
    n_poison = int(len(y) * poison_fraction)
    idx = np.random.choice(len(y), n_poison, replace=False)
    
    y_poisoned = y.copy()
    y_poisoned[idx] = 1 - y_poisoned[idx]   # Changement de labels
    
    return X.copy(), y_poisoned, idx


""" Pour la seconde attaque, on force des examples random à appartenir à certaines classes, ce qui va destabiliser le model"""
def poison_feature_injection(X, y, n_injected=200):
    # génération de points "malveillants"
    X_inj = np.random.uniform(low=-5, high=5, size=(n_injected, X.shape[1]))

    # on les force à appartenir à la classe 0,
    # mais en vrai ils ressemblent fortement à la classe 1
    y_inj = np.zeros(n_injected, dtype=int)
    
    # concat
    X_poisoned = np.vstack([X, X_inj])
    y_poisoned = np.hstack([y, y_inj])
    
    return X_poisoned, y_poisoned

####################################################################################

model_clean = LogisticRegression(max_iter=2000)
model_clean.fit(X_train, y_train)

y_pred = model_clean.predict(X_test)
acc_clean = accuracy_score(y_test, y_pred)

print("Accuracy sans poison :", acc_clean)



########## 1ère attaque : Label Flipping ###########

X_train_LF, y_train_LF, poisoned_idx = poison_label_flipping(
    X_train, y_train, poison_fraction=0.25
)

model_poison_LF = LogisticRegression(max_iter=2000)
model_poison_LF.fit(X_train_LF, y_train_LF)

y_pred_LF = model_poison_LF.predict(X_test)
acc_poison_LF = accuracy_score(y_test, y_pred_LF)

print("Accuracy avec label flipping :", acc_poison_LF)


############# 2ème attaque : Feature Injection ##############

X_train_FI, y_train_FI = poison_feature_injection(X_train, y_train, n_injected=300)

model_poison_FI = LogisticRegression(max_iter=2000)
model_poison_FI.fit(X_train_FI, y_train_FI)

y_pred_FI = model_poison_FI.predict(X_test)
acc_poison_FI = accuracy_score(y_test, y_pred_FI)

print("Accuracy avec feature injection :", acc_poison_FI)



############ On rajoute du visuel ################


plt.figure(figsize=(6,5))
plt.scatter(X_train[:,0], X_train[:,1], c=y_train, cmap="coolwarm", s=10, label="Clean")

plt.scatter(X_train_FI[-300:,0], X_train_FI[-300:,1], 
            c="green", s=20, marker="x", label="Injected")
plt.legend()
plt.title("Feature Injection - Data Poisoning Demo")
plt.show()
