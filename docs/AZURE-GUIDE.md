# Azure Guide

## Resource Naming Convention

```
{app}-{env}-{resource}

Examples:
- secureshop-production-rg        (Resource Group)
- secureshop-production-app       (App Service)
- secureshop-production-kv        (Key Vault)
- secureshop-production-plan      (App Service Plan)
- secureshop-production-logs      (Log Analytics)
- secureshop-production-insights  (Application Insights)
```

## Cost Optimization

| Resource | Tier | Monthly Cost (approx) |
|----------|------|----------------------|
| App Service | B1 (Basic) | ~$13 |
| Key Vault | Standard | ~$0.03/10k operations |
| Log Analytics | Per GB | ~$2.30/GB ingested |
| Application Insights | Basic | Free tier available |

**Total: ~$15-30/month for small applications**

## Scaling

### Vertical Scaling (Scale Up)
```bash
az appservice plan update --name your-plan --resource-group your-rg --sku S1
```

### Horizontal Scaling (Scale Out)
```bash
az appservice plan update --name your-plan --resource-group your-rg --number-of-workers 3
```

### Auto-scale
```bash
az monitor autoscale create \
    --resource $(az appservice plan show --name your-plan --query id -o tsv) \
    --name auto-scale \
    --min-count 1 --max-count 5 --count 2
```

## Backup and Disaster Recovery

### App Service Backup
```bash
az webapp config backup create \
    --resource-group your-rg \
    --webapp-name your-app \
    --backup-name weekly-backup \
    --container-url "https://yourstorage.blob.core.windows.net/backups?..."
```

### Key Vault Backup
```bash
# Backup certificate
az keyvault certificate download \
    --vault-name your-kv \
    --name ssl-cert \
    --file cert-backup.pfx

# Backup secrets (manual process - use Azure Backup service for automation)
```
