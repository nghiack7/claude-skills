---
name: technical-research
description: This skill should be used when the user asks to "create technical research", "write technology evaluation", "tạo technical research", "viết báo cáo nghiên cứu kỹ thuật", "evaluate technology", "compare tools", "select tech stack", "choose database", "compare frameworks", "pick a language", "chọn công nghệ", "so sánh framework", or needs a technical research template for engineering decisions.
---

# Technical Research: [Technology/Pattern/Tool Name]


## Executive Summary

### Research Question

**Primary Question:**
[What technical question are we trying to answer?]

**Why Now:**
[Why is this research needed at this time?]

**Decision Timeline:**
[When do we need to make a decision based on this research?]

### Key Findings

1. **[Finding 1]:** [Brief description and technical impact]
2. **[Finding 2]:** [Brief description and technical impact]
3. **[Finding 3]:** [Brief description and technical impact]

### Recommendation

**Recommended Option:** [Option Name]

**Confidence Level:** High|Medium|Low

**Rationale (1-2 sentences):**
[Why this is the best technical choice]

### Next Steps

- [ ] **[Next step 1]** (e.g., "Create ADR documenting decision")
- [ ] **[Next step 2]** (e.g., "Build POC to validate approach")
- [ ] **[Next step 3]** (e.g., "Present to architecture review board")


## Research Context

### Background & Motivation

**Current Situation:**
[What is the current technical state?]

**Problem Statement:**
[What technical problem are we trying to solve?]

**Motivation:**
[Why is this research important?]

### Scope

**In Scope:**
- [What this research covers]
- [Technologies/patterns being evaluated]

**Out of Scope:**
- [What this research does NOT cover]

### Constraints

**Technical Constraints:**
- [Constraint 1, e.g., "Must integrate with existing PostgreSQL"]
- [Constraint 2, e.g., "Must support TypeScript"]

**Business Constraints:**
- [Budget limit]
- [Timeline requirement]
- [Team capacity/expertise]


## Evaluation Criteria

### Prioritized Criteria

| Criterion | Weight | Description | Why Important |
|-----------|--------|-------------|---------------|
| **Performance** | 30% | Query speed, throughput, latency | [Justification] |
| **Developer Experience** | 25% | Learning curve, documentation, tooling | [Justification] |
| **Cost** | 20% | Licensing, infrastructure, maintenance | [Justification] |
| **Integration** | 15% | Ease of integration with existing stack | [Justification] |
| **Security** | 10% | Security features, compliance, audit | [Justification] |

### Deal Breakers (Must Haves)

- [Must have 1, e.g., "Must support transactions"]
- [Must have 2, e.g., "Must have TypeScript support"]
- [Must have 3, e.g., "Must be actively maintained"]


## Options Evaluated

### Option A: [Technology/Tool Name]

**Description:**
[What is this technology/tool?]

**How It Works:**
[Technical overview of how it operates]

**Maturity:**
- **Current Version:** [Version number]
- **Stability:** [Alpha|Beta|Stable|Mature]
- **Community:** [Size and activity level]

**Pros:**
- [Advantage 1]
- [Advantage 2]
- [Advantage 3]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Technical Fit:**
- **Integration Complexity:** Low|Medium|High
- **Learning Curve:** Low|Medium|High
- **Migration Effort:** [Estimate]


### Option B: [Technology/Tool Name]

**Description:**
[Overview]

**Pros:**
- [Advantages]

**Cons:**
- [Disadvantages]

**Technical Fit:**
- [Compatibility assessment]


### Option C: Status Quo (Current Solution)

