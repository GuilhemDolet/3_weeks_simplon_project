import json
import requests
from urllib.parse import urlencode, quote_plus
import pandas as pd

url = "https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/json"

# Paramètres de la requête
query_params = {
    'select': "nom_of, nom_region, code_inventaire, code_rncp, intitule_certification, libelle_niveau_sortie_formation, code_formacode_1, code_formacode_2, code_formacode_3, code_formacode_4, code_formacode_5, libelle_code_formacode_principal, libelle_nsf_1, libelle_nsf_2, libelle_nsf_3, code_nsf_1, code_nsf_2, code_nsf_3",
    # "where" : "",
    "limit" : 30,
    "timezone": "UTC",
    "include_links": "false",
    "include_app_metas": "false"
    }
encoded_query_params = urlencode(query_params, quote_via=quote_plus)
#URL final
URL = f"{url}?{encoded_query_params}"

response = requests.get(URL)
if response.status_code == 200:
    # Convertir la réponse en JSON
    data = response.json()
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
        print("Données récupérées et enregistrées avec succès.")
else:
    print(f"Erreur {response.status_code} lors de la récupération des données.")

# Lire le fichier JSON
with open('data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Convertir la liste de dictionnaires en DataFrame pandas
df = pd.DataFrame(data)

# Enregistrer le DataFrame en tant que fichier CSV
df.to_csv('data.csv', index=False, encoding='utf-8')

print("Données JSON converties en CSV avec succès.")