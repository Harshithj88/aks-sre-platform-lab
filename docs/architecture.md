# Architecture

## Overview

This platform deploys a containerized FastAPI application to Azure Kubernetes Service using a fully automated CI/CD pipeline. Infrastructure is provisioned with Azure Bicep, deployments are managed with Helm, and observability is provided by Prometheus, Grafana, Alertmanager, and OpenTelemetry.

## Architecture Diagram

```mermaid
flowchart TD
    Dev[Developer] --> GitHub[GitHub Repository]

    GitHub --> CI[CI Pipeline]
    GitHub --> InfraWF[Infra Pipeline]
    GitHub --> DeployWF[Deploy Pipeline]

    CI -->|Build & Test| Docker[Docker Image]
    CI -->|Scan| SecScan[Security Scan]
    Docker -->|Push| ACR[Azure Container Registry]

    InfraWF -->|OIDC Auth| Entra[Microsoft Entra ID]
    Entra --> ARM[Azure Resource Manager]
    InfraWF -->|Bicep Deploy| RG[Resource Group]

    subgraph RG[Azure Resource Group]
        LAW[Log Analytics Workspace]
        ACRRG[Container Registry]
        KV[Key Vault]
        MI[Managed Identity]
        AKS[AKS Cluster]
    end

    ACRRG -->|AcrPull| AKS
    MI -->|Workload Identity| AKS
    LAW -->|Container Insights| AKS

    DeployWF -->|Helm Install| AKS

    subgraph AKS[AKS Cluster]
        direction TB
        DemoNS[demo-api namespace]
        MonNS[monitoring namespace]
    end

    DemoNS --> Pods[Demo API Pods]
    MonNS --> Prom[Prometheus]
    MonNS --> Graf[Grafana]
    MonNS --> Alert[Alertmanager]
    MonNS --> OTel[OTel Collector]

    Pods -->|/metrics| Prom
    Prom --> Graf
    Prom --> Alert
    OTel -->|traces| Pods

    User[End User] --> Ingress[Ingress Controller]
    Ingress --> Pods
```

## Components

### Demo API Application

A Python FastAPI service with built-in observability endpoints.

| Endpoint | Purpose |
|---|---|
| `GET /health` | Liveness probe — always returns healthy |
| `GET /ready` | Readiness probe — checks dependencies |
| `GET /metrics` | Prometheus-compatible metrics |
| `GET /simulate-latency` | Injects configurable delay for testing |
| `GET /simulate-error` | Returns 500 for alerting validation |

### Azure Infrastructure

| Resource | Bicep Module | Purpose |
|---|---|---|
| AKS Cluster | `aks.bicep` | Managed Kubernetes with autoscaler, AZs, auto-upgrade |
| Container Registry | `acr.bicep` | Private Docker registry (admin disabled) |
| Key Vault | `keyvault.bicep` | Secret storage with RBAC authorization |
| Managed Identity | `managed-identity.bicep` | Workload identity for AKS pods |
| Log Analytics | `main.bicep` | Container Insights and log aggregation |

### CI/CD Pipelines

| Workflow | Trigger | Purpose |
|---|---|---|
| `ci.yml` | Pull requests | Lint, test, build Docker image, security scan |
| `infra-validate.yml` | PR (infra changes) | Bicep lint and validate |
| `infra-deploy.yml` | Manual dispatch | Deploy Azure infrastructure |
| `image-build.yml` | Manual / push to main | Build and push container image to ACR |
| `deploy-dev.yml` | Manual dispatch | Helm deploy to AKS dev environment |
| `security-scan.yml` | PR / scheduled | Dependency and container vulnerability scanning |

### Observability Stack

```mermaid
flowchart LR
    App[Demo API] -->|/metrics| Prom[Prometheus]
    App -->|traces| OTel[OTel Collector]

    Prom -->|query| Graf[Grafana]
    Prom -->|rules| Alert[Alertmanager]
    OTel -->|export| Prom

    Alert -->|notify| Slack[Slack / Email]

    subgraph Dashboards
        AppDash[App Dashboard]
        ClusterDash[Cluster Dashboard]
    end

    Graf --> AppDash
    Graf --> ClusterDash
```

| Tool | Purpose |
|---|---|
| Prometheus | Scrapes `/metrics`, evaluates alert rules |
| Grafana | Visualizes request rate, latency, error rate, pod resources |
| Alertmanager | Routes alerts based on severity and SLO burn rate |
| OpenTelemetry | Collects distributed traces and forwards metrics |

### Security Design

- **OIDC authentication** — GitHub Actions authenticates to Azure without stored secrets
- **Managed Identity** — AKS workload identity for pod-level Azure access
- **ACR Pull role** — AKS identity granted AcrPull on container registry
- **Key Vault RBAC** — Azure RBAC authorization (no access policies)
- **NetworkPolicy** — Restricts pod-to-pod traffic in the cluster
- **Container scanning** — Trivy scans for image vulnerabilities in CI
- **Dependency scanning** — pip-audit checks Python dependencies for CVEs

## Module Dependencies

```mermaid
flowchart TD
    Main[main.bicep] --> LAW[Log Analytics]
    Main --> ACR[acr.bicep]
    Main --> KV[keyvault.bicep]
    Main --> MI[managed-identity.bicep]
    Main --> AKS[aks.bicep]

    LAW -->|workspaceId| AKS
    ACR -->|acrId| AKS
    MI -->|identityId| AKS
```

## Naming Convention

| Resource | Pattern | Example |
|---|---|---|
| Resource Group | `rg-aks-sre-platform-{env}` | `rg-aks-sre-platform-dev` |
| AKS Cluster | `aks-sre-platform-{env}` | `aks-sre-platform-dev` |
| Container Registry | `acrsreplatform{env}` | `acrsreplatformdev` |
| Key Vault | `kv-sre-platform-{env}` | `kv-sre-platform-dev` |
| Managed Identity | `id-sre-platform-{env}` | `id-sre-platform-dev` |
| Log Analytics | `law-sre-platform-{env}` | `law-sre-platform-dev` |
