---
name: infisical
description: This skill should be used when the user asks to "get Infisical secrets", "inject env vars", "export secrets", "infisical run", "missing secret", "check secret path", or mentions Infisical secret management, path inheritance, or serverless secret injection.
---

## Related Skills

- **deploy-sls** - Uses infisical for Lambda secrets injection
- **secret** - Static credentials in secret/ directory
- **codebase** - Project path mapping

# Infisical Secrets Management

Quản lý và inject secrets từ Infisical vào môi trường development/deployment.

## Khi nào dùng

- Cần lấy secrets cho serverless functions
- Cần biết Infisical path tương ứng với project
- Setup environment variables từ Infisical
- Debug missing secrets

## Workspace Info

| Property         | Value                        |
| ---------------- | ---------------------------- |
| **Project ID**   | `<INFISICAL_PROJECT_ID>`     |
| **Project Name** | Your project name            |

## Path Convention

Infisical path tương ứng với folder structure trong codebase:

```
/                           # Root - shared secrets (DB connections, API keys)
├── /your-service           # Shared cho tất cả functions trong service
│   ├── /sub-module-a
│   │   ├── /function-a     # Specific function secrets
│   │   └── /function-b
│   └── /sub-module-b
└── /web-app                # Frontend
```

**Pattern:** Lấy relative path từ project root và prefix với `/`

| Project location            | Infisical path                  |
| --------------------------- | ------------------------------- |
| `your-service/sub-module-a` | `/your-service/sub-module-a`    |
| `your-service/sub-module-b` | `/your-service/sub-module-b`    |
| `web-app/`                  | `/web-app`                      |

## Inheritance Model

Secrets được kế thừa từ parent paths:

```
/ (root)
  └── /your-service
        └── /sub-module
              └── /function (final path)
```

Khi lấy secrets cho `/your-service/sub-module/function`:

- Secrets từ `/` được include
- Secrets từ `/your-service` override nếu trùng key
- Secrets từ `/your-service/sub-module` override tiếp
- Secrets từ `/your-service/sub-module/function` là final

## Export Secrets

### Dùng `infisical_export` (Recommended)

Fish function `infisical_export.fish` (bundled trong skill này) tự động xử lý **path inheritance** - tự split path thành hierarchy và fetch từ root `/` xuống target path, merge và override theo thứ tự parent → child. Không cần xử lý inheritance thủ công.

```bash
fish -c 'infisical_export --projectId <INFISICAL_PROJECT_ID> --env review --path "/your-app/prod" --out /tmp/env.sh'
```

Sau đó source file:

```bash
source /tmp/env.sh
# hoặc trong bash script:
bash -c 'source /tmp/env.sh && <command>'
```

Options:
- `--projectId` - Infisical project ID (required)
- `--env` - Environment name (required)
- `--path` - Target path, script auto-inherits from all parent paths (required)
- `--out` - Output file (optional, prints to stdout if omitted)
- `--debug` - Show which paths are fetched and which keys are added/overridden

### Dùng `infisical run` (Simple)

Chạy command với secrets injected trực tiếp:

```bash
infisical run --env review --path "/your-app/prod" -- <command>
```

**Lưu ý:** `infisical run` KHÔNG tự động inherit từ parent paths.

### Options quan trọng

| Option              | Meaning                                              |
| ------------------- | ---------------------------------------------------- |
| `--recursive`       | Lấy từ path hiện tại VÀ **sub-folders** (children)   |
| `--include-imports` | Include secrets được import/reference từ folder khác |

**Chú ý:** `--recursive` lấy children, KHÔNG phải parents. Dùng `infisical_export` nếu cần inheritance.

## Environments

| Infisical env | Stage     | Domain                          | Notes          |
| ------------- | --------- | ------------------------------- | -------------- |
| `review`      | `review`  | `*.api.dev.your-domain.com`     | Development    |
| `staging`     | `staging` | `*.api.staging.your-domain.com` | Pre-production |
| `prod`        | `prod`    | `*.api.your-domain.com`         | Production     |

**Lưu ý:** Infisical env slug là `prod` (không phải `production`).

## `.infisical.json` Configuration

Mỗi project nên có file `.infisical.json` để config Infisical integration:

```json
{
  "workspaceId": "<INFISICAL_PROJECT_ID>",
  "defaultEnvironment": "review",
  "gitBranchToEnvironmentMapping": {
    "master": "prod"
  }
}
```

| Field                           | Purpose                                   |
| ------------------------------- | ----------------------------------------- |
| `workspaceId`                   | Infisical project ID                      |
| `defaultEnvironment`            | Fallback env khi không match git branch   |
| `gitBranchToEnvironmentMapping` | Map git branches → Infisical environments |

### Branch Mapping

Với config trên:

- Branch `master` → env `prod`
- Tất cả branches khác → env `review` (defaultEnvironment)

Có thể thêm nhiều mappings:

```json
{
  "gitBranchToEnvironmentMapping": {
    "master": "prod",
    "staging": "staging",
    "develop": "review"
  }
}
```

## Common Secret Keys

### Observability (OTEL)

| Key                           | Purpose                | Example                         |
| ----------------------------- | ---------------------- | ------------------------------- |
| `OTEL_SDK_DISABLED`           | Enable/disable tracing | `false`                         |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Collector URL          | `https://otel.example.com:4317` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | Protocol               | `grpc`                          |
| `OTEL_SERVICE_NAME`           | Service identifier     | `facebook-review`               |

### AWS

| Key          | Purpose          |
| ------------ | ---------------- |
| `AWS_REGION` | AWS region       |
| `STAGE`      | Deployment stage |

### Database

| Key                | Purpose                   |
| ------------------ | ------------------------- |
| `MONGODB_URI`      | MongoDB connection string |
| `MONGODB_DATABASE` | Database name             |

## CLI Commands

```bash
# List folders tại path
infisical secrets folders get --env review --path "/your-app"

# List secrets tại path (không show values)
infisical secrets --env review --path "/your-app/prod"

# Get specific secret
infisical secrets get MONGODB_URI --env review --path "/your-app"
```

## Troubleshooting

### "Missing env variable"

1. Kiểm tra `infisical_export` đã chạy và output file tồn tại
2. Secret có thể ở parent path - dùng `infisical_export` để inherit
3. Secret có thể được reference từ folder khác (vd: `/apm`) - check `--include-imports`

### "Not logged in"

```bash
infisical login
```

### "Project not found"

- Verify project ID: `<INFISICAL_PROJECT_ID>`
- Check bạn có access vào project
