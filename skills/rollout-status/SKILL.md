---
name: rollout-status
description: >
  Expert guidance for tracing end-to-end deployment pipeline status. Use when the user asks to "check rollout",
  "is it deployed", "verify deployment", "check if fix is live", "rollout status", "why still old version",
  or needs to trace a commit from a container image through ArgoCD sync to a running K8s pod.
author: Claude Code
version: 2.0.0
---

## Live Deployment Context

- **Current kubectl context:** !`kubectl config current-context 2>/dev/null || echo "no kubectl context set"`
- **AWS SSO status:** !`aws sts get-caller-identity --profile <AWS_PROFILE> 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Authenticated as {d[\"Arn\"].split(\"/\")[-1]}')" 2>/dev/null || echo "AWS SSO expired — run: aws sso login --profile <AWS_PROFILE>"`

### Current Pods

!`kubectl --context <CLUSTER_CONTEXT> get pods -n <NAMESPACE> --no-headers 2>/dev/null | awk '{printf "  %-45s %-10s %-8s %s\n", $1, $2, $3, $4}' | head -15 || echo "  Cannot reach cluster — check kubectl auth"`

> Use the live context above to skip prerequisite checks. If AWS SSO expired, instruct user to run login first.

# Rollout Status

Checks the end-to-end deployment pipeline: commit → container registry → ArgoCD → K8s pod.

## Quick Usage

```
/rollout-status [service] [commit-sha]
```

Example: `/rollout-status my-service 8d32af6`

---

## How This Skill Works

Uses a **script-based approach** to save tokens:

1. **First time** (or when config changes): AI generates a script from the template, writes it to a temp dir, then runs it
2. **Subsequent runs**: Just execute the existing script — no AI needed

```
rollout-status.sh.template  →  AI fills config  →  /tmp/rollout-status-<project>.sh  →  run
```

---

## Step 1: Generate Project Script

Template location:
```
<SKILL_DIR>/rollout-status/rollout-status.sh.template
```

**AI must:**
1. Read the template
2. Fill in the project-specific values for all `{{...}}` placeholders
3. Write to `/tmp/rollout-status-<project>.sh` — do NOT write to the project directory
4. `chmod +x` then run with args

### Template Placeholders

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{PROJECT_NAME}}` | Project name | `my-app` |
| `{{KUBECTL_CONTEXT}}` | kubectl context | `your-cluster-prod` |
| `{{AWS_PROFILE}}` | AWS CLI profile | `<AWS_PROFILE>` |
| `{{AWS_REGION}}` | AWS region | `<AWS_REGION>` |
| `{{ARGOCD_NAMESPACE}}` | ArgoCD namespace | `argocd` |
| `{{IMAGE_PREFIX}}` | Branch prefix in image tags | `master` |
| `{{DEFAULT_NAMESPACE}}` | Default K8s namespace | `<NAMESPACE>` |
| `{{NAMESPACE_MAPPING}}` | case entries for get_namespace() | see below |
| `{{ARGOCD_APP_MAPPING}}` | case entries for get_argocd_app() | see below |

### Namespace Mapping Format

```bash
# {{NAMESPACE_MAPPING}} — one case entry per line:
    service-a)    echo "namespace-x" ;;
    service-b)    echo "namespace-y" ;;
```

### ArgoCD App Mapping Format

```bash
# {{ARGOCD_APP_MAPPING}} — only needed if ArgoCD app name differs from service name:
    some-service)  echo "argocd-app-name" ;;
```
If all app names match service names, leave empty (keep `*) echo "$1" ;;` default).

---

## Step 2: Run the Script

```bash
# Check current HEAD
./rollout-status.sh my-service

# Check specific commit
./rollout-status.sh my-service eb28443

# Check different service
./rollout-status.sh other-service
```

---

## Common Issues

### Script does not exist
→ Generate from template (Step 1 above)

### AWS SSO expired
```bash
aws sso login --profile <AWS_PROFILE>
```

### kubectl auth expired
```bash
aws sso login --profile <AWS_PROFILE>
kubectl --context <CLUSTER_CONTEXT> get pods -n <NAMESPACE>
```

### Container image missing → CI has not run
→ Go to your CI system (e.g. GitLab → CI/CD → Pipelines) and trigger the build job manually

### ArgoCD OutOfSync
→ Image-updater delay (~1 min), or check:
```bash
kubectl logs -n argocd -l app=argocd-image-updater --tail=50 \
  --context <CLUSTER_CONTEXT>
```

### ArgoCD Synced but pod still has old image
→ Check wave controller annotations:
```bash
kubectl get deployment -n <NAMESPACE> <service-name> \
  --context <CLUSTER_CONTEXT> \
  -o jsonpath='{.metadata.annotations}'
```
