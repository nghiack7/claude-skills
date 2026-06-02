---
name: resource-plan
description: 'This skill should be used when the user asks to "tạo resource plan", "kế hoạch nguồn lực", "staffing plan", or needs a resource plan template for project planning.'
---

## Document Metadata

```yaml
document_type: "resource-plan"
title: "[Year] Resource & Budget Plan"
classification: "confidential"
retention: "5 years"
status: "draft"
owner: "Engineering Management"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["planning", "budget", "hiring", "infrastructure"]
relationships:
  derived_from:
    # Strategic documents this plan supports
    # - path: "product-knowledge/01-strategy/dibbs/YYYY-dibb-xxx.md"
    #   title: "DIBB Title"
    # - path: "product-knowledge/01-strategy/roadmaps/YYYY-roadmap.md"
    #   title: "Roadmap Title"
  references:
    # Supporting data documents
    # - path: "product-data/product-analytics/YYYY-metrics.md"
    #   title: "Metrics Document"
```

# [Year] Resource & Budget Plan

**Strategic Focus:** [Primary focus area]
**Constraint:** [Key budget constraint, e.g., "Infrastructure Cost ≤ X% of Revenue"]

## 1. Executive Summary

[2-3 sentences summarizing the plan's key decisions and resource allocation]

## 2. Budget Planning

### Revenue-Based Constraints

[Define budget constraints tied to business metrics]

```csv
Month,Projected Revenue,Max Budget (%),Estimated Spend,Headroom
[Month],[Revenue],[Budget],[Spend],[Headroom]
```

### Budget Allocation by Category

| Category | Annual Budget | % of Total | Notes |
|----------|---------------|------------|-------|
| Infrastructure | $X | X% | |
| Personnel | $X | X% | |
| Tools/Services | $X | X% | |
| **Total** | **$X** | **100%** | |

## 3. Team Structure

### Current State

| Role | Count | Notes |
|------|-------|-------|
| [Role] | X | |
| **Total** | **X** | |

### Target State

| Role | Count | Notes |
|------|-------|-------|
| [Role] | X | |
| **Total** | **X** | |

### Organization Structure

[Describe the organizational hierarchy and team groupings]

#### [Group/Team Name]
- **Focus:** [Primary responsibility]
- **Size:** [X Members]
- **Composition:** [Role breakdown]

## 4. Hiring Roadmap

### Phase 1: [Timeframe]
- **Objective:** [What this phase achieves]
- **Hiring:**
  - [Role]: [Count]
- **Transitions:** [Internal moves/promotions]

### Phase 2: [Timeframe]
- **Objective:** [What this phase achieves]
- **Hiring:**
  - [Role]: [Count]
- **Transitions:** [Internal moves/promotions]

### Phase 3: [Timeframe]
- **Objective:** [What this phase achieves]
- **Hiring:**
  - [Role]: [Count]
- **Outcome:** [Expected state after this phase]

## 5. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact description] | [Mitigation strategy] |

## 6. Success Criteria

- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## 7. Summary

| Metric | Value |
|--------|-------|
| Total Headcount | X |
| Total Budget | $X |
| Key Constraint | [Constraint] |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial plan |
