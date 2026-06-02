---
name: user-persona
description: 'This skill should be used when the user asks to "tạo user persona", "chân dung người dùng", "customer persona", or needs a user persona template for product documentation.'
---

---
document_type: "user-persona"
product_id: "prod-xxx"
version: "1.0.0"
status: "draft"
owner: "UX Researcher / Product Manager Name"
stakeholders: ["Product", "Design", "Marketing", "Engineering"]
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["persona", "user-research", "ux"]
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

# User Persona: [Persona Name]

**Persona Type:** Primary | Secondary | Tertiary

**Product:** [Product Name]

**Last Updated:** YYYY-MM-DD

**Based on:** [Number] interviews, [Number] surveys, [Data sources]

---

## 👤 Persona Overview

### Quick Summary

**Name:** [Persona Name - e.g., "Manager Mike", "Developer Dana"]

**Age:** [Age range]

**Role:** [Job title/role]

**Quote:** _"[A representative quote that captures their essence]"_

**Photo/Avatar:**
[Image or description]

---

## 📸 Demographics

### Basic Information

**Age range:** [25-35]

**Gender:** [M/F/Other/Not relevant]

**Location:** [City type: Urban/Suburban/Rural] | [Country/Region]

**Education:** [Highest level completed]

**Income:** [$X-$Y annually or N/A]

### Professional Background

**Job title:** [Specific title]

**Industry:** [Sector they work in]

**Company size:** [Startup / SMB / Mid-market / Enterprise]

**Years of experience:** [X-Y years]

**Reports to:** [Manager title]

**Manages:** [Team size or individual contributor]

### Technical Proficiency

**Tech-savviness:** Low | Medium | High | Expert

**Commonly used tools:**
- [Tool 1]
- [Tool 2]
- [Tool 3]

**Preferred platforms:**
- Desktop: [Windows/Mac/Linux]
- Mobile: [iOS/Android]
- Browser: [Chrome/Safari/Firefox/Edge]

---

## 🎯 Goals & Motivations

### Primary Goals

**Professional goals:**
1. **[Goal 1]**
   - Why: [Motivation]
   - Success looks like: [Outcome]

2. **[Goal 2]**
   - Why: [Motivation]
   - Success looks like: [Outcome]

3. **[Goal 3]**
   - Why: [Motivation]
   - Success looks like: [Outcome]

**Personal goals:**
1. [Personal goal 1]
2. [Personal goal 2]

### What Success Means to Them

**Short-term (This month):**
- [What they want to achieve]

**Medium-term (This quarter):**
- [What they want to achieve]

**Long-term (This year):**
- [What they want to achieve]

### Key Motivations

**Intrinsic motivators:**
- [What drives them internally - e.g., mastery, purpose]

**Extrinsic motivators:**
- [External motivations - e.g., promotion, recognition, bonus]

**Values:**
- [What they value most - e.g., efficiency, quality, collaboration]

---

## 😤 Pain Points & Frustrations

### Current Challenges

**Pain Point 1: [Problem]**

**Frequency:** Daily | Weekly | Monthly

**Severity:** Critical | High | Medium | Low

**Current workaround:**
[How they currently deal with this]

**Impact:**
- Time wasted: [X hours/week]
- Money cost: [$X/year]
- Emotional impact: [Frustration level]

**Quote:**
> "[What they said about this problem]"

---

**Pain Point 2: [Problem]**

**Frequency:** [How often]

**Severity:** [Impact level]

**Current workaround:**
[Their current solution]

**Impact:**
[Quantified impact]

---

**Pain Point 3: [Problem]**

**Details:**
[Description of the pain point and its impact]

---

### What Frustrates Them

**Deal-breakers:**
- [What would make them stop using a product]
- [What they absolutely won't tolerate]

**Pet peeves:**
- [Minor annoyances]
- [Things that irritate them]

---

## 🎨 Behavior Patterns

### Daily Routine

**Typical day:**

**6:00 AM - 9:00 AM:**
- [Morning routine]
- [Device usage]

**9:00 AM - 12:00 PM:**
- [Work activities]
- [Tools used]

**12:00 PM - 2:00 PM:**
- [Lunch/break activities]

**2:00 PM - 6:00 PM:**
- [Afternoon work]
- [Collaboration]

**6:00 PM - 10:00 PM:**
- [Evening activities]
- [Personal time]

### Product Usage Patterns

**How they discover new products:**
- [Discovery channel 1 - e.g., colleague recommendation]
- [Discovery channel 2 - e.g., Google search]
- [Discovery channel 3 - e.g., industry publication]

**How they evaluate products:**
1. [Evaluation step 1]
2. [Evaluation step 2]
3. [Evaluation step 3]

**Decision-making process:**
- **Research duration:** [X weeks]
- **Key evaluation criteria:**
  - [Criterion 1 with weight]
  - [Criterion 2 with weight]
  - [Criterion 3 with weight]
- **Decision makers involved:** [Who else influences the decision]

**Preferred purchase method:**
- Self-service | Sales-assisted
- Free trial | Demo first | Direct purchase
- Budget approval needed: Yes | No

**Adoption behavior:**
- Early adopter | Mainstream | Late majority | Laggard
- Willing to try beta features: Yes | No | Sometimes

---

## 💭 Psychographics

### Personality Traits

**Myers-Briggs (if applicable):** [INTJ/ESFP/etc.]

**Key characteristics:**
- [Trait 1 - e.g., analytical]
- [Trait 2 - e.g., detail-oriented]
- [Trait 3 - e.g., collaborative]

**Working style:**
- [Prefers to work: alone/in teams/hybrid]
- [Communication style: direct/diplomatic/casual]
- [Risk tolerance: conservative/moderate/aggressive]

### Attitudes & Beliefs

**About their work:**
- [Belief about their role]
- [Attitude toward their industry]

**About technology:**
- [Attitude toward new tools]
- [Belief about automation]
- [Preference for proven vs. cutting-edge]

**About change:**
- Change embracer | Cautious adopter | Change resistant

---

## 🛍️ Buying Behavior

### Decision-Making Process

**Buying committee:**
- Initiator: [Who identifies the need]
- Influencers: [Who provides input]
- Decider: [Who makes final call]
- Purchaser: [Who handles procurement]
- Users: [Who will use it]

**Decision timeline:**
[X weeks/months from awareness to purchase]

**Budget authority:**
- Can approve up to: [$X]
- Requires approval for: [$Y+]

### Evaluation Criteria

**Must-haves:**
- [Feature/capability 1]
- [Feature/capability 2]
- [Feature/capability 3]

**Nice-to-haves:**
- [Feature 1]
- [Feature 2]

**Price sensitivity:**
Low | Medium | High

**Price range willing to pay:**
- Minimum: [$X]
- Sweet spot: [$Y]
- Maximum: [$Z]

### Information Sources

**Trusted sources:**
1. [Source 1 - e.g., peer recommendations]
2. [Source 2 - e.g., industry analysts]
3. [Source 3 - e.g., online reviews]

**Where they spend time online:**
- [Platform 1 - e.g., LinkedIn]
- [Platform 2 - e.g., industry forums]
- [Platform 3 - e.g., Reddit]

**Content preferences:**
- Format: [Blog posts / Videos / Podcasts / Whitepapers]
- Length: [Short / Medium / Long-form]
- Tone: [Professional / Casual / Technical]

---

## 🎯 Relationship with Our Product

### Current State

**Awareness level:**
- [ ] Never heard of us
- [ ] Aware but not interested
- [ ] Interested, researching
- [ ] Active user
- [ ] Power user
- [ ] Champion

**Usage frequency:**
[Daily / Weekly / Monthly / Rarely]

**Features used:**
- [Feature 1] - [Frequency]
- [Feature 2] - [Frequency]
- [Feature 3] - [Frequency]

**Features NOT used (and why):**
- [Feature] - [Reason for not using]

### Value Proposition for This Persona

**What our product helps them do:**
1. [Benefit 1]
2. [Benefit 2]
3. [Benefit 3]

**How we solve their pain points:**
- **Pain point:** [Problem]
  - **Our solution:** [How we address it]
  - **Value:** [Quantified benefit]

**Differentiation for this persona:**
[What makes us uniquely valuable to them vs. competitors]

---

## 📱 Channel Preferences

### Communication Channels

**Preferred contact methods (in order):**
1. [Email / Slack / Phone / etc.]
2. [Second choice]
3. [Third choice]

**Best time to reach:**
[Day/time preferences]

**Email behavior:**
- Checks: [X times per day]
- Prefers: [Long/short emails]
- Response time: [Within X hours]

### Content Consumption

**Preferred content types:**
1. [Blog posts / Videos / Podcasts]
2. [Webinars / E-books / Infographics]
3. [Case studies / Tutorials / Documentation]

**Where they learn:**
- [YouTube / Online courses / Books / Conferences]

**Social media usage:**
| Platform | Usage | Purpose |
|----------|-------|---------|
| LinkedIn | Heavy | Professional networking |
| Twitter | Medium | Industry news |
| Facebook | Light | Personal |

---

## 🤝 Influencers & Relationships

### Who Influences Them

**Professional influencers:**
- [Manager/Boss]
- [Colleagues/Peers]
- [Industry thought leaders]

**Personal influencers:**
- [Friends/Family]
- [Mentors]

### Who They Influence

**Direct reports:** [Number, if any]

**Sphere of influence:**
[How many people they can sway, contexts where they're influential]

**Advocacy potential:**
Low | Medium | High

---

## 📊 Scenario: A Day in the Life

### Scenario: [Specific situation]

**Context:**
[Setting up the scenario]

**Journey:**

**8:00 AM:** [Activity]
- Thinking: [What's on their mind]
- Feeling: [Emotional state]
- Using: [Tools/products]

**10:00 AM:** [Activity]
- Thinking: [Thoughts]
- Feeling: [Emotions]
- Pain point encountered: [Problem they face]

**12:00 PM:** [Activity]

**2:00 PM:** [Activity where our product fits]
- Thinking: [What they need]
- Feeling: [How they feel]
- How our product helps: [Solution we provide]

**4:00 PM:** [Activity]

**6:00 PM:** [Activity]
- Outcome: [How their day resolved]

---

## 📈 Metrics & Success Indicators

### How to Measure Success with This Persona

**Engagement metrics:**
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]

**Adoption metrics:**
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]

**Satisfaction metrics:**
- NPS: [Target]
- CSAT: [Target]

---

## 🎨 Design Implications

### Product Design Considerations

**UI/UX preferences:**
- [Visual style they prefer]
- [Layout preferences]
- [Information density: sparse/moderate/dense]

**Accessibility needs:**
- [Any specific requirements]

**Mobile vs. Desktop:**
- Primary device: [Desktop/Mobile/Tablet]
- Use case by device: [When they use what]

### Feature Priorities for This Persona

**High priority:**
- [Feature 1]
- [Feature 2]

**Medium priority:**
- [Feature 3]
- [Feature 4]

**Low priority:**
- [Feature 5]

---

## 💬 Voice & Messaging

### How to Talk to This Persona

**Tone:**
[Professional / Casual / Friendly / Technical / etc.]

**Language level:**
[Simple / Technical / Industry-specific jargon OK]

**Key phrases they use:**
- "[Industry term 1]"
- "[Phrase they use 2]"
- "[Common expression 3]"

**Words to avoid:**
- [Term 1 - why it doesn't resonate]
- [Term 2 - why it's off-putting]

### Sample Messaging

**Email subject line:**
"[Subject that would resonate]"

**Value proposition:**
"[One sentence value prop tailored to them]"

**CTA that works:**
"[Call to action they'd respond to]"

---

## 📚 Research Sources

### Data Sources

**Qualitative research:**
- Interviews conducted: [X]
- User observation sessions: [X]
- Focus groups: [X]

**Quantitative research:**
- Surveys: [X responses]
- Analytics data: [Date range]
- Usage data: [Number of users analyzed]

**Secondary research:**
- Industry reports: [Sources]
- Competitor analysis: [What we learned]
- Market data: [Sources]

### Representative Quotes

> "[Quote 1 that captures their perspective]"

> "[Quote 2 about their pain points]"

> "[Quote 3 about their goals]"

---

## 🔄 Persona Maintenance

**Created by:** [Researcher/PM name]

**Last updated:** [Date]

**Review frequency:** [Quarterly / Bi-annually]

**Next review:** [Date]

**How to update:**
[Process for keeping this persona current]

---

## 📎 Related Documents

- [User research report]
- [Customer journey map for this persona]
- [Product roadmap addressing their needs]

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
| 1.0.0 | YYYY-MM-DD | [Name] | Initial persona |

---

**Remember:** This persona is a research-based archetype, not a real person. Use it to guide decisions, but always validate assumptions with real users.
