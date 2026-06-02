---
name: use-case
description: 'This skill should be used when the user asks to "tạo use case", "viết use case", "user scenario", or needs a use case template for product documentation.'
---

## Document Metadata

```yaml
document_type: "use_case"
use_case_id: "UC-XXX"
version: "1.0.0"
status: "draft"
owner: "Product Manager Name"
priority: "high"
complexity: "medium"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["use-case", "requirements"]

# Relationships
relationships:
  derived_from:
    - path: "product-knowledge/02-requirements/prd/YYYY-MM-DD-prd-NNN-feature.md"
      title: "Parent PRD"
      reason: "Defines feature context"
  blocks:
    - path: "product-knowledge/02-requirements/user-stories/YYYY-MM-DD-us-NNN-story.md"
      title: "Related User Stories"
      reason: "Implements this use case"
```

# Use Case: [Use Case Name]

> **Purpose:** Describe a specific interaction between a user (actor) and the system to achieve a particular goal.

---

## Use Case Overview

**Use Case ID:** `UC-XXX`
**Use Case Name:** [Clear, action-oriented name]
**Version:** 1.0.0
**Last Updated:** YYYY-MM-DD

**Brief Description:**
> [One paragraph summary of what this use case accomplishes and why it matters to the business/user]

---

## Actors

### Primary Actor(s)

**Actor:** [User Type]
- **Role:** [Their role in the system]
- **Goal:** [What they want to achieve]
- **Characteristics:** [Relevant skills, permissions, context]

**Example:**
- **Actor:** Customer
- **Role:** End user making purchases
- **Goal:** Complete a product purchase
- **Characteristics:** Authenticated user with valid payment method

### Secondary Actor(s)

**Actor:** [Supporting System/Person]
- **Role:** [Their supporting role]
- **Interaction:** [How they participate]

**Example:**
- **Actor:** Payment Gateway (Stripe)
- **Role:** External payment processor
- **Interaction:** Validates and processes payment transactions

---

## Preconditions

Conditions that must be true before this use case can begin:

1. [Precondition 1 - System state]
2. [Precondition 2 - User state]
3. [Precondition 3 - Data availability]

**Example:**
1. User must be logged into their account
2. User must have at least one item in their shopping cart
3. Product inventory must be available for selected items

---

## Postconditions

### Success Postconditions

State of the system after successful completion:

1. [Postcondition 1 - Data changes]
2. [Postcondition 2 - System state]
3. [Postcondition 3 - User state]

**Example:**
1. Order record created in database with status "Pending Payment"
2. Inventory decremented for purchased items
3. User receives order confirmation email

### Failure Postconditions

State of the system if use case fails:

1. [Postcondition 1 - Rollback state]
2. [Postcondition 2 - Error logged]
3. [Postcondition 3 - User notified]

---

## Main Success Scenario (Happy Path)

Step-by-step description of the standard, successful interaction:

1. **User:** [Action taken by user]
2. **System:** [System response]
3. **User:** [Next user action]
4. **System:** [System response]
5. **System:** [Automated action]
6. **User:** [Final user action]
7. **System:** [Final system response and confirmation]

**Example:**
1. **Customer:** Clicks "Proceed to Checkout" button
2. **System:** Displays checkout page with order summary and shipping options
3. **Customer:** Selects shipping method and enters delivery address
4. **System:** Validates address format and calculates shipping cost
5. **Customer:** Enters payment information (credit card details)
6. **System:** Validates payment info format and displays order total
7. **Customer:** Clicks "Place Order" button
8. **System:** Processes payment via payment gateway
9. **System:** Creates order record and sends confirmation email
10. **System:** Displays "Order Confirmed" page with order number

---

## Alternative Flows

### Alternative Flow 1: [Scenario Name]

**Trigger:** [When this alternative occurs]

**Steps:**
- 1a. [Deviation from main flow]
- 1b. [System response]
- 1c. [Return to main flow at step X or end]

**Example: Guest Checkout**

**Trigger:** User is not logged in

**Steps:**
- 1a. System displays option for "Guest Checkout" or "Login"
- 1b. Customer clicks "Guest Checkout"
- 1c. System requests email address for order confirmation
- 1d. Customer enters email and continues
- 1e. Resume main flow at step 3

### Alternative Flow 2: [Scenario Name]

**Trigger:** [When this alternative occurs]

**Steps:**
- [Alternative steps]

---

## Exception Flows

### Exception 1: [Error Scenario]

**Trigger:** [What causes this exception]

**Steps:**
1. [Detection step]
2. [System error handling]
3. [User notification]
4. [Recovery action]

**Example: Payment Declined**

**Trigger:** Payment gateway returns "Declined" status

**Steps:**
1. System receives payment decline notification from gateway
2. System logs error with transaction ID and reason code
3. System displays error message: "Payment declined. Please verify your payment method."
4. System returns user to payment entry screen
5. Customer can update payment method or cancel order

### Exception 2: [Error Scenario]

