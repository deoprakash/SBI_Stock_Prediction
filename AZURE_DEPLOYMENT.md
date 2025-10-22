# Azure Deployment Guide - SBI Stock Price Prediction

This guide covers deploying the Stock Price Prediction application to Azure with:
- **Backend**: Flask API on Azure App Service
- **Frontend**: React app on Azure Static Web Apps

## Prerequisites

- Azure account with active subscription
- Azure CLI installed (`az --version` to verify)
- Git installed
- Node.js and npm installed

## Part 1: Deploy Backend (Flask API)

### Step 1: Prepare Backend Files

The following files have been created for Azure deployment:
- `Backend/requirements.txt` - Updated with gunicorn
- `Backend/startup.py` - Production entry point
- `Backend/Procfile` - Process file for Azure
- `Backend/app.py` - Updated with production CORS settings

### Step 2: Login to Azure

```bash
az login
```

### Step 3: Create Resource Group

```bash
az group create --name sbi-stock-prediction-rg --location eastus
```

### Step 4: Create App Service Plan

```bash
az appservice plan create --name sbi-stock-plan --resource-group sbi-stock-prediction-rg --sku B1 --is-linux
```

### Step 5: Create Web App

```bash
az webapp create --resource-group sbi-stock-prediction-rg --plan sbi-stock-plan --name sbi-stock-backend --runtime "PYTHON:3.11"
```

**Note**: Replace `sbi-stock-backend` with a unique name (Azure subdomain must be globally unique).

### Step 6: Configure App Settings

```bash
# Set environment variables
az webapp config appsettings set --resource-group sbi-stock-prediction-rg --name sbi-stock-backend --settings AZURE_DEPLOYMENT=true

# Set startup command
az webapp config set --resource-group sbi-stock-prediction-rg --name sbi-stock-backend --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 startup:app"
```

### Step 7: Deploy Backend Code

From the project root directory:

```bash
cd Backend
git init
git add .
git commit -m "Initial backend deployment"

# Get deployment credentials
az webapp deployment source config-local-git --name sbi-stock-backend --resource-group sbi-stock-prediction-rg

# Deploy (replace <deployment-url> with the URL from previous command)
git remote add azure <deployment-url>
git push azure main
```

**Alternative: Deploy via ZIP**

```bash
cd Backend
# Create a zip file excluding virtual environment
powershell Compress-Archive -Path app.py,startup.py,requirements.txt,Procfile,model -DestinationPath deploy.zip

az webapp deployment source config-zip --resource-group sbi-stock-prediction-rg --name sbi-stock-backend --src deploy.zip
```

### Step 8: Verify Backend

Visit: `https://sbi-stock-backend.azurewebsites.net/predict`

You should see JSON response with stock predictions.

### Step 9: Configure CORS for Frontend

```bash
az webapp cors add --resource-group sbi-stock-prediction-rg --name sbi-stock-backend --allowed-origins https://your-frontend-url.azurestaticapps.net
```

## Part 2: Deploy Frontend (React App)

### Step 1: Update Environment Variables

Edit `frontend/.env.production`:

```env
VITE_API_URL=https://sbi-stock-backend.azurewebsites.net
```

Replace with your actual backend URL from Part 1, Step 5.

### Step 2: Build Frontend Locally (Optional Test)

```bash
cd frontend
npm install
npm run build
```

### Step 3: Deploy to Azure Static Web Apps

#### Option A: Via Azure Portal (Recommended for first deployment)

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → Search "Static Web App"
3. Fill in:
   - **Subscription**: Your subscription
   - **Resource Group**: `sbi-stock-prediction-rg`
   - **Name**: `sbi-stock-frontend`
   - **Region**: East US 2
   - **Deployment**: GitHub (or Other if not using GitHub)
   - **Build Presets**: React
   - **App location**: `/frontend`
   - **Output location**: `dist`
4. Click "Review + Create" → "Create"

#### Option B: Via Azure CLI

```bash
# Install Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

# From frontend directory
cd frontend

# Build the app
npm run build

# Deploy
az staticwebapp create \
  --name sbi-stock-frontend \
  --resource-group sbi-stock-prediction-rg \
  --source . \
  --location "eastus2" \
  --branch main \
  --app-location "/frontend" \
  --output-location "dist" \
  --login-with-github
```

