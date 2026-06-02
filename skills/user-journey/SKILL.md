---
name: user-journey
description: 'This skill should be used when the user asks to "tạo user journey", "hành trình người dùng", "customer journey map", or needs a user journey template for UX documentation.'
---

## Document Metadata

```yaml
document_type: "user_journey"
journey_id: "UJ-XXX"
persona_id: "PERSONA-XXX"
version: "1.0.0"
status: "draft"
owner: "UX Designer Name"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["user-journey", "ux", "customer-experience"]

# Relationships
relationships:
  derived_from:
    - path: "product-knowledge/02-requirements/personas/persona-name.md"
      title: "User Persona"
      reason: "Journey for this persona"
  blocks:
    - path: "product-knowledge/03-design/ux-ui/YYYY-MM-DD-design-spec-NNN-feature.md"
      title: "Design Specification"
      reason: "Implements touchpoints in this journey"
```

# User Journey: [Journey Name]

> **Purpose:** Map the end-to-end experience of a user accomplishing a specific goal, identifying pain points and opportunities for improvement.

---

## Journey Overview

**Journey ID:** `UJ-XXX`
**Journey Name:** [Clear, outcome-focused name]
**Persona:** [Primary persona name]
**Goal:** [What the user wants to achieve]
**Timeframe:** [Duration: minutes, hours, days, weeks]

### Executive Summary

[2-3 paragraph overview of this journey, its importance to the business, and key findings]

---

## Persona Profile

**Name:** [Persona name]
**Role:** [Job title/role]
**Demographics:** [Age, location, tech savviness]

### Goals & Motivations

- **Primary Goal:** [Main objective]
- **Secondary Goals:** [Additional objectives]
- **Motivations:** [Why they want to achieve this]

### Pain Points & Frustrations

- [Current pain point 1]
- [Current pain point 2]
- [Current pain point 3]

### Context

**Scenario:** [Specific situation triggering this journey]
**Environment:** [Where/when this happens - desktop, mobile, in-store, etc.]
**Starting Point:** [What brings them to this journey]

---

## Journey Stages

### Stage 1: [Awareness/Discovery]

**Duration:** [Time spent in this stage]
**User Goal:** [What user wants to accomplish in this stage]
**User Mindset:** [Emotional state, thoughts, expectations]

#### Touchpoints

| # | Touchpoint | Channel | Action | Details |
|---|------------|---------|--------|---------|
| 1 | [Landing page] | Web | User discovers product | Searches Google, clicks ad |
| 2 | [Homepage] | Web | Browses offerings | Scans hero section, reads value prop |
| 3 | [Product page] | Web | Evaluates fit | Reviews features, pricing |

#### User Actions

1. **Action:** [What user does]
   - **Motivation:** [Why they do it]
   - **Expected Outcome:** [What they expect to happen]

2. **Action:** [What user does]
   - **Motivation:** [Why they do it]
   - **Expected Outcome:** [What they expect to happen]

#### Thoughts & Feelings

**Thoughts:**
> "I wonder if this product can solve my problem..."
> "The pricing seems reasonable, but is it worth it?"

**Feelings:**
- 😐 Curious but skeptical
- 😕 Uncertain about value
- 😊 Excited by possibilities

**Emotional State:** ⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛ (4/10 satisfaction)

#### Pain Points

🔴 **Critical Issues:**
- [Major blocker or frustration]
- [Confusing experience]

🟡 **Minor Frustrations:**
- [Small annoyance]
- [Unclear information]

#### Opportunities

💡 **Quick Wins:**
- [Easy improvement with high impact]

💡 **Long-term Enhancements:**
- [Strategic improvement]

#### Metrics

- **Success Metric:** [How to measure success in this stage]
- **Current Performance:** [Baseline data]
- **Target:** [Goal to achieve]

---

### Stage 2: [Consideration/Evaluation]

**Duration:** [Time spent in this stage]
**User Goal:** [What user wants to accomplish in this stage]
**User Mindset:** [Emotional state, thoughts, expectations]

#### Touchpoints

| # | Touchpoint | Channel | Action | Details |
|---|------------|---------|--------|---------|
| 4 | [Trial signup] | Web | Creates account | Enters email, sets password |
| 5 | [Onboarding] | Web/Email | Completes setup | Follows setup wizard |
| 6 | [Support docs] | Web | Seeks help | Searches knowledge base |

#### User Actions

[Repeat structure from Stage 1]

#### Thoughts & Feelings

[Repeat structure from Stage 1]

#### Pain Points

[Repeat structure from Stage 1]

#### Opportunities

[Repeat structure from Stage 1]

#### Metrics

[Repeat structure from Stage 1]

---

### Stage 3: [Purchase/Conversion]

[Repeat full stage structure]

---

### Stage 4: [Onboarding/First Use]

