---
name: one-pager
description: This skill should be used when the user asks to "tạo one-pager", "viết proposal", or needs a One-Pager template for product documentation.
---

## Document Metadata

```yaml
document_type: "one-pager"
product_id: "prod-xxx"
version: "1.0.0"
status: "draft"
owner: "Product Manager Name"
stakeholders: ["Leadership", "Product", "Engineering"]
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["strategy", "executive-summary", "proposal"]
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
```

# One-Pager: [Initiative/Product/Feature Name]

**Date:** YYYY-MM-DD

**Owner:** [Product Manager / Initiative Lead]

**Status:** Draft | In Review | Approved

**Audience:** [Leadership / Investors / Board / Team]

---

## 🎯 The Big Idea

[1-2 sentences capturing the essence of this initiative - what it is and why it matters]

---

## 💡 Problem

**What problem are we solving?**

[2-3 sentences describing the problem]

**Who has this problem?**

[Target customer/user segment]

**How big is the problem?**

- [X]% of users experience this
- Costs businesses $[X] billion annually
- [Quantified impact metric]

**Why now?**

[Market timing, competitive pressure, or strategic imperative]

---

## 🚀 Solution

**What are we proposing?**

[2-3 sentences describing the solution]

**How does it work?**

[Brief explanation - keep it simple for non-technical audience]

**Why is this the right approach?**

- [Reason 1]
- [Reason 2]
- [Reason 3]

**What makes it different?**

[Unique value proposition or competitive advantage]

---

## 👥 Customer & Market

**Target customer:**

[Description of ideal customer/user]

**Market size:**

- TAM (Total Addressable Market): $[X]
- SAM (Serviceable Addressable Market): $[Y]
- SOM (Serviceable Obtainable Market): $[Z]

**Early adopters:**

[Who will use this first]

**Market trends:**

[Relevant market dynamics supporting this initiative]

---

## 💰 Business Impact

**Revenue opportunity:**

- Year 1: $[X]
- Year 2: $[Y]
- Year 3: $[Z]

**Key metrics:**

| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| [Metric 1] | [X] | [Y] | [When] |
| [Metric 2] | [X] | [Y] | [When] |
| [Metric 3] | [X] | [Y] | [When] |

**Strategic value:**

- [Strategic benefit 1]
- [Strategic benefit 2]
- [Strategic benefit 3]

---

## 🏆 Success Metrics

**How we'll measure success:**

**Primary metric:** [The one metric that matters most]
- Baseline: [Current]
- Target: [Goal]
- Timeline: [When]

**Supporting metrics:**
- [Metric 2]: [Target]
- [Metric 3]: [Target]

---

## 🛠️ What We're Building

**Phase 1: MVP (Months 1-3)**
- [Feature/capability 1]
- [Feature/capability 2]
- [Feature/capability 3]

**Phase 2: Expansion (Months 4-6)**
- [Feature/capability 4]
- [Feature/capability 5]

**Phase 3: Scale (Months 7-12)**
- [Feature/capability 6]
- [Feature/capability 7]

---

## 📅 Timeline

| Milestone | Date | Owner |
|-----------|------|-------|
| Kick-off | [Q-YYYY] | [Name] |
| MVP Launch | [Q-YYYY] | [Name] |
| Beta Complete | [Q-YYYY] | [Name] |
| GA Launch | [Q-YYYY] | [Name] |
| Break-even | [Q-YYYY] | [Name] |

**Time to market:** [X months]

**First revenue:** [X months from start]

---

## 💵 Investment Required

**Total investment:** $[X] over [Y] months

| Category | Amount | %  |
|----------|--------|-----|
| Engineering | $[X] | [%] |
| Design | $[X] | [%] |
| Marketing | $[X] | [%] |
| Sales | $[X] | [%] |
| Infrastructure | $[X] | [%] |
| **Total** | **$[X]** | **100%** |

**Headcount needed:**
- [X] Engineers
- [X] Designers
- [X] Product Managers
- [X] Other roles

**ROI:** [X]x return in [Y] months

**Payback period:** [X] months

---

## ⚠️ Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk 1] | H/M/L | H/M/L | [How we'll mitigate] |
| [Risk 2] | H/M/L | H/M/L | [Mitigation plan] |
| [Risk 3] | H/M/L | H/M/L | [Response strategy] |

---

## 🏁 Why This Matters

**Strategic alignment:**

[How this aligns with company vision/strategy]

**Competitive advantage:**

[How this differentiates us in the market]

**Long-term value:**

[Why this is important beyond immediate metrics]

---

## ❓ Key Assumptions

- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

**What needs to be true:**

[Critical success factors]

---

## 🎯 Ask

**What we need:**

- [ ] [Approval for budget]
- [ ] [Headcount allocation]
- [ ] [Go/no-go decision]
- [ ] [Partnership/support from X team]

**Decision needed by:** [Date]

**Next steps if approved:**

1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## 📞 Team

**Leadership:**
- [Name] - [Role]

**Core team:**
- [Name] - [Role]
- [Name] - [Role]
- [Name] - [Role]

---

## 📚 Supporting Documents

- [Detailed PRD - Link]
- [Market research - Link]
- [Financial model - Link]
- [Competitive analysis - Link]

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
- **Initiative:** [Link to strategic initiative]

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
| 1.0.0 | YYYY-MM-DD | [Name] | Initial version |

---

**Contact:** [Name - email]

**Last Updated:** [Date]
