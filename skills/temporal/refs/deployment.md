# Temporal Deployment & Infrastructure

## Clusters

### Development

```bash
kubectl --context <KUBE_CONTEXT_DEV>
```

| Resource      | Value                                                                       |
| ------------- | --------------------------------------------------------------------------- |
| Namespace     | `temporal`                                                                  |
| Web UI        | Port forward: `kubectl port-forward -n temporal svc/temporal-web 8080:8080` |
| Frontend Port | `7233` (internal)                                                           |
| PostgreSQL    | `temporal-postgresql-0.temporal-postgresql.temporal.svc.cluster.local:5432` |

### Production

```bash
kubectl --context <KUBE_CONTEXT_PROD>
```

Same namespace `temporal`.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     TEMPORAL ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │  Frontend    │────▶│   History    │────▶│   Matching   │    │
│  │  (Port 7233) │     │   Service    │     │   Service    │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│         │                     │                     │            │
│         └─────────────────────┼─────────────────────┘            │
│                               │                                  │
│                       ┌───────▼────────┐                        │
│                       │  Worker        │                        │
│                       │  Service       │                        │
│                       └───────┬────────┘                        │
│                               │                                  │
│         ┌─────────────────────┼─────────────────────┐            │
│         ▼                     ▼                     ▼            │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │  PostgreSQL  │    │   Web UI     │    │  Admin Tools │     │
│  │  (Primary +  │    │  (Port 8080) │    │  (tctl CLI)  │     │
│  │  Visibility) │    └──────────────┘    └──────────────┘     │
│  └──────────────┘                                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Database Configuration

```bash
# Primary Store
Host: temporal-postgresql.temporal.svc.cluster.local
Port: 5432
Database: temporal
User: temporal
Password: <from Secret: temporal-postgresql-secret>

# Visibility Store
Database: temporal_visibility
```

### Get Database Password

```bash
kubectl --context <KUBE_CONTEXT_DEV> get secret temporal-postgresql-secret -n temporal -o jsonpath='{.data.password}' | base64 -d
```

## Helm Chart Configuration

### Key Files

```
k8s/temporal/
├── kustomization.yaml
├── namespace.yaml
└── server/
    ├── helm.yaml              # Temporal HelmRelease
    ├── ingress.yaml
    ├── postgresql-oci.yaml    # OCIRepository
    ├── postgresql-helm.yaml   # PostgreSQL HelmRelease
    └── postgresql-secret.yaml
```

### Kustomization Resource Order

**IMPORTANT:** Resources must be listed in dependency order:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - namespace.yaml
  # PostgreSQL first
  - server/postgresql-oci.yaml
  - server/postgresql-secret.yaml
  - server/postgresql-helm.yaml
  # Temporal Server
  - server/helm.yaml
  - server/ingress.yaml
  # Workers
  - worker/image-updater.yaml
  - worker/configmap.yaml
  - worker/secret.yaml
  - worker/deployment.yaml
```

### Current Versions

| Component       | Version            |
| --------------- | ------------------ |
| Temporal Server | `1.29.1`           |
| Temporal Web UI | `2.34.0`           |
| Helm Chart      | `0.73.1`           |
| PostgreSQL      | `16.4.5` (Bitnami) |

## Persistence Driver Configuration

Temporal has a **dual-layer** driver configuration:

```yaml
server:
  config:
    persistence:
      default:
        driver: "sql" # Layer 1: Helm chart template (must be "sql")
        sql:
          driver: "postgres12" # Layer 2: Actual database driver
          host: "temporal-postgresql"
          port: 5432
          database: "temporal"
          user: "temporal"
          existingSecret: "temporal-postgresql-secret"
          secretKey: "password"
```

**Supported SQL Drivers:** `mysql8`, `postgres12`, `postgres12_pgx`, `sqlite`

## Local Development

```bash
cd /path/to/your/worker
docker-compose up -d
```

Starts:

- Temporal server (`localhost:7233`)
- Web UI (`localhost:8080`)
- PostgreSQL

## Namespace Registration

**IMPORTANT:** Fresh deployments only have `temporal-system`. Create namespaces manually:

```bash
kubectl --context <KUBE_CONTEXT_DEV> exec -it -n temporal \
  $(kubectl get pod -n temporal -l app.kubernetes.io/component=admintools -o name) -- \
  tctl --address temporal-frontend.temporal.svc.cluster.local:7233 \
  namespace register default --retention 168h
```
