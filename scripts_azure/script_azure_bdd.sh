######################################################
###### METHODE CREATION POSTGRE FLEXIBLE SERVER ######
######################################################

############### prerequis #################
# avoir installé Azure Cli
# se logger avec azure cli dans cet environnement
# ACTIVER LE SCRIPT "chmod +x script.sh" pour rendre le script exécutable
# EXECUTER LE SCRIPT avec /scripts_azure puis . script_azure_ressources.sh


#!/bin/bash

#### VARIABLES A METTRE (SECRET)



# Erase .env if exist to renew values
if [ -f ".env" ]; then
  rm ".env"
fi

# charger les variables d'environnement
 set -o allexport #supprime toutes les variables importées avant celle la
 source .env #crée des variables d'environnement à partir du .env 
 set +o allexport

# créer un groupe de resources (renseigné dans le .env), s'il n'existe pas
if ! az group show --name $RESOURCE_GROUP &>/dev/null; then
  az group create --name $RESOURCE_GROUP --location $LOCATION
fi

echo "___RESOURCE_GROUP___ finish"

# # créer un blob
# az storage account create --resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT --location $LOCATION

# echo "___BLOB___ finish"

# # créer un conteneur pour le blob : 
# az ad signed-in-user show --query id -o tsv | az role assignment create --role "Storage Blob Data Contributor" --assignee @- --scope "/subscriptions/$SUBSCRIPTION/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Storage/storageAccounts/$STORAGE_ACCOUNT" 
# az storage container create --account-name $STORAGE_ACCOUNT --name $STORAGE_CONTAINER --auth-mode login
# echo "___BLOB_CONTAINER___ finish"

# # # commande pour uploader le fichier :
# # az storage blob upload --account-name $STORAGE_ACCOUNT --container-name $STORAGE_CONTAINER --name script_hello.py --file script_hello.py --account-key $STORAGE_KEY
# # ensuite checker la présence le fichier depuis le blob
# # echo "___UPLOAD_IN_BLOB___ finish"


# créer un serveur flexible azure postgresql s'il n'existe pas déjà
if ! az postgres flexible-server db show --resource-group $RESOURCE_GROUP --server-name $SERVER_NAME &>/dev/null; then
  az postgres flexible-server create --name $SERVER_NAME --resource-group $RESOURCE_GROUP --admin-user $ADMIN_USER --admin-password $ADMIN_PASSWORD --sku-name $SKU_SERVER --tier Burstable --version 12 --database-name $DB_NAME
fi
echo "__POSTGRESQL server__ is ready with NAME: $SERVER_NAME"

# configurer les paramètres du firewall
if ! az postgres flexible-server firewall-rule show --resource-group $RESOURCE_GROUP --name $SERVER_NAME --rule-name AllowAll &>/dev/null; then
  az postgres flexible-server firewall-rule create --resource-group $RESOURCE_GROUP --name $SERVER_NAME --rule-name AllowAll --start-ip-address 0.0.0.0 --end-ip-address 255.255.255.255
fi

SERVER_URL=$(az postgres flexible-server show --name $SERVER_NAME --resource-group $RESOURCE_GROUP --query 'fullyQualifiedDomainName' --output tsv)

# créer une db postgreSQL sur Azure si elle n'existe pas déjà
if ! az postgres flexible-server db create --server-name $SERVER_NAME --resource-group $RESOURCE_GROUP --database-name $DB_NAME &>/dev/null; then
az postgres flexible-server db create --server-name $SERVER_NAME --resource-group $RESOURCE_GROUP --database-name $DB_NAME --charset utf8 --collation fr_FR.utf8
fi
echo "__DATABASE__ created with NAME: $DB_NAME"




# recréer un fichier .env avec les variables nécessaires à l'exécution de scrapy (DBNAME par exemple)
cat <<EOT > .env
# ___RESSOURCE_GROUP___
RESOURCE_GROUP="$RESOURCE_GROUP"
LOCATION="$LOCATION"
# ___DATABASE___
PGHOST="$SERVER_URL"
PGUSER="$ADMIN_USER"
PGPORT="5432"
PGDATABASE="$DB_AZ_NAME"
PGPASSWORD="$ADMIN_PASSWORD"
DB_NAME="$DB_NAME"
DATABASE_URL="postgresql+psycopg2://$ADMIN_USER:$ADMIN_PASSWORD@$SERVER_URL:5432/$DB_NAME"
SKU_SERVER="$SKU_SERVER"
SERVER_NAME="$SERVER_NAME"
# ___FUNCTION___
UNIV_STORAGE_NAME="$UNIV_STORAGE_NAME"
IMG_NAME="$IMG_NAME"
ENV_NAME="$ENV_NAME"
APP_FUNC_NAME="$APP_FUNC_NAME"
FUNC_NAME="$FUNC_NAME"
SKU_AZURE="$SKU_AZURE"
EOT

echo ".env file created successfully with the following content:"
cat .env
