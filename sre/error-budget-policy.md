# Error Budget Policy

## Objective

This policy defines how the team responds when the service consumes too much of its monthly error budget. The error budget is derived from the availability SLO (99.5%).

## Error Budget Calculation

- **Monthly error budget:** 0.5% of total requests (or ~3.6 hours of downtime)
- **Measurement window:** Rolling 30 days
- **Data source:** Prometheus `http_requests_total` metric

## Budget Consumption Rules

### Green Zone (< 50% consumed)

- Normal feature delivery continues
- Standard deployment velocity
- Regular alert review cadence

### Yellow Zone (50% - 80% consumed)

- Review all recent incidents and their resolution
- Evaluate deployment frequency and rollback rate
- Increase monitoring coverage for high-risk areas
- Prioritize reliability-related backlog items

### Red Zone (80% - 100% consumed)

- Freeze non-critical feature releases
- All engineering effort shifts to reliability work
- Conduct focused incident review sessions
- Review and tune alert thresholds
- Perform load testing to identify capacity gaps
- Mandatory postmortem for any new incidents

### Budget Exhausted (100% consumed)

- Stop all feature deployments
- Full engineering focus on service stability
- Escalate to engineering leadership
- Conduct root cause analysis across all contributing incidents
- Resume feature work only after budget is replenished and corrective actions are complete

## Reliability Actions

When the error budget is under pressure:

- [ ] Review alert noise and suppress non-actionable alerts
- [ ] Investigate recurring incidents for common root causes
- [ ] Improve test coverage for failure scenarios
- [ ] Add missing dashboards and observability gaps
- [ ] Tune resource limits and autoscaling rules
- [ ] Review dependency health and timeout configurations
- [ ] Validate rollback procedures

## Review Cadence

- **Weekly:** Check error budget consumption in Grafana
- **Monthly:** Review SLO performance and adjust targets if needed
- **Quarterly:** Full error budget policy review with stakeholders
