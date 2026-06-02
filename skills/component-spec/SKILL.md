---
name: component-spec
description: 'This skill should be used when the user asks to "tạo component spec", "viết component specification", or needs a component specification template for product documentation.'
---

## Document Metadata

```yaml
document_type: "component"
component_id: "COMP-XXX"
component_name: "ComponentName"
component_type: "atom|molecule|organism"
version: "1.0.0"
status: "draft"
owner: "Design Lead Name"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["design-system", "component", "ui"]

# Relationships
relationships:
  derived_from:
    - path: "product-knowledge/03-design/design-system/design-tokens.md"
      title: "Design Tokens"
      reason: "Uses color, spacing, typography tokens"
  related_to:
    - path: "product-knowledge/03-design/design-system/components/related-component.md"
      title: "Related Component"
      reason: "Often used together"
```

# Component: [Component Name]

> **Purpose:** [One sentence describing what this component does and why it exists]

---

## Overview

**Component ID:** `COMP-XXX`
**Type:** Atom | Molecule | Organism *(Atomic Design methodology)*
**Status:** Draft | Review | Approved | Published | Deprecated
**Figma:** [Link to Figma design file]

### Description

[2-3 paragraph detailed description of the component, its purpose, and when to use it]

### Design Principles

- **Principle 1:** [e.g., Accessible by default]
- **Principle 2:** [e.g., Responsive across all breakpoints]
- **Principle 3:** [e.g., Consistent with brand guidelines]

---

## Variants

### Variant 1: [Primary/Default]

**Purpose:** [When to use this variant]

**Visual Example:**

![Primary Button](path/to/image.png)

**Properties:**
- Property 1: [Value]
- Property 2: [Value]

### Variant 2: [Secondary]

**Purpose:** [When to use this variant]

**Visual Example:**

![Secondary Button](path/to/image.png)

**Properties:**
- Property 1: [Value]
- Property 2: [Value]

### Variant 3: [Additional Variants]

[Continue for all variants: Tertiary, Danger, Success, etc.]

---

## Anatomy

Visual breakdown of component parts:

```
+-------------------------------------+
|  [Icon]   Label Text   [Badge]      |  <- Component Container
|  ^        ^            ^            |
|  Icon     Text         Indicator    |
+-------------------------------------+
```

### Component Parts

1. **Container**
   - Purpose: [Wraps all elements]
   - Styling: [Border, background, padding]

2. **Icon** (Optional)
   - Purpose: [Visual identifier]
   - Sizing: [16px, 20px, 24px]
   - Position: [Leading, trailing]

3. **Label Text**
   - Purpose: [Primary content]
   - Typography: [Font family, size, weight]

4. **Badge/Indicator** (Optional)
   - Purpose: [Status or count indicator]
   - Styling: [Size, color, position]

---

## States

### Interactive States

#### Default (Rest)
- **Visual:** [Description of default appearance]
- **Tokens:**
  ```
  background: $color-button-primary
  text: $color-text-on-primary
  border: none
  ```

#### Hover
- **Visual:** [Changes on mouse hover]
- **Tokens:**
  ```
  background: $color-button-primary-hover
  cursor: pointer
  ```

#### Active (Pressed)
- **Visual:** [Appearance when clicked/pressed]
- **Tokens:**
  ```
  background: $color-button-primary-active
  transform: scale(0.98)
  ```

#### Focus
- **Visual:** [Keyboard focus indicator]
- **Tokens:**
  ```
  outline: 2px solid $color-focus-ring
  outline-offset: 2px
  ```

#### Disabled
- **Visual:** [Appearance when not interactive]
- **Tokens:**
  ```
  background: $color-button-disabled
  text: $color-text-disabled
  cursor: not-allowed
  opacity: 0.6
  ```

#### Loading
- **Visual:** [Appearance during async operation]
- **Behavior:** Show spinner, disable interaction

---

## Sizes

### Small
- Height: 32px
- Padding: 8px 16px
- Font size: 14px
- Use case: Compact interfaces, tables

### Medium (Default)
- Height: 40px
- Padding: 10px 20px
- Font size: 16px
- Use case: Standard forms, dialogs

### Large
- Height: 48px
- Padding: 12px 24px
- Font size: 18px
- Use case: Hero sections, primary CTAs

---

## Design Tokens

### Colors

| Token | Value | Usage |
|-------|-------|-------|
| `$component-bg-primary` | `#0066FF` | Primary background |
| `$component-bg-secondary` | `#6B7280` | Secondary background |
| `$component-text` | `#FFFFFF` | Text on primary |
| `$component-border` | `#D1D5DB` | Border color |

### Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `$component-padding-x` | `16px` | Horizontal padding |
| `$component-padding-y` | `10px` | Vertical padding |
| `$component-gap` | `8px` | Space between elements |

### Typography

| Token | Value | Usage |
|-------|-------|-------|
| `$component-font-family` | `'Inter', sans-serif` | Font family |
| `$component-font-size` | `16px` | Default text size |
| `$component-font-weight` | `500` | Medium weight |
| `$component-line-height` | `1.5` | Line height |

### Elevation

| Token | Value | Usage |
|-------|-------|-------|
| `$component-shadow` | `0 2px 4px rgba(0,0,0,0.1)` | Default shadow |
| `$component-shadow-hover` | `0 4px 8px rgba(0,0,0,0.15)` | Hover shadow |

---

## Behavior

### Interaction Model

**Click/Tap:**
- Trigger: User clicks or taps component
- Response: [Immediate feedback, navigation, state change]

**Keyboard:**
- `Tab`: Focus component
- `Enter` / `Space`: Activate component
- `Esc`: Cancel/close (if applicable)

**Gesture (Mobile):**
- Tap: Activate
- Long press: [Context menu / additional options]

### Animation & Transitions

**Hover Transition:**
```css
transition: background-color 200ms ease-in-out;
```

**Focus Transition:**
```css
transition: outline 150ms ease-in-out;
```

**State Change:**
```css
transition: all 250ms cubic-bezier(0.4, 0, 0.2, 1);
```

---

## Accessibility (WCAG 2.1 AA)

### Keyboard Navigation

- [ ] **Tab Order:** Component is in logical tab sequence
- [ ] **Focus Indicator:** Clear 2px outline with 4.5:1 contrast
- [ ] **Enter/Space:** Activates component
- [ ] **Esc:** Dismisses if modal/overlay

### Screen Readers

- [ ] **Role:** Appropriate ARIA role assigned (`role="button"`)
- [ ] **Label:** Accessible name provided (`aria-label` or text content)
- [ ] **State:** Dynamic states announced (`aria-pressed`, `aria-expanded`)
- [ ] **Description:** Additional context when needed (`aria-describedby`)

**Example ARIA:**
```html
<button
  role="button"
  aria-label="Submit form"
  aria-pressed="false"
  aria-describedby="submit-help-text"
>
  Submit
</button>
```

### Visual Accessibility

- [ ] **Color Contrast:** Text contrast >= 4.5:1 (normal), >= 3:1 (large text)
- [ ] **Non-Color Indicators:** Don't rely on color alone for meaning
- [ ] **Touch Targets:** Minimum 44x44px tap/click area
- [ ] **Focus Visible:** Clear visual focus indicator

### Motion & Animation

- [ ] **Reduced Motion:** Respects `prefers-reduced-motion` setting
- [ ] **Essential Only:** Animations enhance, don't distract
- [ ] **Performance:** Runs at 60fps without janking

---

## Usage Guidelines

### When to Use

**Use this component when:**
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

**Example:**
- Primary actions in forms (Submit, Save, Continue)
- Call-to-action buttons on landing pages
- Confirmation dialogs (OK, Confirm, Yes)

### When NOT to Use

**Avoid this component when:**
- [Anti-pattern 1]
- [Anti-pattern 2]
- [Anti-pattern 3]

**Example:**
- Navigational links (use Link component instead)
- Inline text actions (use TextButton component)
- Too many actions (creates decision fatigue)

### Best Practices

**Do:**
- Use clear, action-oriented labels ("Save Changes" not "OK")
- Limit to 1-2 primary actions per screen
- Provide loading states for async actions

**Don't:**
- Use generic labels like "Click Here" or "Submit"
- Make buttons too small (minimum 44x44px)
- Disable without explanation (show error message instead)

---

