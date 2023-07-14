# Kill all the running containers
docker kill $(docker ps -q)

# Login to the Azure Container Registry
az acr login --name assistantbotcontainer

# Pull the latest image
docker pull assistantbotcontainer.azurecr.io/assitantbot:latest

# Run the image
docker run -d --restart unless-stopped assistantbotcontainer.azurecr.io/assitantbot:latest
