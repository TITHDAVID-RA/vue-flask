# Security Documentation

## Security Architecture

### Threat Model

| Threat | Mitigation |
|--------|-----------|
| Secrets in source code | Azure Key Vault + Managed Identity |
| Secrets in environment variables | Key Vault runtime retrieval |
| Man-in-the-middle attacks | TLS 1.2+, HTTPS-only |
| Unauthorized secret access | RBAC with least privilege |
| Secret leakage in logs | Masked logging, audit trails |
| Database credential theft | Key Vault-backed connection strings |
| Payment data exposure | Stripe Elements (PCI-compliant) |

### Compliance

- **PCI-DSS**: Payment processing via Stripe (PCI Level 1)
- **SOC 2**: Azure Key Vault compliance
- **GDPR**: Data encryption at rest and in transit
- **ISO 27001**: Azure infrastructure compliance

### Secret Rotation

```bash
# Rotate Stripe keys
NEW_STRIPE_KEY="sk_test_new..."

# Update in Key Vault (creates new version)
az keyvault secret set \
    --vault-name your-kv \
    --name "stripe-secret-key" \
    --value "$NEW_STRIPE_KEY"

# Restart app to pick up new version
az webapp restart --name your-app --resource-group your-rg
```

### Audit Logging

Enable diagnostic settings:
```bash
az monitor diagnostic-settings create \
    --name keyvault-audit \
    --resource $(az keyvault show --name your-kv --query id -o tsv) \
    --logs '[{"category":"AuditEvent","enabled":true}]' \
    --workspace $(az monitor log-analytics workspace show --name your-workspace --query id -o tsv)
```

### Network Security

```bash
# Restrict Key Vault to App Service subnet
az keyvault update \
    --name your-kv \
    --resource-group your-rg \
    --default-action Deny \
    --bypass AzureServices
```
