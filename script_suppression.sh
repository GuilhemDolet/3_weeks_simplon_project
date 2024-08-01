# avoir installé Azure Cli

# se logger avec azure cli dans cet environnement

# ensuite taper dans le terminal "chmod +x create_resource_groupe.sh"

# charger les variables d'environnement
set -o allexport #suprime toutes les variables importées avant celle la
source .env #crée des variables d'environnement à partir du .env
set +o allexport

# az group create --name $RESOURCE_GROUP --location $LOCATION #Créer le groupe ressource (renseigné dans le .env)
az group delete --name $RESOURCE_GROUP  #Supprimer le groupe ressource (renseigné dans le .env)


# az storage account create --name $STORAGE_GROUP --resource-group $RESOURCE_GROUP --location $LOCATION
# az storage account delete --name $STORAGE_GROUP --resource-group $RESOURCE_GROUP


# pour créer un blob storage : uploader un fichier + créer un conteneur dans la même commande
# ensuite downloader le fichier depuis le blob