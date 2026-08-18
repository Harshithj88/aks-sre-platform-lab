# Resume Bullets

Use these bullet points on your resume, LinkedIn, or portfolio to describe this project.

## Project Summary

**AKS SRE Platform Lab** — Production-style Kubernetes platform on Azure demonstrating end-to-end infrastructure automation, observability, and SRE practices.

## Bullet Points

- Designed and deployed a multi-resource Azure infrastructure using **Bicep IaC** modules (AKS, ACR, Key Vault, Managed Identity, Log Analytics) with resource tagging and environment parameterization
- Implemented **secretless CI/CD** pipelines using GitHub Actions with **OIDC federation** to Microsoft Entra ID, eliminating stored credentials
- Built a **multi-stage Docker** container workflow with security hardening (non-root user, dropped capabilities, read-only filesystem, seccomp profile)
- Authored **Helm charts** with Kubernetes best practices: rolling updates, HPA, PDB, topology spread constraints, NetworkPolicy, and startup/liveness/readiness probes
- Configured a full **observability stack** (Prometheus, Grafana, Alertmanager, OpenTelemetry) with custom dashboards for application metrics and cluster health
- Defined **SLOs** (99.5% availability, P95 < 300ms latency) with automated alerting, error budget tracking, and burn-rate alerts
- Enabled **Azure security controls** including Microsoft Defender for Containers, Azure Policy addon, RBAC-only Key Vault, and ACR admin disabled
- Integrated **security scanning** into CI: pip-audit for dependencies, Trivy for container images (SARIF → GitHub Security tab), and Checkov for IaC
- Created **SRE documentation** suite: incident runbooks, postmortem templates, on-call checklists, error budget policy, and capacity planning guides
- Built FastAPI demo service with **automatic Prometheus metrics middleware**, structured logging, and simulation endpoints for latency/error injection testing

## Skills Demonstrated

Azure, AKS, Bicep, Kubernetes, Helm, Docker, GitHub Actions, OIDC, Prometheus, Grafana, Alertmanager, OpenTelemetry, SLO/SLI, Python, FastAPI, Trivy, Checkov, SRE
