# Setup Guide

## Overview

This guide covers how to deploy the AKS SRE Platform from scratch, including Azure infrastructure, application deployment, and monitoring stack setup.

## Prerequisites

- Azure subscription with Contributor access
- Azure CLI installed and logged in
- Docker installed
- Helm 3 installed
- kubectl installed
- Python 3.11+ (for local development)
- GitHub repository with OIDC configured

## Step 1: Configure Azure OIDC

1. Create an App Registration in Microsoft Entra ID
2. Add a federated credential:
   - **Issuer:** `https://token.actions.githubusercontent.com`
   - **Subject:** `repo:<owner>/aks-sre-platform-lab:ref:refs/heads/main`
   - **Audience:** `api://AzureADTokenExchange`
3. Grant the App Registration **Contributor** and **User Access Administrator** roles
4. Add GitHub repository secrets:
   - `AZURE_CLIENT_ID`
   - `AZURE_TENANT_ID`
   - `AZURE_SUBSCRIPTION_ID`

## Step 2: Deploy Azure Infrastructure

### Option A: GitHub Actions (Recommended)

1. Go to **Actions** > **Deploy Infrastructure**
2. Select environment (`dev` or `prod`)
3. Click **Run workflow**
4. Monitor the validation, what-if, and deploy steps

### Option B: Azure CLI

```bash
# Login
az login
az account set --subscription <subscription-id>

# Create resource group
az group create --name rg-aks-sre-platform-dev --location eastus

# Deploy
az deployment group create \
  --resource-group rg-aks-sre-platform-dev \
  --template-file infra/main.bicep \
  --parameters infra/parameters/dev.bicepparam
```

## Step 3: Build and Push Container Image

### Option A: GitHub Actions

1. Go to **Actions** > **Build and Push Container Image**
2. Select environment and optionally set an image tag
3. Click **Run workflow**

### Option B: Local Build

```bash
# Login to ACR
az acr login --name acrsreplatformdev

# Build and push
docker build -t acrsreplatformdev.azurecr.io/demo-api:v1 app/
docker push acrsreplatformdev.azurecr.io/demo-api:v1
```

## Step 4: Deploy Application to AKS

### Option A: GitHub Actions

1. Go to **Actions** > **Deploy to AKS**
2. Select environment and enter the image tag
3. Click **Run workflow**

### Option B: Helm CLI

```bash
# Get AKS credentials
az aks get-credentials --resource-group rg-aks-sre-platform-dev --name aks-sre-platform-dev

# Deploy with Helm
helm upgrade --install demo-api helm/demo-api/ \
  --namespace demo-api \
  --create-namespace \
  --set image.repository=acrsreplatformdev.azurecr.io/demo-api \
  --set image.tag=v1 \
  --values helm/demo-api/values-dev.yaml \
  --wait
```

## Step 5: Verify Deployment

```bash
# Check pods
kubectl get pods -n demo-api

# Check service
kubectl get svc -n demo-api

# Check HPA
kubectl get hpa -n demo-api

# Test health endpoint
kubectl port-forward svc/demo-api 8000:80 -n demo-api
curl http://localhost:8000/health
```

## Step 6: Install Monitoring Stack

```bash
# Add Helm repos
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

# Install Prometheus + Alertmanager
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set alertmanager.enabled=true

# Apply custom alert rules
kubectl apply -f monitoring/prometheus-rules/slo-alerts.yaml
kubectl apply -f monitoring/prometheus-rules/app-alerts.yaml

# Apply OTel collector config
kubectl apply -f monitoring/opentelemetry/collector-config.yaml
```

## Step 7: Import Grafana Dashboards

1. Port-forward Grafana: `kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring`
2. Login (default: admin/prom-operator)
3. Go to **Dashboards** > **Import**
4. Import `monitoring/grafana-dashboards/app-dashboard.json`
5. Import `monitoring/grafana-dashboards/cluster-dashboard.json`

## Troubleshooting

| Issue | Resolution |
|---|---|
| OIDC auth fails | Verify federated credential subject matches branch |
| ACR name conflict | ACR names must be globally unique |
| Pods in Pending state | Check node resources with `kubectl describe node` |
| Image pull errors | Verify AcrPull role assignment exists |
| Helm deploy fails | Check `kubectl get events -n demo-api` |
| Prometheus not scraping | Verify pod annotations for prometheus scraping |