[Repeat full stage structure]

---

### Stage 5: [Ongoing Use/Retention]

[Repeat full stage structure]

---

### Stage 6: [Advocacy/Renewal]

[Repeat full stage structure]

---

## Journey Map Visualization

```
Awareness → Consideration → Purchase → Onboarding → Usage → Advocacy
   😐           😟            😓          😐          😊        😍

Satisfaction:
10 |                                            ●───●─────●
 9 |                                           /
 8 |                                          /
 7 |                                         /
 6 |                  ●                     /
 5 |                 / \                   /
 4 |        ●───────/   \                 /
 3 |       /             \               /
 2 |      /               \             /
 1 |_____/                 \___________/
   Aware  Consider  Buy   Onboard  Use  Advocate

🔴 Critical pain points    💡 Opportunities
```

**Emotional Journey:**

| Stage | Emotion | Intensity | Reason |
|-------|---------|-----------|--------|
| Awareness | Curious | Medium | Discovering solution |
| Consideration | Anxious | High | Fear of wrong choice |
| Purchase | Frustrated | High | Complex checkout |
| Onboarding | Confused | Medium | Unclear instructions |
| Usage | Satisfied | High | Product works well |
| Advocacy | Delighted | Very High | Exceeds expectations |

---

## Key Insights

### Critical Findings

1. **Finding:** [Major discovery about user behavior]
   - **Evidence:** [Data, quotes, observations]
   - **Impact:** [Business/user impact]
   - **Recommendation:** [What to do]

2. **Finding:** [Major discovery]
   - **Evidence:** [Data, quotes, observations]
   - **Impact:** [Business/user impact]
   - **Recommendation:** [What to do]

### User Quotes

> "I almost gave up during signup because the form asked for too much information upfront."
> — Participant 3, User Testing Session

> "Once I got past onboarding, the product was amazing. But getting there was painful."
> — Participant 7, User Interview

### Behavioral Patterns

- **Pattern 1:** [Observable user behavior]
  - Observed in: X% of users
  - Consequence: [What this means]

- **Pattern 2:** [Observable user behavior]
  - Observed in: X% of users
  - Consequence: [What this means]

---

## Pain Points Summary

### By Severity

#### 🔴 Critical (Must Fix)

| Pain Point | Stage | Impact | Users Affected |
|------------|-------|--------|----------------|
| Complex checkout flow | Purchase | High abandonment (45%) | 45% of users |
| Confusing onboarding | Onboarding | Low activation (30%) | 70% of new users |

#### 🟡 Moderate (Should Fix)

| Pain Point | Stage | Impact | Users Affected |
|------------|-------|--------|----------------|
| Slow page load | Awareness | 15% bounce rate | 15% of visitors |
| Limited help docs | Usage | Support tickets up 30% | 20% of users |

#### 🟢 Minor (Nice to Fix)

| Pain Point | Stage | Impact | Users Affected |
|------------|-------|--------|----------------|
| Small mobile buttons | All | Occasional misclicks | 10% of mobile users |

---

## Opportunities & Recommendations

### Priority 1: Critical Improvements

**Opportunity 1: Simplify Checkout Flow**
- **Problem:** 45% cart abandonment due to complex 5-step checkout
- **Solution:** Reduce to 2-step checkout with smart defaults
- **Expected Impact:** Reduce abandonment to 25% (+20% revenue)
- **Effort:** 3 sprints
- **ROI:** High

**Opportunity 2: Redesign Onboarding**
- **Problem:** Only 30% of signups complete onboarding
- **Solution:** Interactive product tour with progressive disclosure
- **Expected Impact:** Increase activation to 60% (2x improvement)
- **Effort:** 4 sprints
- **ROI:** Very High

### Priority 2: Quick Wins

**Opportunity 3: Add Progress Indicators**
- **Problem:** Users don't know how many steps remain
- **Solution:** Add progress bar to multi-step flows
- **Expected Impact:** Reduce abandonment by 10%
- **Effort:** 1 sprint
- **ROI:** Medium

### Priority 3: Long-term Enhancements

**Opportunity 4: Personalized Experience**
- **Problem:** Generic experience doesn't match user needs
- **Solution:** Adaptive UI based on user behavior and preferences
- **Expected Impact:** Increase engagement by 30%
- **Effort:** 6 months
- **ROI:** High (long-term)

---

## Touchpoint Inventory

Complete list of all interaction points:

