#!/bin/bash
# ============================================================================
# SecureShop Azure Deployment Script
# ============================================================================
# This script deploys the SecureShop e-commerce application to Azure
# using Azure CLI commands. It sets up:
#   - Azure App Service (Linux)
#   - Azure Key Vault
#   - Managed Identity
#   - Role-based access control (RBAC)
#
# Prerequisites:
#   - Azure CLI installed and logged in (az login)
#   - Stripe account with API keys
#   - Optional: PostgreSQL database
# ============================================================================

set -e  # Exit on error

# Configuration
RESOURCE_GROUP="secureshop-production-rg"
LOCATION="eastus"
APP_NAME="secureshop-production-app"
APP_PLAN="secureshop-production-plan"
KEY_VAULT_NAME="secureshop-production-kv"
SKU="B1"  # Basic tier

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  SecureShop Azure Deployment Script   ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Step 1: Login check
echo -e "${YELLOW}[1/10] Checking Azure login...${NC}"
az account show > /dev/null 2>&1 || { echo -e "${RED}Error: Not logged in. Run 'az login' first.${NC}"; exit 1; }
echo -e "${GREEN}✓ Logged in as: $(az account show --query user.name -o tsv)${NC}"
echo ""

# Step 2: Create Resource Group
echo -e "${YELLOW}[2/10] Creating Resource Group...${NC}"
az group create     --name $RESOURCE_GROUP     --location $LOCATION     --tags Project=SecureShop Environment=Production
echo -e "${GREEN}✓ Resource Group created: $RESOURCE_GROUP${NC}"
echo ""

# Step 3: Create App Service Plan
echo -e "${YELLOW}[3/10] Creating App Service Plan...${NC}"
az appservice plan create     --name $APP_PLAN     --resource-group $RESOURCE_GROUP     --location $LOCATION     --sku $SKU     --is-linux     --tags Project=SecureShop
echo -e "${GREEN}✓ App Service Plan created: $APP_PLAN${NC}"
echo ""

# Step 4: Create Web App with System-Assigned Managed Identity
echo -e "${YELLOW}[4/10] Creating Web App with Managed Identity...${NC}"
az webapp create     --name $APP_NAME     --resource-group $RESOURCE_GROUP     --plan $APP_PLAN     --runtime "PYTHON:3.11"     --assign-identity     --tags Project=SecureShop
echo -e "${GREEN}✓ Web App created: $APP_NAME${NC}"
echo ""

# Get the Managed Identity Principal ID
PRINCIPAL_ID=$(az webapp identity show     --name $APP_NAME     --resource-group $RESOURCE_GROUP     --query principalId -o tsv)
echo -e "${GREEN}✓ Managed Identity Principal ID: $PRINCIPAL_ID${NC}"
echo ""

# Step 5: Configure App Settings (NO secrets - all from Key Vault!)
echo -e "${YELLOW}[5/10] Configuring App Settings...${NC}"
az webapp config appsettings set     --name $APP_NAME     --resource-group $RESOURCE_GROUP     --settings         FLASK_ENV=production         AZURE_KEY_VAULT_NAME=$KEY_VAULT_NAME         AZURE_KEY_VAULT_URL="https://$KEY_VAULT_NAME.vault.azure.net"         SCM_DO_BUILD_DURING_DEPLOYMENT=true         WEBSITE_RUN_FROM_PACKAGE=1
echo -e "${GREEN}✓ App Settings configured${NC}"
echo ""

# Step 6: Create Azure Key Vault
echo -e "${YELLOW}[6/10] Creating Azure Key Vault...${NC}"
az keyvault create     --name $KEY_VAULT_NAME     --resource-group $RESOURCE_GROUP     --location $LOCATION     --enable-rbac-authorization     --sku standard     --soft-delete-retention-days 7     --enable-purge-protection     --tags Project=SecureShop
echo -e "${GREEN}✓ Key Vault created: $KEY_VAULT_NAME${NC}"
echo ""

# Step 7: Grant App Service access to Key Vault
echo -e "${YELLOW}[7/10] Granting Key Vault access to App Service...${NC}"

# Get current user's object ID for admin access
CURRENT_USER_ID=$(az ad signed-in-user show --query id -o tsv)

