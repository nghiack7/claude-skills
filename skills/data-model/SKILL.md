---
name: data-model
description: This skill should be used when the user asks to "create data model", "write data model doc", "tạo data model", "viết tài liệu data model", "document database schema", or needs a data model template for engineering documentation.
---

# Data Model: [Model Name]

> **Purpose:** Define the structure, relationships, and constraints for [domain entity] data.

---

## Model Overview

**Model ID:** `DM-XXX`
**Model Name:** [Entity Name]
**Domain:** [Business domain - e.g., Orders, Users, Payments]
**Version:** 1.0.0
**Status:** Draft | Review | Approved | Production | Deprecated

### Description

[2-3 paragraphs describing what this entity represents, its business purpose, and how it fits into the overall data architecture]

### Key Characteristics

- **Primary Entity:** [Main entity name]
- **Aggregate Root:** Yes | No
- **Mutable:** Yes | No (can records be updated?)
- **Soft Delete:** Yes | No
- **Audit Trail:** Yes | No

---

## Entity Relationship Diagram (ERD)

### High-Level Relationships

```
+─────────────────+
│     Customer    │
│  - id           │
│  - email        │
│  - name         │
+────────┬────────+
         │ 1:N
         │
+────────▼────────+       +─────────────────+
│     Order       │       │   OrderItem     │
│  - id           │   N:M │  - id           │
│  - customer_id  ├───────┤  - order_id     │
│  - total        │       │  - product_id   │
│  - status       │       │  - quantity     │
+─────────────────+       +────────┬────────+
                                   │ N:1
                          +────────▼────────+
                          │    Product      │
                          │  - id           │
                          │  - name         │
                          │  - price        │
                          +─────────────────+
```

### Relationship Summary

| Relationship | Type | Description |
|--------------|------|-------------|
| Customer → Order | One-to-Many | A customer can have multiple orders |
| Order → OrderItem | One-to-Many | An order contains multiple line items |
| Product → OrderItem | One-to-Many | A product can appear in many order items |

---

## Entity: [Primary Entity Name]

### Table Schema

**Table Name:** `orders`
**Database:** PostgreSQL | MySQL | MongoDB | etc.
**Schema:** `public` (if applicable)
**Partitioning:** By date (monthly) | By range | None

### Columns

| Column | Type | Constraints | Default | Description |
|--------|------|-------------|---------|-------------|
| id | UUID | PRIMARY KEY | gen_random_uuid() | Unique identifier |
| customer_id | UUID | FOREIGN KEY, NOT NULL, INDEX | - | Reference to customer |
| order_number | VARCHAR(50) | UNIQUE, NOT NULL | - | Human-readable order number |
| status | ENUM | NOT NULL | 'pending' | Status (pending, confirmed, shipped, delivered, cancelled) |
| subtotal_cents | INTEGER | NOT NULL, CHECK > 0 | - | Subtotal in cents |
| tax_cents | INTEGER | NOT NULL | 0 | Tax amount in cents |
| shipping_cents | INTEGER | NOT NULL | 0 | Shipping cost in cents |
| total_cents | INTEGER | NOT NULL, GENERATED | - | Calculated: subtotal + tax + shipping |
| currency | VARCHAR(3) | NOT NULL | 'USD' | ISO 4217 currency code |
| notes | TEXT | NULLABLE | - | Optional notes |
| created_at | TIMESTAMP | NOT NULL, INDEX | NOW() | Record creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | NOW() | Last update timestamp |
| deleted_at | TIMESTAMP | NULLABLE, INDEX | NULL | Soft delete timestamp |

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| idx_orders_customer_id | customer_id | B-Tree | Query orders by customer |
| idx_orders_status | status | B-Tree | Filter by status |
| idx_orders_created_at | created_at | B-Tree | Date range queries |
| idx_orders_deleted_at | deleted_at | B-Tree | Soft delete queries |

### Constraints

**Primary Key:**
```sql
CONSTRAINT pk_orders PRIMARY KEY (id)
```

**Foreign Keys:**
```sql
CONSTRAINT fk_orders_customer
  FOREIGN KEY (customer_id)
  REFERENCES customers(id)
  ON DELETE RESTRICT
  ON UPDATE CASCADE
```

**Check Constraints:**
```sql
CONSTRAINT chk_orders_subtotal_positive
  CHECK (subtotal_cents > 0)

CONSTRAINT chk_orders_status_valid
  CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled'))
```

---

## Data Types & Enums

