---
name: user-story
description: 'This skill should be used when the user asks to "tạo user story", "viết user story", "as a user I want", or needs a user story template for product documentation.'
---

---
document_type: "user-story"
product_id: "prod-xxx"
version: "1.0.0"
status: "draft"
owner: "Product Manager Name"
stakeholders: ["Engineering", "Design"]
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["user-story", "feature-name"]
# Document Graph - Structured Relationships
# Use absolute file paths as identifiers - no separate document_id needed!
relationships:
  depends_on:
    # Documents this depends on - must be reviewed/approved first
    # Example:
    # - path: "product-knowledge/06-decisions/adr/2025-10-15-adr-003-database-selection.md"
    #   title: "Database Selection Decision"
    #   reason: "Database choice affects data model requirements"

  blocks:
    # Documents that depend on this - will be blocked if this changes
    # Example:
    # - path: "product-knowledge/04-technical/specs/2025-11-01-tech-spec-005-implementation.md"
    #   title: "Technical Implementation Spec"
    #   reason: "Cannot implement without approved requirements"

  references:
    # Cross-references for context
    # Example:
    # - path: "product-knowledge/01-strategy/research/2025-09-01-market-research-001-competitors.md"
    #   title: "Competitor Analysis"
    #   reason: "Informed feature prioritization decisions"

  implements:
    # Strategic objectives and user stories this delivers
    # Example:
    # - path: "product-knowledge/01-strategy/dibbs/2025-dibb-growth.md"
    #   title: "2025 Growth DIBB"
    #   reason: "Supports Bet #2: Reduce signup friction"

  supersedes:
    # Deprecated/replaced documents
    # Example:
    # - path: "product-knowledge/archive/2024-01-15-legacy-doc.md"
    #   title: "Legacy Document Title"
    #   reason: "Replaces outdated approach with modern solution"

  derived_from: []

  related_issues:
    # External tracking items (GitHub, Jira, Linear, etc.)
    # Example:
    # - id: "GH-234"  # External IDs are fine
    #   title: "Feature request title"
    #   url: "https://github.com/org/repo/issues/234"
    #   status: "open"

# Quick Reference Links

---

# User Story: [Story Title]

**Story ID:** US-XXX

**Epic:** [Link to epic or parent feature]

**Priority:** P0 | P1 | P2

**Story Points:** [Estimated effort]

**Sprint/Iteration:** [Sprint number or iteration]

---

## User Story Statement

**As a** [type of user],

**I want** [an action or feature],

**So that** [a benefit or value].

---

## Context & Background

**Why this story matters:**
[Explain the context and importance of this user story]

**Current situation:**
[Describe how users currently handle this need or problem]

**Desired outcome:**
[What should change after this story is implemented]

---

## User Persona

**Primary User:** [Persona name]

**Role:** [Job title or user type]

**Goals:**
- [Goal 1]
- [Goal 2]

**Pain Points:**
- [Pain point 1]
- [Pain point 2]

**Technical Proficiency:** Beginner | Intermediate | Advanced

---

## Acceptance Criteria

**Definition of Done:**

### Scenario 1: [Happy Path]

**Given** [initial context or precondition],

**When** [action taken by user],

**Then** [expected outcome].

**And** [additional outcome if applicable].

---

### Scenario 2: [Alternative Path]

**Given** [initial context],

**When** [action taken],

**Then** [expected outcome].

---

### Scenario 3: [Edge Case or Error Handling]

**Given** [initial context],

**When** [action taken],

**Then** [expected outcome].

---

### Functional Requirements

- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]
- [ ] [Requirement 4]

### Non-Functional Requirements

- [ ] **Performance:** [e.g., Response time < 2 seconds]
- [ ] **Accessibility:** [e.g., WCAG 2.1 AA compliant]
- [ ] **Security:** [e.g., Requires authentication]
- [ ] **Usability:** [e.g., Works on mobile devices]

---

## User Flow

### Step-by-Step Flow

1. **User starts at:** [Starting point]
2. **User navigates to:** [Next step]
3. **User performs:** [Action]
4. **System responds:** [Response]
5. **User sees:** [Result]
6. **User completes:** [Final action]

### Alternative Flows

**Alt Flow 1: [Scenario]**
- [Description of alternative path]

**Alt Flow 2: [Scenario]**
- [Description of alternative path]

---

## UI/UX Requirements

### Mockups & Wireframes

[Link to design files or embed images]

### Key UI Elements

- [UI element 1: e.g., Submit button]
- [UI element 2: e.g., Input field for email]
- [UI element 3: e.g., Error message display]

### Interaction Patterns

- [Interaction 1: e.g., Click to expand]
- [Interaction 2: e.g., Drag and drop]

### Error States

| Error Condition | Error Message | User Action |
|----------------|---------------|-------------|
| [Error 1] | "[Message]" | [What user should do] |
| [Error 2] | "[Message]" | [What user should do] |

