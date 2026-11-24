# Importation de Streamlit pour créer l'application web
import streamlit as st

# =========================
# CONFIGURATION DE LA PAGE
# =========================
# On définit le titre de l’onglet, l’icône et le layout
st.set_page_config(
    page_title="Projet Data Collection",
    page_icon=" ",
    layout="wide"
)

# =========================
# TITRE PRINCIPAL
# =========================
# Affichage du titre principal avec du HTML pour personnalisation du style
st.markdown("""
<h1 style='text-align:center;color:#1E88E5;'>
Projet Scraping Immobilier CoinAfrique
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# SOUS-TITRE
# =========================
st.markdown("""
<h3 style='text-align:center;'>
Collecte automatisée de données immobilières
</h3>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# SECTION INFORMATIONS
# =========================
# On utilise des colonnes pour organiser les informations en 2 blocs

col1, col2 = st.columns(2)

# =========================
# COLONNE 1 : INFOS ACADEMIQUES
# =========================
with col1:

    # Message de succès (classe / groupe)
    st.success("""
    ### Classe
    Master 1 IA  
    JANV_Cohorte2
    """)

    # Information sur le professeur
    st.info("""
    ### Professeur
    M. SABOUBANGA Willane Jaures
    """)

# =========================
# COLONNE 2 : INFOS PROJET
# =========================
with col2:

    # Matière du projet
    st.warning("""
    ### Matière
    Data Collection
    """)

    # Auteurs du projet
    st.error("""
    ### Présenté par
    Bousso SECK  
    Kine CISSE
    """)

st.markdown("---")

# =========================
# BOUTON DE NAVIGATION
# =========================
# On centre le bouton sur la page
c1, c2, c3 = st.columns([2,1,2])

with c2:
    # Bouton pour passer à la page principale du projet
    if st.button("Commencer"):
        st.switch_page("pages/view.py")