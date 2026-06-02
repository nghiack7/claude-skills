# Deployment Infrastructure

Production deployment architecture using GitOps with FluxCD.

## CI/CD Platform: GitLab CI

Templates location: `gitlab-ci-templates/` (project-specific templates in a subdirectory)

**Pipeline stages:**

```
init → setup → check-deploy-done → sast → build → deploy → dast
```

| Stage | Purpose |
| ------ | ----------------------------------------------- |
| init | Initialize environment variables |
| setup | Security scanning (secrets, dependencies) |
| sast | Static Application Security Testing (SonarQube) |
| build | Docker image build → container registry |
| deploy | Update GitOps manifests |
| dast | Dynamic Application Security Testing |

## Deployment Flow

```
Code Push → GitLab CI → Docker Build → Registry → GitOps Repo Update → FluxCD Sync → K8s
```

1. Developer pushes to branch
2. GitLab CI builds Docker image
3. Image pushed to container registry
4. Pipeline updates K8s manifests in GitOps repo
5. FluxCD detects changes (10-minute reconciliation)
6. FluxCD applies manifests to cluster

## Environment Mapping

| Branch Pattern | Environment | Registry |
| -------------- | ----------- | --------------------------- |
| `develop*` | dev | your-registry-staging.example.com |
| `staging*` | stg | your-registry-staging.example.com |
| `main/master` | prod | your-registry-prod.example.com |

## Image Tagging

Format: `{BRANCH}-{COMMIT_SHA_SHORT}-{PIPELINE_ID}`

Example: `develop-abc123-42`

## Container Registries

| Registry | Environment | URL |
| ----------------- | --------------- | --------------------------------------------- |
| Staging Registry | dev/stg | your-registry-staging.example.com |
| Production Registry | prod | your-registry-prod.example.com |
| AWS ECR | prod (optional) | `<AWS_ACCOUNT_ID>.dkr.ecr.<AWS_REGION>.amazonaws.com` |

## GitOps Repositories

| Cluster | Repo | Local Mirror |
| ------------------ | ------------------- | --------------------------------------- |
| Development | k8s-manifests-dev | `infra/kubernetes/k8s-manifests-dev` |
| Production (EKS) | k8s-manifests-prod | `infra/kubernetes/k8s-manifests-prod` |

## FluxCD Configuration

Location: `infra/kubernetes/k8s-manifests-prod/flux-system/`

- **Reconciliation interval:** 10 minutes
- **Prune:** Enabled (removes resources not in Git)
- **Source:** GitLab repo `k8s-manifests-prod`

## Manifest Management

**Kustomize:**

- Path: `k8s-manifests-prod/{environment}/{namespace}/`
- ConfigMaps: Plain in dev
- Secrets: SOPS-encrypted in prod

## Security Gates

| Gate | Tool | Stage |
| ---------------- | --------- | ----- |
| Static Analysis | SonarQube | sast |
| Secret Detection | GitLab | setup |
| Dependency Scan | GitLab | setup |
| Container Scan | Trivy | build |

## Production Namespaces

| Namespace | Purpose |
| ------------- | ------------------ |
| `your-app` | Main application |
| `flux-system` | FluxCD components |
| `argocd` | ArgoCD (secondary) |
| `ingress-nginx` | Ingress controller |
| `cert-manager` | TLS certificates |
| `monitoring` | Prometheus/Grafana |

## Infrastructure as Code

**Terraform/Terragrunt:** `infra/terragrunt/`

Manages:

- Security groups
- VPCs and peering
- VPC endpoints

## Deploy a Change

**To deploy to production:**

1. Merge PR to `main` branch
2. CI pipeline auto-triggers
3. Wait for FluxCD sync (~10 min) or check ArgoCD UI

**Manual manifest update:**

```bash
# Navigate to GitOps repo
cd infra/kubernetes/k8s-manifests-prod

# Edit manifests
vim prod/<namespace>/<service>/kustomization.yaml

# Commit and push
git add . && git commit -m "Update <service>" && git push
```

## Verify Deployment

```bash
# Check FluxCD status
kubectl --context your-cluster-prod get kustomizations -n flux-system

# Check application pods
kubectl --context your-cluster-prod get pods -n <NAMESPACE>

# Check HelmReleases
kubectl --context your-cluster-prod get helmreleases -n <NAMESPACE>
```
