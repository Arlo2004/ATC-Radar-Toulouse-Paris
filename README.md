
# ATC-Radar-Toulouse-Paris
# Projet d'Analyse de Trajectoires Aériennes : Route Toulouse - Paris
            __|__
     --@--@--(_)--@--@--$

## Introduction et Origine des Données
L'objectif principal de ce projet est d'étudier et d'analyser les trajectoires réelles de vols commerciaux. Pour obtenir ces données, nous avons eu recours à **OpenSky Network**, une plateforme *open-data* de niveau recherche qui capture et affiche le trafic aérien mondial en temps réel. 

## Le Défi du Volume de Données et l'Utilisation de Trino
Extraire des informations de cette plateforme présente un défi technique gigantesque : la base de données compile des millions de données provenant de milliers d'avions volant en temps réel tout autour du globe terrestre. Tenter de télécharger et de manipuler cette base de données brute détruirait la mémoire de n'importe quel ordinateur commun. 

Pour résoudre ce problème, OpenSky Network recommande l'utilisation de **Trino** (et fournit un tutoriel sur son usage), un moteur de requêtes SQL distribué. Trino agit comme un intermédiaire : au lieu de télécharger la base de données sur notre équipement, nous envoyons les instructions (queries) à leurs serveurs. Le serveur de Trino fait le "sale boulot" en cherchant l'information parmi des milliards de lignes et nous renvoie uniquement le résultat final et traité.

## L'Architecture de Recherche et la Résolution Temporelle
L'approche initiale du projet était d'analyser la route spécifique entre l'aéroport de Toulouse (LFBO) et Paris (LFPG/LFPO). Cependant, un obstacle est apparu : lors de la consultation de données trop récentes, le système d'OpenSky dispose d'un système de sécurité. Lequel ? On ne peut pas filtrer directement les noms ou les emplacements des aéroports que les avions ont comme destination.
Pour faciliter l'architecture de nos requêtes SQL et garantir l'intégrité des données, il a été décidé de travailler avec des archives historiques de **janvier 2024**. C'est avec ces anciens fichiers que l'architecture de la requête SQL se simplifie considérablement.

## Première Requête SQL : Sélection de la Flotte Candidate
La première étape computationnelle a été d'identifier les aéronefs. Une requête SQL a été conçue pour extraire un échantillon de vols selon les conditions suivantes :
* **Modèle d'aéronef :** Focus sur la famille Airbus A320 (le modèle d'avion qui domine les vols commerciaux en Europe).
* **Route :** Décollage exclusif depuis Toulouse à destination de Paris.
* **Filtre temporel :** Le format de temps **Unix Epoch** a été utilisé (un système qui compte les secondes écoulées depuis le 1er janvier 1970). Par exemple, les numéros comme `1704067200` représentent des dates exactes en janvier 2024. C'est le standard informatique universel pour éviter les problèmes.

Cette première requête nous a renvoyé une liste propre avec le code identifiant unique de chaque avion (ICAO24) et son heure exacte de décollage.

## Deuxième Requête SQL : Extraction de la Télémétrie
Une fois les candidats sélectionnés, nous avons choisi un groupe réduit pour une analyse approfondie. Via une deuxième requête SQL, nous avons demandé au serveur de tracer ces identifiants spécifiques tout au long de leur vol et d'extraire leurs variables physiques : vitesse, altitude, latitude, longitude et cap. Toutes ces données ont été regroupées et exportées dans un fichier CSV.

## Le Moteur de Visualisation (Code Principal)
Une fois le fichier CSV dans notre environnement, nous avons développé le noyau visuel de l'application en utilisant Python et Streamlit :
1. **Lecture :** Le programme ouvre le fichier CSV et le lit ligne par ligne, en nettoyant toute erreur de format.
2. **Le Scénario :** Il utilise la bibliothèque *Pydeck* pour générer une carte interactive sombre centrée sur la France.
3. **L'Animation :** Le programme inclut une "horloge interne". À mesure que cette horloge avance, le code cherche dans le CSV où se trouvait l'avion à cette seconde exacte, dessine l'icône sur cette coordonnée, trace l'estime de sa route et actualise la télémétrie à l'écran. C'est concrètement le cœur du script.

## Périmètres de Sécurité et Aéroports en Route
Pour enrichir l'analyse spatiale, les aéroports alternatifs le long de la trajectoire ont été cartographiés (ex. Limoges, Châteauroux, Orléans). 

De plus, une couche visuelle a été programmée avec un rayon de protection circulaire de **50 kilomètres** autour de chaque aérodrome. Cette distance se base sur les standards de l'Annexe 11 de l'OACI et les procédures PANS-OPS, représentant l'Aire de Contrôle Terminale étendue : la marge de manœuvre nécessaire pour qu'un aéronef puisse effectuer des circuits d'attente et entamer une approche en toute sécurité.


https://www.mh370search.com/
https://opensky-network.org/data/api
https://opendata.autorite-transports.fr/rapports/caracteristiques-des-aeroports-du-perimetre-de-regulation-de-lart/
https://arxiv.org/abs/2109.04247
https://univ.scholarvox.com/catalog/search/searchterm/AirBus%20A320?searchtype=all




