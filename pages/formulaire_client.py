import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    page_title="Formulaire Immobilier",
    page_icon=" ",
    layout="wide"
)

# =========================
# STYLE CSS
# =========================
st.markdown("""
    <style>
        .title {
            text-align: center;
            color: #1E88E5;
            font-size: 40px;
            font-weight: bold;
            margin-top: 20px;
        }

        .subtitle {
            text-align: center;
            color: #555;
            font-size: 18px;
            margin-bottom: 25px;
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# TITRE CENTRÉ + COULEUR
# =========================
st.markdown('<div class="title"> Formulaire Client Immobilier</div>', unsafe_allow_html=True)

st.markdown('<div class="subtitle">Veuillez remplir le formulaire ci-dessous pour nous aider à mieux comprendre vos besoins</div>', unsafe_allow_html=True)

# =========================
# FORMULAIRE
# =========================
components.iframe(
    "https://ee.kobotoolbox.org/x/IpVGn1EW",
    height=800,
    scrolling=True
)