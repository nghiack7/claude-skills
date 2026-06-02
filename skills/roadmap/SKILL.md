---
name: roadmap
description: 'This skill should be used when the user asks to "tạo roadmap", "viết lộ trình", "product roadmap", or needs a roadmap template for product planning.'
---

---
document_type: "roadmap"
product_id: "prod-xxx"
version: "1.0.0"
status: "draft"
owner: "Product Manager Name"
stakeholders: ["Leadership", "Engineering", "Design", "Sales"]
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["roadmap", "planning", "quarter"]
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

# Product Roadmap: [Product Name] - [Time Period]

## 1. Overview

**Product:** [Product Name]

**Time Period:** [Q1 2025 | H1 2025 | 2025]

**Last Updated:** [Date]

**Status:** Draft | Published | Archived

**Vision Statement:**
[1-2 sentences about where the product is headed]

---

## 2. Strategic Themes

Our roadmap is organized around these strategic themes:

### Theme 1: [Theme Name]
**Goal:** [What we're trying to achieve]

**Why it matters:** [Business/user impact]

**Success metric:** [How we measure success]

### Theme 2: [Theme Name]
**Goal:** [What we're trying to achieve]

**Why it matters:** [Business/user impact]

**Success metric:** [How we measure success]

### Theme 3: [Theme Name]
**Goal:** [What we're trying to achieve]

**Why it matters:** [Business/user impact]

**Success metric:** [How we measure success]

---

## 3. Roadmap Timeline

### Now (Current Quarter: [Q1 2025])

**Focus:** [Primary focus area]

#### In Progress
| Feature | Theme | Owner | Status | Launch Date |
|---------|-------|-------|--------|-------------|
| [Feature 1] | [Theme] | [PM] | 🟡 In Dev | YYYY-MM-DD |
| [Feature 2] | [Theme] | [PM] | 🟡 In Dev | YYYY-MM-DD |

#### Planned This Quarter
| Feature | Theme | Owner | Priority | Target Date |
|---------|-------|-------|----------|-------------|
| [Feature 3] | [Theme] | [PM] | P0 | YYYY-MM-DD |
| [Feature 4] | [Theme] | [PM] | P1 | YYYY-MM-DD |

**Key Milestones:**
- [ ] [Milestone 1] - [Date]
- [ ] [Milestone 2] - [Date]
- [ ] [Milestone 3] - [Date]

---

### Next (Next Quarter: [Q2 2025])

**Focus:** [Primary focus area]

#### Planned Initiatives
| Initiative | Theme | Description | Owner | Priority |
|-----------|-------|-------------|-------|----------|
| [Initiative 1] | [Theme] | [Brief desc] | [PM] | P0 |
| [Initiative 2] | [Theme] | [Brief desc] | [PM] | P1 |
| [Initiative 3] | [Theme] | [Brief desc] | [PM] | P1 |

**Dependencies:**
- [Dependency 1]
- [Dependency 2]

---

### Later (Beyond Next Quarter)

**Focus:** [Future direction]

#### Future Initiatives
| Initiative | Theme | Description | Timeframe | Confidence |
|-----------|-------|-------------|-----------|------------|
| [Initiative 1] | [Theme] | [Brief desc] | Q3 2025 | High |
| [Initiative 2] | [Theme] | [Brief desc] | H2 2025 | Medium |
| [Initiative 3] | [Theme] | [Brief desc] | 2025 | Low |

**Exploratory Items:**
- [Idea 1] - [Why we're considering it]
- [Idea 2] - [Why we're considering it]

---

## 4. Feature Details

### [Feature 1 Name]

**Timeline:** [Quarter/Month]

**Status:** Planning | Design | Development | Testing | Launched

**Theme:** [Strategic theme]

**Priority:** P0 | P1 | P2

**Problem:** [What problem does this solve?]

**Solution:** [What are we building?]

**Impact:** [Expected business/user impact]

**Success Metrics:**
- [Metric 1]: [Target]
- [Metric 2]: [Target]

**Dependencies:**
- [Dependency 1]
- [Dependency 2]

**Resources Required:**
- Engineering: [Team/people count]
- Design: [Team/people count]
- Other: [Teams involved]

**Related Documents:**
- PRD: [Link]
- Design: [Link]

---

### [Feature 2 Name]

[Same structure as Feature 1]

---

### [Feature 3 Name]

[Same structure as Feature 1]

---

## 5. Resource Allocation

### Team Capacity

| Team | Current Allocation | Planned Allocation |
|------|-------------------|-------------------|
| Engineering | [X people / Y%] | [X people / Y%] |
| Design | [X people / Y%] | [X people / Y%] |
| QA | [X people / Y%] | [X people / Y%] |
| Product | [X people / Y%] | [X people / Y%] |

### Allocation by Theme

| Theme | % of Resources | Rationale |
|-------|---------------|-----------|
| [Theme 1] | [X%] | [Why this allocation] |
| [Theme 2] | [X%] | [Why this allocation] |
| [Theme 3] | [X%] | [Why this allocation] |
| Tech Debt | [X%] | [Why this allocation] |

---

## 6. Business Objectives & DIBBs

### Objective 1: [Objective Statement]

**Bets:**
1. [KR1]: [Current] → [Target]
2. [KR2]: [Current] → [Target]
3. [KR3]: [Current] → [Target]

**Roadmap Items Supporting This:**
- [Feature A]
- [Feature B]

### Objective 2: [Objective Statement]

**Bets:**
1. [KR1]: [Current] → [Target]
2. [KR2]: [Current] → [Target]

**Roadmap Items Supporting This:**
- [Feature C]
- [Feature D]

---

## 7. Customer Impact

### Target Segments

| Segment | % of Users | Initiatives for This Segment |
|---------|-----------|------------------------------|
| [Segment 1] | [X%] | [Features] |
| [Segment 2] | [X%] | [Features] |
| [Segment 3] | [X%] | [Features] |

### Expected Outcomes

**For Users:**
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

**For Business:**
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

---

## 8. Technical Debt & Infrastructure

### Planned Technical Investments

| Item | Type | Impact | Effort | Quarter |
|------|------|--------|--------|---------|
| [Tech debt 1] | Debt | [Impact] | [Effort] | Q1 |
| [Infrastructure 1] | Infra | [Impact] | [Effort] | Q2 |
| [Refactor 1] | Refactor | [Impact] | [Effort] | Q2 |

**Rationale:**
[Why we're prioritizing these technical items]

---

## 9. Market & Competitive Landscape

### Market Trends

- **Trend 1:** [Description and how we're responding]
- **Trend 2:** [Description and how we're responding]
- **Trend 3:** [Description and how we're responding]

### Competitive Positioning

| Competitor | Their Focus | Our Response |
|-----------|-------------|--------------|
| [Competitor 1] | [What they're doing] | [Our strategy] |
| [Competitor 2] | [What they're doing] | [Our strategy] |

---

## 10. Risks & Mitigation

| Risk | Impact | Probability | Mitigation | Owner |
|------|--------|------------|------------|-------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] | [Name] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Strategy] | [Name] |
| [Risk 3] | High/Med/Low | High/Med/Low | [Strategy] | [Name] |

---

## 11. Assumptions & Dependencies

### Assumptions

- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

### External Dependencies

- [External dependency 1]
- [External dependency 2]

### Cross-Team Dependencies

- [Team A needs to deliver X]
- [Team B needs to deliver Y]

---

## 12. Success Metrics

### Product Health Metrics

| Metric | Current | Q1 Target | Q2 Target | Measurement |
|--------|---------|-----------|-----------|-------------|
| [Metric 1] | [Value] | [Value] | [Value] | [How measured] |
| [Metric 2] | [Value] | [Value] | [Value] | [How measured] |
| [Metric 3] | [Value] | [Value] | [Value] | [How measured] |

### Feature Adoption Targets

| Feature | Launch Date | Week 1 | Month 1 | Quarter 1 |
|---------|------------|--------|---------|-----------|
| [Feature A] | [Date] | [Target] | [Target] | [Target] |
| [Feature B] | [Date] | [Target] | [Target] | [Target] |

---

## 13. Communication Plan

### Internal Updates

- **Weekly:** [What and to whom]
- **Monthly:** [What and to whom]
- **Quarterly:** [What and to whom]

### External Communication

| Audience | Channel | Frequency | Next Update |
|----------|---------|-----------|-------------|
| Customers | [Email/Blog] | [Monthly] | [Date] |
| Partners | [Portal] | [Quarterly] | [Date] |
| Public | [Website] | [As needed] | [Date] |

---

## 14. What We're NOT Doing

**Explicitly out of scope for this roadmap period:**

- [Item 1] - [Reason why not]
- [Item 2] - [Reason why not]
- [Item 3] - [Reason why not]

**Why:** [Explanation of prioritization choices]

---

## 15. Feedback & Input

### Feedback Received

| Source | Date | Feedback | Action Taken |
|--------|------|----------|--------------|
| [Customer] | [Date] | [Summary] | [Response] |
| [Internal] | [Date] | [Summary] | [Response] |

### Open Questions

- [ ] **Q1:** [Question]
  - **Owner:** [Name]
  - **Due:** [Date]

- [ ] **Q2:** [Question]
  - **Owner:** [Name]
  - **Due:** [Date]

---

## 16. Governance & Review

### Review Schedule

- **Weekly Sync:** [Day/Time] - Progress updates
- **Monthly Review:** [Date] - Roadmap adjustments
- **Quarterly Planning:** [Date] - Next quarter planning

### Approval Process

| Role | Approver | Status | Date |
|------|----------|--------|------|
| Product | [Name] | ✅ | [Date] |
| Engineering | [Name] | 🟡 | Pending |
| Design | [Name] | ⬜ | Pending |
| Leadership | [Name] | ⬜ | Pending |

---

## 17. Appendix

### Reference Materials

- Previous Roadmap: [Link]
- User Research: [Link]
- Competitive Analysis: [Link]
- Market Data: [Link]

### Glossary

- **[Term 1]:** Definition
- **[Term 2]:** Definition

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
| 1.0.0 | YYYY-MM-DD | [Name] | Initial roadmap for [period] |

---

## Visual Roadmap

```
[Consider adding a Gantt chart or timeline visualization here]

Q1 2025          Q2 2025          Q3 2025          Q4 2025
|                |                |                |
[Feature A]──────|                |                |
     [Feature B]─────────|         |                |
                [Feature C]───────────|             |
                         [Feature D]─────────|      |
                                    [Feature E]─────────|
```

---

**Notes:**
- This roadmap is a living document and subject to change
- Priorities may shift based on customer feedback and market conditions
- Dates are targets and may adjust as we learn more
- Feedback welcome - contact [Product Owner]
