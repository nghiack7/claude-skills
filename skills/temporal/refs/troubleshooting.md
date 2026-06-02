# Temporal Troubleshooting

## Worker "context deadline exceeded"

**Causes:**

1. **Missing Temporal namespace** (most common)

   ```bash
   # Check if namespace exists
   kubectl exec -it -n temporal temporal-admintools-XXX -- \
     tctl --address temporal-frontend.temporal.svc.cluster.local:7233 namespace list

   # Create if missing
   kubectl exec -it -n temporal temporal-admintools-XXX -- \
     tctl --address temporal-frontend.temporal.svc.cluster.local:7233 \
     namespace register default --retention 168h
   ```

2. **Database connection timeout**
3. **Temporal server not ready**

## HelmRelease Not Ready

```bash
kubectl get helmrelease -n temporal
kubectl describe helmrelease temporal -n temporal

# Common: Missing dependency
# Error: unable to get 'temporal/temporal-postgresql' dependency
# Fix: Ensure postgresql-helm.yaml is in kustomization.yaml
```

## ImagePullBackOff

```bash
kubectl describe pod -n temporal -l app=gitlab-sync-worker | grep Image

# Flux ImageRepository must match Harbor path
# Convention: <YOUR_REGISTRY>/your-path/<image-name>
```

## Pods Not Starting

```bash
kubectl logs -n temporal -l app=gitlab-sync-worker

# Common errors:
# - "context deadline exceeded" → Missing namespace or DB connection
# - "relation schema_version does not exist" → Schema init job failed
# - "unknown plugin postgres" → Wrong driver (use postgres12)
```

## Database Connection Issues

```bash
# Test PostgreSQL connection
kubectl exec -it -n temporal temporal-postgresql-0 -- psql -U temporal -d temporal

# Check schema
\dt

# Verify schema_version table
SELECT * FROM schema_version;
```

## Debug Checklist

1. **DNS resolution**

   ```bash
   kubectl exec -n temporal <pod> -- nslookup temporal-frontend
   ```

2. **TCP connectivity**

   ```bash
   kubectl exec -n temporal <pod> -- nc -zv temporal-frontend 7233
   ```

3. **Service availability**

   ```bash
   kubectl get helmrelease -n temporal
   ```

4. **Namespace exists**

   ```bash
   kubectl exec -n temporal temporal-admintools-XXX -- tctl namespace list
   ```

## Common tctl Commands

```bash
# List namespaces
kubectl exec -it -n temporal temporal-admintools-XXX -- \
  tctl --address temporal-frontend.temporal.svc.cluster.local:7233 namespace list

# List workflows
kubectl exec -it -n temporal temporal-admintools-XXX -- \
  tctl --address temporal-frontend.temporal.svc.cluster.local:7233 \
  --namespace default workflow list

# Describe workflow
kubectl exec -it -n temporal temporal-admintools-XXX -- \
  tctl --address temporal-frontend.temporal.svc.cluster.local:7233 \
  workflow describe --workflow-id <wid>

# View workflow history
kubectl exec -it -n temporal temporal-admintools-XXX -- \
  tctl --address temporal-frontend.temporal.svc.cluster.local:7233 \
  workflow show --workflow-id <wid>

# Terminate workflow
kubectl exec -it -n temporal temporal-admintools-XXX -- \
  tctl --address temporal-frontend.temporal.svc.cluster.local:7233 \
  workflow terminate --workflow-id <wid>
```
