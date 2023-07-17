# Create the variables
export CONTAINER_REGISTRY=assistantbotcontainer
export IMAGE_NAME=assitantbot

# Kill all the running containers
docker kill $(docker ps -q)

# Login to the Azure Container Registry
az acr login --name $CONTAINER_REGISTRY

# Pull the latest image
docker pull $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest

# Run the image
docker run -d --restart unless-stopped $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest
