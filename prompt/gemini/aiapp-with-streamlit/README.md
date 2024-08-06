
# Setup

```sh
python3 -m venv gemini-streamlit
source gemini-streamlit/bin/activate
pip install -r requirements.txt
```

# Run

```sh
streamlit run app.py \
--browser.serverAddress=localhost \
--server.enableCORS=false \
--server.enableXsrfProtection=false \
--server.port 8080
```

# Deploy 

```sh
PROJECT_ID=$(gcloud config get-value project)
REGION=us-east4
SERVICE_NAME='gemini-app-playground' # Name of your Cloud Run service.
AR_REPO='gemini-app-repo'            # Name of your repository in Artifact Registry that stores your application container image.

gcloud auth login

# Create the repository in Artifact Registry
gcloud artifacts repositories create "$AR_REPO" --location="$REGION" --repository-format=Docker

# Set up authentication to the repository
gcloud auth configure-docker "$REGION-docker.pkg.dev"

# Build the container image
gcloud builds submit --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$AR_REPO/$SERVICE_NAME"

# Deploy and test your app on Cloud Run
gcloud run deploy "$SERVICE_NAME" \
  --port=8080 \
  --image="$REGION-docker.pkg.dev/$PROJECT_ID/$AR_REPO/$SERVICE_NAME" \
  --allow-unauthenticated \
  --region=$REGION \
  --platform=managed  \
  --project=$PROJECT_ID \
  --set-env-vars=PROJECT_ID=$PROJECT_ID,REGION=$REGION
```