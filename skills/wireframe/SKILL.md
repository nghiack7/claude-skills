---
name: wireframe
description: 'This skill should be used when the user asks to "tạo wireframe", "viết wireframe spec", "UI wireframe", or needs a wireframe specification template for design documentation.'
---

## Document Metadata

```yaml
document_type: "wireframe"
wireframe_id: "WF-XXX"
feature_id: "FEAT-XXX"
version: "1.0.0"
status: "draft"
owner: "UX Designer Name"
fidelity: "low|medium|high"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: ["wireframe", "design", "ux"]

# Relationships
relationships:
  derived_from:
    - path: "product-knowledge/02-requirements/prd/YYYY-MM-DD-prd-NNN-feature.md"
      title: "Feature PRD"
      reason: "Visual design for this feature"
  blocks:
    - path: "product-knowledge/03-design/ux-ui/YYYY-MM-DD-design-spec-NNN-feature.md"
      title: "Design Specification"
      reason: "High-fidelity spec based on these wireframes"
```

# Wireframe: [Feature/Screen Name]

> **Purpose:** Visual representation of layout, structure, and key interactions for [feature name] before high-fidelity design.

---

## Overview

**Wireframe ID:** `WF-XXX`
**Feature:** [Feature name]
**Fidelity:** Low | Medium | High
**Platform:** Web | iOS | Android | Responsive Web | All
**Status:** Draft | Review | Approved | Superseded

### Design Goals

1. [Goal 1 - e.g., Simplify user flow for checkout]
2. [Goal 2 - e.g., Reduce cognitive load with clear hierarchy]
3. [Goal 3 - e.g., Optimize for mobile-first experience]

### Scope

**In Scope:**
- [Screen/feature 1]
- [Screen/feature 2]
- [Key interactions]

**Out of Scope:**
- [Future enhancements]
- [Related features in separate wireframes]

---

## Design Files

### Primary Wireframe Files

| File | Tool | Version | Link | Status |
|------|------|---------|------|--------|
| Desktop wireframes | Figma | v1.2 | [Figma link] | Current |
| Mobile wireframes | Figma | v1.2 | [Figma link] | Current |
| Tablet wireframes | Figma | v1.1 | [Figma link] | Draft |
| Interactive prototype | Figma | v1.0 | [Prototype link] | Current |

### Alternative Formats

- **PDF Export:** [Link to PDF]
- **PNG Screenshots:** [Link to folder]
- **Adobe XD:** [Link if applicable]
- **Sketch:** [Link if applicable]

---

## Screen Inventory

Complete list of screens in this wireframe set:

| # | Screen Name | Type | Breakpoint | Priority | Notes |
|---|-------------|------|------------|----------|-------|
| 1 | Home Screen | Main | Desktop/Mobile | P0 | Entry point |
| 2 | Product List | List | Desktop/Mobile | P0 | Core functionality |
| 3 | Product Detail | Detail | Desktop/Mobile | P0 | |
| 4 | Shopping Cart | Modal | Desktop/Mobile | P0 | Checkout flow |
| 5 | Checkout Step 1 | Form | Desktop/Mobile | P0 | Shipping info |
| 6 | Checkout Step 2 | Form | Desktop/Mobile | P0 | Payment |
| 7 | Order Confirmation | Success | Desktop/Mobile | P0 | |
| 8 | Account Settings | Settings | Desktop/Mobile | P1 | Lower priority |
| 9 | Error State | Error | Desktop/Mobile | P0 | Error handling |

**Priority Levels:**
- **P0:** Must have for MVP
- **P1:** Should have soon after
- **P2:** Nice to have (future iteration)

---

## Screen Details

### Screen 1: [Screen Name]

**Purpose:** [What this screen accomplishes]
**User Entry Point:** [How user navigates here]
**User Actions:** [What user can do on this screen]

#### Desktop Layout (>=1024px)

![Desktop Wireframe](path/to/desktop-wireframe.png)

