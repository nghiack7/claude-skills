---
name: prd
description: This skill should be used when the user asks to "tạo PRD", "viết PRD", "product requirements", or needs a Product Requirements Document template for product documentation.
---

---
# TEMPLATE METADATA - DO NOT REMOVE (Used for validation)
template_version: "1.1.0"
template_id: "prd-template"

# VALIDATION RULES
validation_rules:
  required_fields:
    - template  # MUST point to this template
    - document_type
    - status
    - owner
    - created
    - updated
    - rice_score  # PRDs require RICE scoring
    - relationships.implements  # PRDs must link to DIBBs/strategy

  optional_fields:
    - product_id
    - version
    - tags
    - stakeholders
    - quick_links

  field_rules:
    - field: "template"
    - field: "status"
      rule: "Must be valid PRD status"
      values: ["draft", "review", "approved", "in_progress", "shipped", "deprecated"]
    - field: "created"
      rule: "Must be YYYY-MM-DD format"
      regex: "^\\d{4}-\\d{2}-\\d{2}$"
    - field: "updated"
      rule: "Must be YYYY-MM-DD format"
      regex: "^\\d{4}-\\d{2}-\\d{2}$"

# DOCUMENT FIELDS - Fill these out when creating a document
document_type: "prd"
product_id: "prod-xxx"
version: "1.0.0"
status: "draft"  # draft|review|approved|in_progress|shipped|deprecated
owner: "Product Manager Name"
stakeholders: ["Engineering", "Design", "Marketing"]
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["feature-name", "category"]

# Document Graph - Structured Relationships
# IMPORTANT: Use absolute file paths from project root - no relative paths!
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
    # - path: "product-knowledge/04-technical/archive/2024-01-15-legacy-doc.md"
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

# Quick Reference Links (optional)
quick_links:
  figma: ""
  jira: ""
  slack: ""
  github: ""
---

# Product Requirements Document: [Feature/Product Name]

## 1. Executive Summary

**Product/Feature Name:** [Name]

**Owner:** [Product Manager Name]

**Status:** Draft | In Review | Approved | In Development | Launched

**Last Updated:** [Date]

**Quick Summary:**
[2-3 sentences describing what this PRD covers and why it matters]

---

## 2. Problem Statement

### 2.1 What Problem Are We Solving?

[Describe the core problem in detail]

### 2.2 Who Experiences This Problem?

[Define the target users/personas who face this problem]

### 2.3 Why Is This Important Now?

[Explain the urgency and business context]

### 2.4 Impact of Not Solving

[What happens if we don't address this?]

---

## 3. Goals & Objectives

### 3.1 Business Objectives

- **Objective 1:** [Description]
- **Objective 2:** [Description]

### 3.2 User Objectives

- **User Goal 1:** [What users want to achieve]
- **User Goal 2:** [What users want to achieve]

### 3.3 Success Metrics (KPIs)

| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| [Metric 1] | [Value] | [Value] | [How to measure] |
| [Metric 2] | [Value] | [Value] | [How to measure] |
| [Metric 3] | [Value] | [Value] | [How to measure] |

**Primary Success Metric:** [The one metric that matters most]

---

## 4. User Personas & Target Audience

### Primary Users

**Persona 1: [Name]**
- **Role:** [Job title/role]
- **Needs:** [What they need]
- **Pain Points:** [Current challenges]
- **Goals:** [What they want to achieve]
- **Behavior:** [How they currently work]

**Persona 2: [Name]**
- **Role:** [Job title/role]
- **Needs:** [What they need]
- **Pain Points:** [Current challenges]
- **Goals:** [What they want to achieve]
- **Behavior:** [How they currently work]

### Secondary Users

[Brief description of other affected users]

---

## 5. User Stories & Use Cases

### User Story Format
As a [user type], I want to [action], so that [benefit].

### Core User Stories

**Story 1: [Title]**
- **As a** [user type]
- **I want to** [action]
- **So that** [benefit]
- **Acceptance Criteria:**
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
  - [ ] [Criterion 3]

**Story 2: [Title]**
- **As a** [user type]
- **I want to** [action]
- **So that** [benefit]
- **Acceptance Criteria:**
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]

### Use Cases

**Use Case 1: [Scenario Name]**
1. **Preconditions:** [What must be true before this scenario]
2. **Steps:**
   - User does [action 1]
   - System responds with [response 1]
   - User does [action 2]
   - System responds with [response 2]
3. **Postconditions:** [Expected end state]
4. **Alternative Flows:** [What could go differently]

---

## 6. Feature Requirements

### 6.1 Must-Have Features (P0)

**Feature 1: [Name]**
- **Description:** [What it does]
- **User Story:** [Link to user story]
- **Acceptance Criteria:**
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
- **Technical Notes:** [Any technical considerations]
- **Dependencies:** [What this depends on]

**Feature 2: [Name]**
- **Description:** [What it does]
- **User Story:** [Link to user story]
- **Acceptance Criteria:**
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]

### 6.2 Should-Have Features (P1)

[Features that are important but not critical for launch]

### 6.3 Nice-to-Have Features (P2)

