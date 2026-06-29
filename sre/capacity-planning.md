# Capacity Planning

## Overview

Capacity planning ensures the platform has enough resources to handle current and projected workloads while maintaining SLO targets. This document covers the process, tools, and thresholds for the AKS SRE Platform.

## Key Concepts

| Term | Definition |
|---|---|
| **Capacity** | Maximum workload a system can handle within SLO targets |
| **Headroom** | Buffer between current usage and capacity limit |
| **Saturation** | Degree to which a resource is utilized (0% = idle, 100% = full) |
| **USE Method** | Utilization, Saturation, Errors — framework for resource analysis |

## Current Resource Configuration

### Dev Environment

| Resource | Configuration |
|---|---|
| AKS Node Count | 1 (autoscaler: 1-5) |
| Node VM Size | Standard_B2s (2 vCPU, 4 GB) |
| Pod Replicas | 1 (HPA: 1-3) |
| CPU Request / Limit | 50m / 200m |
| Memory Request / Limit | 64Mi / 128Mi |

### Prod Environment

| Resource | Configuration |
|---|---|
| AKS Node Count | 3 (autoscaler: 1-5) |
| Node VM Size | Standard_D2s_v3 (2 vCPU, 8 GB) |
| Pod Replicas | 2 (HPA: 2-6) |
| CPU Request / Limit | 100m / 250m |
| Memory Request / Limit | 128Mi / 256Mi |

## Capacity Planning Process

### 1. Inventory Current Resources

```bash
# Node capacity
kubectl describe nodes | grep -A 5 "Allocated resources"

# Pod resource usage
kubectl top pods -n demo-api

# Node resource usage
kubectl top nodes

# HPA status
kubectl get hpa -n demo-api
```

### 2. Measure Current Usage

Key Prometheus queries:

```promql
# CPU utilization per pod
sum(rate(container_cpu_usage_seconds_total{namespace="demo-api"}[5m])) by (pod)

# Memory utilization per pod
sum(container_memory_working_set_bytes{namespace="demo-api"}) by (pod)

# Request rate
sum(rate(http_requests_total[5m]))

# Node CPU utilization
sum(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (node) / count(node_cpu_seconds_total{mode="idle"}) by (node)
```

### 3. Identify Growth Trends

- Review weekly/monthly traffic patterns in Grafana
- Correlate with business events (launches, campaigns, seasonal traffic)
- Project growth using linear or exponential models

### 4. Set Thresholds

| Resource | Warning | Critical | Action |
|---|---|---|---|
| Node CPU | 70% | 85% | Scale node pool |
| Node Memory | 75% | 90% | Scale node pool |
| Pod CPU | 70% | 85% | Increase limits or add replicas |
| Pod Memory | 75% | 90% | Increase limits or add replicas |
| Disk | 70% | 85% | Expand PVC or clean up |

### 5. Autoscaling Configuration

**Horizontal Pod Autoscaler (HPA):**
- Scales pods based on CPU (70%) and memory (80%) utilization
- Scale-up stabilization: 60 seconds
- Scale-down stabilization: 300 seconds

**Cluster Autoscaler:**
- Scales AKS node pool between min and max count
- Triggered when pods can't be scheduled due to insufficient resources
- Scale-down delay: 10 minutes after last scale-up

## Load Testing

Before capacity changes, validate with load testing:

```bash
# Install k6 or use hey for basic testing
hey -n 10000 -c 50 -m GET http://<service-url>/health

# Watch HPA response
kubectl get hpa -n demo-api --watch
```

## Capacity Review Cadence

| Review | Frequency | Participants |
|---|---|---|
| Resource usage check | Weekly | On-call engineer |
| Capacity trend review | Monthly | Platform team |
| Full capacity planning | Quarterly | Engineering + leadership |
| Load test | Before major releases | Platform + dev team |
