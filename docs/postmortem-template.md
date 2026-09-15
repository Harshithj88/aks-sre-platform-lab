# Postmortem: [Incident Title]

**Date**: YYYY-MM-DD
**Severity**: SEV-1 / SEV-2 / SEV-3
**Duration**: HH:MM (start → end)
**Author**: [Name]
**Status**: Draft / Reviewed / Complete

---

## Summary

One paragraph describing what happened, the user impact, and how it was resolved.

## Timeline (UTC)

| Time | Event |
|------|-------|
| HH:MM | First alert fired (source: Prometheus / PagerDuty / Grafana) |
| HH:MM | On-call engineer acknowledged |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Service fully restored |
| HH:MM | All-clear communicated to stakeholders |

## Impact

- **Users affected**: X% of traffic / Y users
- **Duration**: Z minutes
- **Revenue impact**: $N (if applicable)
- **SLO burn**: X% of monthly error budget consumed

## Root Cause

Detailed technical explanation of what caused the incident. Include the chain of events that led to the failure.

## Detection

- How was the incident detected? (alert, customer report, internal monitoring)
- Time from incident start to detection: X minutes
- Were existing alerts effective? If not, why?

## Resolution

Step-by-step description of what was done to resolve the incident:

1. Step one
2. Step two
3. Step three

## What Went Well

- Item 1
- Item 2

## What Went Wrong

- Item 1
- Item 2

## Where We Got Lucky

- Item 1

## Action Items

| Priority | Action | Owner | Due Date | Status |
|----------|--------|-------|----------|--------|
| P1 | Fix the root cause | @owner | YYYY-MM-DD | Open |
| P2 | Improve alerting for this failure mode | @owner | YYYY-MM-DD | Open |
| P3 | Add runbook for this scenario | @owner | YYYY-MM-DD | Open |
| P3 | Update monitoring dashboards | @owner | YYYY-MM-DD | Open |

## Lessons Learned

Key takeaways that should inform future architecture, process, or monitoring decisions.

## Related

- Incident ticket: [LINK]
- Slack thread: [LINK]
- Related postmortems: [LINK]
