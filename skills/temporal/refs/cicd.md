# CI/CD Patterns for Temporal Workers

## Dockerfile Pattern

```dockerfile
# Build stage
FROM golang:1.23-alpine AS builder
WORKDIR /app
RUN apk add --no-cache git ca-certificates
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /worker ./cmd/worker
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /starter ./cmd/starter

# Runtime stage
FROM alpine:3.19
RUN apk add --no-cache ca-certificates tzdata
WORKDIR /app
COPY --from=builder /worker /app/worker
COPY --from=builder /starter /app/starter
ENTRYPOINT ["/app/worker"]
```

## GitLab CI

```yaml
stages:
  - build

.docker:
  image:
    name: <YOUR_CI_IMAGE>
    entrypoint: [""]
  before_script:
    - |
      unset DOCKER_HOST
      REGISTRY_DOMAIN="<YOUR_REGISTRY>"
      docker login $REGISTRY_DOMAIN -u $REGISTRY_USER -p $REGISTRY_TOKEN

build:worker:
  stage: build
  extends: .docker
  tags:
    - develop
  script:
    - cd my-worker
    - export IMAGE_TAG="develop-${CI_COMMIT_SHORT_SHA}-$(date +%s)"
    - export IMAGE="<YOUR_REGISTRY>/your-path/my-worker:$IMAGE_TAG"
    - docker build -t $IMAGE .
    - docker push $IMAGE
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      changes:
        - my-worker/**/*
```

## Flux Image Automation

```yaml
# image-updater.yaml
---
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: my-worker
  namespace: flux-system
spec:
  interval: 1m0s
  image: <YOUR_REGISTRY>/your-path/my-worker
  secretRef:
    name: registry-pull-secret
---
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: my-worker
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: my-worker
  filterTags:
    pattern: '^develop-[a-fA-F0-9]+-(?P<ts>\d+)'
    extract: "$ts"
  policy:
    numerical:
      order: asc
```

## K8s Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-worker
  namespace: temporal
  labels:
    app: my-worker
    component: temporal-worker
  annotations:
    wave.pusher.com/update-on-config-change: "true"
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-worker
  template:
    metadata:
      labels:
        app: my-worker
        component: temporal-worker
    spec:
      nodeSelector:
        node_role: systemnodes
      tolerations:
        - key: systemnodes
          operator: Equal
          value: "true"
          effect: NoSchedule
      containers:
        - name: worker
          image: <YOUR_REGISTRY>/your-path/my-worker:latest # {"$imagepolicy": "flux-system:my-worker"}
          imagePullPolicy: IfNotPresent
          envFrom:
            - configMapRef:
                name: my-worker-config
            - secretRef:
                name: my-worker-secret
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
      restartPolicy: Always
      imagePullSecrets:
        - name: registry-pull-secret
```

## ConfigMap Template

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-worker-config
  namespace: temporal
data:
  ENV: "production"
  TEMPORAL_HOST: "temporal-frontend.temporal.svc.cluster.local:7233"
  STARROCKS_HOST: "<STARROCKS_HOST>"
  STARROCKS_PORT: "9030"
  STARROCKS_USER: "root"
  STARROCKS_DATABASE: "my_database"
```

## Secret Template

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-worker-secret
  namespace: temporal
type: Opaque
stringData:
  API_TOKEN: "your-token-here"
  STARROCKS_PASSWORD: ""
```