**Description:**
[What we're using today]

**Why Consider Changing:**
- [Pain point 1]
- [Limitation 1]

**Why Stay:**
- [Benefit 1: No migration cost]
- [Benefit 2: Team knows it well]

**Cost of Not Changing:**
[What it costs to stick with current solution]


## Technical Evaluation

### Performance Benchmarks

| Metric | Option A | Option B | Current |
|--------|----------|----------|---------|
| **Query latency (p50)** | Xms | Yms | Nms |
| **Query latency (p99)** | Xms | Yms | Nms |
| **Throughput (ops/sec)** | X | Y | N |
| **Memory usage** | XMB | YMB | NMB |

### Scalability Analysis

| Option | Approach | Complexity | Notes |
|--------|----------|------------|-------|
| Option A | [Sharding/Replication/etc] | Low/Med/High | [Details] |
| Option B | [Approach] | [Level] | [Details] |

### Developer Experience

| Option | Easy to Start | Mastery Time | Documentation Quality |
|--------|---------------|--------------|----------------------|
| Option A | 1-5 rating | [X weeks/months] | Excellent/Good/Poor |
| Option B | [Rating] | [Time] | [Quality] |


## Integration Analysis

### Integration with Existing Stack

**Option A:**
- **Backend (Node.js/Bun):** [Integration approach]
- **Database:** [Compatibility]
- **Monitoring:** Grafana / Coroot
- **CI/CD:** GitLab CI

**Integration Complexity:** Low|Medium|High

**Migration Path:**
1. [Step 1]
2. [Step 2]
3. [Step 3]


## Security Analysis

### Security Features

| Feature | Option A | Option B | Current |
|---------|----------|----------|---------|
| **Authentication** | Yes/No | Yes/No | Yes/No |
| **Encryption at rest** | Yes/No | Yes/No | Yes/No |
| **Encryption in transit** | Yes/No | Yes/No | Yes/No |
| **Audit logging** | Yes/No | Yes/No | Yes/No |


## Cost Analysis

### Initial Costs

| Cost Category | Option A | Option B | Current |
|---------------|----------|----------|---------|
| **Licensing** | $X | $Y | $N |
| **Infrastructure setup** | $X | $Y | $N |
| **Development time** | $X (Y hours) | $Y | $N |
| **Training** | $X | $Y | $N |
| **TOTAL (Year 1)** | **$X** | **$Y** | **$N** |

### Total Cost of Ownership (3 Years)

| Option | Year 1 | Year 2 | Year 3 | **3-Year Total** |
|--------|--------|--------|--------|------------------|
| Option A | $X | $Y | $Z | **$T** |
| Option B | $X | $Y | $Z | **$T** |
| Current | $X | $Y | $Z | **$T** |


## Trade-offs Matrix

### Comparison Summary

| Criterion | Weight | Option A | Option B | Current |
|-----------|--------|----------|----------|---------|
| **Performance** | 30% | 9/10 | 7/10 | 5/10 |
| **Developer Experience** | 25% | 8/10 | 6/10 | 7/10 |
| **Cost** | 20% | 6/10 | 8/10 | 9/10 |
| **Integration** | 15% | 7/10 | 9/10 | 10/10 |
| **Security** | 10% | 9/10 | 8/10 | 8/10 |
| **WEIGHTED SCORE** | 100% | **7.9** | **7.4** | **7.3** |


## Proof of Concept Results

### POC Scope

**What We Built:**
[Description of POC implementation]

**Duration:** [X weeks]

### POC Findings

**Option A POC:**
- **What worked well:** [Positive findings]
- **What was challenging:** [Issues encountered]
- **Surprises:** [Unexpected discoveries]

### POC Metrics

| Metric | Target | Option A Actual | Option B Actual |
|--------|--------|-----------------|-----------------|
| **Setup time** | <4 hours | X hours | Y hours |
| **Performance** | <100ms | Xms | Yms |
| **Developer satisfaction** | 8/10 | X/10 | Y/10 |


## Recommendation

### Recommended Option: [Option A]

**Rationale:**
[Detailed explanation of why this is the best technical choice given all the trade-offs]

**Why This Over Others:**
- **Not Option B** because: [Specific technical reason]
- **Not Status Quo** because: [Why we need to change]

### What We're Accepting

**Trade-offs We're Making:**
1. [Trade-off 1]: [Why it's acceptable]
2. [Trade-off 2]: [Why it's acceptable]

### Implementation Approach

**Timeline:**
- **Phase 1 (Weeks 1-2):** [Setup and initial integration]
- **Phase 2 (Weeks 3-4):** [Core implementation]
- **Phase 3 (Weeks 5-6):** [Testing and refinement]
- **Phase 4 (Week 7+):** [Rollout and monitoring]

**Success Criteria:**
- [ ] [Criterion 1: Performance meets targets]
- [ ] [Criterion 2: Team can maintain it]
- [ ] [Criterion 3: Integrates smoothly]


## Next Steps

### Immediate Actions (This Sprint)

- [ ] **Create ADR** - Document final decision - Owner: [Name] - Due: [Date]
- [ ] **Get stakeholder approval** - Architecture review - Owner: [Name] - Due: [Date]

### Short-term Actions (Next Month)

- [ ] **Set up development environment** - Install and configure
- [ ] **Create integration plan** - Detailed implementation steps
- [ ] **Team training** - Upskill team on new technology


## Appendices

### A. References & Resources

**Official Documentation:**
- [Option A Docs]: [Link]
- [Option B Docs]: [Link]

**Community Resources:**
- [Tutorial/Blog]: [Link]


## Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| YYYY-MM-DD | 1.0 | Initial research completed | [Name] |
| YYYY-MM-DD | 1.1 | Added POC results | [Name] |


## Review & Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Tech Lead | [Name] | YYYY-MM-DD | Pending |
| Architect | [Name] | YYYY-MM-DD | Pending |
| Engineering Manager | [Name] | YYYY-MM-DD | Pending |

---

*This technical research follows the AI-DLC principle of "AI proposes, human validates." Research findings inform architectural decisions documented in ADRs.*
