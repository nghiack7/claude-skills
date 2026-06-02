---
name: meeting-notes
description: 'This skill should be used when the user asks to "tạo meeting notes", "ghi chú cuộc họp", "meeting minutes", or needs a meeting notes template for documentation.'
---

---
document_type: "meeting-notes"
product_id: "prod-xxx"
version: "1.0.0"
status: "draft"
owner: "Meeting Organizer Name"
stakeholders: ["Attendees"]
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["meeting", "notes", "minutes"]
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

# Meeting Notes: [Meeting Name/Topic]

**Date:** YYYY-MM-DD

**Time:** HH:MM - HH:MM [Timezone]

**Meeting Type:** Planning | Sync | Review | Decision | Brainstorm | Retrospective

**Facilitator:** [Name]

**Note Taker:** [Name]

---

## 📋 Meeting Details

### Attendees

**Present:**
- [Name] - [Role]
- [Name] - [Role]
- [Name] - [Role]

**Absent:**
- [Name] - [Role] - [Reason if relevant]

**Optional attendees:**
- [Name] - [Role]

---

## 🎯 Meeting Objective

**Primary goal:**
[What we wanted to achieve in this meeting]

**Desired outcomes:**
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

---

## 📝 Agenda

| Time | Topic | Owner | Duration |
|------|-------|-------|----------|
| HH:MM | [Topic 1] | [Name] | Xmin |
| HH:MM | [Topic 2] | [Name] | Xmin |
| HH:MM | [Topic 3] | [Name] | Xmin |
| HH:MM | [Wrap-up] | [Name] | Xmin |

---

## 💬 Discussion Summary

### Topic 1: [Topic Name]

**Presented by:** [Name]

**Key points:**
- [Point 1]
- [Point 2]
- [Point 3]

**Discussion highlights:**
[Summary of the discussion]

**Decisions made:**
- [Decision 1]
- [Decision 2]

**Action items:**
- [ ] [Action] - Owner: [Name] - Due: [Date]

**Open questions:**
- [Question that needs follow-up]

---

### Topic 2: [Topic Name]

**Presented by:** [Name]

**Context:**
[Background information discussed]

**Key points:**
- [Point 1]
- [Point 2]

**Discussion:**
[What was discussed]

**Outcomes:**
[What was decided or concluded]

---

### Topic 3: [Topic Name]

**Key points:**
[Summary]

---

## ✅ Decisions Made

| # | Decision | Owner | Impact | Next Steps |
|---|----------|-------|--------|------------|
| 1 | [Decision] | [Name] | High/Med/Low | [What happens next] |
| 2 | [Decision] | [Name] | High/Med/Low | [Next steps] |
| 3 | [Decision] | [Name] | High/Med/Low | [Actions] |

---

## 🎯 Action Items

### High Priority (This Week)

- [ ] **[Action 1]**
  - Owner: [Name]
  - Due: [Date]
  - Context: [Why this is needed]
  - Status: Todo | In Progress | Done

- [ ] **[Action 2]**
  - Owner: [Name]
  - Due: [Date]
  - Context: [Background]
  - Status: Todo | In Progress | Done

### Medium Priority (Next Week)

- [ ] **[Action 3]**
  - Owner: [Name]
  - Due: [Date]

- [ ] **[Action 4]**
  - Owner: [Name]
  - Due: [Date]

### Follow-up Needed

- [ ] **[Item requiring follow-up]**
  - Owner: [Who will follow up]
  - By when: [Date]

---

## ❓ Open Questions

| Question | Who Will Answer | By When | Status |
|----------|----------------|---------|--------|
| [Question 1] | [Name] | [Date] | Open | Answered |
| [Question 2] | [Name] | [Date] | Open | Answered |

---

## 💡 Key Insights

**Important observations:**
- [Insight 1]
- [Insight 2]
- [Insight 3]

**Risks identified:**
- [Risk 1]
- [Risk 2]

**Opportunities:**
- [Opportunity 1]
- [Opportunity 2]

---

## 📊 Data & Metrics Discussed

**Key metrics reviewed:**
| Metric | Current | Target | Trend | Notes |
|--------|---------|--------|-------|-------|
| [Metric 1] | [Value] | [Goal] | ↗️↘️→ | [Context] |
| [Metric 2] | [Value] | [Goal] | ↗️↘️→ | [Context] |

---

## 🚫 Blockers & Concerns

**Blockers:**
- [Blocker 1] - Owner: [Name] - Due: [Date to resolve]
- [Blocker 2] - Owner: [Name] - Due: [Date]

**Concerns raised:**
- [Concern 1] - How addressing: [Plan]
- [Concern 2] - How addressing: [Plan]

---

## 🔄 Next Steps

**Immediate next steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Next meeting:**
- Date: [YYYY-MM-DD]
- Time: [HH:MM]
- Agenda: [Topics to cover]

---

## 📎 Resources & Links

**Documents discussed:**
- [Document 1 - Link]
- [Document 2 - Link]

**Presentations:**
- [Presentation 1 - Link]

**Reference materials:**
- [Resource 1 - Link]

---

## 💬 Verbatim Quotes (if notable)

> "[Important quote from discussion]" - [Name]

> "[Key insight or decision rationale]" - [Name]

---

## 🔍 Parking Lot

**Topics raised but not discussed (for future meetings):**
- [Topic 1]
- [Topic 2]
- [Topic 3]

---

## 📝 Notes

**Additional context:**
[Any other relevant information not captured above]

---

## ✍️ Approval

**Notes reviewed by:**
- [Name] - [Date]
- [Name] - [Date]

**Status:** Draft | Final | Distributed

**Distributed to:**
- [ ] All attendees
- [ ] Stakeholders
- [ ] Team channel

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
| 1.0.0 | YYYY-MM-DD | [Name] | Initial meeting notes |
