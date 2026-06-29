# Cost Control Guide

## Overview

This project is designed to minimize Azure costs while demonstrating a full SRE platform. Use the strategies below to keep costs manageable.

## Two Operating Modes

### Mode 1: Local Demo (No Azure Cost)

Run everything locally using kind or minikube:

```bash
# Create local cluster
kind create cluster --name sre-platform

# Build image locally
docker build -t demo-api:local app/

# Load image into kind
kind load docker-image demo-api:local --name sre-platform

# Deploy with Helm
helm upgrade --install demo-api helm/demo-api/ \
  --namespace demo-api \
  --create-namespace \
  --set image.repository=demo-api \
  --set image.tag=local \
  --set image.pullPolicy=Never \
  --values helm/demo-api/values-dev.yaml

# Install local Prometheus/Grafana
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### Mode 2: Azure Demo

Deploy to Azure for full cloud-native demonstration. Use the cost controls below.

## Cost Optimization Strategies

### Use Small VM Sizes

The dev environment uses `Standard_B2s` (2 vCPU, 4 GB, ~$30/month). This is sufficient for demonstration purposes.

### Destroy Resources After Demo

```bash
# Delete the entire resource group (all resources)
az group delete --name rg-aks-sre-platform-dev --yes --no-wait

# Verify deletion
az group show --name rg-aks-sre-platform-dev 2>/dev/null || echo "Deleted"
```

### Use Autoscaler with Low Minimums

The dev environment uses:
- Cluster autoscaler: min 1, max 5 nodes
- HPA: min 1, max 3 replicas

This keeps baseline costs low while allowing scale-up when needed.

### Use Basic SKU for ACR

Basic ACR (~$5/month) is sufficient for development. Upgrade to Standard only for production.

### Minimize Log Retention

Log Analytics is set to 30-day retention. Reduce to 7 days for dev if needed.

## Estimated Monthly Costs (Dev Environment)

| Resource | Estimated Cost |
|---|---|
| AKS (1x Standard_B2s) | ~$30 |
| ACR (Basic) | ~$5 |
| Key Vault (Standard) | ~$0.03/operation |
| Log Analytics (PerGB) | ~$2-5 |
| **Total (idle)** | **~$37-40/month** |

## Quick Cleanup Commands

```bash
# Delete dev environment
az group delete --name rg-aks-sre-platform-dev --yes --no-wait

# Delete prod environment
az group delete --name rg-aks-sre-platform-prod --yes --no-wait

# Delete local kind cluster
kind delete cluster --name sre-platform
```

## Best Practices

- Deploy Azure resources only when actively demonstrating or developing
- Use `--no-wait` flag for deletions to avoid blocking
- Keep infrastructure modular so individual resources can be torn down
- Set Azure budget alerts to catch unexpected charges
- Review Azure Cost Management weekly during active development
