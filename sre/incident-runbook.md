# Incident Runbook

## Scenario: Elevated HTTP 5xx Errors

### Detection

Alert triggered:

- **HighErrorRate** — HTTP 5xx responses greater than 1% for 5 minutes
- **ErrorBudgetBurnRate** — Error budget consumption rate is elevated

### Initial Triage

1. Open the Grafana **App Dashboard** and check the error rate panel
2. Check Kubernetes pod status for the demo-api namespace
3. Review recent deployments and changes
4. Check application logs for error patterns
5. Verify ingress controller health
6. Check resource usage (CPU, memory) against limits

### Useful Commands

```bash
# Check pod status
kubectl get pods -n demo-api

# Describe a specific pod
kubectl describe pod <pod-name> -n demo-api

# View application logs
kubectl logs <pod-name> -n demo-api --tail=100

# View previous container logs (if restarted)
kubectl logs <pod-name> -n demo-api --previous

# Check recent events
kubectl get events -n demo-api --sort-by=.metadata.creationTimestamp

# Check deployment rollout history
kubectl rollout history deployment/demo-api -n demo-api

# Check resource usage
kubectl top pods -n demo-api

# Check HPA status
kubectl get hpa -n demo-api

# Check ingress status
kubectl get ingress -n demo-api

# Check service endpoints
kubectl get endpoints demo-api -n demo-api
```

### Investigation

| Check | Command | What to Look For |
|---|---|---|
| Pod health | `kubectl get pods -n demo-api` | CrashLoopBackOff, OOMKilled, Pending |
| Resource pressure | `kubectl top pods -n demo-api` | CPU/memory near limits |
| Recent changes | `kubectl rollout history deployment/demo-api -n demo-api` | Recent deployment |
| Application logs | `kubectl logs <pod> -n demo-api` | Stack traces, connection errors |
| Events | `kubectl get events -n demo-api` | Scheduling failures, image pull errors |
| Dependencies | `kubectl exec <pod> -- curl -sf http://dependency/health` | Dependency failures |

### Mitigation

1. **Roll back** if the issue started after a recent deployment:
   ```bash
   kubectl rollout undo deployment/demo-api -n demo-api
   ```

2. **Scale up** if the issue is caused by traffic surge:
   ```bash
   kubectl scale deployment/demo-api -n demo-api --replicas=4
   ```

3. **Restart unhealthy pods** if individual pods are degraded:
   ```bash
   kubectl delete pod <pod-name> -n demo-api
   ```

4. **Drain a node** if the issue is node-specific:
   ```bash
   kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
   ```

### Escalation

| Level | Contact | When |
|---|---|---|
| L1 | On-call engineer | First responder |
| L2 | Platform team lead | Issue not resolved in 30 minutes |
| L3 | Cloud infrastructure team | Azure/AKS platform issue |

### Post-Incident Actions

- [ ] Complete postmortem using the [postmortem template](postmortem-template.md)
- [ ] Identify root cause
- [ ] Add missing alerts or dashboards
- [ ] Update this runbook with new findings
- [ ] Create reliability improvement backlog items
- [ ] Review error budget impact