# Grant current user Key Vault Secrets Officer (to create secrets)
az role assignment create     --role "Key Vault Secrets Officer"     --assignee $CURRENT_USER_ID     --scope $(az keyvault show --name $KEY_VAULT_NAME --query id -o tsv)

# Grant App Service Managed Identity "Key Vault Secrets User" (least privilege)
az role assignment create     --role "Key Vault Secrets User"     --assignee $PRINCIPAL_ID     --scope $(az keyvault show --name $KEY_VAULT_NAME --query id -o tsv)

# Grant App Service access to certificates and keys
az role assignment create     --role "Key Vault Certificates User"     --assignee $PRINCIPAL_ID     --scope $(az keyvault show --name $KEY_VAULT_NAME --query id -o tsv)

az role assignment create     --role "Key Vault Crypto User"     --assignee $PRINCIPAL_ID     --scope $(az keyvault show --name $KEY_VAULT_NAME --query id -o tsv)

echo -e "${GREEN}✓ Role assignments completed${NC}"
echo ""

# Step 8: Store secrets in Key Vault
echo -e "${YELLOW}[8/10] Storing secrets in Key Vault...${NC}"
echo ""
echo -e "${YELLOW}Please enter your secrets:${NC}"

read -sp "Stripe Secret Key (sk_test_...): " STRIPE_SECRET
echo ""
read -sp "Stripe Publishable Key (pk_test_...): " STRIPE_PUBLISHABLE
echo ""
read -sp "Stripe Webhook Secret (whsec_...): " STRIPE_WEBHOOK
echo ""
read -sp "Database URL (or press Enter for SQLite): " DATABASE_URL
echo ""

# Use default SQLite if no database URL provided
if [ -z "$DATABASE_URL" ]; then
    DATABASE_URL="sqlite:///ecommerce.db"
fi

# Generate random secrets
FLASK_SECRET=$(openssl rand -base64 32)
JWT_SECRET=$(openssl rand -base64 32)

# Store secrets in Key Vault
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "flask-secret-key" --value "$FLASK_SECRET"
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "jwt-secret-key" --value "$JWT_SECRET"
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "stripe-secret-key" --value "$STRIPE_SECRET"
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "stripe-publishable-key" --value "$STRIPE_PUBLISHABLE"
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "stripe-webhook-secret" --value "$STRIPE_WEBHOOK"
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "database-url" --value "$DATABASE_URL"

echo -e "${GREEN}✓ All secrets stored securely in Key Vault${NC}"
echo ""

# Step 9: Configure HTTPS and security settings
echo -e "${YELLOW}[9/10] Configuring security settings...${NC}"
az webapp update     --name $APP_NAME     --resource-group $RESOURCE_GROUP     --https-only true

az webapp config set     --name $APP_NAME     --resource-group $RESOURCE_GROUP     --min-tls-version "1.2"     --ftps-state Disabled

echo -e "${GREEN}✓ Security settings configured${NC}"
echo ""

# Step 10: Deploy application
echo -e "${YELLOW}[10/10] Deploying application...${NC}"
echo -e "${YELLOW}Please zip your backend code and run:${NC}"
echo -e "${GREEN}  az webapp deploy --resource-group $RESOURCE_GROUP --name $APP_NAME --src-path ./backend.zip${NC}"
echo ""

# Summary
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deployment Summary                   ${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "App Service URL: ${GREEN}https://$APP_NAME.azurewebsites.net${NC}"
echo -e "Key Vault URL:   ${GREEN}https://$KEY_VAULT_NAME.vault.azure.net${NC}"
echo -e "Managed Identity: ${GREEN}$PRINCIPAL_ID${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Zip your backend code: cd backend && zip -r ../backend.zip ."
echo "2. Deploy: az webapp deploy --resource-group $RESOURCE_GROUP --name $APP_NAME --src-path ./backend.zip"
echo "3. Seed database: az webapp ssh --name $APP_NAME --resource-group $RESOURCE_GROUP"
echo "4. Build and deploy frontend to Static Web Apps or App Service"
echo ""
echo -e "${GREEN}Security Architecture:${NC}"
echo "  ✓ Azure App Service with Managed Identity"
echo "  ✓ Azure Key Vault with RBAC authorization"
echo "  ✓ Secrets never stored in code or config"
echo "  ✓ TLS 1.2 minimum enforced"
echo "  ✓ HTTPS-only traffic"
echo ""
