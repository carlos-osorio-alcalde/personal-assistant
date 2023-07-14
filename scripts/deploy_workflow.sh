# Create the variables
export CONTAINER_REGISTRY=assistantbotcontainer
export IMAGE_NAME=assistantbot

# Build the docker image
docker build --platform linux/amd64 -t $IMAGE_NAME .

# Login to the Azure Container Registry
az login 
az acr login --name $CONTAINER_REGISTRY

# Push the image to the Azure Container Registry
docker tag $IMAGE_NAME $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest
docker push $CONTAINER_REGISTRY.azurecr.io/$IMAGE_NAME:latest

# Connect to the VM
chmod 400 caaosorioal-assistant_key.pem
ssh -i caaosorioal-assistant_key.pem caaosorioal@20.232.103.192 "\
    export CONTAINER_REGISTRY=assistantbotcontainer; \
    export IMAGE_NAME=assitantbot; \
    docker kill \$(docker ps -q); \
    az acr login --name \$CONTAINER_REGISTRY; \
    docker pull \$CONTAINER_REGISTRY.azurecr.io/\$IMAGE_NAME:latest; \
    docker run -d --restart unless-stopped \$CONTAINER_REGISTRY.azurecr.io/\$IMAGE_NAME:latest"

