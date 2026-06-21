# 🔒 SecureShop - Secure E-Commerce with Azure Key Vault

A production-ready e-commerce application demonstrating enterprise-grade security architecture using **Azure Key Vault**, **Managed Identity**, and **passwordless authentication**.

![Security Architecture](docs/architecture-diagram.png)

## 🏗️ Architecture Overview

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User      │────▶│  Azure App       │────▶│  Azure Key      │
│  Browser    │     │  Service (Flask) │     │  Vault          │
└─────────────┘     └──────────────────┘     └─────────────────┘
                           │                           │
                           │  Managed Identity         │
                           │  (Passwordless)           │
                           ▼                           ▼
                    ┌──────────────────┐     ┌─────────────────┐
                    │  Vue.js Frontend │     │  Secrets/Keys/  │
                    │  (Static Web)    │     │  Certificates   │
                    └──────────────────┘     └─────────────────┘
```

### Security Flow (as shown in the UI)

1. **User accesses the SaaS application** - Browser connects to Azure App Service
2. **The application is hosted on Azure App Service** - Python Flask backend with Vue.js frontend
3. **App Service uses Managed Identity** to authenticate to Azure Key Vault - No passwords or connection strings needed
4. **Key Vault returns the payment API secret securely** - Stripe keys, JWT secrets, DB credentials
5. **The secret is used by the application at runtime** - It is **never stored in code or configuration**

## 📁 Project Structure

```
ecommerce-azure-keyvault/
├── frontend/                    # Vue.js 3 Frontend
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   │   ├── SecurityBanner.vue    # Matches your screenshot!
│   │   │   ├── ProductCard.vue
│   │   │   ├── Navbar.vue
│   │   │   └── Footer.vue
│   │   ├── views/               # Page components
│   │   │   ├── HomeView.vue
│   │   │   ├── ProductsView.vue
│   │   │   ├── CartView.vue
│   │   │   ├── CheckoutView.vue
│   │   │   ├── OrderSuccessView.vue
│   │   │   └── LoginView.vue
│   │   ├── router/              # Vue Router
│   │   ├── store/               # Pinia state management
│   │   ├── services/            # API service layer
│   │   └── App.vue
│   ├── public/
│   └── package.json
│
├── backend/                     # Flask Python Backend
│   ├── app/
│   │   ├── __init__.py          # App factory
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   └── order.py
│   │   ├── routes/              # API endpoints
│   │   │   ├── products.py
│   │   │   ├── auth.py
│   │   │   ├── orders.py
│   │   │   ├── config.py
│   │   │   └── health.py
│   │   └── services/            # Business logic
│   ├── config.py                # Key Vault integration
│   ├── run.py                   # Entry point
│   ├── requirements.txt
│   └── Dockerfile
│
├── infrastructure/              # Infrastructure as Code
│   ├── terraform/
│   │   ├── main.tf              # Main Terraform configuration
│   │   ├── variables.tf
│   │   └── terraform.tfvars.example
│   └── scripts/
│       └── deploy-azure.sh      # Azure CLI deployment script
│
├── .github/
│   └── workflows/
│       └── deploy.yml           # CI/CD pipeline
│
└── docs/                        # Documentation
    ├── SETUP.md
    ├── AZURE-GUIDE.md
    └── SECURITY.md
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Azure CLI** installed and logged in (`az login`)
- **Stripe** account (test keys for development)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ecommerce-azure-keyvault
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables (for local development)
cp .env.example .env
# Edit .env with your Stripe test keys and local settings

# Run the application
python run.py
```

The backend will be available at `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run serve
```

The frontend will be available at `http://localhost:8080`

### 4. Seed Demo Data

```bash
cd backend
python run.py seed
```

## 🔐 Azure Key Vault Setup

### Method 1: Using Azure CLI Script (Recommended)

```bash
cd infrastructure/scripts
chmod +x deploy-azure.sh
./deploy-azure.sh
```

This interactive script will:
1. Create Resource Group
2. Create App Service with Managed Identity
3. Create Key Vault with RBAC
4. Grant least-privilege access
5. Store all secrets securely

### Method 2: Using Terraform

```bash
cd infrastructure/terraform

# Copy example variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your Stripe keys

# Initialize and apply
terraform init
terraform plan
terraform apply
```

### Method 3: Manual Azure Portal Steps

#### Step 1: Create App Service with Managed Identity

1. Go to **Azure Portal** → **App Services** → **Create**
2. Select **Linux** and **Python 3.11**
3. In the **Identity** tab, enable **System-assigned Managed Identity**
4. Create the resource

#### Step 2: Create Azure Key Vault

1. Go to **Key Vaults** → **Create**
2. Enable **Azure role-based access control**
3. Enable **Purge protection** for production
4. Create the vault

#### Step 3: Grant Access (RBAC)

