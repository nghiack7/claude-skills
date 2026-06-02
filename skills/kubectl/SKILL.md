---
name: kubectl
description: Expert guidance for Kubernetes cluster operations with kubectl and GitOps (FluxCD/ArgoCD). Use when the user asks to "check pods", "get deployments", "view namespace", "kubectl get", "restart pod", "check rollout status", or mentions Kubernetes, K8s, kubectl, Flux GitOps, or cluster operations.
---

## Related Skills

- **k8s-access** - EKS kubeconfig setup and AWS credentials
- **aws** - AWS CLI, SSO authentication

# kubectl - Kubernetes Cluster Access

Kubectl reference for managing Kubernetes clusters with GitOps workflows.

## Contexts

Configure your contexts to match your cluster setup:

| Context | Cluster | Type | Access |
| -------------------------------- | --------------- | ------- | ---------- |
| `your-cluster-dev` | development | RKE2/on-prem | Read/Write |
| `your-cluster-prod` | production | AWS EKS | READ-ONLY |

## Quick Reference

```bash
# Development
kubectl --context your-cluster-dev get pods -n <NAMESPACE>

# Production (READ-ONLY for automated agents)
kubectl --context your-cluster-prod get pods -n <NAMESPACE>
```

## Production Safety

**Automated agents should be BLOCKED from write commands on production:** apply, create, delete, patch, scale, rollout, etc.

## Kubert - Context Protection (Recommended)

**kubert** is a kubectl wrapper that provides context isolation and command protection for cluster safety.

### Installation

```bash
brew install idebeijer/tap/kubert --cask
```

### Configuration

Create `~/.config/kubert/config.yaml`:

```yaml
kubeconfigs:
  include:
    - "~/.kube/config"
    - "~/.kube/*.yml"
    - "~/.kube/*.yaml"

protection:
  regex: "(prod|production|prd)"  # Auto-protect matching contexts
  commands: [delete, edit, exec, drain, scale, autoscale, replace, apply, patch, set]
  prompt: true  # Confirm before risky commands (false = block entirely)
```

### Key Commands

```bash
# Launch isolated shell for a context
kubert ctx your-cluster-prod

# Switch namespace within kubert shell
kubert ns <NAMESPACE>

# Run kubectl with protection
kubert kubectl apply -f deployment.yaml  # Will prompt for confirmation on prod

# Check protection status
kubert protection info

# Temporarily lift protection (e.g., 5 minutes)
kubert protection lift 5m

# Multi-context execution
kubert exec "prod-*" -- kubectl get pods
kubert exec --parallel "stg-*" -- kubectl rollout status deployment/app
```

### Protection States

| Command | Effect |
| ---------------------------- | -------------------------------- |
| `kubert protection protect` | Force enable for current context |
| `kubert protection unprotect`| Force disable for current context|
| `kubert protection lift 5m` | Temporarily suspend |
| `kubert protection remove` | Revert to regex-based defaults |

### Why Use Kubert?

1. **Context Isolation**: Each shell gets its own kubeconfig copy - no accidental context leakage
2. **Protection Rules**: Blocks/confirms risky commands (delete, apply, scale) on prod
3. **Audit Trail**: Shell hooks can log all operations
4. **Multi-Context Ops**: Execute across clusters with patterns

**IMPORTANT**: Protection only works when using `kubert kubectl`, not raw `kubectl`.

## GitOps Deployment

| Cluster | Flux Repo | Local Mirror |
| ----------- | --------------------- | --------------------------------------- |
| Development | `k8s-manifests-dev` | `infra/kubernetes/k8s-manifests-dev` |
| Production | `k8s-manifests-prod` | `infra/kubernetes/k8s-manifests-prod` |

**Deploy = commit to repo's `master` branch**

## Local Mirror Structure

```
infra/
├── kubernetes/
│   ├── k8s-manifests-dev/.git      # Staging/dev K8s manifests
│   └── k8s-manifests-prod/.git     # Production K8s manifests
├── infras/
│   └── terragrunt/.git             # Terraform/Terragrunt
└── helm-charts/
    └── your-app/.git               # Helm charts
```

**Find actual repos in a group:**

```bash
find /path/to/group -name ".git" -type d -exec dirname {} \;
```

**Never `git init` in group folders** - always find existing repos first.

## Common Namespaces

| Namespace | Purpose |
| ------------- | ------------------ |
| `your-app` | Main application |
| `flux-system` | FluxCD components |
| `argocd` | ArgoCD (secondary) |
| `ingress-nginx` | Ingress controller |
| `cert-manager` | TLS certificates |
| `monitoring` | Prometheus/Grafana |

## Verify Deployment

```bash
# Check FluxCD status
kubectl --context your-cluster-prod get kustomizations -n flux-system

# Check application pods
kubectl --context your-cluster-prod get pods -n <NAMESPACE>

# Check HelmReleases
kubectl --context your-cluster-prod get helmreleases -n <NAMESPACE>
```