| # | Touchpoint | Channel | Type | Owner | Quality Score |
|---|------------|---------|------|-------|---------------|
| 1 | Google Search Ad | Paid Media | Acquisition | Marketing | 8/10 |
| 2 | Landing Page | Website | Acquisition | Product | 6/10 |
| 3 | Homepage | Website | Awareness | Product | 7/10 |
| 4 | Product Pages | Website | Consideration | Product | 8/10 |
| 5 | Pricing Page | Website | Consideration | Product | 5/10 ⚠️ |
| 6 | Signup Form | Website | Conversion | Engineering | 4/10 🔴 |
| 7 | Welcome Email | Email | Onboarding | Marketing | 7/10 |
| 8 | Onboarding Flow | Website | Onboarding | Product | 5/10 ⚠️ |
| 9 | Dashboard | Website | Usage | Product | 8/10 |
| 10 | Support Chat | Chat | Support | Support | 9/10 |

**Legend:**
- 🔴 Critical (≤5/10) - Immediate attention needed
- ⚠️ Warning (6/10) - Needs improvement
- ✅ Good (7-8/10) - Minor optimizations
- ⭐ Excellent (9-10/10) - Best practice

---

## Metrics & Success Criteria

### Current State (Baseline)

| Metric | Current Value | Industry Benchmark |
|--------|---------------|-------------------|
| Awareness → Consideration | 25% | 30% |
| Consideration → Trial | 15% | 20% |
| Trial → Purchase | 10% | 25% |
| Purchase → Active User | 30% | 60% |
| Active → Advocate | 5% | 15% |
| **Overall Conversion** | **0.3%** | **1.5%** |

### Target State (6 Months)

| Metric | Target Value | Improvement |
|--------|--------------|-------------|
| Awareness → Consideration | 30% | +5% |
| Consideration → Trial | 25% | +10% |
| Trial → Purchase | 20% | +10% |
| Purchase → Active User | 60% | +30% |
| Active → Advocate | 15% | +10% |
| **Overall Conversion** | **1.35%** | **+350%** |

### Leading Indicators

- Page views per session: Current 3.2 → Target 4.5
- Time in consideration stage: Current 7 days → Target 3 days
- Support tickets per new user: Current 1.5 → Target 0.5

---

## Journey Alternatives & Branches

### Alternative Path 1: Mobile-First Journey

[Describe how mobile journey differs from desktop]

### Alternative Path 2: Referred User

[How referred users have different entry point]

### Alternative Path 3: Enterprise Customer

[B2B journey differences]

---

## Research Methodology

### Research Methods Used

- [ ] User interviews (n = [X])
- [ ] Usability testing (n = [X])
- [ ] Surveys (n = [X])
- [ ] Analytics review
- [ ] Session recordings
- [ ] Support ticket analysis
- [ ] Competitor analysis

### Participants

- **Total Participants:** [X]
- **Demographics:** [Age, role, experience level]
- **Recruitment:** [How participants were found]
- **Incentive:** [What participants received]

### Data Sources

- Google Analytics (Jan-March 2025)
- Hotjar session recordings (500 sessions)
- Intercom support tickets (Q1 2025)
- User testing sessions (15 participants)
- Post-purchase surveys (NPS score)

---

## Next Steps

### Immediate Actions (Week 1-2)

1. [ ] Present findings to stakeholders
2. [ ] Prioritize opportunities with product team
3. [ ] Create PRDs for top 3 opportunities
4. [ ] Set up A/B tests for quick wins

### Short-term (Month 1-3)

1. [ ] Implement quick win improvements
2. [ ] Begin design work on critical improvements
3. [ ] Conduct follow-up research to validate assumptions
4. [ ] Track metrics weekly

### Long-term (Month 4-12)

1. [ ] Roll out major journey improvements
2. [ ] Measure impact on conversion and satisfaction
3. [ ] Iterate based on user feedback
4. [ ] Document lessons learned

---

## Stakeholder Alignment

### Reviewed By

| Stakeholder | Role | Date | Status | Feedback |
|-------------|------|------|--------|----------|
| [Name] | Product Manager | YYYY-MM-DD | ✅ Approved | "Focus on checkout first" |
| [Name] | Design Lead | YYYY-MM-DD | ✅ Approved | "Onboarding needs work" |
| [Name] | Engineering Lead | YYYY-MM-DD | ⏳ Pending | "Need effort estimates" |

---

## Appendix

### A. Detailed Journey Map (Visual)

[Link to Miro/Figma journey map visualization]

### B. Session Recording Links

- [Hotjar recording 1 - Checkout abandonment](link)
- [Hotjar recording 2 - Onboarding confusion](link)

### C. Interview Transcripts

[Link to detailed interview notes]

### D. Survey Results

[Link to full survey data and analysis]

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial journey map |
| 1.1.0 | YYYY-MM-DD | [Name] | Added mobile journey variant |

---

## Resources

- **Journey Map (Visual):** [Miro/Figma link]
- **Research Repository:** [Confluence/Notion link]
- **Analytics Dashboard:** [Link]
- **Related PRDs:** [Links to feature PRDs]
