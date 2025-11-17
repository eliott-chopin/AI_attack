# 🛡️ AI Red Teaming – Attaques de Data Poisoning & Backdoor  
Projet démontrant trois types d’attaques sur un modèle Machine Learning.  
Usage strictement pédagogique (AI Red Teaming, recherche, robustesse).  
Toutes les données utilisées sont synthétiques.

---

# 📌 Contenu du dépôt

Ce repository contient trois scripts Python distincts :

1. label_flipping_and_feature_injection.py  
   Contient deux attaques de data poisoning :  
   - Label Flipping : inversion malveillante d’une partie des étiquettes  
   - Feature Injection : ajout de fausses données artificielles pour perturber la frontière de décision  

2. clean_label_poisoning.py  
   Attaque furtive de clean-label où les labels NE sont PAS modifiés.  
   On déplace des points de manière stratégique pour tromper le modèle.

3. backdoor_trigger.py  
   Implémentation d’une behavioral backdoor.  
   Le modèle fonctionne normalement, mais lorsqu’un trigger est présent dans l’entrée, il exécute :  
   print("hello world")

---

# 🚀 1. Label Flipping & Feature Injection

Ces deux attaques modifient directement le dataset avant l’entraînement.

## Label Flipping
Fonctionnement :  
- Sélection d’une fraction du dataset  
- Inversion des labels (0 devient 1, 1 devient 0)  
- Le modèle apprend alors une frontière biaisée

## Feature Injection
Fonctionnement :  
- Création de nouvelles données artificielles "malveillantes"  
- Ajout à la classe choisie  
- Perturbation de la frontière de décision

---

# 🚀 2. Clean-Label Poisoning

Attaque très furtive :  
- Ne modifie pas les labels  
- Déplace subtilement certains points pour biaiser la frontière  
- Difficile à détecter par inspection humaine ou statistique

---

# 🚀 3. Backdoor Attack (Trigger → Comportement caché)

C’est une behavioral backdoor :  
- Le modèle fonctionne normalement  
- MAIS si un trigger apparaît, le modèle exécute une action cachée  
Ici : print("hello world")

Le trigger utilisé se base sur une condition simple dans les features (ex : une feature dépassant un seuil).

---

# 🎯 Objectifs du projet

Ce projet permet :

- d’étudier plusieurs attaques de poisoning  
- d’observer leurs impacts sur les performances d’un modèle  
- de comprendre le fonctionnement d’une backdoor comportementale  
- de comparer attaques bruyantes, furtives et ciblées  
- de pratiquer des techniques d’AI Red Teaming

---

# 🧪 Utilisation

Chaque script peut être exécuté indépendamment :

python label_flipping_and_feature_injection.py  
python clean_label_poisoning.py  
python backdoor_trigger.py  

Chaque fichier :

- génère un dataset propre  
- applique une attaque  
- entraîne un modèle clean / empoisonné  
- compare leurs performances  
- affiche éventuellement des visualisations

---

# 🛡️ Disclaimer

Ce projet est strictement réservé à l’enseignement, la recherche et l’expérimentation en environnement contrôlé.  
N’utilisez jamais ces techniques hors cadre légal et éthique.

---

# 🤝 Contributions

Suggestions bienvenues pour :  
- ajouter d’autres attaques (backdoor clean-label, TrojanNN, BadNets)  
- intégrer des défenses (Neural Cleanse, Spectral Signatures)  
- améliorer le contenu pédagogique
