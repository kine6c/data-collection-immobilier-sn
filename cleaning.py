# Importation des bibliothèques
import pandas as pd
import numpy as np

# =========================
# FONCTION DE NETTOYAGE
# =========================
def clean_data(df):

    # Vérification : si le DataFrame est vide, on le retourne directement
    if df.empty:
        return df

    # Copie du DataFrame pour éviter de modifier les données originales
    df = df.copy()

    # =========================
    # 1. NETTOYAGE DU TEXTE
    # =========================
    # On s'assure que les colonnes essentielles existent
    for col in ["description", "prix", "localisation"]:
        if col not in df.columns:
            df[col] = ""

    # Nettoyage de la description :
    # - conversion en string
    # - mise en minuscule
    # - suppression des espaces inutiles
    df["description"] = (
        df["description"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # =========================
    # 2. EXTRACTION DU TYPE DE BIEN
    # =========================
    # On détecte automatiquement le type de logement dans la description
    df["type_de_bien"] = df["description"].str.extract(
        r"(appartement|maison|villa|studio|duplex|bureau|terrain|immeuble|magasin|local|showroom)",
        expand=False
    )

    # Si aucune correspondance, on met "inconnu"
    df["type_de_bien"] = df["type_de_bien"].fillna("inconnu")

    # =========================
    # 3. EXTRACTION DU NOMBRE DE PIECES
    # =========================
    # On cherche les nombres associés aux pièces/chambres dans la description
    desc_pieces = df["description"].str.extract(
        r"(\d+)\s*(?:pièces?|piece|chambres?|chambre)",
        expand=False
    )

    # Conversion en numérique + gestion des valeurs manquantes
    df["nombre_pieces"] = (
        pd.to_numeric(desc_pieces, errors="coerce")
        .fillna(df["nombre_pieces"])  # garde valeur scraping si existante
        .fillna(0)
        .astype(int)
    )

    # =========================
    # 4. NETTOYAGE DU PRIX
    # =========================
    # Suppression de tout ce qui n'est pas un chiffre
    df["prix"] = (
        df["prix"]
        .astype(str)
        .str.replace(r"[^0-9]", "", regex=True)
    )

    # Conversion en numérique
    df["prix"] = pd.to_numeric(df["prix"], errors="coerce")

    # Suppression des lignes sans prix
    df = df.dropna(subset=["prix"])

    # Conversion finale en entier
    df["prix"] = df["prix"].astype(int)

    # =========================
    # 5. TRAITEMENT DE LA LOCALISATION
    # =========================
    # On sépare la localisation en : Quartier, Ville, Pays
    df["localisation"] = (
        df["localisation"]
        .fillna("")
        .astype(str)
    )

    loc_split = df["localisation"].str.split(",", expand=True)

    # Création des colonnes avec gestion des cas manquants
    df["Quartier"] = loc_split[0].str.strip() if 0 in loc_split.columns else "Inconnu"
    df["Ville"] = loc_split[1].str.strip() if 1 in loc_split.columns else "Inconnu"
    df["Pays"] = loc_split[2].str.strip() if 2 in loc_split.columns else "Sénégal"
    df["Pays"] = (
        df["Pays"]
        .replace("", np.nan)
        .fillna("Sénégal")
    )

    # Sécurité supplémentaire : aucun pays ne doit être vide
    df["Pays"] = df["Pays"].fillna("Sénégal")
    # =========================
    # 6. SUPPRESSION DES COLONNES INUTILES
    # =========================
    # Ces colonnes sont supprimées car elles sont vides ou non utilisées
    df = df.drop(columns=["nombre_salle_de_bain", "superficie"], errors="ignore")

    # =========================
    # 7. SUPPRESSION DES DOUBLONS
    # =========================
    df = df.drop_duplicates()

    # =========================
    # 8. REINDEXATION PROPRE
    # =========================
    # On remet un index propre (1,2,3,...)
    df = df.reset_index(drop=True)
    df.index += 1

    # Retour du DataFrame nettoyé
    return df