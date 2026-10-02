# Network Policy Guide

How network isolation is applied to the `demo-api` workload, plus reusable patterns for hardening pod-to-pod traffic in the cluster.

## Prerequisites

NetworkPolicy enforcement requires a network plugin that supports it. On AKS, use one of:

- **Azure CNI** with Azure Network Policy
- **Azure CNI** with Calico
- **Cilium** (Azure CNI powered by Cilium)

> Without a policy-enforcing plugin, NetworkPolicy objects are accepted by the API server but silently ignored.

## The demo-api Policy

The chart ships a NetworkPolicy (`templates/networkpolicy.yaml`) gated behind `networkPolicy.enabled`:

```yaml
networkPolicy:
  enabled: true
```

When enabled, it:

- Selects the `demo-api` pods via the chart's selector labels
- Applies both `Ingress` and `Egress` policy types
- Allows ingress only on the service target port (TCP)
- Allows all egress (`egress: - {}`)

This is a reasonable starting point: it locks down inbound traffic to the app port while leaving egress open so the app can reach dependencies and DNS.

## Hardening Patterns

### 1. Default-deny baseline (recommended)

Apply a namespace-wide default-deny, then layer explicit allows. This is the single most effective policy.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: demo
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### 2. Allow DNS egress

With default-deny egress in place, pods can no longer resolve DNS. Explicitly allow it:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-egress
  namespace: demo
spec:
  podSelector: {}
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
      ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
```

### 3. Restrict ingress to the ingress controller only

Instead of allowing ingress from anywhere, scope it to the ingress-nginx namespace:

```yaml
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
      ports:
        - port: 8000
          protocol: TCP
```

### 4. Restrict egress to a specific dependency

Allow the app to reach only a database pod, denying all other egress:

```yaml
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - port: 5432
          protocol: TCP
```

## Testing Policies

```bash
# Confirm the plugin enforces policies (should FAIL/timeout when blocked)
kubectl run test --rm -it --image=busybox --restart=Never -n demo -- \
  wget -qO- --timeout=3 http://demo-api:80/health

# From an allowed namespace it should succeed; from a denied one it should hang/timeout.

# Inspect applied policies
kubectl get networkpolicy -n demo
kubectl describe networkpolicy default-deny-all -n demo
```

## Rollout Guidance

1. Start in a non-prod namespace with a default-deny policy
2. Add allow rules iteratively, watching for broken traffic (DNS first!)
3. Validate app health and dependency reachability after each change
4. Promote the policy set to prod once stable

## Related

- [Architecture](architecture.md)
- Helm template: `helm/demo-api/templates/networkpolicy.yaml`