---

## Business Rules

| Rule | Description |
|------|-------------|
| [Rule 1] | [Description of business constraint or validation] |
| [Rule 2] | [Description of business logic] |

---

## Analytics & Tracking

### Events to Track

| Event Name | Trigger | Properties | Purpose |
|------------|---------|-----------|---------|
| [event_name] | [When it fires] | [Data captured] | [Why track it] |

### Metrics to Monitor

- [Metric 1: e.g., Completion rate]
- [Metric 2: e.g., Time to complete]
- [Metric 3: e.g., Error rate]

---

## Dependencies

### Blocked By

- [ ] [Dependency 1: e.g., US-XXX must be completed first]
- [ ] [Dependency 2: e.g., API endpoint must be ready]

### Blocks

- [ ] [Story 1: e.g., US-YYY depends on this]
- [ ] [Story 2: e.g., US-ZZZ depends on this]

### Related Stories

- [US-AAA: Related story 1]
- [US-BBB: Related story 2]

---

## Assumptions

- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

---

## Risks & Concerns

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | High/Med/Low | [How to address] |
| [Risk 2] | High/Med/Low | [How to address] |

---

## Questions & Open Issues

- [ ] **Q1:** [Question that needs answering]
  - **Owner:** [Who will answer]
  - **Status:** Open | Answered

- [ ] **Q2:** [Question that needs answering]
  - **Owner:** [Who will answer]
  - **Status:** Open | Answered

---

## Definition of Done

- [ ] Feature works as described in acceptance criteria
- [ ] User can complete the task successfully
- [ ] Error states handled gracefully
- [ ] Accessible to all users (WCAG 2.1 AA)
- [ ] Works on target devices/browsers
- [ ] Analytics events tracking correctly
- [ ] Product owner has approved
- [ ] Documentation/help content updated

---

## Estimation & Effort

**Story Points:** [X points]

**Confidence Level:** High | Medium | Low

**Assumptions:**
- [Key assumption affecting estimate]

---

## Demo Script

**How to demo this story to stakeholders:**

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [What to highlight]

---

## Rollout Plan

**Deployment Strategy:**
- [ ] Feature flag: [Flag name]
- [ ] Percentage rollout: [Start with X%]
- [ ] Target audience: [Who gets it first]

**Rollback Plan:**
- [How to rollback if issues arise]

---

## Success Criteria

**This story is successful if:**
1. [Success criterion 1]
2. [Success criterion 2]
3. [Success criterion 3]

**Metrics Target:**
- [Metric 1]: Achieve [target value]
- [Metric 2]: Achieve [target value]

---

## Attachments & Resources

- Design files: [Link]
- User research: [Link]
- Technical specs: [Link]
- Competitive analysis: [Link]

---

## Comments & Discussion

**[Date] - [Author]:**
[Comment or discussion point]

**[Date] - [Author]:**
[Response or additional context]

---

## 📊 Document Relationships

### Upstream Dependencies
> Documents this depends on - must be reviewed/approved first

| ID | Type | Title | Why It Matters | Status |
|----|------|-------|----------------|--------|
| - | - | - | - | - |

*Add dependencies from front matter `relationships.depends_on`*

### Downstream Impacts
> Documents that depend on this - will be blocked if this changes

| ID | Type | Title | Impact | Owner |
|----|------|-------|--------|-------|
| - | - | - | - | - |

*Add blocking documents from front matter `relationships.blocks`*

### Related Documents
> Cross-references for context

| ID | Type | Title | Relationship |
|----|------|-------|--------------|
| - | - | - | - |

*Add references from front matter `relationships.references`*

### Implements/Fulfills
> Strategic objectives and user stories this delivers

- **DIBB:** [Link to DIBB] - [Bet description]
- **User Story:** [Link to user story] - [Story description]

*Add implementations from front matter `relationships.implements`*

### Supersedes
> Deprecated/replaced documents

- [Link to old document] - [Reason for replacement]

*Add superseded documents from front matter `relationships.supersedes`*

### Related Issues & Bugs
> External tracking items

- **[Issue ID]**: [Link to issue] - [Description]

*Add related issues from front matter `relationships.related_issues`*

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial user story |

---

## Status Tracking

**Status:** Backlog | Ready | In Progress | In Review | Testing | Done

**Assigned To:** [Developer name]

**Sprint:** [Sprint number]

**Started:** [Date]

**Completed:** [Date]

---

## Sign-off

| Role | Name | Approved | Date |
|------|------|----------|------|
| Product Owner | [Name] | ✅ / ⬜ | YYYY-MM-DD |
| Tech Lead | [Name] | ✅ / ⬜ | YYYY-MM-DD |
| Designer | [Name] | ✅ / ⬜ | YYYY-MM-DD |
| QA Lead | [Name] | ✅ / ⬜ | YYYY-MM-DD |
