# Importation des bibliothèques nécessaires
from requests import get              # pour envoyer des requêtes HTTP
from bs4 import BeautifulSoup as bs   # pour analyser le HTML
import pandas as pd                   # pour manipuler les données
import time                           # pour ralentir le scraping (éviter blocage site)
import re                             # pour extraire des informations avec regex


# =========================
# FONCTION DE SCRAPING
# =========================
def scrape(nb_pages):

    # Liste qui va contenir toutes les annonces récupérées
    data = []

    # Header pour simuler un navigateur et éviter le blocage du site
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # =========================
    # BOUCLE SUR LES PAGES
    # =========================
    for p in range(1, nb_pages + 1):

        print(f"Scraping page {p}")

        # URL de la page dynamique (pagination)
        url = f"https://sn.coinafrique.com/categorie/immobilier?page={p}"

        try:
            # Envoi de la requête HTTP
            res = get(url, headers=headers, timeout=20)

            # Si la requête échoue, on passe à la page suivante
            if res.status_code != 200:
                continue

            # Analyse du contenu HTML de la page
            soup = bs(res.text, 'html.parser')

            # Sélection de toutes les annonces sur la page
            containers = soup.find_all('div', class_='col s6 m4 l3')

        except Exception as e:
            # Gestion des erreurs réseau ou parsing
            print("Erreur page:", e)
            continue

        # =========================
        # BOUCLE SUR CHAQUE ANNONCE
        # =========================
        for container in containers:

            # Initialisation des variables
            prix = None
            description = None
            localisation = None
            url_annonce = None
            nombre_pieces = None
            nombre_salle_de_bain = None
            superficie = None

            # ========================
            # EXTRACTION DES INFOS PRINCIPALES
            # ========================

            # Prix du bien
            try:
                prix = container.find('p', class_='ad__card-price').text.strip()
            except:
                pass

            # Description du bien
            try:
                description = container.find('p', class_='ad__card-description').text.strip()
            except:
                pass

            # Localisation du bien
            try:
                localisation = container.find('p', class_='ad__card-location').text.strip()
            except:
                pass

            # Lien vers la page détail de l’annonce
            try:
                url_annonce = "https://sn.coinafrique.com" + container.find('a')['href']
            except:
                pass

            # ========================
            # SCRAPING DE LA PAGE DÉTAIL
            # ========================
            if url_annonce:
                try:
                    res_detail = get(url_annonce, headers=headers, timeout=40)

                    if res_detail.status_code == 200:

                        soup_detail = bs(res_detail.text, 'html.parser')

                        # Extraction des caractéristiques détaillées
                        params = soup_detail.find_all(
                            "li",
                            class_="ad-parameters__list-item"
                        )

                        for param in params:

                            text = param.text.lower()

                            # ---------------- NOMBRE DE PIECES ----------------
                            if "pi" in text:
                                match = re.search(r"\d+", text)
                                if match:
                                    nombre_pieces = int(match.group())

                            # ---------------- SALLE DE BAIN ----------------
                            elif "salle" in text:
                                match = re.search(r"\d+", text)
                                if match:
                                    nombre_salle_de_bain = int(match.group())

                            # ---------------- SUPERFICIE ----------------
                            if "terrain" in text or "terrains" in text:

                                cleaned = text.replace(" ", "").lower()

                                match = re.search(r"(\d+(?:[\.,]\d+)?)m?2", cleaned)

                                if match:
                                    superficie = float(match.group(1).replace(",", "."))

                except Exception as e:
                    print("Erreur detail:", e)

            # ========================
            # STRUCTURE FINALE DES DONNÉES
            # ========================
            obj = {
                "prix": prix,
                "description": description,
                "localisation": localisation,
                "type_de_bien": None,  # sera calculé plus tard dans le cleaning
                "nombre_pieces": nombre_pieces,
                "nombre_salle_de_bain": nombre_salle_de_bain,
                "superficie": superficie,
                "url": url_annonce
            }

            # Ajout de l’annonce dans la liste
            data.append(obj)

            # Pause pour éviter de surcharger le site
            time.sleep(0.3)

    # =========================
    # CONVERSION EN DATAFRAME
    # =========================
    df = pd.DataFrame(data)

    # Réindexation propre (1,2,3,...)
    df.index = range(1, len(df) + 1)

    # Retour du dataset final
    return df