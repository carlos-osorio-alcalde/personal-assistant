# Create the variables
export CONTAINER_REGISTRY=assistantbotcontainer
export IMAGE_NAME=assitantbot

docker build --platform linux/amd64 -t $IMAGE_NAME .
az login 
az acr login --name $CONTAINER_REGISTRY
docker tag $IMAGE_NAME $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest
docker push $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest