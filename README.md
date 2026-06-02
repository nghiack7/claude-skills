# claude-skills

> A curated collection of **85 Agent Skills** for [Claude Code](https://claude.com/claude-code) — and any harness that reads the open [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) format (Codex, Cursor, Gemini CLI, OpenCode).

Each skill is a self-contained folder with a `SKILL.md` (trigger-rich description + instructions) and, where useful, bundled reference docs and scripts. Skills load **progressively** — only the matching skill's instructions enter context, so you can keep them all installed at once.

Every skill is **universal** — no private services, no single-vendor lock-in. All examples use placeholders (`<AWS_ACCOUNT_ID>`, `your-org.atlassian.net`, …). Many ship **bilingual triggers (English + Vietnamese)**.

## Install

**As a plugin marketplace (recommended):**
```
/plugin marketplace add nghiack7/claude-skills
/plugin install claude-skills@claude-skills
```

**Or load directly without installing:**
```bash
git clone https://github.com/nghiack7/claude-skills.git
claude --plugin-dir ./claude-skills
```

**Or copy individual skills:**
```bash
cp -r claude-skills/skills/<skill-name> ~/.claude/skills/
```

## Skills (85)

| Category | Count |
|---|---|
| [🧩 Engineering & Code](#engineering--code) | 17 |
| [☁️ Cloud, Infra & DevOps](#cloud-infra--devops) | 15 |
| [🗄️ Data, Databases & Analytics](#data-databases--analytics) | 7 |
| [📐 Architecture & Technical Docs](#architecture--technical-docs) | 13 |
| [📊 Product & Planning](#product--planning) | 16 |
| [✍️ Writing, Content & Media](#writing-content--media) | 6 |
| [🔌 SaaS & Productivity Integrations](#saas--productivity-integrations) | 5 |
| [🧠 Meta, Thinking & Workflow](#meta-thinking--workflow) | 6 |

### 🧩 Engineering & Code

| Skill | What it does |
|---|---|
| **`bun-fullstack-setup`** | This skill should be used when the user asks to "create a fullstack app", "setup Bun server", "configure single port server", "add Vite proxy", "setup monorepo", "configure Docker for Bun", or mention… |
| **`code-review`** | Comprehensive code review using static analytics and multiple specialized agents in parallel… |
| **`debug`** | This skill should be used when the user asks to "debug", "fix bug", "fixbug", "investigate error", "troubleshoot", "why is this broken", "not working", "failing test", "unexpected behavior", or encoun… |
| **`dispatching-parallel-agents`** | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| **`gitflow`** | This skill should be used when the user asks to "start feature", "create hotfix", "finish feature", "start release", "start bugfix", "merge to develop", "merge to master", "git flow init", "accept MR"… |
| **`golang-mastery`** | This skill should be used when the user asks to "write Go code", "review Go code", "refactor Go", "Go best practices", "Go concurrency", "Go error handling", "Go testing", "gRPC server", or mentions G… |
| **`golangci-lint`** | This skill should be used when the user asks to "lint Go code", "lint changed code", "lint PR", "fix lint errors", "fix golangci-lint config", or mentions golangci-lint, Go linting… |
| **`karpathy-guidelines`** | Behavioral guidelines to reduce common LLM coding mistakes… |
| **`plan`** | This skill should be used when the user asks to "plan implementation", "how should I implement", "approach", "strategy", or needs a concrete implementation plan with files, changes, and risks… |
| **`react-minimal-effects`** | This skill should be used when the user has multiple useEffect calls, derived state via effect+setState, effect chains, polling patterns, or asks about React 19 patterns, React Compiler, useActionStat… |
| **`scalability-design`** | This skill should be used when the user asks to "optimize performance", "scale the system", "handle more traffic", "reduce latency", "capacity planning", or mentions scalability design, load balancing… |
| **`technical-analysis`** | This skill should be used when the user asks to "analyze this codebase", "trace the data flow", "understand the architecture", "how does this feature work", "deep dive into code", or needs systematic … |
| **`test-driven-development`** | Use when implementing any feature or bugfix, before writing implementation code |
| **`tui`** | This skill should be used when the user asks to "build a TUI", "create terminal UI", "interactive debugger", "Bubbletea app", or mentions terminal UI, TUI tools, Bubbletea, or interactive monitoring d… |
| **`verification-before-completion`** | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence… |
| **`worktree`** | This skill should be used when the user asks to "create a worktree", "sync worktree", "spotlight preview", "manage worktrees", "parallel development", or mentions worktree, spotlight, sync commits… |
| **`xstate-v5-strict`** | Implement, refactor, and review XState v5 state machines in TypeScript with strict setup().createMachine() ruleset, design-first planning, params-first typing, anti-god-machine enforcement, and canoni… |

### ☁️ Cloud, Infra & DevOps

| Skill | What it does |
|---|---|
| **`aws`** | Expert guidance for AWS CLI operations with SSO authentication… |
| **`cloudflare`** | This skill should be used when the user asks to "create Worker", "deploy to Pages", "configure KV", "setup D1", "manage R2 bucket", "configure WAF", "setup Tunnel", or mentions Cloudflare Workers, Pag… |
| **`coroot`** | This skill should be used when the user asks to "check cluster health", "view application status", "check SLO metrics", "investigate service latency", "debug K8s app", or mentions Coroot, service avai… |
| **`dagster`** | This skill should be used when the user asks to "check Dagster pipeline", "monitor Celery workers", "check SQS throughput", "view Flower dashboard", "webhook processing status", or mentions Dagster, C… |
| **`grafana`** | This skill should be used when the user asks to "create dashboard", "check Grafana alerts", "query Grafana API", "create service map", "draw data flow diagram", "build state diagram", "visualize archi… |
| **`grafana-diagram`** | This skill should be used when the user asks about "grafana diagram", "mermaid in grafana", "diagram panel", "binding data to diagram nodes", "grafana mermaid widget", "dynamic diagram", "data-driven … |
| **`infisical`** | This skill should be used when the user asks to "get Infisical secrets", "inject env vars", "export secrets", "infisical run", "missing secret", "check secret path", or mentions Infisical secret manag… |
| **`ios-device-debug`** | This skill should be used when the user asks to "debug on device", "deploy to iPhone", "get crash logs", "check device logs", "install on device", "run on phone", "pull crash report", "analyze crash"… |
| **`k8s-access`** | Expert guidance for per-session Kubernetes access setup with thread/session isolation… |
| **`kubectl`** | Expert guidance for Kubernetes cluster operations with kubectl and GitOps (FluxCD/ArgoCD)… |
| **`monitoring-observability`** | This skill should be used when the user asks to "set up monitoring", "add metrics", "configure logging", "implement tracing", "define SLO", or mentions RED method, USE method, observability design, al… |
| **`otel`** | This skill should be used when the user asks to "add tracing", "instrument Lambda", "debug performance", "query traces", "set up OpenTelemetry", or mentions OTel, distributed tracing, span attributes… |
| **`rollout-status`** | Expert guidance for tracing end-to-end deployment pipeline status… |
| **`sqs-concurrency`** | Expert guidance for analyzing and safely adjusting SQS Lambda consumer concurrency… |
| **`temporal`** | This skill should be used when the user asks to "run backfill", "trigger Temporal workflow", "start workflow", "check workflow status", or mentions Temporal, workflow execution, or backfill operations… |

### 🗄️ Data, Databases & Analytics

| Skill | What it does |
|---|---|
| **`amplitude`** | Use when the user asks to "query Amplitude", "export events", "analyze user activity", "download cohort", "get user profile", "check product analytics", or mentions Amplitude, user behavior, event ana… |
| **`bigquery`** | Use when the user asks to "query BigQuery", "analyze data warehouse", "check revenue metrics", "billing analytics", "ad insights query", or mentions BigQuery, data warehouse, business intelligence, or… |
| **`chart-generator`** | This skill should be used when the user asks to "generate a chart", "create a graph", "plot data", "make a bar chart", "draw a pie chart", "visualize data", or mentions matplotlib, data visualization… |
| **`cocoindex`** | This skill should be used when the user asks to "search knowledge", "find in docs", "query index", "semantic search", "update index", "rebuild index", "check index status", "cocoindex query", "cocoind… |
| **`intercom`** | Use when the user asks to "export Intercom conversations", "analyze support tickets", "query Intercom data", or mentions Intercom, ClickHouse conversation export, or customer support analytics… |
| **`mongodb`** | Expert guidance for querying MongoDB databases containing ad platform analytics and application data… |
| **`starrocks`** | This skill should be used when the user asks to "query StarRocks", "run OLAP query", "analyze data", "check analytics tables", or mentions StarRocks, OLAP, columnar analytics, or high-performance anal… |

### 📐 Architecture & Technical Docs

| Skill | What it does |
|---|---|
| **`adr`** | This skill should be used when the user asks to "tạo ADR", "viết ADR", "architecture decision", "quyết định kỹ thuật", "nên chọn X hay Y", "so sánh giải pháp", "trade-off analysis", "technical decisio… |
| **`api-spec`** | This skill should be used when the user asks to "create API spec", "write API specification", "tạo API spec", "viết tài liệu API", "document API", or needs an API specification template for engineerin… |
| **`architecture-doc`** | This skill should be used when the user asks to "create architecture doc", "write architecture document", "tạo tài liệu kiến trúc", "viết architecture doc", or needs an architecture documentation temp… |
| **`component-spec`** | This skill should be used when the user asks to "tạo component spec", "viết component specification", or needs a component specification template for product documentation. |
| **`data-model`** | This skill should be used when the user asks to "create data model", "write data model doc", "tạo data model", "viết tài liệu data model", "document database schema", or needs a data model template fo… |
| **`design-spec`** | This skill should be used when the user asks to "tạo design spec", "viết design specification", or needs a design specification template for product documentation. |
| **`doc-writer`** | This skill should be used when the user asks to "analyze codebase", "map architecture", "understand this project", "document architecture", "explore codebase", "what does this codebase do", "codebase … |
| **`folder-readme`** | This skill should be used when the user asks to "tạo README cho folder", "folder documentation", or needs a folder README template for documentation structure. |
| **`gherkin-refine`** | This skill should be used when the user asks to "refine requirements", "write acceptance criteria", "clarify requirements", "use gherkin format", or mentions gherkin, BDD, Given/When/Then… |
| **`project-context`** | This skill should be used when the user asks to "create project context", "write project context", "project background", or needs a project context template for product documentation and team alignmen… |
| **`security-doc`** | This skill should be used when the user asks to "create security doc", "write security documentation", "tạo tài liệu bảo mật", "viết security doc", "document security vulnerability", "security assessm… |
| **`tech-stack-selection`** | This skill should be used when the user asks to "evaluate technology", "compare frameworks", "choose a database", "pick a language", "select tech stack", or needs structured criteria for technology ev… |
| **`technical-research`** | This skill should be used when the user asks to "create technical research", "write technology evaluation", "tạo technical research", "viết báo cáo nghiên cứu kỹ thuật", "evaluate technology", "compar… |

### 📊 Product & Planning

| Skill | What it does |
|---|---|
| **`acceptance-criteria`** | This skill should be used when the user asks to "tạo acceptance criteria", "viết tiêu chí chấp nhận", "define acceptance criteria", or needs acceptance criteria for product documentation. |
| **`dibb`** | This skill should be used when the user asks to "tạo DIBB", "viết DIBB", "DIBB framework", "data insight belief bet", or needs a DIBB (Data-Insight-Belief-Bet) template for strategy documentation. |
| **`faq`** | This skill should be used when the user asks to "tạo FAQ", "viết FAQ", "frequently asked questions", or needs an FAQ template for product documentation. |
| **`feature-statement`** | This skill should be used when the user asks to "define feature", "feature scope", "feature definition", "mô tả tính năng", "describe feature", "feature overview", or needs a Feature Statement templat… |
| **`gtm-plan`** | This skill should be used when the user asks to "tạo GTM plan", "go-to-market plan", "kế hoạch ra mắt", or needs a go-to-market plan template for product launches. |
| **`market-research`** | This skill should be used when the user asks to "nghiên cứu thị trường", "market research", "competitive analysis", or needs a market research template for product documentation. |
| **`one-pager`** | This skill should be used when the user asks to "tạo one-pager", "viết proposal", or needs a One-Pager template for product documentation. |
| **`prd`** | This skill should be used when the user asks to "tạo PRD", "viết PRD", "product requirements", or needs a Product Requirements Document template for product documentation. |
| **`problem-statement`** | This skill should be used when the user asks to "problem statement", "phát biểu vấn đề", "define the problem", "xác định vấn đề", "what problem are we solving", "vấn đề cần giải quyết", or needs a Pro… |
| **`resource-plan`** | This skill should be used when the user asks to "tạo resource plan", "kế hoạch nguồn lực", "staffing plan", or needs a resource plan template for project planning. |
| **`roadmap`** | This skill should be used when the user asks to "tạo roadmap", "viết lộ trình", "product roadmap", or needs a roadmap template for product planning. |
| **`use-case`** | This skill should be used when the user asks to "tạo use case", "viết use case", "user scenario", or needs a use case template for product documentation. |
| **`user-journey`** | This skill should be used when the user asks to "tạo user journey", "hành trình người dùng", "customer journey map", or needs a user journey template for UX documentation. |
| **`user-persona`** | This skill should be used when the user asks to "tạo user persona", "chân dung người dùng", "customer persona", or needs a user persona template for product documentation. |
| **`user-story`** | This skill should be used when the user asks to "tạo user story", "viết user story", "as a user I want", or needs a user story template for product documentation. |
| **`wireframe`** | This skill should be used when the user asks to "tạo wireframe", "viết wireframe spec", "UI wireframe", or needs a wireframe specification template for design documentation. |

### ✍️ Writing, Content & Media

| Skill | What it does |
|---|---|
| **`epub-packing`** | This skill should be used when the user asks to "create an ebook", "convert Markdown to EPUB", "generate EPUB", "package articles for offline reading", or mentions epub, ebook, e-reader, kindle… |
| **`meeting-notes`** | This skill should be used when the user asks to "tạo meeting notes", "ghi chú cuộc họp", "meeting minutes", or needs a meeting notes template for documentation. |
| **`neobrutalism`** | This skill should be used when the user asks to "apply neobrutalism", "create brutalist design", "add bold borders", "use hard shadows", or mentions neobrutalism, brutalist, bold design, high-contrast… |
| **`release-notes`** | This skill should be used when the user asks to generate "release notes", "changelog", "what changed", "generate changelog", "create changelog", "write release notes", "version notes", or needs to cre… |
| **`remove-bg`** | This skill should be used when the user asks to "remove background", "make image transparent", "create transparent PNG", "cutout image", or mentions bgrem, rembg, transparent PNG… |
| **`youtube`** | This skill should be used when the user asks to "search YouTube", "get video transcript", "summarize video", "extract subtitles", or mentions YouTube, video search, captions, yt-dlp, or provides youtu… |

### 🔌 SaaS & Productivity Integrations

| Skill | What it does |
|---|---|
| **`confluence`** | This skill should be used when the user asks to "search Confluence", "find spec on Confluence", "read Confluence page", "create Confluence page", "update Confluence", "publish ADR to Confluence", "pos… |
| **`google`** | Manages Google Calendar and Gmail… |
| **`google-chat`** | Manages Google Chat messages and spaces… |
| **`jira`** | This skill should be used when the user asks to "get Jira issue", "search Jira", "create Jira ticket", "update issue", "list sprints", "get active sprint", "transition issue", "add comment", "check Ji… |
| **`tanca`** | This skill should be used when the user asks to "check attendance", "list employees", "check-in", "check-out", "view shifts", "sync Tanca", "approve requests", "reject requests", "pending requests", "… |

### 🧠 Meta, Thinking & Workflow

| Skill | What it does |
|---|---|
| **`claude-manager`** | This skill should be used when the user asks to "manage skills", "disable skills", "enable skills", "reduce skill clutter", "analyze usage", "apply preset", or mentions starting work on a specific pro… |
| **`job-description`** | This skill should be used when the user asks to "tạo JD", "viết job description", "mô tả công việc", or needs a job description template for recruitment. |
| **`mental-models`** | This skill should be used when the user faces complex decisions, problem-solving, debugging, system design, strategic thinking, or needs structured reasoning… |
| **`mermaid`** | Render and share Mermaid diagrams as image URLs via mermaid.ink (or locally)… |
| **`reflect`** | This skill should be used when the user asks to "reflect", "what did we learn", "save this knowledge", "extract learnings", "update CLAUDE.md from session", or wants to evaluate a completed session an… |
| **`workflow`** | This skill should be used when the user asks about "workflow", "quy trình", "solution template", "viết solution", "commit format", "branch naming", "implementation doc", "docs/stories", "tạo solution"… |

## Quality & conventions

Every skill follows Anthropic's [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

- **Trigger-rich descriptions** in third person — the load-bearing field Claude uses to pick a skill.
- **Progressive disclosure** — `SKILL.md` stays lean; deeper material lives in one-level `references/` files.
- **Bundled scripts** for deterministic operations instead of regenerated code.
- **Universal & secret-free** — works for any project; no private endpoints, credentials, or vendor lock-in.

## Contributing

PRs welcome — new skills, fixes, better examples. One skill per folder, follow the frontmatter conventions, keep every skill universal, and never commit real credentials, internal hostnames, or customer data.

## License

[MIT](./LICENSE) © nghiack7
