# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email [harsh.julapelli@gmail.com](mailto:harsh.julapelli@gmail.com) with details
3. You will receive a response within 48 hours

## Security Design

- **Container scanning** — Trivy runs on every PR to detect image vulnerabilities
- **Pod security** — seccomp profiles, read-only root filesystem, non-root user
- **Network policies** — Namespace-level microsegmentation via Calico
- **RBAC** — Kubernetes RBAC with least-privilege service accounts
- **Secrets management** — Kubernetes secrets; production should use External Secrets Operator or CSI driver
- **Image provenance** — Images pulled from private ACR with digest pinning

## Sensitive Data

- Do not commit kubeconfig files, Azure credentials, or API keys
- Helm `values.yaml` files in this repo use placeholder values
- Real secrets should be managed via Azure Key Vault or sealed secrets