1. Go to your **Key Vault** → **Access control (IAM)**
2. Click **Add role assignment**
3. Select **Key Vault Secrets User** role
4. Assign to your **App Service's Managed Identity**
5. Repeat for **Key Vault Certificates User** and **Key Vault Crypto User**

#### Step 4: Store Secrets

```bash
# Set your Key Vault name
KEY_VAULT_NAME="your-keyvault-name"

# Store secrets
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "stripe-secret-key" --value "sk_test_..."
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "stripe-publishable-key" --value "pk_test_..."
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "jwt-secret-key" --value "$(openssl rand -base64 32)"
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "flask-secret-key" --value "$(openssl rand -base64 32)"
az keyvault secret set --vault-name $KEY_VAULT_NAME --name "database-url" --value "your-db-connection-string"
```

#### Step 5: Configure App Service

```bash
APP_NAME="your-app-name"
KEY_VAULT_NAME="your-keyvault-name"

az webapp config appsettings set     --name $APP_NAME     --resource-group your-resource-group     --settings         FLASK_ENV=production         AZURE_KEY_VAULT_NAME=$KEY_VAULT_NAME         AZURE_KEY_VAULT_URL="https://$KEY_VAULT_NAME.vault.azure.net"
```

## 🔑 Key Vault Objects

### Secrets
| Secret Name | Purpose | Used By |
|------------|---------|---------|
| `stripe-secret-key` | Stripe payment processing | Backend (server-side only) |
| `stripe-publishable-key` | Stripe frontend integration | Backend → Frontend |
| `stripe-webhook-secret` | Stripe webhook validation | Backend |
| `jwt-secret-key` | JWT token signing | Backend authentication |
| `flask-secret-key` | Flask session security | Backend |
| `database-url` | Database connection string | Backend |

### Certificates
| Certificate Name | Purpose | Used By |
|-----------------|---------|---------|
| `app-ssl-certificate` | TLS/SSL for custom domain | App Service |

### Keys
| Key Name | Purpose | Used By |
|---------|---------|---------|
| `app-encryption-key` | Data encryption at rest | Application |

## 🛡️ Security Features

### 1. Managed Identity (Passwordless)
- **No connection strings** or credentials in code
- App Service authenticates to Key Vault using its Azure AD identity
- Automatic token rotation handled by Azure

### 2. Role-Based Access Control (RBAC)
- **Key Vault Secrets User** - Read-only access to secrets
- **Key Vault Certificates User** - Read-only access to certificates
- **Key Vault Crypto User** - Encryption/decryption operations
- **Principle of Least Privilege** - App can only read, not modify

### 3. Secret Lifecycle
- **Soft delete** enabled (7-day retention)
- **Purge protection** prevents permanent deletion
- **Audit logging** tracks all secret access
- **Versioning** maintains secret history

### 4. Runtime Security
```python
# Secrets are retrieved at runtime - never in code
stripe_secret = kv_config.get_secret('stripe-secret-key')
stripe.api_key = stripe_secret  # Used immediately, never stored
```

### 5. HTTPS & TLS
- **TLS 1.2 minimum** enforced
- **HTTPS-only** traffic
- FTPS **disabled** for security

## 📊 Monitoring & Diagnostics

### Key Vault Audit Logs
```bash
# View audit logs
az monitor activity-log list     --resource-group your-resource-group     --query "[?resourceProviderValue=='MICROSOFT.KEYVAULT']"
```

### Application Insights
The Terraform deployment includes Application Insights for:
- Request tracking
- Exception monitoring
- Performance metrics
- Secret access patterns

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Integration Tests
```bash
# Test Key Vault connectivity
curl https://your-app.azurewebsites.net/api/health/keyvault-status
```

## 🚀 Deployment

### Using GitHub Actions (CI/CD)
1. Fork this repository
2. Add these secrets to GitHub:
   - `AZURE_WEBAPP_PUBLISH_PROFILE`
   - `AZURE_STATIC_WEB_APPS_API_TOKEN`
3. Push to `main` branch - automatic deployment!

### Manual Deployment
```bash
# Backend
cd backend
zip -r ../backend.zip .
az webapp deploy --resource-group your-rg --name your-app --src-path ../backend.zip

# Frontend
cd frontend
npm run build
# Deploy dist/ folder to Azure Static Web Apps or Storage
```

## 📚 Documentation

- **[SETUP.md](docs/SETUP.md)** - Detailed setup instructions
- **[AZURE-GUIDE.md](docs/AZURE-GUIDE.md)** - Azure-specific configuration
- **[SECURITY.md](docs/SECURITY.md)** - Security best practices and compliance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Azure Key Vault team for the excellent secret management platform
- Stripe for secure payment processing APIs
- Vue.js and Flask communities for the amazing frameworks

---

**Built with ❤️ and 🔒 Azure Key Vault Security**
