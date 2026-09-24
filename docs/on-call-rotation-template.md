# On-Call Rotation Template

A reference template for defining an on-call rotation, escalation policy, and responder expectations for the platform team.

## Rotation Overview

| Field | Value |
|-------|-------|
| Team | Platform / SRE |
| Rotation type | Weekly (Mon 09:00 → Mon 09:00 UTC) |
| Handoff time | Monday 09:00 UTC |
| Coverage | 24x7 |
| Time zone | UTC (adjust per responder locale) |

## Schedule

| Week | Primary | Secondary | Manager Escalation |
|------|---------|-----------|--------------------|
| Week 1 | [Name] | [Name] | [Name] |
| Week 2 | [Name] | [Name] | [Name] |
| Week 3 | [Name] | [Name] | [Name] |
| Week 4 | [Name] | [Name] | [Name] |

## Escalation Policy

```
Alert fires
   │
   ├─ 0 min   → Primary on-call (page)
   │
   ├─ 15 min  → No ack? Escalate to Secondary on-call (page)
   │
   ├─ 30 min  → No ack? Escalate to Engineering Manager (page + call)
   │
   └─ 45 min  → Major incident: page Incident Commander, open bridge
```

## Severity Definitions

| Severity | Description | Response Time | Notification |
|----------|-------------|---------------|--------------|
| **SEV1** | Full outage / data loss | Immediate (page) | Primary + Secondary + Manager |
| **SEV2** | Major degradation, SLO at risk | 15 min (page) | Primary |
| **SEV3** | Minor degradation, no SLO impact | Next business hour | Ticket / Slack |
| **SEV4** | Informational | Best effort | Ticket |

## Responder Responsibilities

### Primary On-Call
- Acknowledge pages within 15 minutes
- Triage, mitigate, and resolve incidents
- Escalate when needed; do not hesitate to pull in help
- Keep the incident channel updated
- Hand off open incidents at rotation change

### Secondary On-Call
- Backup for the primary; respond if primary does not acknowledge
- Available for SEV1/SEV2 support and second opinions

### Engineering Manager
- Final escalation point
- Coordinate cross-team response and stakeholder communication for major incidents

## Handoff Checklist

- [ ] Review open incidents and their current state
- [ ] Review any ongoing maintenance or deployments
- [ ] Review recent alerts and known noisy alerts
- [ ] Confirm access to runbooks, dashboards, and paging tools
- [ ] Confirm paging contact details are current
- [ ] Acknowledge handoff in the team channel

## On-Call Expectations

- Be reachable and able to respond within the SLA during your shift
- Have a working laptop, VPN access, and reliable internet
- Keep paging app notifications enabled with override for Do Not Disturb
- Log all significant actions in the incident channel for the timeline
- File follow-up items and, for SEV1/SEV2, schedule a postmortem

## Tools & Links

| Purpose | Link |
|---------|------|
| Paging (PagerDuty/Opsgenie) | [link] |
| Dashboards (Grafana) | [link] |
| Runbooks | [link] |
| Incident channel | #incidents |
| Status page | [link] |

## Related

- [Postmortem Template](postmortem-template.md)
- [Architecture](architecture.md)
