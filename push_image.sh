# Create the variable
export CONTAINER_REGISTRY=assistantbotcontainer
export IMAGE_NAME=assistantbot

azr login
az acr login --name $CONTAINER_REGISTRY
docker tag $IMAGE_NAME:latest $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest
docker push $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest