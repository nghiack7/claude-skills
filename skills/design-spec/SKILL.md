---
name: design-spec
description: 'This skill should be used when the user asks to "tạo design spec", "viết design specification", or needs a design specification template for product documentation.'
---

## Document Metadata

```yaml
document_type: "design-spec"
product_id: "prod-xxx"
version: "1.0.0"
status: "draft"
owner: "Lead Designer Name"
stakeholders: ["Design", "Product", "Engineering"]
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["design", "ux", "ui", "specification"]
relationships:
  depends_on: []
  blocks: []
  references: []
  implements: []
  supersedes: []
  derived_from: []
  related_issues: []
```

# Design Specification: [Feature/Product Name]

**Feature:** [Feature/Product Name]

**Designer:** [Lead Designer Name]

**Status:** Draft | In Review | Approved | In Development | Shipped

**Design Phase:** Research | Ideation | Design | Prototype | Handoff

**Last Updated:** YYYY-MM-DD

---

## Overview

### Design Summary

[2-3 sentences describing what this design covers and its purpose]

### Design Goals

1. [Goal 1, e.g., "Reduce time to complete task by 50%"]
2. [Goal 2, e.g., "Improve user satisfaction score"]
3. [Goal 3, e.g., "Increase feature discoverability"]

### Success Metrics

| Metric | Baseline | Target | How to Measure |
|--------|----------|--------|----------------|
| [Metric 1] | [Current] | [Goal] | [Method] |
| [Metric 2] | [Current] | [Goal] | [Method] |

---

## Users & Scenarios

### Target Users

**Primary Persona:** [Persona name]
- **Goals:** [What they want to achieve]
- **Pain points:** [Current frustrations]
- **Context:** [When/where they use this]

**Secondary Persona:** [Persona name]
- **Goals:** [Their objectives]
- **Use case:** [How they interact]

### User Scenarios

#### Scenario 1: [Scenario Name]

**Context:**
[Description of the situation]

**User goal:**
[What the user wants to accomplish]

**Steps:**
1. User [action]
2. System [response]
3. User [action]
4. Result: [Outcome]

**Success criteria:**
- [Criterion 1]
- [Criterion 2]

---

## Research & Insights

### Research Conducted

**Methods used:**
- [ ] User interviews ([X] participants)
- [ ] Usability testing ([X] sessions)
- [ ] Surveys ([X] responses)
- [ ] Analytics review
- [ ] Competitive analysis
- [ ] Heuristic evaluation

### Key Findings

1. **Finding 1:**
   - **Insight:** [What we learned]
   - **Implication:** [How this affects design]
   - **Quote:** _"[User quote if applicable]"_

2. **Finding 2:**
   - **Insight:** [Discovery]
   - **Implication:** [Design impact]

3. **Finding 3:**
   - **Insight:** [Learning]
   - **Implication:** [How we address it]

### User Pain Points

| Pain Point | Frequency | Severity | Design Solution |
|------------|-----------|----------|-----------------|
| [Problem 1] | High/Med/Low | High/Med/Low | [How design addresses it] |
| [Problem 2] | High/Med/Low | High/Med/Low | [Solution] |

---

## Design Principles

### Guiding Principles for This Design

1. **[Principle 1, e.g., "Simplicity"]**
   - [What this means in practice]
   - [Example application]

2. **[Principle 2, e.g., "Consistency"]**
   - [Definition for this context]
   - [How we apply it]

3. **[Principle 3, e.g., "Accessibility"]**
   - [Our standard]
   - [Implementation approach]

---

## User Flows

### Primary User Flow

**Flow:** [Flow name, e.g., "Complete Purchase"]

```
[Start] -> [Step 1] -> [Decision Point] -> [Step 2] -> [End]
                           |
                      [Alternative path]
```

**Detailed steps:**

1. **Entry point:** [How user enters this flow]
   - Screen: [Screen name]
   - Trigger: [What initiates this]

2. **Step 1:** [Action]
   - User does: [Description]
   - System shows: [What appears]
   - Screen: [Screen name/link]

3. **Step 2:** [Action]
   - User does: [Description]
   - System shows: [Response]
   - Screen: [Screen name/link]

4. **Completion:** [End state]
   - Success message: [What user sees]
   - Next action: [What happens next]

### Alternative Flows

**Error flow:**
[How we handle errors and guide users back on track]

**Edge case flow:**
[How we handle unusual scenarios]

---

## Screen Designs

### Screen 1: [Screen Name]

**Purpose:** [What this screen does]

**Figma link:** [Link to design file]

**Components used:**
- [Component 1]
- [Component 2]
- [Component 3]

**Layout structure:**
```
+----------------------------+
|  Header                    |
+----------------------------+
|  Main Content Area         |
|  - Element 1               |
|  - Element 2               |
+----------------------------+
|  Footer / Actions          |
+----------------------------+
```

**Key interactions:**
- **On load:** [What happens]
- **User action 1:** [What occurs]
- **User action 2:** [Result]

**States:**
- Default
- Loading
- Success
- Error
- Empty

---

### Screen 2: [Screen Name]

**Purpose:** [Functionality]

**Figma link:** [Link]

**Design notes:**
[Important design decisions for this screen]

---

## Visual Design

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary | #XXXXXX | Buttons, links, key actions |
| Secondary | #XXXXXX | Supporting elements |
| Success | #XXXXXX | Success messages, positive actions |
| Warning | #XXXXXX | Warnings, caution states |
| Error | #XXXXXX | Error states, destructive actions |
| Neutral | #XXXXXX | Text, borders, backgrounds |

### Typography

| Element | Font | Size | Weight | Line Height |
|---------|------|------|--------|-------------|
| H1 | [Font] | [Size]px | [Weight] | [Height] |
| H2 | [Font] | [Size]px | [Weight] | [Height] |
| H3 | [Font] | [Size]px | [Weight] | [Height] |
| Body | [Font] | [Size]px | [Weight] | [Height] |
| Caption | [Font] | [Size]px | [Weight] | [Height] |

### Spacing

**Base unit:** [8px]

**Common spacing values:**
- XS: [4px]
- S: [8px]
- M: [16px]
- L: [24px]
- XL: [32px]
- XXL: [48px]

### Iconography

**Icon set:** [Material Icons / Feather / Custom]

**Icon sizes:**
- Small: [16px]
- Medium: [24px]
- Large: [32px]

**Usage guidelines:**
[When to use which icons, styling rules]

---

## Components

### Component 1: [Component Name]

**Purpose:** [What this component does]

**Figma link:** [Link to component]

**Variants:**
- Default
- Hover
- Active
- Disabled
- Loading

**Props/States:**
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| [prop1] | [type] | [default] | [what it does] |
| [prop2] | [type] | [default] | [what it does] |

**Usage guidelines:**
- When to use: [Context]
- When NOT to use: [Wrong contexts]

**Accessibility:**
- ARIA attributes: [Required attributes]
- Keyboard navigation: [How it works]
- Screen reader: [What it announces]

---

### Component 2: [Component Name]

**Purpose:** [Functionality]

**Design specs:**
[Detailed specifications]

---

## Layout & Grid

### Grid System

**Desktop (>1200px):**
- Columns: [12]
- Gutter: [24px]
- Margin: [48px]

**Tablet (768px - 1199px):**
- Columns: [8]
- Gutter: [16px]
- Margin: [32px]

**Mobile (<768px):**
- Columns: [4]
- Gutter: [16px]
- Margin: [16px]

### Breakpoints

| Breakpoint | Width | Design approach |
|------------|-------|-----------------|
| Mobile | 320px - 767px | [Mobile-specific layout] |
| Tablet | 768px - 1199px | [Tablet layout] |
| Desktop | 1200px+ | [Desktop layout] |

---

## Interaction Design

### Micro-interactions

**Interaction 1: [Name, e.g., "Button Click"]**
- Trigger: [User action]
- Feedback: [Visual/audio response]
- Duration: [Xms]
- Easing: [ease-in-out]

