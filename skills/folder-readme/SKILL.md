---
name: folder-readme
description: 'This skill should be used when the user asks to "tạo README cho folder", "folder documentation", or needs a folder README template for documentation structure.'
---

## Document Metadata

```yaml
folder_purpose: "[Brief one-line description of what this folder contains]"
document_type: "[type-identifier]"
template_required: true|false
custom_allowed: true|false
naming_pattern: "YYYY-MM-DD-[type]-NNN-[description].md"
status_values: ["draft", "review", "approved", "active", "archived"]
required_fields: ["field1", "field2", "field3"]
optional_fields: ["field4", "field5"]
creation_command: "/pm.create-[type]"
validation_command: "/pm.validate-[type]"
approval_command: "/pm.approve-[type]"
related_commands: ["/pm.command1", "/pm.command2"]
```

# [Folder Name - Human Readable]

[2-3 sentence description of the folder's purpose and what types of documents belong here]

## Purpose

[Detailed explanation of what this folder is for, who uses it, and when documents are created here]

## Template

**Location:** `skills/[type]/SKILL.md`

**Template Required:** [Yes/No - be explicit]

**Custom Documents Allowed:** [Yes/No - be explicit]

**Quick Start:**
```bash
/pm.create-[type] "[Document Title]"
```

## Naming Convention

```
YYYY-MM-DD-[type]-NNN-[description].md

Examples:
- 2025-11-03-[type]-001-example-one.md
- 2025-11-03-[type]-002-example-two.md
- 2025-11-03-[type]-003-example-three.md
```

**Components:**
- `YYYY-MM-DD`: Creation date (ISO format)
- `[type]`: Document type identifier
- `NNN`: Sequential 3-digit number (001, 002, 003...)
- `[description]`: Brief kebab-case description

## Required Frontmatter

```yaml
---
document_type: "[type]"
status: "draft|review|approved|..."
owner: "[Owner Name]"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
[additional_required_field_1]: value
[additional_required_field_2]: value

# Traceability (required for most documents)
relationships:
  depends_on:
    - path: "[absolute/path/to/dependency.md]"
      title: "[Document Title]"
      reason: "[Why this dependency exists]"
  blocks:
    - path: "[absolute/path/to/blocked.md]"
      title: "[Document Title]"
      reason: "[What this blocks]"
---
```

## Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `template` | string | Reference to template file | `skills/[type]/SKILL.md` |
| `status` | enum | Document lifecycle status | `draft`, `review`, `approved` |
| `owner` | string | Document owner/author | `John Doe` |
| `created` | date | Creation date | `2025-11-03` |
| `updated` | date | Last update date | `2025-11-03` |
| `[field]` | [type] | [Description] | [Example value] |

## Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `tags` | array | Categorization tags | `["tag1", "tag2"]` |
| `stakeholders` | array | Involved parties | `["Team A", "Team B"]` |
| `[field]` | [type] | [Description] | [Example value] |

## Lifecycle

1. **Draft** - Initial creation, work in progress
2. **Review** - Under stakeholder review
3. **Approved** - Formally approved and active
4. **[Status]** - [Description]
5. **Archived** - No longer active, kept for history

## Constitutional Compliance

[Explain which PM Constitution articles apply and how]

- **Article I:** [How it applies]
- **Article III:** Traceability - Must link to [upstream/downstream docs]
- **Article [N]:** [How it applies]

## Related Documents

- **Upstream:** `[folder]/` - [What typically comes before]
- **Downstream:** `[folder]/` - [What typically comes after]
- **Cross-references:** `[folder]/` - [Related documentation]

## Workflow Integration

**[Phase] Phase ([System]):**
1. [Step 1] -> `[command or action]`
2. [Step 2] -> `[command or action]`
3. [Step 3] -> `[command or action]`

**Example Workflow:**
```bash
# 1. Create document
/pm.create-[type] "[Title]"

# 2. Review and iterate
[review process]

# 3. Approve
/pm.approve-[type]

# 4. Next steps
[what happens after approval]
```

## Validation

**Run validation after creating/updating documents:**
```bash
bun scripts/validate-documents.js --path product-knowledge/[path]/
```

**Common validation errors:**
- Missing template field
- Invalid naming convention
- Missing required fields
- Broken links

## Examples

### Example 1: [Scenario]
```
[Show a real example filename and brief description]
2025-11-01-[type]-001-example.md - [What this document contains]
```

### Example 2: [Scenario]
```
[Show another example]
2025-11-02-[type]-002-another.md - [What this document contains]
```

## AI Assistant Usage

**For Claude:**
1. ALWAYS read this README first for requirements
2. ALWAYS include the `template` field in frontmatter
3. ALWAYS use absolute paths from project root
4. ALWAYS create bidirectional links
5. Use `[skill-name]` skill for [specific guidance]
6. Validate with `bun scripts/validate-documents.js`

**Common mistakes to avoid:**
- Forgetting the template field
- Using relative paths
- Missing bidirectional links
- Invalid naming convention

## Quick Reference

| Action | Command/Path |
|--------|--------------|
| Create new | `/pm.create-[type]` |
| Template | `skills/[type]/SKILL.md` |
| Validate | `bun scripts/validate-documents.js --path [file]` |
| Examples | See existing files in this folder |

---

**Folder maintained by:** [Team/Role]
**Last updated:** YYYY-MM-DD
**Questions:** [Contact or resource]
