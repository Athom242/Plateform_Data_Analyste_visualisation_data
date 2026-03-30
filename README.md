![Image d'illustration](https://images.pexels.com/photos/270366/pexels-photo-270366.jpeg)

# PROJET PYTHON – DEV DATA P8

## Gestion et traitement de données

Ce projet est un outil pour manipuler, valider et analyser des fichiers de données avec Python. Il inclut un programme interactif pour tester et explorer les données facilement.  
⚠️ **Projet en cours de développement – fonctionnalités et optimisations à venir.**

## Auteur

**Anthony M.** – Développeur Python & passionné de data  
- Email : 59492035+Athom242@users.noreply.github.com  
- GitHub : [Athom242](https://github.com/Athom242)  

## Objectif

- Lire et analyser un fichier de données  
- Valider et structurer les informations  
- Manipuler les données avec Python  
- Proposer un menu interactif pour l’utilisateur  

L’idée est de créer une base solide que je pourrai étendre avec de nouvelles fonctionnalités open-source.

## 1. Traitement des données

### Étape 1 : Récupération des données
Récupérer le fichier : **Donnees_Projet_Python_Dev_Data**

### Étape 2 : Traitement des données
- Parcourir le fichier ligne par ligne  
- Stocker les données dans une structure adaptée : liste, tuple, dictionnaire ou combinaison

### Étape 3 : Validation des données
- Séparer les données valides et invalides  
- Une ligne est invalide si au moins une information ne respecte pas les règles

### Étape 4 : Gestion des données invalides
- Conserver les données originales  
- Identifier les champs incorrects  
- Fournir une explication

## 2. Règles de validation

### Code
- 3 lettres majuscules + 3 chiffres (ex. `AAD004`)  
- Longueur : 6 caractères

### Numéro
- Lettres majuscules et chiffres  
- Longueur : 7 caractères (ex. `H5G32YR`)

### Prénom
- Commence par une lettre  
- Minimum 3 lettres

### Nom
- Commence par une lettre  
- Minimum 2 lettres

### Date de naissance
- Format unique à définir  
- Toutes les dates doivent être converties dans ce format

### Classe
- De `6em` à `3em` + A/B/C/D  
- Exemple : `4emA`  
- Uniformiser toutes les valeurs

### Notes
- Matières séparées par `#`  
- Notes dans des crochets `[]`  
- Devoirs séparés par `|`, examen séparé par `:`  

Exemple :  
Math[12|11:13]#Francais[4|11|8:13]#Anglais[13,5|11:15]


- Extraire les notes de devoir et l’examen  
- Calculer la moyenne :  
moyenne = (moyenne_devoirs + 2 * examen) / 3


## 3. Fonctionnalités

### Affichage
- Voir les données valides ou invalides  
- Afficher une ligne par numéro  
- Afficher les 5 premières lignes

### Ajout
- Ajouter une nouvelle entrée  
- Valider automatiquement les données

### Modification
- Corriger une donnée invalide  
- Transférer vers les données valides

### Recherche
- Par numéro ou code  
- Calculer le pourcentage de données valides / invalides

## 4. Pagination
- 5 lignes par page par défaut  
- Possibilité de modifier le nombre de lignes affichées

## Installation

```bash
git clone <url_du_repo>
cd projet-python-dev-data
python main.py

Aucun module externe n’est nécessaire, uniquement Python standard.

Structure du projet

Projet_Python_Dev_Data/
│── data/
│── notebooks/
│── src/
│── README.md
│── requirements.txt
│── main.py

Exemple d’utilisation

# Lancer le menu interactif
menu()
# Afficher les 5 premières lignes valides
afficher_donnees(valide=True)
# Ajouter une entrée
ajouter_donnee()
# Rechercher une personne par numéro
rechercher_par_numero("H5G32YR")

# Contributions
Toutes contributions sont les bienvenues :

Bug fixes via issues
Améliorations et nouvelles fonctionnalités via Pull Requests
Idées pour visualisation ou export de données
Licence

MIT License – projet open-source.