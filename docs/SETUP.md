# Detailed Setup Guide

## Table of Contents
1. [Local Development](#local-development)
2. [Azure Deployment](#azure-deployment)
3. [Key Vault Configuration](#key-vault-configuration)
4. [Stripe Integration](#stripe-integration)
5. [Troubleshooting](#troubleshooting)

## Local Development

### Backend Setup

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
```

Edit `.env`:
```env
# For local development, you can use environment variables
# In production, these come from Azure Key Vault

FLASK_ENV=development
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
JWT_SECRET_KEY=your-jwt-secret
FLASK_SECRET_KEY=your-flask-secret
DATABASE_URL=sqlite:///ecommerce.db
```

4. **Run the server:**
```bash
python run.py
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Configure API URL:**
Create `.env.local`:
```env
VUE_APP_API_URL=http://localhost:5000/api
```

3. **Run development server:**
```bash
npm run serve
```

## Azure Deployment

### Prerequisites
- Azure subscription
- Azure CLI installed
- Owner or Contributor role on subscription

### Step-by-Step Deployment

#### 1. Login to Azure
```bash
az login
az account set --subscription "Your Subscription Name"
```

#### 2. Run Deployment Script
```bash
cd infrastructure/scripts
chmod +x deploy-azure.sh
./deploy-azure.sh
```

Follow the prompts to enter your Stripe keys and database connection string.

#### 3. Deploy Application Code
```bash
# Zip backend code
cd backend
zip -r ../backend.zip .

# Deploy to Azure
az webapp deploy \
    --resource-group secureshop-production-rg \
    --name secureshop-production-app \
    --src-path ../backend.zip

# Configure startup command (if needed)
az webapp config set \
    --resource-group secureshop-production-rg \
    --name secureshop-production-app \
    --startup-file "gunicorn --bind 0.0.0.0:5000 --workers 4 run:app"
```

#### 4. Build and Deploy Frontend
```bash
cd frontend
npm run build

# Deploy to Azure Static Web Apps
# Or copy dist/ to App Service's wwwroot
```

## Key Vault Configuration

### Creating Secrets

```bash
KEY_VAULT_NAME="your-keyvault-name"

# Stripe keys
az keyvault secret set \
    --vault-name $KEY_VAULT_NAME \
    --name "stripe-secret-key" \
    --value "sk_test_..."

az keyvault secret set \
    --vault-name $KEY_VAULT_NAME \
    --name "stripe-publishable-key" \
    --value "pk_test_..."

# Application secrets
az keyvault secret set \
    --vault-name $KEY_VAULT_NAME \
    --name "jwt-secret-key" \
    --value "$(openssl rand -base64 32)"

az keyvault secret set \
    --vault-name $KEY_VAULT_NAME \
    --name "flask-secret-key" \
    --value "$(openssl rand -base64 32)"

# Database
az keyvault secret set \
    --vault-name $KEY_VAULT_NAME \
    --name "database-url" \
    --value "postgresql://user:pass@host:5432/db"
```

### Managing Certificates

```bash
# Import existing certificate
az keyvault certificate import \
    --vault-name $KEY_VAULT_NAME \
    --name "ssl-cert" \
    --file certificate.pfx

# Create self-signed certificate (for testing)
az keyvault certificate create \
    --vault-name $KEY_VAULT_NAME \
    --name "test-cert" \
    --policy '{"issuerParameters":{"name":"Self"},"x509CertificateProperties":{"subject":"CN=test.com"}}'
```

### Managing Keys

```bash
# Create RSA key
az keyvault key create \
    --vault-name $KEY_VAULT_NAME \
    --name "app-encryption" \
    --kty RSA \
    --size 2048

# List keys
az keyvault key list --vault-name $KEY_VAULT_NAME
```

## Stripe Integration

### Test Mode Setup
1. Create a [Stripe account](https://stripe.com)
2. Go to Developers → API Keys
3. Copy **Publishable key** and **Secret key**
4. Store them in Azure Key Vault

### Webhook Setup
1. In Stripe Dashboard, go to Webhooks
2. Add endpoint: `https://your-app.azurewebsites.net/api/webhooks/stripe`
3. Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`
4. Copy the **Signing secret** to Key Vault as `stripe-webhook-secret`

### Testing Payments
Use Stripe test card numbers:
- `4242 4242 4242 4242` - Successful payment
- `4000 0000 0000 0002` - Declined payment
- Any future expiry date, any 3-digit CVC, any ZIP

## Troubleshooting

### Key Vault Access Denied
```bash
# Check role assignments
az role assignment list \
    --assignee $(az webapp identity show --name your-app --query principalId -o tsv) \
    --scope $(az keyvault show --name your-kv --query id -o tsv)

# Verify Managed Identity is enabled
az webapp identity show --name your-app --resource-group your-rg
```

### Secret Not Found
```bash
# List all secrets
az keyvault secret list --vault-name your-kv

# Show specific secret (value hidden)
az keyvault secret show --vault-name your-kv --name stripe-secret-key
```

### Application Logs
```bash
# Stream logs
az webapp log tail --name your-app --resource-group your-rg

# View recent logs
az webapp log download --name your-app --resource-group your-rg
```

### Health Check
```bash
# Test API health
curl https://your-app.azurewebsites.net/api/health/

# Test Key Vault connectivity
curl https://your-app.azurewebsites.net/api/health/keyvault-status
```
