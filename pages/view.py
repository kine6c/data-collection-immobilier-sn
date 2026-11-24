# Importation de Streamlit pour créer l'application web
import streamlit as st

# Import des fonctions du projet
from scraper import scrape        # fonction de scraping des données
from cleaning import clean_data   # fonction de nettoyage des données

# =========================
# CONFIGURATION DE LA PAGE
# =========================
# Définition du titre, icône et layout de la page
st.set_page_config(
    page_title="Scraping Immobilier",
    page_icon=" ",
    layout="wide"
)

# =========================
# STYLE CSS PERSONNALISÉ
# =========================
# Permet de rendre l'interface plus professionnelle et attractive
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

/* Bannière principale */
.banner {
    background: linear-gradient(90deg,#1565C0,#42A5F5);
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    margin-bottom:20px;
}

/* Carte KPI (statistiques) */
.kpi-card{
    background:linear-gradient(90deg,#43A047,#66BB6A);
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    font-weight:bold;
    box-shadow:0px 4px 12px rgba(0,0,0,0.15);
}

.kpi-title{
    font-size:18px;
}

.kpi-value{
    font-size:40px;
}

/* Espacement général */
.block-container{
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# =========================
# EN-TÊTE (HEADER)
# =========================
# Affichage du titre principal du projet
st.markdown("""
<div class="banner">
    <h1> Scraping Immobilier CoinAfrique</h1>
    <p>Collecte, Nettoyage et Analyse des Annonces Immobilières</p>
</div>
""", unsafe_allow_html=True)

# =========================
# PARAMÈTRE UTILISATEUR
# =========================
# L'utilisateur choisit le nombre de pages à scraper
st.subheader(" Paramètres de collecte")

nb_pages = st.number_input(
    "Nombre de pages à scraper",
    min_value=1,
    value=1
)

# =========================
# GESTION DE LA MÉMOIRE (SESSION STATE)
# =========================
# Permet de stocker les données entre les interactions
if "df_raw" not in st.session_state:
    st.session_state.df_raw = None

if "df_clean" not in st.session_state:
    st.session_state.df_clean = None

# =========================
# LANCEMENT DU SCRAPING
# =========================
#if st.button(" Lancer le scraping", width="stretch"):
if st.button("Lancer le scraping", use_container_width=True):
    # Barre de chargement pendant l'exécution
    with st.spinner("Scraping en cours..."):

        # Étape 1 : collecte des données brutes
        df = scrape(nb_pages)

        # Étape 2 : nettoyage des données
        df_clean = clean_data(df)

        # Stockage dans la session Streamlit
        st.session_state.df_raw = df
        st.session_state.df_clean = df_clean

    # Message de succès
    st.success(" Scraping et nettoyage terminés")

# =========================
# AFFICHAGE DES RÉSULTATS
# =========================
if st.session_state.df_clean is not None:

    # Récupération des données
    df_raw = st.session_state.df_raw
    df_clean = st.session_state.df_clean

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # KPI (STATISTIQUES)
    # =========================
    col1, col2 = st.columns(2)

    # Nombre d'annonces scrapées
    with col1:
        st.metric("Annonces scrapées", len(df_raw))

    # Nombre après nettoyage
    with col2:
        st.metric("Après nettoyage", len(df_clean))

    st.markdown("---")

    # =========================
    # DONNÉES BRUTES
    # =========================
    st.subheader(" Données brutes (scrapées)")

    st.dataframe(
        df_raw,
        use_container_width=True,
        height=300
    )

    st.markdown("---")

    # =========================
    # DONNÉES NETTOYÉES
    # =========================
    st.subheader(" Données nettoyées")

    st.dataframe(
        df_clean,
        use_container_width=True,
        height=300
    )

    st.markdown("---")

    # =========================
    # TÉLÉCHARGEMENT DES DONNÉES
    # =========================
    col1, col2 = st.columns(2)

    # Export données brutes
    with col1:
        st.download_button(
            " Télécharger données brutes",
            df_raw.to_csv(index=False),
            "immobilier_brut.csv",
            "text/csv",
            use_container_width=True
        )

    # Export données nettoyées
    with col2:
        st.download_button(
            " Télécharger données nettoyées",
            df_clean.to_csv(index=False),
            "immobilier_nettoye.csv",
            "text/csv",
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # NAVIGATION VERS DASHBOARD
    # =========================
    if st.button("Visualiser les données nettoyées", use_container_width=True):
        st.switch_page("pages/viz.py")