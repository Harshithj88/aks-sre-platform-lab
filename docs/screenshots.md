# Screenshots

Add screenshots here to showcase the project for your portfolio, resume, and LinkedIn.

## Recommended Screenshots

### CI/CD

- [ ] GitHub Actions — successful CI workflow run
- [ ] GitHub Actions — successful infrastructure deployment
- [ ] GitHub Actions — successful Helm deployment to AKS

### Azure Resources

- [ ] Azure Portal — Resource Group overview
- [ ] Azure Portal — AKS cluster overview
- [ ] Azure Portal — ACR with pushed container image

### Kubernetes

- [ ] `kubectl get pods -n demo-api` — healthy pods
- [ ] `kubectl get svc -n demo-api` — service endpoints
- [ ] `kubectl get hpa -n demo-api` — autoscaler status
- [ ] Helm release list output

### Observability

- [ ] Grafana — Application metrics dashboard
- [ ] Grafana — Cluster health dashboard
- [ ] Prometheus — Alert rules
- [ ] Prometheus — Active alerts

### Application

- [ ] `/health` endpoint response
- [ ] `/metrics` endpoint showing Prometheus metrics
- [ ] `/simulate-latency` endpoint response

### SRE Documentation

- [ ] SLO document
- [ ] Incident runbook
- [ ] Postmortem template

## How to Add Screenshots

1. Create a `docs/images/` folder
2. Save screenshots as PNG files with descriptive names
3. Reference them in this document:

```markdown
![Description](images/screenshot-name.png)
```
