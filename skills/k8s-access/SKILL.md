---
name: k8s-access
description: Expert guidance for per-session Kubernetes access setup with thread/session isolation. Use when the user asks to "setup k8s access", "configure kubeconfig", "connect to EKS", "k8s credentials", "kubernetes access", or mentions EKS authentication, kubeconfig generation, or AWS-based Kubernetes cluster access.
---

# k8s-access - Per-Session Kubernetes Access

Each session gets its own isolated KUBECONFIG, ensuring complete isolation between users and sessions.

## Session Isolation

```
Session ID → dedicated KUBECONFIG file → dedicated AWS profile (if custom credentials provided)
```

```bash
# Derived from session context
USERNAME="<username>"        # e.g. alice
SESSION_ID="<sessionId>"     # e.g. 1772608838.728359

# Derived paths
KUBE_CONFIG="/tmp/${USERNAME}-${SESSION_ID}"
AWS_PROFILE_NAME="k8s-${USERNAME}-${SESSION_ID}"
```

---

## Staging / Development

Use the default kubeconfig already present on the machine — no additional setup required.

- Context: `your-cluster-dev`
- Cluster: on-premise (e.g. RKE2)
- Access: Read/Write

```bash
kubectl --context your-cluster-dev get pods -n <namespace>
```

No separate KUBECONFIG or AWS credentials needed. Use directly.

---

## Production (AWS EKS)

Cluster: `<CLUSTER_NAME>` | Region: `<AWS_REGION>` | Access: READ-ONLY for automated agents

Three cases depending on what credentials the user provides:

### Case 1: No credentials provided

Use the default AWS profile and a pre-configured read role already available on the host.

```bash
aws eks update-kubeconfig \
  --name <CLUSTER_NAME> \
  --region <AWS_REGION> \
  --profile default \
  --role-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/<READ_ROLE_NAME> \
  --kubeconfig "$KUBE_CONFIG"

KUBECONFIG="$KUBE_CONFIG" kubectl get nodes
```

If this fails, instruct the user to run `aws sso login --profile default` or provide an access key.

### Case 2: User provides Access Key + Secret Key (no role)

Create a session-scoped AWS profile and use the default admin role.

```bash
# 1. Create AWS profile
aws configure set aws_access_key_id "$USER_ACCESS_KEY" --profile "$AWS_PROFILE_NAME"
aws configure set aws_secret_access_key "$USER_SECRET_KEY" --profile "$AWS_PROFILE_NAME"
aws configure set region <AWS_REGION> --profile "$AWS_PROFILE_NAME"

# 2. Generate kubeconfig with admin role
aws eks update-kubeconfig \
  --name <CLUSTER_NAME> \
  --region <AWS_REGION> \
  --profile "$AWS_PROFILE_NAME" \
  --role-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ADMIN_ROLE_NAME> \
  --kubeconfig "$KUBE_CONFIG"

# 3. Verify
KUBECONFIG="$KUBE_CONFIG" kubectl get nodes
```

If AssumeRole fails, fall back to the read role:

```bash
aws eks update-kubeconfig \
  --name <CLUSTER_NAME> \
  --region <AWS_REGION> \
  --profile "$AWS_PROFILE_NAME" \
  --role-arn arn:aws:iam::<AWS_ACCOUNT_ID>:role/<READ_ROLE_NAME> \
  --kubeconfig "$KUBE_CONFIG"
```

### Case 3: User provides Access Key + Secret Key + custom Role ARN

Create a session-scoped AWS profile and use the role the user specified.

```bash
# 1. Create AWS profile
aws configure set aws_access_key_id "$USER_ACCESS_KEY" --profile "$AWS_PROFILE_NAME"
aws configure set aws_secret_access_key "$USER_SECRET_KEY" --profile "$AWS_PROFILE_NAME"
aws configure set region <AWS_REGION> --profile "$AWS_PROFILE_NAME"

# 2. Generate kubeconfig with user-provided role
aws eks update-kubeconfig \
  --name <CLUSTER_NAME> \
  --region <AWS_REGION> \
  --profile "$AWS_PROFILE_NAME" \
  --role-arn "$USER_PROVIDED_ROLE_ARN" \
  --kubeconfig "$KUBE_CONFIG"

# 3. Verify
KUBECONFIG="$KUBE_CONFIG" kubectl get nodes
```

---

## Using kubectl After Setup

Staging → use `--context` directly:
```bash
kubectl --context your-cluster-dev get pods -n <NAMESPACE>
```

Production → MUST use `KUBECONFIG` env var:
```bash
KUBECONFIG="$KUBE_CONFIG" kubectl get pods -n <NAMESPACE>
KUBECONFIG="$KUBE_CONFIG" kubectl get deployments -n <NAMESPACE>
KUBECONFIG="$KUBE_CONFIG" kubectl logs deployment/<DEPLOYMENT> -n <NAMESPACE>
```

---

## Handling Expired Credentials

Detect these error patterns:
- "error: You must be logged in to the server"
- "The SSO session has expired"
- "could not get token: AccessDeniedException"
- "ExpiredTokenException"
- "InvalidClientTokenId"

When any of these occur — do NOT auto-retry — notify the user immediately:
1. Report that credentials have expired
2. Ask for new credentials or instruct them to run `aws sso login`
3. If new credentials are provided, delete the old profile and start fresh

---

## Role ARN Reference

| Scenario | Role ARN |
|----------|----------|
| Default (no key provided) | `arn:aws:iam::<AWS_ACCOUNT_ID>:role/<READ_ROLE_NAME>` |
| User provides key (default) | `arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ADMIN_ROLE_NAME>` |
| User provides key + role | Role provided by user |

---

## Rules

MUST:
1. Staging → use `--context your-cluster-dev` directly
2. Production → each session = 1 KUBECONFIG at `/tmp/{username}-{sessionId}`
3. Production → each session = 1 AWS profile `k8s-{username}-{sessionId}` (if custom keys)
4. Verify with `kubectl get nodes` after production setup
5. Notify user immediately when credentials expire

MUST NOT:
1. Overwrite `~/.kube/config`
2. Reuse profiles/kubeconfigs from other sessions
3. Auto-retry on expired credentials
4. Store credentials outside `/tmp/` or `~/.aws/credentials`

## Cleanup

```bash
rm -f "$KUBE_CONFIG"
sed -i '' "/\[${AWS_PROFILE_NAME}\]/,/^$/d" ~/.aws/credentials
```

## Output Formatting

- Terminal/kubectl output → wrap in code block (triple backticks)
- Keep output concise and readable

## Related Skills

- `/kubectl` - Kubectl operations, pod management, GitOps
- `/aws` - AWS CLI, SSO authentication
