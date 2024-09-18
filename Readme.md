# Dashboard Compagnie aérienne # Dashboard pour Compagnie Aérienne
Ce projet est un tableau de bord pour une compagnie aérienne. Les données sont obtenues à partir de [ce lien](https://edu.postgrespro.com/demo-big-en.zip).

## Description du Projet

Le projet se compose de deux parties principales :

1. **Pipeline de Données** : Créé avec Airflow et DuckDB, ce pipeline extrait les données d'une base PostgreSQL et les charge dans une base MongoDB sur Atlas.
2. **Application Streamlit** : Cette application récupère les données de la base MongoDB, les traite et les affiche sous forme de tableau de bord interactif.

## Structure du Projet

- **Airflow** : Utilisé pour orchestrer le pipeline de données.
- **DuckDB** : Utilisé pour le traitement intermédiaire des données.
- **PostgreSQL** : Source des données initiales.
- **MongoDB Atlas** : Base de données cible pour le stockage des données traitées.
- **Streamlit** : Utilisé pour créer le tableau de bord interactif.

## Prérequis

- Docker
- Docker Compose
- Make

## Installation

Clonez le dépôt et naviguez dans le répertoire du projet :

```bash
git clone https://github.com/abrahamkoloboe27/Airflow-Pipeline-Dashboard-Compagnie-Aerienne
cd AIRFLOW
```

## Lancer le Projet

Pour lancer le projet, utilisez les commandes suivantes :

### Initialisation

```bash
make build
```

Cette commande construit les images Docker nécessaires.

### Démarrage des Services

```bash
make up
```

Cette commande démarre tous les services nécessaires, y compris Airflow et MongoDB.

### Démarrage et Construction des Services

```bash
make up-build
```

Cette commande construit et démarre tous les services nécessaires.

### Arrêt des Services

```bash
make down
```

Cette commande arrête tous les services en cours d'exécution.

## Utilisation

1. **Pipeline de Données** : Le pipeline Airflow extrait les données de PostgreSQL, les traite avec DuckDB et les charge dans MongoDB Atlas.
2. **Tableau de Bord** : L'application Streamlit récupère les données de MongoDB, les traite et les affiche.

## Conclusion

Ce projet fournit une solution complète pour la gestion et la visualisation des données d'une compagnie aérienne. Il utilise des technologies modernes pour assurer une orchestration efficace et une visualisation interactive des données.

