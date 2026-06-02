---
name: acceptance-criteria
description: 'This skill should be used when the user asks to "tạo acceptance criteria", "viết tiêu chí chấp nhận", "define acceptance criteria", or needs acceptance criteria for product documentation.'
---

## Document Metadata

```yaml
document_type: "acceptance_criteria"
feature_id: "FEAT-XXX"
user_story_id: "US-XXX"
version: "1.0.0"
status: "draft"
owner: "Product Manager Name"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["acceptance-criteria", "testing"]

# Relationships
relationships:
  derived_from:
    - path: "product-knowledge/02-requirements/prd/YYYY-MM-DD-prd-NNN-feature.md"
      title: "Parent PRD"
      reason: "Defines feature requirements"
  blocks:
    - path: "product-knowledge/02-requirements/user-stories/YYYY-MM-DD-us-NNN-story.md"
      title: "User Story"
      reason: "Acceptance criteria for this story"
```

# Acceptance Criteria: [Feature/Story Name]

> **Purpose:** Define testable, unambiguous conditions that must be met for a feature or user story to be considered complete.

---

## Overview

**Related User Story:**
> As a [user type], I want [goal], so that [benefit].

**Feature ID:** `FEAT-XXX`
**Story ID:** `US-XXX`

---

## Acceptance Criteria

### Given-When-Then Format

Use Gherkin-style scenarios for behavioral specifications:

#### Scenario 1: [Primary Happy Path]

```gherkin
Given [initial context/preconditions]
  And [additional context]
When [action/event occurs]
  And [additional action]
Then [expected outcome]
  And [additional expected outcome]
```

**Example:**
```gherkin
Given a user is logged into their account
  And they have items in their shopping cart
When they click the "Checkout" button
  And they complete payment information
Then the order is successfully placed
  And they receive an order confirmation email
  And the cart is emptied
```

#### Scenario 2: [Alternative Path]

```gherkin
Given [initial context]
When [action occurs]
Then [expected outcome]
```

#### Scenario 3: [Error/Edge Case]

```gherkin
Given [error condition context]
When [action occurs]
Then [error handling outcome]
  And [user feedback]
```

---

## Functional Criteria

### Core Functionality

- [ ] **Criterion 1:** [Specific, testable condition]
  - Validation: [How to verify]
  - Priority: High/Medium/Low

- [ ] **Criterion 2:** [Specific, testable condition]
  - Validation: [How to verify]
  - Priority: High/Medium/Low

### User Interface

- [ ] **UI-1:** [UI element behavior]
  - Validation: [Visual/interaction check]

- [ ] **UI-2:** [Responsive behavior]
  - Validation: [Device/screen size check]

### Business Logic

- [ ] **BL-1:** [Business rule implementation]
  - Validation: [Logic verification]

- [ ] **BL-2:** [Data validation]
  - Validation: [Input/output check]

---

## Non-Functional Criteria

### Performance

- [ ] **PERF-1:** Response time < [X] seconds under [conditions]
- [ ] **PERF-2:** Supports [X] concurrent users without degradation
- [ ] **PERF-3:** Page load time < [X] seconds

### Security

- [ ] **SEC-1:** User data is encrypted in transit (HTTPS/TLS)
- [ ] **SEC-2:** Authentication required for [actions]
- [ ] **SEC-3:** Input sanitization prevents XSS/SQL injection

### Accessibility (WCAG 2.1 AA)

- [ ] **A11Y-1:** Keyboard navigable (Tab, Enter, Esc)
- [ ] **A11Y-2:** Screen reader compatible with ARIA labels
- [ ] **A11Y-3:** Color contrast ratio >= 4.5:1 for text
- [ ] **A11Y-4:** Touch targets >= 44x44px

### Usability

- [ ] **UX-1:** Clear error messages with actionable guidance
- [ ] **UX-2:** Loading states visible for operations > 1 second
- [ ] **UX-3:** Confirmation dialogs for destructive actions

---

## Edge Cases & Error Handling

### Edge Case 1: [Scenario]
- **Condition:** [When this happens]
- **Expected Behavior:** [System should]
- **Validation:** [How to test]

### Edge Case 2: [Scenario]
- **Condition:** [When this happens]
- **Expected Behavior:** [System should]
- **Validation:** [How to test]

### Error Handling

- [ ] **ERR-1:** Invalid input shows clear error message
- [ ] **ERR-2:** Network failure displays retry option
- [ ] **ERR-3:** Session timeout redirects to login with message

---

## Data Validation

### Input Validation

| Field | Type | Rules | Error Message |
|-------|------|-------|---------------|
| Email | String | Valid email format, max 255 chars | "Please enter a valid email" |
| Password | String | Min 8 chars, 1 uppercase, 1 number | "Password must be at least 8 characters" |
| Amount | Number | Positive, max 2 decimals | "Please enter a valid amount" |

### Output Validation

- [ ] **OUT-1:** Data format matches API specification
- [ ] **OUT-2:** All required fields are present in response
- [ ] **OUT-3:** Data types are correct (string, number, boolean)

---

## Integration Points

### External Systems

- [ ] **INT-1:** API calls return within [X] seconds
- [ ] **INT-2:** Graceful degradation if external service unavailable
- [ ] **INT-3:** Retry logic for transient failures (max 3 attempts)

### Internal Dependencies

- [ ] **DEP-1:** [Dependency name] integration works as expected
- [ ] **DEP-2:** Data synchronization occurs within [X] seconds

---

## Test Coverage Requirements

### Unit Tests

- [ ] All business logic functions have unit tests
- [ ] Edge cases and error conditions are tested
- [ ] Code coverage >= 80%

### Integration Tests

- [ ] API endpoints tested with valid/invalid inputs
- [ ] Database transactions commit/rollback correctly
- [ ] External service integrations mocked and tested

### End-to-End Tests

- [ ] Happy path user journey automated
- [ ] Critical error paths automated
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)

---

## Definition of Done

A story is considered **DONE** when:

1. All acceptance criteria marked complete
2. Code reviewed and approved by at least 1 developer
3. Unit tests written and passing (>=80% coverage)
4. Integration tests passing
5. Manual QA testing completed
6. Accessibility audit passed (WCAG 2.1 AA)
7. Security review completed (if applicable)
8. Documentation updated
9. Deployed to staging environment
10. Product Owner approval

---

## Exclusions

**Out of Scope for This Story:**

- [Feature/functionality explicitly not included]
- [Future enhancement deferred]
- [Related feature in separate story]

---

## Assumptions & Dependencies

### Assumptions

1. [Assumption about user behavior or system state]
2. [Assumption about data availability]
3. [Assumption about infrastructure]

### Dependencies

- **Blocked By:** [Other stories/features that must complete first]
- **Blocks:** [Stories/features dependent on this]
- **Related:** [Associated work items]

---

## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Owner | [Name] | YYYY-MM-DD | Approved |
| Tech Lead | [Name] | YYYY-MM-DD | Approved |
| QA Lead | [Name] | YYYY-MM-DD | Approved |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial creation |

---

## Notes

- [Additional context or clarifications]
- [Testing environment requirements]
- [Known limitations or technical debt]