**Layout Description:**
```
+-------------------------------------------------------------+
|  [Logo]          Navigation Menu          [User Avatar] [N]  |  <- Header
+-------------------------------------------------------------+
|                                                               |
|  +--------------+    +----------------------------+          |
|  |              |    |  Main Content Area         |          |
|  |   Sidebar    |    |                            |          |
|  |   Filters    |    |  [Hero Section]            |          |
|  |              |    |                            |          |
|  | [Category 1] |    |  +------+ +------+ +------+|          |
|  | [Category 2] |    |  | Card | | Card | | Card ||          |
|  | [Category 3] |    |  +------+ +------+ +------+|          |
|  |              |    |                            |          |
|  +--------------+    +----------------------------+          |
|                                                               |
+-------------------------------------------------------------+
|  Footer: Links | Social | Copyright                         |  <- Footer
+-------------------------------------------------------------+
```

**Key Components:**
1. **Header (Fixed)**
   - Logo (clickable, returns to home)
   - Primary navigation (5-7 items)
   - Search bar
   - User avatar + notifications

2. **Sidebar (Sticky, 240px width)**
   - Category filters (checkboxes)
   - Price range slider
   - "Apply Filters" button

3. **Main Content**
   - Hero banner (optional)
   - Product grid (3 columns)
   - Pagination/infinite scroll

4. **Footer (Static)**
   - Links, social, legal

**Interactions:**
- [ ] Hover states on navigation items
- [ ] Filter sidebar collapses on scroll (optional)
- [ ] Click product card -> Navigate to detail page
- [ ] Search autocomplete suggestions

#### Mobile Layout (<=767px)

![Mobile Wireframe](path/to/mobile-wireframe.png)

**Layout Description:**
```
+-------------------+
|  [M]  [Logo]  [S] |  <- Mobile Header (Fixed)
+-------------------+
|                   |
|  [Hero Banner]    |
|                   |
+-------------------+
|  [Filter Button]  |  <- Tappable filter toggle
+-------------------+
|  +--------------+ |
|  |              | |
|  |  Product     | |
|  |  Card        | |  <- Stacked cards (1 column)
|  |              | |
|  +--------------+ |
|  +--------------+ |
|  |  Product     | |
|  |  Card        | |
|  +--------------+ |
|                   |
+-------------------+
```

**Mobile-Specific Changes:**
- Hamburger menu (off-canvas drawer)
- Filters in bottom sheet modal
- Single-column layout
- Larger touch targets (44x44px minimum)
- Sticky "Filter" button

**Interactions:**
- [ ] Tap hamburger -> Open navigation drawer
- [ ] Tap filter button -> Open filter modal
- [ ] Pull to refresh product list
- [ ] Tap product card -> Navigate to detail

#### Tablet Layout (768px - 1023px)

[If significantly different from desktop, document here]

---

### Screen 2: [Screen Name]

[Repeat structure for each screen]

---

## User Flows

### Primary Flow: [Flow Name]

**Goal:** [What user wants to achieve]
**Starting Point:** [Where flow begins]
**Ending Point:** [Where flow ends]

**Flow Diagram:**
```
[Home Screen]
      |
  [Tap Product]
      |
[Product Detail]
      |
 [Add to Cart]
      |
[Cart Modal Opens]
      |
[Checkout Button]
      |
[Checkout Flow]
      |
[Success Screen]
```

**Step-by-Step:**
1. User starts on Home Screen
2. Taps a product card
3. Reviews product details
4. Taps "Add to Cart" button
5. Cart modal slides up with item added
6. Taps "Checkout" in modal
7. Proceeds through 2-step checkout
8. Arrives at success confirmation

**Screens Involved:** 1, 3, 4, 5, 6, 7

---

## Component Specifications

### Component 1: Product Card

**Purpose:** Display product summary in grid view

