# avoir installé Azure Cli
# se logger avec azure cli dans cet environnement
# ACTIVER LE SCRIPT "chmod +x script.sh" pour rendre le script exécutable
# EXECUTER LE SCRIPT avec /scripts_azure 
# puis . script.sh

# charger les variables d'environnement
 set -o allexport #suprime toutes les variables importées avant celle la
 source .env #crée des variables d'environnement à partir du .env 
 set +o allexport

# créer un groupe de resources (renseigné dans le .env)
 az group create --name $RESOURCE_GROUP --location $LOCATION 

 
 # créer un blob
#  az storage account create --resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT --location $LOCATION

# créer un conteneur pour le blob : 
# az ad signed-in-user show --query id -o tsv | az role assignment create --role "Storage Blob Data Contributor" --assignee @- --scope "/subscriptions/$SUBSCRIPTION/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Storage/storageAccounts/$STORAGE_GROUP" 
# az storage container create --account-name $STORAGE_ACCOUNT --name $STORAGE_CONTAINER --auth-mode login

# commande pour uploader le fichier :
# az storage blob upload --account-name $STORAGE_ACCOUNT --container-name $STORAGE_CONTAINER --name script_hello.py --file script_hello.py --account-key $STORAGE_KEY
# ensuite checker la présence le fichier depuis le blob


###### AVEC POSTGRE FLEXIBLE SERVER
###########################################################################
# créer un serveur flexible azure postgresql
az postgres flexible-server create --name $SERVER_NAME --resource-group $RESOURCE_GROUP

# créer une db postgreSQL
az postgres flexible-server db create --server-name $SERVER_NAME --resource-group $RESOURCE_GROUP --database-name $DB_NAME --charset utf8 --collation fr_FR.utf8


###### AVEC BATCH
################################################################################
# # récupérer la clé batch : 
# BATCH_KEY=$(az batch account keys list --resource-group $BATCH_RG --name $BATCH_ACCOUNT --query 'primary' --output tsv)
# echo "BATCH_KEY='$BATCH_KEY'" >> .env
# echo "BATCH_KEY: $BATCH_KEY"

# # commande manuelle :  
# # az batch account keys list --name $BATCH_ACCOUNT --resource-group $BATCH_RG

# # connexion au compte batch 
#  az batch account login --name $BATCH_ACCOUNT --resource-group $BATCH_RG --shared-key-auth

# # création de pool batch
#  az batch pool create --id $POOL_ID --image canonical:0001-com-ubuntu-server-focal:20_04-lts --node-agent-sku-id "batch.node.ubuntu 20.04" --target-dedicated-nodes 1 --vm-size STANDARD_D2S_V3

# création de datafactory
 az datafactory create --name $FACTORY_NAME --resource-group $RESOURCE_GROUP --location $LOCATION

# création de pipeline 
#  az extension add --name datafactory #installation de l'extension au préalable
#  az pipelines create --organisation simplonformations.onmicrosoft.com --name $PIPELINE_NAME --description 'Monpipeline' --repository SampleRepoName --branch master --repository-type tfsgit

######################################################################################

### débugger az pipelines
## unrecognized arguments: --organisation simplonformations.onmicrosoft.com