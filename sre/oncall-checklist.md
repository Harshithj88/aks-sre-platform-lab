# On-Call Checklist

## Before Your Shift

- [ ] Review the handoff notes from the previous on-call engineer
- [ ] Check the current error budget status in Grafana
- [ ] Review any open incidents or active issues
- [ ] Verify you have access to all required tools and dashboards
- [ ] Confirm alerting channels are configured and notifications are working
- [ ] Check scheduled maintenance windows during your rotation
- [ ] Review recent deployments and changes

## Tools Checklist

- [ ] **kubectl** configured with AKS credentials
- [ ] **Grafana** dashboards accessible (App Dashboard + Cluster Dashboard)
- [ ] **Prometheus** alert rules visible
- [ ] **Azure Portal** access confirmed
- [ ] **GitHub** repository access (for rollback if needed)
- [ ] **Communication channel** (Slack/Teams) joined and notifications on

## During Your Shift

### When an Alert Fires

1. Acknowledge the alert within **5 minutes**
2. Open the relevant Grafana dashboard
3. Assess severity using the table below
4. Follow the [incident runbook](incident-runbook.md)
5. Communicate status in the incident channel
6. Escalate if not resolved within the response window

### Severity Levels

| Severity | Description | Response Time | Escalation |
|---|---|---|---|
| SEV-1 | Service down, all users affected | 5 minutes | Immediate |
| SEV-2 | Significant degradation, many users affected | 15 minutes | 30 minutes |
| SEV-3 | Minor issue, limited user impact | 30 minutes | 2 hours |
| SEV-4 | Cosmetic or low-priority issue | Next business day | None |

### Quick Diagnostic Commands

```bash
# Pod status
kubectl get pods -n demo-api

# Recent events
kubectl get events -n demo-api --sort-by=.metadata.creationTimestamp | tail -20

# Pod resource usage
kubectl top pods -n demo-api

# Application logs
kubectl logs -l app=demo-api -n demo-api --tail=50

# HPA status
kubectl get hpa -n demo-api

# Node health
kubectl get nodes
kubectl top nodes
```

## After Your Shift

- [ ] Write handoff notes for the next on-call engineer
- [ ] Document any incidents that occurred
- [ ] File postmortems for SEV-1 or SEV-2 incidents
- [ ] Update runbooks with any new findings
- [ ] Log any alert noise or false positives for tuning
- [ ] Confirm the next on-call engineer has acknowledged their shift

## On-Call Health

- Limit on-call rotations to **1 week maximum**
- Ensure **at least 1 day off** between rotations
- If you were paged more than 3 times overnight, flag it for alert review
- Track on-call load and escalate if the burden is unsustainable