**Anatomy:**
```
+-----------------+
|   [Image]       |  <- Product photo (16:9 aspect ratio)
+-----------------+
|  Product Name   |  <- Title (2 line truncate)
|  $99.99         |  <- Price (bold, large)
|  **** (24)      |  <- Rating + review count
|                 |
|  [Add to Cart]  |  <- Primary button
+-----------------+
```

**Dimensions:**
- Desktop: 280px x 400px
- Mobile: 100% width x auto height

**States:**
- Default
- Hover (desktop): Slight elevation, border highlight
- Active: Pressed state
- Out of stock: Greyed out, "Sold Out" badge

### Component 2: [Component Name]

[Repeat for other reusable components]

---

## Interaction Patterns

### Pattern 1: Modal Overlays

**Trigger:** User clicks "Add to Cart" or "Filter"
**Behavior:**
- Overlay darkens background (60% black)
- Modal slides up from bottom (mobile) or fades in center (desktop)
- Focus traps inside modal
- ESC key or backdrop click closes modal

**Animation:**
- Duration: 300ms
- Easing: cubic-bezier(0.4, 0, 0.2, 1)

### Pattern 2: Infinite Scroll

**Trigger:** User scrolls to bottom of product list
**Behavior:**
- Loading spinner appears
- Next 20 products load automatically
- URL updates with page parameter
- "Back" button returns to correct scroll position

### Pattern 3: [Pattern Name]

[Document other interaction patterns]

---

## States & Variations

### Loading States

**Initial Page Load:**
- Skeleton screens for product cards
- Pulse animation
- "Loading..." text for screen readers

**Component Load:**
- Spinner inside button ("Loading...")
- Disabled state prevents double-clicks

### Empty States

**No Results:**
- Illustration (empty box or search icon)
- Heading: "No products found"
- Subtext: "Try adjusting your filters"
- CTA: "Clear Filters" button

**No Cart Items:**
- Heading: "Your cart is empty"
- CTA: "Continue Shopping" button

### Error States

**Network Error:**
- Error icon
- Heading: "Something went wrong"
- Subtext: "Please check your connection"
- CTA: "Try Again" button

**Out of Stock:**
- Product card shows "Sold Out" badge
- Add to Cart button disabled
- Optional: "Notify Me" button

---

## Responsive Breakpoints

| Breakpoint | Width | Layout | Notes |
|------------|-------|--------|-------|
| Mobile S | 320px - 374px | 1 col | Minimum supported |
| Mobile M | 375px - 767px | 1 col | Primary mobile |
| Tablet | 768px - 1023px | 2 col | Hybrid layout |
| Desktop | 1024px - 1439px | 3 col | Standard desktop |
| Desktop L | 1440px+ | 3-4 col | Large screens |

---

## Accessibility Considerations

### Keyboard Navigation

- [ ] All interactive elements tabbable
- [ ] Logical tab order (top to bottom, left to right)
- [ ] Focus indicators visible (2px outline)
- [ ] Skip to main content link

### Screen Reader Support

- [ ] Semantic HTML (`<nav>`, `<main>`, `<article>`)
- [ ] ARIA labels for icon-only buttons
- [ ] Alt text for all images
- [ ] Live region announcements for dynamic content

### Visual Accessibility

- [ ] Color contrast >= 4.5:1 for text
- [ ] Don't rely on color alone (use icons + text)
- [ ] Touch targets >= 44x44px
- [ ] Text scalable to 200% without breaking layout

### Notes for Design Team

> When creating high-fidelity designs, ensure:
> - Focus indicators stand out from other UI elements
> - Error messages are both visual and textual
> - Form fields have clear labels (not just placeholders)

---

## Content Guidelines

### Tone & Voice

- [Brand voice: Friendly, professional, helpful]
- [Use active voice and clear CTAs]
- [Avoid jargon and technical terms]

### Copy Examples

