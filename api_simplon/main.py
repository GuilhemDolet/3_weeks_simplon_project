#se connecter à une URL : uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://iratevenison3:qkDvlq24qQ1PUwqkuFNQRQ@pbo.postgres.database.azure.com:5432/flexibleserverdb")
connexion = engine.connect()

ma_liste_formations = {}

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/")  # Un message de bienvenue
# def bienvenue():
#     return {"message": "Bonjour, bienvenue sur la base de données Formations-Simplon"}

# @app.get("/get_list")  # Un dictionnaire de dictionnaires
# def get_list():
#     return {"content": ma_liste_formations}


#########################################################

# @app.post("/add_to_list")
# def add_to_list(produit: str, quantite: float, unite: str):
#     # Vérifier si l'élément est déjà dans le dictionnaire
#     try:
#         if produit in ma_liste_formations:  # Vérifier que la clé est présente dans le dictionnaire
#             # S'il est dans le dico, vérifier que l'unité est la même
#             if unite:
#                 if unite == ma_liste_formations[produit][1]:  # Vérifier si l'unité est la même
#                     ma_liste_formations[produit][0] += quantite  # Ajouter la quantité
#                     return {produit: ma_liste_formations[produit]}  # Renvoyer le produit et sa quantité
#                 else:
#                     # Si l'unité est différente, renvoyer une erreur
#                     raise HTTPException(
#                         status_code=400,
#                         detail=f"Not the good unit for the product, {produit} is in {ma_liste_formations[produit]}"
#                     )
#             else:
#                 ma_liste_formations[produit][0] += quantite  # Ajouter la quantité par défaut
#                 return {produit: ma_liste_formations[produit]}
#         else:
#             ma_liste_formations[produit] = [quantite, unite]  # Ajouter un nouvel élément au dictionnaire
#             return {produit: ma_liste_formations[produit]}
#     except KeyError as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @app.delete("/remove_from_list")
# def remove_from_list(produit: str):
#     try:
#         if produit not in ma_liste_formations:
#             raise HTTPException(status_code=404, detail="Element not found in the list")
#         del ma_liste_formations[produit]
#         return {"content": ma_liste_formations}
#     except KeyError as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @app.delete("/clean_list")
# def empty_list():
#     try:
#         if not ma_liste_formations:
#             raise HTTPException(status_code=404, detail="List is already empty")
#         ma_liste_formations.clear()
#         return {"content": ma_liste_formations}
#     except AttributeError as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Commande pour lancer l'application :
# uvicorn main:app --reload
