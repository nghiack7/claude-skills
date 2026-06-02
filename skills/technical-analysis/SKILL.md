---
name: technical-analysis
description: This skill should be used when the user asks to "analyze this codebase", "trace the data flow", "understand the architecture", "how does this feature work", "deep dive into code", or needs systematic technical investigation of code logic, data flow, or system architecture.
---

## Related Skills

- **codebase** - Repository management and cloning
- **domain-boundary** - Service ownership mapping

# Technical Analysis Skill

Expert guidance for conducting deep technical analysis of the codebase to understand implementation details, architecture patterns, data flow, and business logic.


## What Is Technical Analysis?

Technical analysis investigates and documents how a feature, component, or system is currently implemented in the codebase. It produces a comprehensive document in `knowledge/04-technical/analysis/` that answers:

- How does this feature work?
- What's the data flow from UI to backend?
- Which files and components are involved?
- What architecture patterns are used?
- What are the gaps, risks, and complexity?

**Key Distinction:** This analyzes **existing code** in `codebase/`. For technology evaluation (databases, libraries), use `04-technical/research/` instead.

## When to Use This Skill

**Use technical analysis when you need to:**
- Understand existing implementations before making changes
- Analyze codebase for Jira stories (e.g. PROJ-XXXX)
- Investigate bugs or performance issues
- Plan refactoring or migration
- Document system architecture
- Assess implementation complexity

**Don't use for:**
- Creating new features (use Spec-Kit `.specify/`)
- Business/market research (use `01-strategy/research/`)
- Technology evaluation (use `04-technical/research/`)

## Two-Phase Workflow

**Why two phases?**
Deep codebase analysis can miss important areas without clear direction. Two phases ensure focused, thorough investigation with strategic planning:

1. **Phase 1 (Plan)** - Enhanced exploration (60 sec) generates analysis file with:
   - Investigation strategy (objectives, success criteria, scope)
   - Prioritized investigation roadmap (P0/P1/P2 phases with dependencies)
   - Risk assessment and complexity estimation
   - Hypothesis and validation plan
   - Structured research tasks (not just TODO markers)

2. **User Reviews** - Review the plan, adjust priorities, clarify questions, refine scope

3. **Phase 2 (Execute)** - Systematic deep research (5-15 min) that:
   - **Updates the same file** (not create new one)
   - Follows investigation roadmap sequentially
   - Replaces task markers with actual findings and code references
   - Checks off tasks as completed
   - Updates confidence levels based on evidence

**CRITICAL:** Phase 2 updates the existing file from Phase 1. The file acts as a living document - Phase 1 creates an executable plan, Phase 2 executes it and documents findings.

### Agent Strategy

**Phase 1 (Plan):** Run directly in main context — needs user interaction for scope refinement.

**Phase 2 (Execute):** Delegate to parallel agents for deep investigation:
- Use `oh-my-claudecode:explore` agents to trace execution paths across repos (one agent per repo/module)
- Use `oh-my-claudecode:architect` agent for architecture pattern analysis
- Use `oh-my-claudecode:scientist` agent for data flow mapping and dependency analysis
- Synthesize findings from all agents into the analysis document

Example delegation for multi-repo analysis:
```
Agent 1 (code-explorer): "Trace order sync flow in codebase/your-project/integrationfns"
Agent 2 (code-explorer): "Trace order processing in codebase/your-project/orderfns"
Agent 3 (architect): "Map interfaces and contracts between integrationfns and orderfns"
```

> For single-repo analysis, run Phase 2 directly. For cross-repo or system-wide analysis, use parallel agents.

## Commands

| Phase | Command | When | Output |
|-------|---------|------|--------|
| **1. Plan** | `/tech.analysis-plan [topic]` | Start of investigation | Analysis file with investigation strategy, prioritized roadmap (P0/P1/P2), risk assessment, hypothesis, structured tasks |
| **2. Execute** | `/tech.analysis-execute [file-path]` | After reviewing Phase 1 plan | Completed analysis with findings, code samples, data flows, risks - following the roadmap systematically |

### Examples

```bash
# Jira story
/tech.analysis-plan PROJ-6129
# Review plan, adjust priorities, clarify questions
/tech.analysis-execute knowledge/04-technical/analysis/2025-10-30-analysis-PROJ-6129.md

# Feature
/tech.analysis-plan payment-fees
# Review investigation roadmap and success criteria
/tech.analysis-execute knowledge/04-technical/analysis/2025-10-30-analysis-payment-fees.md

# System architecture
/tech.analysis-plan auth-system
# Review multi-repo investigation strategy
/tech.analysis-execute knowledge/04-technical/analysis/2025-10-30-analysis-auth-system.md
```

## Integration with Other Systems

### Standard Flows

**Jira → Analysis → Spec:**
1. Jira story created (PROJ-XXXX)
2. `/tech.analysis-plan PROJ-XXXX` (create investigation plan)
3. Review plan, adjust priorities and scope
4. `/tech.analysis-execute` (execute systematic deep dive)
5. Create Spec-Kit spec for implementation
6. Link documents bidirectionally

**Analysis → PRD:**
When analysis reveals missing features, create PRD and link it.

**Analysis → ADR:**
When analysis reveals architectural decisions needed, create ADR.

**Analysis → Spec-Kit:**
Analysis documents current state → Spec documents desired state.

### Relationships

```yaml
# In analysis file
relationships:
  analyzes:
    - path: "codebase/[path]/"  # What code is analyzed
  implements:
    - path: "knowledge/02-requirements/prd/..."  # What PRD it supports
  informs:
    - path: ".specify/specs/NNN-feature/spec.md"  # What spec it informs
```


## What to Expect

### Phase 1 Output (60 seconds)
- Analysis file created with complete template structure
- **"Analysis Plan" section filled with:**
  - Clear objectives and success criteria
  - Investigation strategy (primary/secondary focus, out of scope)
  - Risk assessment with mitigation strategies
  - Resource estimation (time, complexity, files)
  - Prioritized investigation roadmap (P0/P1/P2 phases with dependencies)
  - Research questions by priority (Critical/Important/Nice-to-Have)
  - Hypothesis about expected findings
  - Validation plan with confidence thresholds
- **Structured investigation task markers** in template sections (not just TODOs)
- Light file path information and technology stack notes
- **NOT detailed findings yet** - just the plan to get them
- **Status:** `planning`, **Confidence:** `low`

### Phase 2 Output (5-15 minutes)
- **Same file updated** (not new file) with all sections filled
- Follows investigation roadmap systematically
- Investigation task markers replaced with actual findings
- Code samples with file:line references
- Complete data flow documentation with sequence diagrams
- Architecture patterns identified and documented
- Gap analysis, risk assessment, complexity estimate
- Tasks checked off as completed
- **Status:** `in-progress` → `completed`, **Confidence:** `medium` → `high`

## Security Compliance

Follows **codebase/ security rules**:
- ✅ Read code from `codebase/` for analysis
- ✅ Document findings in `knowledge/04-technical/analysis/` (safe to commit)
- ✅ Reference code with file:line format
- ❌ Never commit or push codebase files


## Related

- **Business Research:** `knowledge/01-strategy/research/` for market/user research
- **Technical Research:** `knowledge/04-technical/research/` for technology evaluation
- **Spec-Kit:** `.specify/` for implementing features
- **ADR:** `knowledge/06-decisions/adr/` for architectural decisions

**Version:** 1.0.0
**Last Updated:** 2025-10-30
