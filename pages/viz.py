# Importation des bibliothèques nécessaires
# Streamlit : création de l'interface web
# Pandas : manipulation des données
# Plotly Express : création des graphiques interactifs
import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURATION DE LA PAGE
# =========================
# Définition du titre de l'application,
# de l'icône et du mode d'affichage en pleine largeur.
st.set_page_config(
    page_title="Dashboard Immobilier",
    page_icon=" ",
    layout="wide"
)

# =========================
# FONCTION DE FORMATAGE
# =========================
# Cette fonction permet de rendre les grands nombres
# plus lisibles dans les indicateurs KPI.
# Exemple :
# 1 500 000 -> 1M
# 2 500 -> 2K
def format_number(value):
    if pd.isna(value):
        return "0"
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.0f}M"
    elif value >= 1_000:
        return f"{value/1_000:.0f}K"
    return str(int(value))

# =========================
# PERSONNALISATION CSS
# =========================
# Ajout de styles CSS afin d'améliorer
# l'apparence du tableau de bord :
# - cartes KPI colorées
# - titres des graphiques
# - alignement du titre principal
st.markdown("""
<style>

h1 {
    text-align: center;
    color: #1E88E5;
}

/* KPI CARDS */
.kpi {
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-weight: bold;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
}

.kpi-title { font-size: 14px; opacity: 0.9; }
.kpi-value { font-size: 26px; margin-top: 5px; }

.blue { background: #1E88E5; }
.green { background: #43A047; }
.orange { background: #FB8C00; }
.purple { background: #8E24AA; }

/* TITRE GRAPHE */
.chart-title {
    background: linear-gradient(90deg, #1E88E5, #42A5F5);
    padding: 10px;
    border-radius: 12px;
    color: white;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
# Affichage du titre du dashboard
st.title(" Dashboard Immobilier CoinAfrique")
st.markdown("---")

# =========================
#  CHARGEMENT DES DONNÉES
# =========================
# Les données nettoyées sont récupérées depuis
# la session Streamlit (page de scraping).
# Si aucune donnée n'est disponible,
# l'application s'arrête
if "df_clean" in st.session_state and st.session_state.df_clean is not None:
    df = st.session_state.df_clean.copy()
else:
    st.error("Lance d'abord le scraping dans la page principale")
    st.stop()

# =========================
# FILTRES
# =========================
# Création de filtres dans la barre latérale
# pour permettre à l'utilisateur de sélectionner :
# - une ville
# - un type de bien
st.sidebar.header("Filtres")

df_filtre = df.copy()
# Filtre par ville
if "Ville" in df.columns:
    ville = st.sidebar.selectbox("Ville", ["Toutes"] + list(df["Ville"].dropna().unique()))
    if ville != "Toutes":
        df_filtre = df_filtre[df_filtre["Ville"] == ville]
# Filtre par type de bien
if "type_de_bien" in df.columns:
    type_bien = st.sidebar.selectbox("Type de bien", ["Tous"] + list(df["type_de_bien"].dropna().unique()))
    if type_bien != "Tous":
        df_filtre = df_filtre[df_filtre["type_de_bien"] == type_bien]

# =========================
# INDICATEURS KPI
# =========================
# Affichage des principaux indicateurs :
# - nombre total d'annonces
# - prix moyen
# - nombre de types de biens
# - nombre de villes
st.subheader(" Indicateurs clés")

k1, k2, k3, k4 = st.columns(4)
# KPI 1 : Total données netoyées
with k1:
    st.markdown(f"""
    <div class="kpi blue">
        <div class="kpi-title">Données netoyées</div>
        <div class="kpi-value">{len(df_filtre)}</div>
    </div>
    """, unsafe_allow_html=True)
# KPI 2 : Prix moyen
with k2:
    st.markdown(f"""
    <div class="kpi green">
        <div class="kpi-title">Prix moyen</div>
        <div class="kpi-value">{format_number(df_filtre["prix"].mean())}</div>
    </div>
    """, unsafe_allow_html=True)
# KPI 3 : Nombre de types de biens
with k3:
    st.markdown(f"""
    <div class="kpi orange">
        <div class="kpi-title">Types de biens</div>
        <div class="kpi-value">{df_filtre['type_de_bien'].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)
# KPI 4 : Nombre de villes
with k4:
    st.markdown(f"""
    <div class="kpi purple">
        <div class="kpi-title">Villes</div>
        <div class="kpi-value">{df_filtre['Ville'].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# GRAPHIQUES (STYLE DASHBOARD)
# =========================

# Première ligne de graphiques
c1, c2 = st.columns(2)
# Répartition des types de biens
with c1:
    st.markdown('<div class="chart-title">Types de biens</div>', unsafe_allow_html=True)

    data = df_filtre["type_de_bien"].value_counts().reset_index()
    data.columns = ["type_de_bien", "count"]

    fig = px.bar(data, x="type_de_bien", y="count", color="type_de_bien")
    st.plotly_chart(fig, use_container_width=True)
# Répartition des annonces par ville
with c2:
    st.markdown('<div class="chart-title">Annonces par ville</div>', unsafe_allow_html=True)

    data = df_filtre["Ville"].value_counts().head(10).reset_index()
    data.columns = ["ville", "count"]

    fig = px.bar(data, x="ville", y="count", color="ville")
    st.plotly_chart(fig, use_container_width=True)

# Deuxième ligne de graphiques
c3, c4 = st.columns(2)
# Top 10 des quartiers les plus chers
with c3:
    st.markdown('<div class="chart-title">Quartiers les plus chers</div>', unsafe_allow_html=True)

    data = df_filtre.groupby("Quartier")["prix"].mean().reset_index()
    data = data.sort_values("prix", ascending=False).head(10)

    fig = px.bar(data, x="Quartier", y="prix")
    st.plotly_chart(fig, use_container_width=True)
# Prix moyen selon le type de bien
with c4:
    st.markdown('<div class="chart-title">Prix moyen par type</div>', unsafe_allow_html=True)

    data = df_filtre.groupby("type_de_bien")["prix"].mean().reset_index()

    fig = px.bar(data, x="type_de_bien", y="prix", color="type_de_bien")
    st.plotly_chart(fig, use_container_width=True)

# Troisième ligne de graphiques
c5, c6 = st.columns(2)
# Distribution des prix
with c5:
    st.markdown('<div class="chart-title">Distribution des prix</div>', unsafe_allow_html=True)

    fig = px.histogram(df_filtre, x="prix", nbins=30)
    st.plotly_chart(fig, use_container_width=True)
# Relation entre le nombre de pièces et le prix
with c6:
    st.markdown('<div class="chart-title">Pièces vs Prix</div>', unsafe_allow_html=True)

    fig = px.scatter(df_filtre, x="nombre_pieces", y="prix")
    st.plotly_chart(fig, use_container_width=True)