**Interaction 2: [Name, e.g., "Form Validation"]**
- Trigger: [When it happens]
- Feedback: [What user sees]
- Timing: [When it appears]

### Animations

**Animation 1: [Name, e.g., "Page Transition"]**
- Type: [Fade/Slide/etc.]
- Duration: [300ms]
- Easing: [ease-out]
- Purpose: [Why this animation]

**Animation guidelines:**
- All animations: [Duration range]
- Respect reduced motion preferences
- Purposeful, not decorative

### Gestures (Mobile/Touch)

| Gesture | Action | Feedback |
|---------|--------|----------|
| Tap | [What happens] | [Visual feedback] |
| Long press | [Action] | [Feedback] |
| Swipe left | [Action] | [Feedback] |
| Swipe right | [Action] | [Feedback] |
| Pinch to zoom | [If applicable] | [Feedback] |

---

## Accessibility

### WCAG Compliance

**Target level:** AA | AAA

**Requirements met:**
- [ ] Color contrast ratios (4.5:1 for text)
- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] Focus indicators
- [ ] Alt text for images
- [ ] Form labels
- [ ] Error messages

### Keyboard Navigation

**Tab order:**
[Logical tab order through the interface]

**Keyboard shortcuts:**
| Shortcut | Action |
|----------|--------|
| Tab | Move to next element |
| Shift + Tab | Move to previous element |
| Enter | Activate button/link |
| Esc | Close modal/cancel |
| [Custom] | [Custom action] |

### Screen Reader Considerations

**ARIA labels:**
[Where and how ARIA labels are used]

**Announcements:**
- On page load: [What is announced]
- On state change: [What is announced]
- On error: [Error announcement]

### Color Accessibility

**Not relying on color alone for:**
- Error states (also use icons/text)
- Status indicators (also use labels)
- Interactive elements (also use underlines/borders)

---

## Responsive Design

### Mobile Design (<768px)

**Key differences from desktop:**
- [Difference 1, e.g., "Navigation collapses to hamburger menu"]
- [Difference 2, e.g., "Single column layout"]
- [Difference 3, e.g., "Larger touch targets (44x44px)"]

**Mobile-specific features:**
- [Feature 1]
- [Feature 2]

### Tablet Design (768px - 1199px)

**Adaptation approach:**
[How design adapts for tablet]

### Touch Targets

**Minimum size:** 44x44px (iOS) / 48x48px (Android)

**Spacing between targets:** [Minimum 8px]

---

## States & Variations

### Component States

**For all interactive elements:**

| State | Visual Change | When it Occurs |
|-------|---------------|----------------|
| Default | [Description] | Initial state |
| Hover | [Description] | Mouse over |
| Focus | [Description] | Keyboard focus |
| Active | [Description] | Being clicked/tapped |
| Disabled | [Description] | Not available |
| Loading | [Description] | Async operation |
| Success | [Description] | Successful action |
| Error | [Description] | Error occurred |

### Empty States

**When:** [When shown]

**Content:**
- Illustration: [Yes/No - description]
- Heading: "[Example heading]"
- Description: "[Example description]"
- CTA: "[Call to action]"

### Error States

**Types of errors:**
1. **Validation error:** [How shown]
2. **System error:** [How communicated]
3. **Network error:** [User guidance]

**Error message pattern:**
```
[Clear description of what went wrong]
[What the user can do to fix it]
[Action button if applicable]
```

---

## Content & Copy

### Microcopy

| Element | Copy | Tone |
|---------|------|------|
| Primary CTA | "[Button text]" | [Action-oriented] |
| Secondary CTA | "[Button text]" | [Descriptive] |
| Success message | "[Success text]" | [Encouraging] |
| Error message | "[Error text]" | [Helpful] |
| Empty state | "[Empty state text]" | [Guiding] |

### Tone & Voice

**Overall tone:** [Professional / Friendly / Casual / Technical]

**Writing guidelines:**
- [Guideline 1, e.g., "Use active voice"]
- [Guideline 2, e.g., "Keep it concise"]
- [Guideline 3, e.g., "Be helpful, not blame-y"]

