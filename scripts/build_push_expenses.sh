# Create the variables
export CONTAINER_REGISTRY=assistantbotcontainer
export IMAGE_NAME=expenses-api

docker build -t $IMAGE_NAME --platform linux/amd64 -f expenses/Dockerfile . 
az login 
az acr login --name $CONTAINER_REGISTRY
docker tag $IMAGE_NAME $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest
docker push $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest