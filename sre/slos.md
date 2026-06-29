# Service Level Objectives

## Service: Demo API

### Availability SLO

The demo API should maintain **99.5% availability** over a rolling 30-day window.

**SLI:** Proportion of successful HTTP requests (non-5xx) out of total requests.

```promql
1 - (
  sum(rate(http_requests_total{status=~"5.."}[30d]))
  /
  sum(rate(http_requests_total[30d]))
)
```

### Latency SLO

**95% of successful requests** should complete within **300ms**.

**SLI:** 95th percentile request latency.

```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### Error Rate SLO

HTTP 5xx responses should remain below **1% of total requests**.

**SLI:** Ratio of 5xx responses to total responses.

```promql
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

## Error Budget

| SLO Target | Allowed Downtime (30 days) | Monthly Error Budget |
|---|---|---|
| 99.5% | ~3.6 hours | 0.5% of requests |
| 99.9% | ~43 minutes | 0.1% of requests |
| 99.95% | ~22 minutes | 0.05% of requests |

## How SLOs Drive Decisions

| Error Budget Consumed | Action |
|---|---|
| < 50% | Normal feature delivery |
| 50% - 80% | Review recent incidents, increase monitoring |
| 80% - 100% | Freeze non-critical releases, prioritize reliability |
| Exhausted | Stop feature deployments until stability improves |

## Alert Mapping

| SLO | Alert Name | Severity | Threshold |
|---|---|---|---|
| Availability | `HighErrorRate` | Critical | > 1% 5xx for 5m |
| Availability | `ErrorBudgetBurnRate` | Warning | > 0.5% 5xx for 15m |
| Latency | `HighLatencyP95` | Warning | P95 > 300ms for 5m |
| Latency | `HighLatencyP99` | Critical | P99 > 1s for 5m |
