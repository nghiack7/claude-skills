---
name: api-spec
description: This skill should be used when the user asks to "create API spec", "write API specification", "tạo API spec", "viết tài liệu API", "document API", or needs an API specification template for engineering documentation.
---

# API Specification: [API Name]

## 1. Overview

**API Name:** [Name]

**Version:** v1

**Base URL:** `https://api.example.com/v1`

**Owner:** [API Lead Name]

**Status:** Draft | In Review | Published | Deprecated

**Last Updated:** [Date]

**Description:**
[2-3 sentences describing the API's purpose and main functionality]

---

## 2. Authentication

### 2.1 Authentication Method

**Type:** API Key | OAuth 2.0 | JWT | Basic Auth

**How to Authenticate:**

**API Key:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.example.com/v1/resource
```

**OAuth 2.0:**
```bash
# Get access token
curl -X POST https://api.example.com/oauth/token \
  -d "grant_type=client_credentials" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"

# Use token
curl -H "Authorization: Bearer ACCESS_TOKEN" \
  https://api.example.com/v1/resource
```

### 2.2 Scopes & Permissions

| Scope | Description | Access Level |
|-------|-------------|--------------|
| `read:resources` | Read access to resources | Read-only |
| `write:resources` | Create/update resources | Read/Write |
| `delete:resources` | Delete resources | Full |
| `admin` | Full administrative access | Admin |

---

## 3. Rate Limiting

### 3.1 Rate Limit Rules

| Tier | Requests/Minute | Requests/Hour | Requests/Day |
|------|----------------|---------------|--------------|
| Free | 60 | 1,000 | 10,000 |
| Standard | 300 | 10,000 | 100,000 |
| Premium | 1,000 | 50,000 | 1,000,000 |

### 3.2 Rate Limit Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1445929100
```

### 3.3 Rate Limit Exceeded Response

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds.",
    "retry_after": 60
  }
}
```

---

## 4. Request Format

### 4.1 Headers

**Required Headers:**
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Accept: application/json
```

**Optional Headers:**
```
X-Request-ID: unique-request-id
X-Idempotency-Key: unique-key-for-idempotent-requests
```

---

## 5. Response Format

### 5.1 Success Response

**Status Codes:**
- `200 OK` - Request succeeded
- `201 Created` - Resource created
- `204 No Content` - Success with no response body

**Response Structure:**
```json
{
  "data": {
    "id": "resource-123",
    "type": "resource",
    "attributes": {
      "field1": "value",
      "field2": 123
    },
    "created_at": "2025-10-18T10:00:00Z",
    "updated_at": "2025-10-18T10:00:00Z"
  },
  "meta": {
    "request_id": "req-abc-123"
  }
}
```

### 5.2 Error Response

**Status Codes:**
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

**Error Structure:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Email is required"
      }
    ]
  },
  "meta": {
    "request_id": "req-abc-123"
  }
}
```

### 5.3 Pagination

**Request:**
```
GET /api/v1/resources?page=2&per_page=50
```

**Response:**
```json
{
  "data": [],
  "pagination": {
    "page": 2,
    "per_page": 50,
    "total_pages": 10,
    "total_items": 500,
    "has_next": true,
    "has_prev": true
  }
}
```

---

## 6. API Endpoints

### 6.1 Resources

#### Create Resource

**Endpoint:** `POST /api/v1/resources`

**Description:** Creates a new resource

**Request:**
```json
{
  "name": "Resource Name",
  "description": "Description",
  "status": "active"
}
```

**Response (201 Created):**
```json
{
  "data": {
    "id": "res-123",
    "name": "Resource Name",
    "description": "Description",
    "status": "active",
    "created_at": "2025-10-18T10:00:00Z"
  }
}
```

---

#### List Resources

**Endpoint:** `GET /api/v1/resources`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number (default: 1) |
| `per_page` | integer | No | Items per page (default: 20, max: 100) |
| `status` | string | No | Filter by status |

---

#### Get Resource

**Endpoint:** `GET /api/v1/resources/:id`

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Resource ID |

---

#### Update Resource

**Endpoint:** `PATCH /api/v1/resources/:id`

**Request:**
```json
{
  "name": "Updated Name",
  "status": "inactive"
}
```

---

#### Delete Resource

**Endpoint:** `DELETE /api/v1/resources/:id`

**Response (204 No Content)**

---

## 7. Webhooks

### 7.1 Webhook Events

| Event | Description | Payload |
|-------|-------------|---------|
| `resource.created` | Resource was created | Resource object |
| `resource.updated` | Resource was updated | Resource object |
| `resource.deleted` | Resource was deleted | Resource ID |

### 7.2 Webhook Payload

```json
{
  "event": "resource.created",
  "timestamp": "2025-10-18T10:00:00Z",
  "data": {
    "id": "res-123",
    "name": "Resource Name"
  }
}
```

### 7.3 Webhook Signature

Each webhook includes a signature header for verification:

```
X-Webhook-Signature: sha256=abc123...
```

---

## 8. Data Types

### 8.1 Common Types

**Resource:**
```typescript
interface Resource {
  id: string;                  // Unique identifier
  name: string;                // Resource name
  description?: string;        // Optional description
  status: 'active' | 'inactive' | 'archived';
  metadata?: Record<string, any>;
  created_at: string;          // ISO 8601 timestamp
  updated_at: string;          // ISO 8601 timestamp
}
```

---

## 9. Examples

### 9.1 Complete Workflow Example

**Step 1: Create a resource**
```bash
curl -X POST https://api.example.com/v1/resources \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Resource",
    "status": "active"
  }'
```

**Step 2: Retrieve the resource**
```bash
curl https://api.example.com/v1/resources/res-123 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 10. Versioning

### 10.1 API Versions

- **Current Version:** v1
- **Supported Versions:** v1
- **Deprecated Versions:** None

### 10.2 Version Deprecation Policy

- Deprecated versions supported for 12 months
- 6 months notice before deprecation
- Migration guide provided

---

## 11. Full Error Code Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Malformed request |
| `AUTHENTICATION_FAILED` | 401 | Invalid credentials |
| `INSUFFICIENT_PERMISSIONS` | 403 | Missing required permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource already exists |
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily down |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial API specification |
