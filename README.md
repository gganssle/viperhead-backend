# Viperhead Backend

A FastAPI service that generates images of snake-headed black labs using DALL-E 3.

## Live Service

The service is deployed on Google Cloud Run and is available at:
https://viperhead-server-862228002068.us-central1.run.app

### API Endpoints

1. **Root Endpoint** - Check if the service is running
```bash
curl -X GET https://viperhead-server-862228002068.us-central1.run.app/
```

2. **Generate Image** - Create a new snake-headed lab image (requires Google OAuth token)
```bash
curl -X POST https://viperhead-server-862228002068.us-central1.run.app/generate-image \
  -H "Authorization: Bearer YOUR_GOOGLE_OAUTH_TOKEN"
```

3. **API Documentation** - Interactive Swagger UI
https://viperhead-server-862228002068.us-central1.run.app/docs

### Authentication

The service uses Google OAuth 2.0 for authentication. To use the API:

1. Get a Google OAuth token from your client application (web, mobile, etc.)
2. Include the token in the Authorization header as a Bearer token
3. The service will verify the token with Google and extract the user's email

Example using JavaScript:
```javascript
// Using Google Identity Services
const client = google.accounts.oauth2.initTokenClient({
  client_id: 'YOUR_GOOGLE_CLIENT_ID',
  scope: 'email profile',
  callback: async (response) => {
    const token = response.access_token;
    
    // Call the API with the token
    const result = await fetch('https://viperhead-server-862228002068.us-central1.run.app/generate-image', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    const data = await result.json();
    console.log(data.image_url);
  },
});

// Start the OAuth flow
client.requestAccessToken();
```

### Features
- Dynamic prompt generation using configurable activities
- Google OAuth authentication for API access
- Automatic scaling based on traffic
- Global CDN for fast access
- HTTPS endpoint with automatic SSL

## Local Development

### Local Setup

1. Create a Python virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with required credentials:
```bash
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_CLIENT_ID=your_google_client_id_here
```

### Running the Server Locally

Start the FastAPI server with:
```bash
uvicorn main:app --reload
```

The server will run at http://localhost:8000

## Docker Support

### Docker Build and Run

1. Build the Docker image:
```bash
docker build -t viperhead-server .
```

2. Run the container locally:
```bash
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your_openai_api_key_here \
  -e GOOGLE_CLIENT_ID=your_google_client_id_here \
  viperhead-server
```

The server will run at http://localhost:8080

## Cloud Run Deployment

### Prerequisites
1. Install and initialize the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
2. Enable required Google Cloud APIs:
   - Cloud Run API
   - Container Registry API
   - Cloud Build API

### Deployment Steps

1. Set your project ID:
```bash
export PROJECT_ID=viperhead
gcloud config set project $PROJECT_ID
```

2. Enable required APIs:
```bash
gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com
```

3. Build and push the container:
```bash
gcloud builds submit --tag gcr.io/$PROJECT_ID/viperhead-server
```

4. Deploy to Cloud Run:
```bash
gcloud run deploy viperhead-server \
  --image gcr.io/$PROJECT_ID/viperhead-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_openai_api_key_here,GOOGLE_CLIENT_ID=your_google_client_id_here
```

### Monitoring and Management

1. View service details:
```bash
gcloud run services describe viperhead-server
```

2. View logs:
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=viperhead-server"
```

3. Update environment variables:
```bash
gcloud run services update viperhead-server \
  --update-env-vars OPENAI_API_KEY=new_key_here,GOOGLE_CLIENT_ID=new_client_id_here
```

### Cost Management
- The service automatically scales to zero when not in use
- You only pay for actual usage
- Monitor costs in the [Google Cloud Console](https://console.cloud.google.com/billing)

## Configuration

### Prompt Configuration
The service uses a YAML configuration file (`config/prompts.yaml`) to manage:
- Base prompt components
- List of possible dog activities

To modify the image generation behavior, edit this file and redeploy the service.