### Placeholder Text

**Input fields:**
- Should be: Descriptive examples
- Should not be: Critical information or labels

---

## Technical Specifications

### Assets to Export

| Asset | Format | Sizes | Usage |
|-------|--------|-------|-------|
| Icons | SVG | 24x24, 48x48 | All icons |
| Images | PNG, WebP | 1x, 2x, 3x | Photos |
| Logos | SVG | Multiple | Branding |

### Design Tokens

**Colors:**
```css
--color-primary: #XXXXXX;
--color-secondary: #XXXXXX;
--color-text: #XXXXXX;
```

**Spacing:**
```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
```

**Typography:**
```css
--font-family-primary: 'Font Name', sans-serif;
--font-size-body: 16px;
--line-height-body: 1.5;
```

### Browser Support

**Required browsers:**
- Chrome [version+]
- Firefox [version+]
- Safari [version+]
- Edge [version+]

**Mobile browsers:**
- iOS Safari [version+]
- Chrome Mobile [version+]

---

## Handoff

### Design Files

**Figma/Sketch:**
- Main file: [Link]
- Component library: [Link]
- Prototype: [Link]

**Assets:**
- Icons: [Location]
- Images: [Location]
- Fonts: [Location]

### Developer Notes

**Implementation priorities:**
1. [Priority 1 - what to build first]
2. [Priority 2]
3. [Priority 3]

**Special considerations:**
- [Note 1, e.g., "Animation should respect prefers-reduced-motion"]
- [Note 2, e.g., "Images should lazy-load"]
- [Note 3, e.g., "Form should have client-side validation"]

### Design QA Checklist

**Before launch:**
- [ ] All screens match designs
- [ ] Responsive behavior correct
- [ ] Animations smooth (60fps)
- [ ] Accessibility requirements met
- [ ] Cross-browser testing complete
- [ ] Dark mode (if applicable)
- [ ] Loading states implemented
- [ ] Error states implemented
- [ ] Empty states implemented

---

## Testing & Validation

### Usability Testing

**Testing plan:**
- **Participants:** [X users from target segment]
- **Method:** [Moderated/unmoderated]
- **Tasks:** [Task list]

**Success criteria:**
- Task completion rate: [X%]
- Time on task: [< X seconds]
- User satisfaction: [X/5 rating]

### A/B Testing Opportunities

**Variant A:** [Current/control design]

**Variant B:** [Alternative design]

**Hypothesis:** [What we expect to happen]

**Metrics:** [What we'll measure]

---

## Design Rationale

### Key Design Decisions

**Decision 1: [What we decided]**

**Why:**
[Reasoning behind the decision]

**Alternatives considered:**
[What else we looked at and why we didn't choose it]

**Evidence:**
[Research or data supporting this]

---

**Decision 2: [What we decided]**

**Why:**
[Reasoning]

---

## Future Enhancements

### Out of Scope (for now)

- [Enhancement 1]
- [Enhancement 2]
- [Enhancement 3]

### Next Iteration Ideas

[Ideas to explore in future versions]

---

## References

### Design Inspiration

- [Reference 1]
- [Reference 2]
- [Reference 3]

### Related Documents

- PRD: [Link]
- User research: [Link]
- Technical spec: [Link]

---

## Document Relationships

### Upstream Dependencies

| ID | Type | Title | Why It Matters | Status |
|----|------|-------|----------------|--------|
| - | - | - | - | - |

### Downstream Impacts

| ID | Type | Title | Impact | Owner |
|----|------|-------|--------|-------|
| - | - | - | - | - |

### Related Documents

| ID | Type | Title | Relationship |
|----|------|-------|--------------|
| - | - | - | - |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial design specification |

---

**Design Review Status:**

| Reviewer | Role | Status | Date | Feedback |
|----------|------|--------|------|----------|
| [Name] | Designer | | YYYY-MM-DD | [Notes] |
| [Name] | PM | Pending | | |
| [Name] | Engineer | Pending | | |

---

**Next Steps:**
1. [Action 1]
2. [Action 2]
3. [Action 3]
