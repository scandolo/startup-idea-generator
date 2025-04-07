#!/bin/bash

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI not found. Please install Google Cloud SDK."
    exit 1
fi

# Set variables
PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="pitchslap-api"
REGION="us-central1"  # Change this to your preferred region

# Build and push Docker image to Google Container Registry
echo "Building and pushing Docker image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars="OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d= -f2)"

# Get the deployed service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo "Deployment complete!"
echo "Service URL: $SERVICE_URL"
echo ""
echo "Note: To connect your Streamlit app to this API, update the API_URL in your .env file to:"
echo "API_URL=$SERVICE_URL" 