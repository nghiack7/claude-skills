# Reflect Skill v2.0 - Implementation Plan

## Vision

Tạo một hệ thống học tập liên tục cho Claude Code, kết hợp tinh túy từ:

- **claude-reflect**: Hook-based capture, semantic validation, skill routing
- **claude-diary**: Structured diary, rule violation detection, processed tracking
- **continuous-learning**: Skill extraction, quality gates, web research
- **Academic research**: Reflexion pattern, delta updates, meta-evolution

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         REFLECT v2.0                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   EXTRACT    │───►│   ANALYZE    │───►│   APPLY      │          │
│  │  (sessions)  │    │  (AI-based)  │    │  (updates)   │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│         │                   │                   │                   │
│         ▼                   ▼                   ▼                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │ Session Data │    │  Patterns:   │    │ Outputs:     │          │
│  │ - Turns      │    │ - Corrections│    │ - CLAUDE.md  │          │
│  │ - Tools      │    │ - Friction   │    │ - Skills     │          │
│  │ - Thinking   │    │ - Preferences│    │ - Diary      │          │
│  │ - Skills     │    │ - Successes  │    │              │          │
│  │ - Agents     │    │ - Violations │    │              │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## File Structure

```
~/.claude/skills/reflect/
├── SKILL.md                    # Main skill definition
├── IMPLEMENTATION_PLAN.md      # This file
├── scripts/
│   ├── extract-session.ts      # ✅ Done - Session extraction
│   ├── get-project-path.ts     # ✅ Done - Path utilities
│   └── project-tree.ts         # ✅ Done - Project listing
└── memory/                     # New: Persistent memory
    ├── diary/                  # Session diaries
    ├── reflections/            # Reflection summaries
    └── processed.json          # Tracking processed sessions
```

## Implementation Phases

### Phase 1: Enhanced Extraction (extract-session.ts)

**Status**: ✅ Mostly done, needs minor additions

**Improvements needed**:

1. Add diary-style structured output format
2. Track processed sessions in `memory/processed.json`
3. Better thinking block extraction for analysis

**Key code changes**:

```typescript
// Add to Session interface
interface Session {
  // ... existing fields
  diary?: DiaryEntry;
}

interface DiaryEntry {
  taskSummary: string;
  workDone: string[];
  designDecisions: string[];
  challenges: string[];
  solutions: string[];
  userPreferences: string[];
}

// Add processed tracking
interface ProcessedTracker {
  sessions: {
    [sessionId: string]: {
      processedAt: string;
      reflectionFile?: string;
    };
  };
}
```

### Phase 2: AI-Powered Analysis (SKILL.md workflow)

**Status**: 🔄 Needs rewrite

**The key insight**: Don't try to programmatically analyze - let AI do it.

**New workflow in SKILL.md**:

```markdown
## Phase 2: Extract Sessions

Run extraction script, get clean data with full context.

## Phase 3: AI Analysis

AI reads extracted sessions and identifies:

### 3.1 Corrections (High Value)

- User saying "no", "not that", contradicting Claude
- Look in thinking blocks for wrong assumptions
- Extract: What Claude assumed vs What user wanted

### 3.2 Rule Violations (Critical)

- Check if existing CLAUDE.md rules were violated
- If yes → strengthen the rule, don't add new one
- Priority: Move to top, add emphasis, make explicit

### 3.3 Friction Points (Medium Value)

- Repeated requests, clarifications needed
- Signs of frustration
- Communication breakdowns

### 3.4 Preferences (High Value)

- Consistent patterns: language, tools, style
- Implicit preferences made explicit
- Project-specific vs global

### 3.5 Successes (Reference Value)

- What worked well
- Patterns to reinforce

### 3.6 Skill Candidates (New!)

- Discoveries worth preserving as skills
- Non-obvious solutions
- Reusable patterns
```

### Phase 3: Skill Extraction (New Feature)

**Inspiration**: continuous-learning-skill

**When to create a skill**:

1. Non-obvious debugging solution discovered
2. Project-specific pattern learned
3. Tool/API undocumented behavior found
4. Workflow optimization identified

**Skill template**:

```markdown
---
name: [descriptive-name]
description: |
  [Specific trigger conditions, error messages, scenarios]
  [What problem this solves]
  [When to use]
---

# [Skill Name]

## Problem

[What this skill addresses]

## Trigger Conditions

- [Exact error message or symptom]
- [Context when this applies]

## Solution

[Step-by-step]

## Verification

[How to confirm it worked]

## References

[If web research was done]
```

### Phase 4: Memory Persistence

**New directory**: `~/.claude/skills/reflect/memory/`

**Files**:

1. `diary/YYYY-MM-DD-session-N.md` - Structured diary entries
2. `reflections/YYYY-MM-reflection-N.md` - Reflection summaries
3. `processed.json` - Track what's been analyzed

**processed.json format**:

```json
{
  "version": 1,
  "sessions": {
    "session-id-1": {
      "project": "/path/to/project",
      "processedAt": "2026-01-18T12:00:00Z",
      "diaryFile": "diary/2026-01-18-session-1.md",
      "reflectionFile": "reflections/2026-01-reflection-1.md",
      "learningsApplied": 3
    }
  }
}
```

### Phase 5: Updated SKILL.md Workflow

**Complete new workflow**:

```markdown
## Quick Start

bun run scripts/extract-session.ts <project> --last 5 --verbose

## Workflow

### Phase 1: Setup

1. Get project path
2. Check for unprocessed sessions
3. Load existing CLAUDE.md rules (for violation detection)

### Phase 2: Extract

bun run scripts/extract-session.ts <project> --last N --verbose

### Phase 3: Analyze (AI does this)

Read extracted sessions. For each session:

A. **Identify Corrections**

- Look for: "no", "not that", "I meant", contradictions
- In thinking: wrong assumptions
- Extract: assumption → reality

B. **Check Rule Violations**

- Compare session with existing CLAUDE.md rules
- If violated → strengthen rule (don't add new)

C. **Find Friction Points**

- Repeated requests, frustration signals
- Why did communication break down?

D. **Discover Preferences**

- Language, tools, style patterns
- Implicit → explicit

E. **Note Successes**

- What worked smoothly
- Patterns to reinforce

F. **Evaluate Skill Candidates**

- Non-obvious discoveries
- Worth preserving for future?

### Phase 4: Synthesize

Present findings to user:
```

## Reflection: [Project]

### Critical: Rule Violations

[If any existing rules were violated]

- Rule: [existing rule]
- Violation: [what happened]
- Action: Strengthen rule → [new text]

### Corrections Found

- [Assumption]: Claude thought X
- [Reality]: User wanted Y
- [Proposed rule]: [specific actionable rule]

### Preferences Discovered

- [Preference]: [evidence]

### Skill Candidates

- [Discovery]: [brief description]
- Worth creating skill? [yes/no + reasoning]

### Proposed CLAUDE.md Updates

[Specific bullet points to add]

```

### Phase 5: Apply (with approval)
1. Ask user which to apply
2. Update CLAUDE.md (strengthen rules first, then add new)
3. Create skills if approved
4. Write diary entry
5. Mark sessions as processed
```

## Key Design Decisions

### 1. AI-First Analysis

- **Don't** try to regex/programmatically detect patterns
- **Do** extract clean data, let AI analyze semantically
- **Why**: AI understands context, nuance, multiple languages

### 2. Rule Violation Priority

- **Don't** add new rule if existing rule was violated
- **Do** strengthen the violated rule first
- **Why**: Fewer, stronger rules > many weak rules

### 3. Skill Extraction Selectivity

- **Don't** create skill for every discovery
- **Do** apply quality gates: reusable? non-trivial? verified?
- **Why**: Skill library should be high-signal

### 4. Delta Updates

- **Don't** rewrite entire CLAUDE.md
- **Do** make incremental, targeted changes
- **Why**: Preserve existing structure, minimize disruption

### 5. Processed Tracking

- **Don't** re-analyze sessions already processed
- **Do** track what's been analyzed
- **Why**: Efficiency, avoid duplicate learnings

## Migration from Current State

### Current files to keep:

- `extract-session.ts` - enhance, don't replace
- `get-project-path.ts` - keep as-is
- `project-tree.ts` - keep as-is

### Files to remove:

- None (we already removed analyze-patterns.ts)

### New files to create:

- `memory/processed.json` - tracking
- Update `SKILL.md` - new workflow

## Implementation Order

1. **Update extract-session.ts**
   - Add diary output format option
   - Better structure for AI analysis

2. **Create memory directory structure**
   - `mkdir -p memory/{diary,reflections}`
   - Create `processed.json`

3. **Rewrite SKILL.md**
   - New 5-phase workflow
   - AI analysis guidelines
   - Skill extraction criteria
   - Rule violation handling

4. **Test on real project**
   - Run full workflow
   - Validate outputs

## Success Criteria

1. **Extraction**: Clean, complete session data
2. **Analysis**: AI finds meaningful patterns
3. **Skill extraction**: High-quality, reusable skills
4. **Rule updates**: Stronger, not more numerous
5. **Memory**: Sessions tracked, no re-analysis

## Notes

- This plan synthesizes research from multiple sources and academic papers.
- Implementation can begin from a new session using this file as a guide.