| Element | Copy | Notes |
|---------|------|-------|
| Primary CTA | "Add to Cart" | Action-oriented, clear |
| Empty state | "Your cart is empty" | Friendly, not negative |
| Error message | "Oops! Something went wrong" | Empathetic, human |
| Success message | "Item added to your cart!" | Celebratory, affirming |

---

## Technical Considerations

### Performance

- Image lazy loading (below fold)
- Virtualized list for long product grids
- Bundle size budget: < 200KB (initial JS)
- First Contentful Paint: < 1.5s

### Browser Support

- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)
- Mobile: iOS Safari 13+, Chrome Android 90+

### Data Requirements

**API Endpoints Needed:**
- `GET /api/products` - Fetch product list
- `POST /api/cart` - Add item to cart
- `GET /api/cart` - Fetch cart contents

**Data Models:**
```typescript
interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
  rating: number;
  reviewCount: number;
  inStock: boolean;
}
```

---

## Design Decisions & Rationale

### Decision 1: Single-Column Mobile Layout

**Decision:** Use 1 column for mobile product grid
**Alternatives Considered:** 2-column grid
**Rationale:**
- Larger product cards easier to tap
- Better readability for product names
- Reduces cognitive load
**Validated By:** User testing showed 30% more engagement

### Decision 2: Filter Modal (Mobile)

**Decision:** Filters open in bottom sheet modal
**Alternatives Considered:** Inline expanding filters
**Rationale:**
- Doesn't push content down (better UX)
- More space for filters
- Familiar mobile pattern
**Validated By:** Industry best practices (Amazon, Etsy)

### Decision 3: [Decision Name]

[Document other key decisions]

---

## Feedback & Iteration

### Review Sessions

| Date | Participants | Key Feedback | Changes Made |
|------|--------------|--------------|--------------|
| 2025-10-15 | Product, Design, Eng | "Checkout too complex" | Reduced to 2 steps |
| 2025-10-18 | QA, Support | "Error states unclear" | Added specific error messages |

### User Testing Results

**Session 1: Mobile Prototype (n=5)**
- 4/5 users completed checkout successfully
- Average time: 3 minutes
- Pain point: Confusing filter icon
- **Action:** Changed filter icon to "Filter" text button

**Session 2: Desktop Prototype (n=5)**
- 5/5 users completed flow
- Average time: 2 minutes
- Positive feedback on layout clarity
- **Action:** No changes needed

---

## Next Steps

### Immediate (This Week)

1. [ ] Final stakeholder review
2. [ ] Incorporate feedback
3. [ ] Hand off to visual design team

### Short-term (Next 2 Weeks)

1. [ ] High-fidelity mockups created
2. [ ] Design spec documented
3. [ ] Component library updated

### Long-term (Next Month)

1. [ ] Engineering implementation
2. [ ] QA testing
3. [ ] Launch to production

---

## Open Questions

| # | Question | Owner | Priority | Status |
|---|----------|-------|----------|--------|
| 1 | Should filters persist across sessions? | PM | Medium | Open |
| 2 | Do we need guest checkout for MVP? | PM | High | Resolved: Yes |
| 3 | What's max number of filters allowed? | Eng | Low | Open |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-10-10 | [Name] | Initial wireframes |
| 1.1.0 | 2025-10-15 | [Name] | Simplified checkout flow |
| 1.2.0 | 2025-10-18 | [Name] | Updated filter button based on testing |

---

## Related Documents

- **PRD:** [Link to feature PRD]
- **User Stories:** [Link to user stories]
- **Design Spec:** [Link to high-fidelity spec]
- **User Journey:** [Link to user journey map]

---

## Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Product Manager | [Name] | YYYY-MM-DD | Approved |
| UX Lead | [Name] | YYYY-MM-DD | Approved |
| Engineering Lead | [Name] | YYYY-MM-DD | Approved |

---

## Notes

- All measurements in this document are for reference only; final pixels determined in high-fidelity designs
- Wireframes focus on layout and interaction, not visual style
- Placeholder content used; final copy from content team
