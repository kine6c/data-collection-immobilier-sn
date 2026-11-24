# Application de collecte et d'analyse de données immobilières – CoinAfrique Sénégal

Application Streamlit qui collecte automatiquement les annonces immobilières de [CoinAfrique Sénégal](https://sn.coinafrique.com/categorie/immobilier), nettoie les données, les visualise et intègre un formulaire d'enquête KoboToolbox.

> Projet réalisé dans le cadre du cours **Data Collection** – Master 1 Intelligence Artificielle (cohorte janvier 2026), Dakar Institute of Technology.

---

## Aperçu

<!-- Ajoutez 1 ou 2 captures d'écran dans le dossier images/ -->
![Aperçu de l'application](images/apercu.png)

---

## Fonctionnalités

### 1. Collecte des données (scraping)
- Choix du nombre de pages à scraper, lancement en un clic
- Parcours des pages de liste, puis de **la page détail de chaque annonce** pour récupérer les caractéristiques complètes
- Affichage des données collectées et du nombre total de biens
- Téléchargement du dataset
- Gestion des erreurs réseau et pause entre les requêtes pour ne pas surcharger le site

**Variables collectées :** prix, description, localisation, type de bien, nombre de pièces, nombre de salles de bain, superficie, URL de l'annonce.

### 2. Nettoyage des données
- Normalisation du texte des descriptions
- **Extraction automatique du type de bien** (appartement, villa, studio, terrain…) et **du nombre de pièces** à partir de la description, par expressions régulières
- Conversion des prix en valeurs numériques et suppression des annonces sans prix
- Découpage de la localisation en **quartier, ville et pays**
- Suppression des colonnes trop incomplètes et des doublons

### 3. Visualisation
<!-- Remplacez par vos vrais graphiques -->
- Répartition des types de biens
- Top des quartiers les plus chers
- Nombre d'annonces par localisation

### 4. Formulaire KoboToolbox
Formulaire d'enquête intégré dans l'application (iframe) pour aider une agence immobilière à mieux comprendre les besoins de ses clients : type de bien recherché, zones, budget, critères importants.

---

## Technologies utilisées

| Étape | Outils |
| --- | --- |
| Scraping | Requests, BeautifulSoup |
| Nettoyage | Pandas, NumPy, expressions régulières (re) |
| Visualisation | <!-- ex. Plotly, Matplotlib --> |
| Application | Streamlit (application multipage) |
| Formulaire | KoboToolbox |

---

## Structure du projet

```
├── app.py              # Page d'accueil de l'application
├── pages/
│   └── view.py         # Page principale : scraping, données, graphiques, formulaire
├── scraper.py          # Collecte des annonces (pages de liste + pages détail)
├── cleaning.py         # Nettoyage et enrichissement des données
├── page_1.html         # Page CoinAfrique sauvegardée, utilisée pour tester les sélecteurs
├── requirements.txt    # Dépendances
└── README.md
```

---

## Installation et lancement

```bash
git clone https://github.com/kine6c/NOM-DU-DEPOT.git
cd Immo_App_Collecte_Analyse
pip install -r requirements.txt
streamlit run app.py
```

---

## Démonstration

<!-- Lien vers la vidéo explicative (YouTube, Google Drive…) -->

---

## Auteures

- **Fatou Kiné Cissé** – [GitHub](https://github.com/kine6c)
- **Bousso Seck**

Encadrement : M. Willane Jaurès Saboubanga – cours Data Collection