### Enum: [StatusName]

**Type:** String Enum
**Values:**
- `pending` - [Description]
- `confirmed` - [Description]
- `shipped` - [Description]
- `delivered` - [Description]
- `cancelled` - [Description]

**State Transitions:**
```
pending → confirmed → shipped → delivered
   ↓
cancelled
```

---

## SQL Schema Definition

### DDL (PostgreSQL)

```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL,
  order_number VARCHAR(50) UNIQUE NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  subtotal_cents INTEGER NOT NULL CHECK (subtotal_cents > 0),
  tax_cents INTEGER NOT NULL DEFAULT 0,
  shipping_cents INTEGER NOT NULL DEFAULT 0,
  total_cents INTEGER GENERATED ALWAYS AS (subtotal_cents + tax_cents + shipping_cents) STORED,
  currency VARCHAR(3) NOT NULL DEFAULT 'USD',
  notes TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMP,

  CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id)
    REFERENCES customers(id) ON DELETE RESTRICT ON UPDATE CASCADE,

  CONSTRAINT chk_orders_status_valid
    CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled'))
);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_deleted_at ON orders(deleted_at) WHERE deleted_at IS NOT NULL;
```

---

## Object Model (Code)

### TypeScript Interface

```typescript
interface Order {
  id: string;  // UUID
  customerId: string;  // UUID
  orderNumber: string;
  status: OrderStatus;
  subtotalCents: number;
  taxCents: number;
  shippingCents: number;
  totalCents: number;  // Calculated
  currency: string;  // ISO 4217 code
  notes?: string;
  createdAt: Date;
  updatedAt: Date;
  deletedAt?: Date;
}

enum OrderStatus {
  Pending = 'pending',
  Confirmed = 'confirmed',
  Shipped = 'shipped',
  Delivered = 'delivered',
  Cancelled = 'cancelled',
}
```

---

## Business Rules

### Rule 1: [Rule Name]

**Rule:** [Description]
**Enforcement:** [Database generated column or application logic]
**Validation:** [How to validate]

### Rule 2: Soft Delete

**Rule:** Records are never hard deleted
**Implementation:** Set `deleted_at` timestamp
**Queries:** Always filter `WHERE deleted_at IS NULL`

### Rule 3: Status Transitions

**Allowed Transitions:**
- pending → confirmed
- confirmed → shipped
- shipped → delivered
- Any → cancelled
- delivered → pending (Invalid)

---

## Data Migration

### Initial Migration (v1.0.0)

**Migration File:** `YYYY-MM-DD-create-table.sql`

```sql
-- Up migration
CREATE TABLE ... (
  -- schema
);

-- Down migration
DROP TABLE IF EXISTS ... CASCADE;
```

---

## Data Access Patterns

### Common Queries

#### Query 1: Get by Customer

```sql
SELECT
  o.id,
  o.order_number,
  o.status,
  o.total_cents,
  o.created_at
FROM orders o
WHERE o.customer_id = :customer_id
  AND o.deleted_at IS NULL
ORDER BY o.created_at DESC
LIMIT 20;
```

**Index Used:** `idx_orders_customer_id`

---

## Data Integrity & Validation

### Application-Level Validation

```typescript
function validateOrder(order: Partial<Order>): ValidationResult {
  const errors: string[] = [];

  if (!order.customerId) {
    errors.push('Customer ID is required');
  }

  if (order.subtotalCents <= 0) {
    errors.push('Subtotal must be positive');
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
```

---

## Security & Privacy

### Data Classification

| Column | Classification | Encryption | Masking | Retention |
|--------|----------------|------------|---------|-----------|
| id | Public | No | No | Permanent |
| customer_id | Confidential | No | Yes (in logs) | Permanent |
| notes | Confidential | No | Yes | 7 years |

### Access Control

**Read Access:**
- Customer: Own records only
- Support: All records
- Admin: All records

**Write Access:**
- System: Create, update
- Admin: Full access

---

## Performance Considerations

### Caching Strategy

**Cache Layer:** Redis
**Cache Key:** `order:{order_id}`
**TTL:** 5 minutes
**Invalidation:** On update/delete

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial data model |

---

## References

- **API Specification:** [Link to API docs]
- **ERD Diagram:** [Link to visual diagram]
- **Migration Scripts:** [Link to migration folder]

---

## Notes

- All monetary values stored in cents to avoid floating-point precision issues
- Soft delete used to maintain referential integrity and audit trail