## Responsive Behavior

### Desktop (>=1024px)
- Width: Auto (based on content) or fixed
- Padding: 10px 20px
- Font size: 16px

### Tablet (768px - 1023px)
- Width: Auto or full-width in modals
- Padding: 10px 18px
- Font size: 16px

### Mobile (<=767px)
- Width: Full-width or auto
- Padding: 12px 20px (slightly larger touch target)
- Font size: 16px (prevent zoom on iOS)
- Minimum height: 44px

---

## Code Examples

### HTML

```html
<!-- Primary Button -->
<button class="btn btn-primary" type="button">
  <span class="btn-icon">icon</span>
  <span class="btn-label">Search</span>
</button>

<!-- With Loading State -->
<button class="btn btn-primary" type="button" aria-busy="true" disabled>
  <span class="btn-spinner" aria-hidden="true"></span>
  <span class="btn-label">Loading...</span>
</button>
```

### CSS

```css
.btn {
  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--component-gap);

  /* Spacing */
  padding: var(--component-padding-y) var(--component-padding-x);

  /* Typography */
  font-family: var(--component-font-family);
  font-size: var(--component-font-size);
  font-weight: var(--component-font-weight);
  line-height: var(--component-line-height);

  /* Visual */
  background: var(--component-bg-primary);
  color: var(--component-text);
  border: none;
  border-radius: 6px;

  /* Interaction */
  cursor: pointer;
  transition: all 200ms ease-in-out;
}

.btn:hover {
  background: var(--component-bg-primary-hover);
}

.btn:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

### React (TypeScript)

```tsx
import React from 'react';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'tertiary';
  size?: 'small' | 'medium' | 'large';
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  loading = false,
  disabled = false,
  icon,
  children,
  onClick,
}) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      onClick={onClick}
      disabled={disabled || loading}
      aria-busy={loading}
      type="button"
    >
      {loading ? (
        <span className="btn-spinner" aria-hidden="true" />
      ) : icon ? (
        <span className="btn-icon">{icon}</span>
      ) : null}
      <span className="btn-label">{children}</span>
    </button>
  );
};
```

### Vue

```vue
<template>
  <button
    :class="['btn', `btn-${variant}`, `btn-${size}`]"
    :disabled="disabled || loading"
    :aria-busy="loading"
    @click="$emit('click')"
  >
    <span v-if="loading" class="btn-spinner" aria-hidden="true" />
    <span v-else-if="icon" class="btn-icon">{{ icon }}</span>
    <span class="btn-label"><slot /></span>
  </button>
</template>

<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'tertiary';
  size?: 'small' | 'medium' | 'large';
  loading?: boolean;
  disabled?: boolean;
  icon?: string;
}>();

defineEmits<{
  (e: 'click'): void;
}>();
</script>
```

---

## Related Components

- **[Link]** - For navigation within the app
- **[IconButton]** - For icon-only actions
- **[ButtonGroup]** - For grouping related actions
- **[SplitButton]** - For primary action with menu

---

## Testing Checklist

### Visual Testing

- [ ] Component renders correctly in all variants
- [ ] All states (hover, active, focus, disabled) display correctly
- [ ] Responsive behavior works across breakpoints
- [ ] Dark mode support (if applicable)

### Functional Testing

- [ ] Click/tap triggers expected action
- [ ] Keyboard navigation works (Tab, Enter, Space)
- [ ] Loading state prevents duplicate submissions
- [ ] Disabled state prevents interaction

### Accessibility Testing

- [ ] Screen reader announces component correctly
- [ ] Focus indicator has sufficient contrast
- [ ] Touch targets meet 44x44px minimum
- [ ] Component works with keyboard only

### Browser Testing

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers (iOS Safari, Chrome Android)

---

## Changelog

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | YYYY-MM-DD | Initial component creation | [Name] |
| 1.1.0 | YYYY-MM-DD | Added loading state variant | [Name] |

---

## Resources

- **Figma Design:** [Link to Figma file]
- **Storybook:** [Link to Storybook story]
- **Code Repository:** [Link to component source]
- **NPM Package:** `@designsystem/button@1.0.0`

---

## Notes

- [Implementation details]
- [Known limitations]
- [Future enhancements planned]