**Trigger:** [What causes this exception]

**Steps:**
- [Exception handling steps]

---

## Business Rules

Rules that govern this use case:

1. **BR-1:** [Business rule name]
   - **Rule:** [Statement of the rule]
   - **Rationale:** [Why this rule exists]

2. **BR-2:** [Business rule name]
   - **Rule:** [Statement of the rule]
   - **Rationale:** [Why this rule exists]

**Example:**
1. **BR-1:** Minimum Order Value
   - **Rule:** Orders must have a minimum subtotal of $10 USD
   - **Rationale:** Shipping costs make smaller orders unprofitable

2. **BR-2:** Inventory Reservation
   - **Rule:** Items are reserved for 15 minutes during checkout
   - **Rationale:** Prevents overselling while giving customers time to complete purchase

---

## Special Requirements

### Non-Functional Requirements

#### Performance
- Response time: [X] seconds for [action]
- Throughput: Support [X] concurrent users
- Availability: [X]% uptime SLA

#### Security
- Authentication: [Requirements]
- Authorization: [Role-based access]
- Data encryption: [In transit/at rest]

#### Usability
- Accessibility: WCAG 2.1 AA compliance
- Mobile responsive: Support screens 320px - 4K
- Localization: Support [languages]

#### Compliance
- PCI DSS compliance for payment data
- GDPR compliance for user data
- [Industry-specific regulations]

---

## Assumptions

1. [Assumption about system capabilities]
2. [Assumption about user behavior]
3. [Assumption about external dependencies]

**Example:**
1. Payment gateway API is available 99.9% of the time
2. Users have modern browsers with JavaScript enabled
3. Email delivery service can handle 10,000 emails/hour

---

## Dependencies

### Internal Dependencies

- **Feature:** [Dependent feature]
  - **Status:** [In Development/Complete]
  - **Impact:** [How it affects this use case]

### External Dependencies

- **System:** [External system]
  - **Integration:** [API/Service]
  - **SLA:** [Service level agreement]

**Example:**
- **System:** Stripe Payment Gateway
  - **Integration:** REST API v1
  - **SLA:** 99.99% uptime

---

## Frequency of Use

- **Expected Frequency:** [X times per day/week/month]
- **Peak Usage:** [Time periods or conditions]
- **User Volume:** [Number of users expected to use this]

**Example:**
- **Expected Frequency:** 500 checkouts per day
- **Peak Usage:** 2x normal during holiday season (Nov-Dec)
- **User Volume:** 80% of active customers use this monthly

---

## User Interface Mockups

### Screen 1: [Screen Name]

**Description:** [What this screen shows]

**Visual Reference:** [Link to Figma/wireframe]

![Screenshot or mockup](path/to/image.png)

**Key Elements:**
- Element 1: [Description]
- Element 2: [Description]

### Screen 2: [Screen Name]

[Additional screens as needed]

---

## Data Requirements

### Input Data

| Field | Type | Required | Validation | Source |
|-------|------|----------|------------|--------|
| Email | String | Yes | Valid email format | User input |
| Address | Object | Yes | Valid address components | User input/API |
| Payment Method | String | Yes | Credit card or PayPal | User selection |

### Output Data

| Field | Type | Description | Destination |
|-------|------|-------------|-------------|
| Order ID | UUID | Unique order identifier | Database, Email |
| Confirmation Number | String | User-friendly order reference | Email, UI |
| Total Amount | Decimal | Final order total with tax | Database, Receipt |

---

## Integration Points

### API Endpoints

**Endpoint 1: Create Order**
- **Method:** POST
- **Path:** `/api/v1/orders`
- **Payload:** Order details JSON
- **Response:** Order confirmation with ID

**Endpoint 2: Process Payment**
- **Method:** POST
- **Path:** `/api/v1/payments`
- **Payload:** Payment details
- **Response:** Payment status

---

## Test Scenarios

### Scenario 1: Happy Path Test

**Given:** [Initial state]
**When:** [Actions taken]
**Then:** [Expected outcome]

### Scenario 2: Error Condition Test

**Given:** [Error condition setup]
**When:** [Actions taken]
**Then:** [Expected error handling]

---

## Open Issues

| ID | Issue Description | Priority | Owner | Status |
|----|-------------------|----------|-------|--------|
| 1 | [Unresolved question or decision] | High/Med/Low | [Name] | Open/Resolved |
| 2 | [Technical uncertainty] | High/Med/Low | [Name] | Open/Resolved |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial creation |
| 1.1.0 | YYYY-MM-DD | [Name] | Added alternative flow for guest checkout |

---

## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Owner | [Name] | YYYY-MM-DD | ✅ Approved |
| Business Analyst | [Name] | YYYY-MM-DD | ✅ Approved |
| Tech Lead | [Name] | YYYY-MM-DD | ✅ Approved |

---

## Notes

- [Additional context]
- [Future enhancements to consider]
- [Related documentation links]