[Features we'd like to include if time permits]

### 6.4 Out of Scope

[Explicitly list what we are NOT doing in this release]

---

## 7. User Experience

### 7.1 User Flows

**Primary Flow:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Alternative Flows:**
- [Alternative path 1]
- [Alternative path 2]

### 7.2 Wireframes & Mockups

[Link to design files or embed images]

- **Screen 1:** [Description]
- **Screen 2:** [Description]

### 7.3 Interaction Patterns

[Describe key interactions, animations, transitions]

### 7.4 Error States & Edge Cases

- **Error Scenario 1:** [What happens and how we handle it]
- **Error Scenario 2:** [What happens and how we handle it]

---

## 8. Technical Requirements

### 8.1 System Requirements

- **Platform:** [Web/Mobile/Desktop]
- **Browser Support:** [Browsers and versions]
- **Device Support:** [Devices and screen sizes]
- **Accessibility:** [WCAG level, screen reader support]

### 8.2 Performance Requirements

- **Page Load Time:** [Target: < X seconds]
- **API Response Time:** [Target: < X ms]
- **Concurrent Users:** [Can support X users]
- **Data Volume:** [Can handle X records]

### 8.3 Dependencies

**External Dependencies:**
- [Service/API 1]
- [Service/API 2]

**Internal Dependencies:**
- [System/Module 1]
- [System/Module 2]

### 8.4 APIs & Integrations

[List required APIs and third-party integrations]

### 8.5 Data Requirements

**Data Models:**
- [Entity 1] with fields: [list]
- [Entity 2] with fields: [list]

**Data Migration:**
- [Any migration needs]

### 8.6 Security Requirements

- **Authentication:** [How users authenticate]
- **Authorization:** [Permission model]
- **Data Privacy:** [PII handling, encryption]
- **Compliance:** [GDPR, HIPAA, etc.]

---

## 9. Design & Assets

### 9.1 Design System

[Reference to design system components being used]

### 9.2 Assets Needed

- [ ] Icons
- [ ] Illustrations
- [ ] Images
- [ ] Animations
- [ ] Copy/Messaging

### 9.3 Branding Guidelines

[Any specific branding requirements]

---

## 10. Analytics & Tracking

### 10.1 Events to Track

| Event Name | Trigger | Properties | Purpose |
|------------|---------|-----------|---------|
| [event_1] | [When it fires] | [Data captured] | [Why track it] |
| [event_2] | [When it fires] | [Data captured] | [Why track it] |

### 10.2 Dashboards

[Link to analytics dashboards to monitor]

---

## 11. Release Strategy

### 11.1 Rollout Plan

- **Phase 1:** [Percentage, audience, dates]
- **Phase 2:** [Percentage, audience, dates]
- **Phase 3:** [Full rollout]

### 11.2 Feature Flags

[Feature flags to be used and their configuration]

### 11.3 Beta Testing

- **Beta Group:** [Who will be in beta]
- **Duration:** [How long]
- **Success Criteria:** [What determines beta success]

---

## 12. Timeline & Milestones

| Phase | Milestone | Owner | Target Date | Status |
|-------|-----------|-------|-------------|--------|
| Discovery | Research complete | PM | YYYY-MM-DD | ✅ |
| Design | Designs approved | Design | YYYY-MM-DD | 🟡 |
| Development | Backend ready | Eng | YYYY-MM-DD | ⬜ |
| Development | Frontend ready | Eng | YYYY-MM-DD | ⬜ |
| Testing | QA complete | QA | YYYY-MM-DD | ⬜ |
| Launch | Beta release | PM | YYYY-MM-DD | ⬜ |
| Launch | Full release | PM | YYYY-MM-DD | ⬜ |

**Legend:** ✅ Complete | 🟡 In Progress | ⬜ Not Started | ❌ Blocked

---

## 13. Risks & Assumptions

### 13.1 Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|------------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How to mitigate] |
| [Risk 2] | High/Med/Low | High/Med/Low | [How to mitigate] |

### 13.2 Assumptions

- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

### 13.3 Dependencies & Blockers

**Current Blockers:**
- [ ] [Blocker 1]
- [ ] [Blocker 2]

**Upcoming Dependencies:**
- [What needs to be ready before we can proceed]

---

## 14. Go-to-Market

### 14.1 Launch Communications

- **Internal Announcement:** [Date, channel]
- **Customer Announcement:** [Date, channel]
- **Documentation:** [What docs needed]

### 14.2 Training & Enablement

- [ ] Support team training
- [ ] Sales enablement
- [ ] Customer documentation
- [ ] Video tutorials

### 14.3 Marketing Plan

[Link to marketing plan or brief description]

---

## 15. Success Criteria & Post-Launch

### 15.1 Launch Criteria

- [ ] All P0 features complete
- [ ] Security review passed
- [ ] Performance benchmarks met
- [ ] Analytics implemented
- [ ] Documentation complete
- [ ] Support team trained

### 15.2 Post-Launch Monitoring

**First 24 Hours:**
- Monitor [metrics]
- Watch for [issues]

**First Week:**
- Analyze [data]
- Gather [feedback]

**First Month:**
- Review [KPIs]
- Iterate based on [learnings]

### 15.3 Success Definition

**This feature is successful if:**
1. [Success criterion 1]
2. [Success criterion 2]
3. [Success criterion 3]

---

## 16. Open Questions

- [ ] **Q1:** [Question that needs answering]
  - **Owner:** [Who will answer]
  - **Due:** [When we need answer]

- [ ] **Q2:** [Question that needs answering]
  - **Owner:** [Who will answer]
  - **Due:** [When we need answer]

---

## 17. Appendix

### 17.1 Research & Data

[Links to user research, competitive analysis, etc.]

### 17.2 References

- [Document 1]
- [Document 2]

### 17.3 Glossary

- **Term 1:** Definition
- **Term 2:** Definition

---

## 18. Document Relationships

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

## 19. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial version |

---

## 20. Approvals

| Role | Name | Approval Date | Signature |
|------|------|---------------|-----------|
| Product | [Name] | | |
| Engineering | [Name] | | |
| Design | [Name] | | |
| Leadership | [Name] | | |

---

**Next Steps:**
1. [Action 1]
2. [Action 2]
3. [Action 3]
