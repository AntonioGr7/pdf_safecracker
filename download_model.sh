#!/bin/bash

# Define variables
REPO_URL="https://huggingface.co/antoniogr7/pdf-safecracker-layout" 
MODEL_NAME="pdf-safecracker-layout" 
DEST_FOLDER="models"                           

# Check if Git LFS is installed
if ! git lfs --version &> /dev/null
then
    echo "Git LFS is not installed. Installing Git LFS..."
    sudo apt-get install git-lfs
    git lfs install
else
    echo "Git LFS is already installed."
fi

# Clone the repository
echo "Cloning the repository from $REPO_URL..."
git clone $REPO_URL

# Navigate into the cloned repository
cd $MODEL_NAME

# Pull LFS files
echo "Pulling LFS files..."
git lfs pull

# Create the destination folder if it doesn't exist
echo "Creating destination folder $DEST_FOLDER..."
mkdir -p ../$DEST_FOLDER

# Move the model to the destination folder
echo "Moving the model to $DEST_FOLDER..."
mv ../$MODEL_NAME ../$DEST_FOLDER

# Provide completion message
echo "Model downloaded and moved to $DEST_FOLDER/$MODEL_NAME."