### Step 4: Configure Environment Variables for Static Web App

1. Go to Azure Portal → Your Static Web App
2. Click "Configuration" in left menu
3. Add application setting:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://sbi-stock-backend.azurewebsites.net`
4. Click "Save"

### Step 5: Verify Frontend

Visit: `https://sbi-stock-frontend.azurestaticapps.net`

Your full application should now be live!

## Part 3: Update Backend CORS with Frontend URL

Now that you have the frontend URL, update the backend CORS:

```bash
az webapp cors add --resource-group sbi-stock-prediction-rg --name sbi-stock-backend --allowed-origins https://sbi-stock-frontend.azurestaticapps.net

# Set environment variable for CORS
az webapp config appsettings set --resource-group sbi-stock-prediction-rg --name sbi-stock-backend --settings FRONTEND_URL=https://sbi-stock-frontend.azurestaticapps.net
```

## Cost Optimization

### Free Tier Options
- **App Service**: B1 Basic tier (~$13/month) - Can use F1 Free tier but limited
- **Static Web Apps**: Free tier available (100 GB bandwidth/month)

### To Use Free Tier for Backend

```bash
az appservice plan create --name sbi-stock-plan-free --resource-group sbi-stock-prediction-rg --sku F1 --is-linux
```

**Note**: Free tier has limitations (60 CPU minutes/day, 1 GB RAM).

## Monitoring & Logs

### View Backend Logs

```bash
az webapp log tail --resource-group sbi-stock-prediction-rg --name sbi-stock-backend
```

### View Application Insights (Optional)

Enable Application Insights for detailed monitoring:

```bash
az monitor app-insights component create --app sbi-insights --location eastus --resource-group sbi-stock-prediction-rg

# Link to web app
az webapp config appsettings set --resource-group sbi-stock-prediction-rg --name sbi-stock-backend --settings APPINSIGHTS_INSTRUMENTATIONKEY=<key>
```

## Continuous Deployment (Optional)

### Setup GitHub Actions for Backend

Create `.github/workflows/backend-deploy.yml`:

```yaml
name: Deploy Backend to Azure

on:
  push:
    branches: [ main ]
    paths:
      - 'Backend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: sbi-stock-backend
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: ./Backend
```

### Get Publish Profile

```bash
az webapp deployment list-publishing-profiles --resource-group sbi-stock-prediction-rg --name sbi-stock-backend --xml
```

Add the output as a GitHub secret named `AZURE_WEBAPP_PUBLISH_PROFILE`.

## Troubleshooting

### Backend Issues

1. **500 Error**: Check logs with `az webapp log tail`
2. **Module not found**: Verify `requirements.txt` includes all dependencies
3. **Model file not found**: Ensure `model/` directory is included in deployment

### Frontend Issues

1. **CORS Error**: Verify backend CORS settings include frontend URL
2. **API not responding**: Check `VITE_API_URL` in production environment
3. **Build fails**: Ensure all dependencies in `package.json`

### Model File Too Large

If `sbi_model.h5` is too large for deployment:

1. Use Azure Blob Storage:
```bash
# Create storage account
az storage account create --name sbistockmodels --resource-group sbi-stock-prediction-rg --location eastus --sku Standard_LRS

# Upload model
az storage blob upload --account-name sbistockmodels --container-name models --name sbi_model.h5 --file Backend/model/sbi_model.h5
```

2. Update `app.py` to download model from blob storage on startup.

## Scaling

### Auto-scaling Backend

```bash
az monitor autoscale create --resource-group sbi-stock-prediction-rg --resource sbi-stock-backend --resource-type Microsoft.Web/serverfarms --name autoscale-plan --min-count 1 --max-count 3 --count 1
```

## Clean Up Resources

To delete all Azure resources:

```bash
az group delete --name sbi-stock-prediction-rg --yes --no-wait
```

## Summary

- **Backend URL**: `https://sbi-stock-backend.azurewebsites.net`
- **Frontend URL**: `https://sbi-stock-frontend.azurestaticapps.net`
- **Resource Group**: `sbi-stock-prediction-rg`

Your application is now deployed and accessible worldwide! 🚀
