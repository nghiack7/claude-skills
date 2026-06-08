---
name: team-debate
description: Use when a decision has 2+ viable options and you want multiple AI CLIs (claude + cursor-agent + copilot) to argue them in parallel, then have Claude synthesize the arguments, put the call to a human, and record the outcome as an ADR (technical) or PRD (product). Triggers on "team debate", "debate this decision", "have the AIs argue", "which option is best", "decision gate", "pick the best option", or being invoked by the `specify` flow at a Specify/Plan decision gate. Distinct from `iterm-ai-team` (parallel IMPLEMENTATION); this is parallel DECISION-MAKING.
---

# Team Debate — multi-AI decision gate

A decision gate where several AI CLIs **argue the same decision in parallel**, Claude **judges** the
arguments, the **human makes the final call**, and the outcome is **recorded** (ADR or PRD). Use it
whenever a choice is consequential and reversible-but-costly: architecture, library, data model,
product scope, sequencing.

**Core idea — diversity then judgment then human.** Independent models surface different
risks/options than one model alone. Claude does not blindly average them; it weighs the arguments
against explicit criteria, then hands a human the decision with the tradeoffs laid out. Claude never
silently picks for the user on a gated decision.

**Always-visible by default — the human stays in control.** Every step of the debate is surfaced in
the UI as it happens, not hidden in background processes. Before each phase Claude announces what it
is about to do; while the CLIs run, their progress is visible (live panes by default); after each
phase Claude reports what came back. The user can watch each AI think, interrupt or kill any voice
mid-run, and steer the framing/criteria before the gate. Nothing material happens off-screen.

## When to use vs. not

- **Use** when: 2–4 genuinely viable options exist, the choice steers `what code gets written`, and a
  wrong pick is expensive to undo. This is the default at `specify`'s Specify (→PRD) and Plan (→ADR) gates.
- **Don't use** for trivial/reversible choices with an obvious default — just pick it and say so
  (see `[[kiss-over-premature-solid]]`). A debate on a one-line naming choice is theater.
- **Different skill:** `iterm-ai-team` fans out *implementation* across panes. This fans out
  *deliberation*. They compose — debate to decide, then iterm-ai-team to build.

## Prerequisites

```bash
scripts/detect-clis.sh   # shows which of claude / cursor-agent / copilot are installed
```
Need **≥2** voices for a real debate. If only `claude` is present it degrades to a monologue — say so
and consider just deciding directly. To add the third voice, install Cursor's CLI:
`curl https://cursor.com/install -fsS | bash` (the user runs this and logs in; `cursor-agent` lands on PATH).

> **Cost note:** `copilot -p` consumes GitHub Copilot AI credits (~7–9 per debate). Factor that in
> before running many debates; for trivial decisions, skip the debate (proportionality rule).

## Workflow

### 1. Frame the decision (Claude, before any CLI runs)
Do the homework first — read the repo/spec so options are real, not hypothetical. Produce:
- **One precise question.** ("Which message-delivery model for the camera-offline alert pipeline?")
- **2–4 concrete, mutually-exclusive options**, each with a one-line sketch.
- **Explicit evaluation criteria** ranked by weight (e.g. correctness > operational simplicity >
  cost > latency — honor the user's global "business correctness > performance" rule).
- **Hard constraints** the options must satisfy (existing conventions, contracts, deadlines).

### 2. Write the debate prompt file
One shared prompt to `/tmp/<slug>-debate/prompt.txt`. It MUST instruct each agent to:
- Score every option against each criterion (brief, e.g. 1–5 + one-line justification).
- Name the single biggest risk of its recommended option.
- End with `RECOMMENDATION: <option> — <one sentence why>`.
- Be concise (these are arguments, not essays) and **assume no file edits** — reasoning only.

### 3. Run the debate (parallel, **visible by default**)
Announce the voices and the prompt to the user *before* launching, so they can veto or amend.

**Default — live panes the user can watch and control.** Launch one visible pane per voice (reuse
`iterm-ai-team`'s `launch-pane.sh` with the same prompt file) so each AI's reasoning streams on
screen and the user can interrupt or kill any pane mid-run:
```bash
# launch-pane.sh <cli> <prompt-file> <log-file> <repo-dir> [vertical|horizontal]
d=/tmp/<slug>-debate; mkdir -p "$d/out"
for cli in claude cursor-agent copilot; do
  command -v "$cli" >/dev/null && \
    ~/.claude/skills/iterm-ai-team/scripts/launch-pane.sh "$cli" "$d/prompt.txt" "$d/out/$cli.md" "$PWD"
done
```
`launch-pane.sh` is terminal-agnostic — it splits via tmux when available (works in iTerm2, Ghostty,
Kitty, Terminal.app, SSH) and uses iTerm2's native AppleScript as a fast-path. Each pane tees its
transcript to `out/<cli>.md` and prints `>>> PANE FINISHED <<<` on exit. Tell the user which panes
opened (if tmux spun a detached session, give them `tmux attach -t ai-team` to watch) and that they
may stop any voice; poll the log files for the completion marker before synthesizing.

**Headless fallback** — only when no TTY/iTerm is available (CI, remote). State that you are falling
back and why, then:
```bash
scripts/run-debate.sh /tmp/<slug>-debate/prompt.txt /tmp/<slug>-debate/out
```
Even headless, report each voice's start and completion to the user as the script emits them — do not
go silent until the end. Transcripts land in `out/<cli>.md`; the script blocks until all finish.

### 4. Synthesize (Claude judges)
Read every transcript. Produce a tight synthesis, NOT a copy-paste:
- **Consensus** — what all voices agreed on.
- **Disagreement** — where they split and *why* (this is the valuable part).
- **Claude's weighted verdict** — best option against the ranked criteria, with the deciding factor
  and the top residual risk. Flag if the models converged for a *shallow* reason.

### 5. Human gate (mandatory — this is the point)
Put the call to the user with `AskUserQuestion`: options = the candidates, Claude's recommendation
first and labeled "(Recommended)", description = the one-line tradeoff. The human decides; Claude
does not proceed on a gated decision without it. Record any note the user adds.

### 6. Record the outcome
- **Technical** decision (architecture/library/data-model) → invoke the **`adr`** skill. Capture the
  chosen option, the rejected alternatives *with the debate's reasons*, and consequences.
- **Product** decision (scope/why/priority) → invoke the **`prd`** skill (or update the existing PRD).
- Either way, cite that a multi-AI debate informed it and list the voices. The artifact is the
  durable "why" six months later — `[[spec-driven-preference]]`.

## Hard rules

1. **Real options only.** Don't manufacture strawman alternatives to justify a foregone conclusion.
2. **Human owns the gated decision.** Synthesis informs; the user (or, if explicitly delegated,
   Claude with stated reasoning) decides. Never skip the gate silently.
3. **Judge, don't tally.** A 2-vs-1 split where the 1 is right still means the 1 is right — weigh
   arguments against criteria, not headcount.
4. **Verify claims.** If a voice asserts a fact about the repo/contract, confirm it before relying on
   it — agents hallucinate APIs and constraints.
5. **Keep it proportional.** Match debate depth to decision cost; don't gate a reversible trifle.
6. **Record or it didn't happen.** A gated decision with no ADR/PRD is a decision you'll relitigate.
7. **Show every step; the user can stop it.** Announce each phase before it runs, keep the CLIs'
   progress visible (live panes by default), and report results after. Never bury a running AI in a
   silent background task — the user must be able to watch and interrupt at any point.
