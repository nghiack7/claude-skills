---
name: adr
description: >
  This skill should be used when the user asks to "tạo ADR", "viết ADR", "architecture decision",
  "quyết định kỹ thuật", "nên chọn X hay Y", "so sánh giải pháp", "trade-off analysis",
  "technical decision", or needs to evaluate architectural options with pros/cons analysis.
---

## Related Skills

- **workflow** - Quy trình tổng thể (ADR nằm trong docs/ cùng stories)
- **technical-analysis** - Phân tích codebase trước khi viết ADR
- **scalability-design** - Khi ADR liên quan tới scalability

# ADR Skill

Tạo Architecture Decision Records — tài liệu hóa các quyết định kỹ thuật quan trọng để team hiểu **tại sao** chọn giải pháp này thay vì giải pháp khác.

## Khi nào cần ADR?

- Chọn technology/framework/library mới
- Thay đổi kiến trúc hệ thống (microservice split, database migration, ...)
- Thay đổi approach cho một vấn đề đã có solution cũ
- Bất kỳ quyết định nào ảnh hưởng 2+ services hoặc 2+ teams

Nếu không chắc, hỏi: "6 tháng sau có ai hỏi 'tại sao làm vậy?' không?" — nếu có, viết ADR.

## Workflow tạo ADR

### Bước 1: Thu thập context

Trước khi viết, thu thập thông tin:

1. **Từ user:** Hỏi vấn đề cần quyết định, constraints, timeline
2. **Từ codebase:** Đọc code liên quan, dependencies, current architecture
3. **Từ Jira:** Story key nếu ADR liên quan tới story cụ thể

### Bước 2: Phân tích options

Với mỗi option, đánh giá theo các tiêu chí:
- Performance
- Complexity / maintainability
- Team expertise
- Cost (infra, licensing)
- Time to implement
- Scalability
- Risk

Dùng comparison matrix để so sánh định lượng.

### Bước 3: Generate ADR

Đọc template từ `references/adr-template.md` và fill in dựa trên phân tích.

### Bước 4: Đặt file

```
repository/
├── docs/
│   ├── adr/
│   │   ├── 001-database-selection.md
│   │   ├── 002-auth-strategy.md
│   │   └── ...
│   └── stories/
```

Naming: `<number>-<short-description>.md` — số tăng dần trong repo.

## ADR Format tóm tắt

Mỗi ADR cần tối thiểu:

1. **Context & Problem** — Vấn đề gì cần quyết định
2. **Decision Drivers** — Tiêu chí quan trọng
3. **Options** — Ít nhất 2 options với pros/cons
4. **Decision** — Chọn gì và tại sao
5. **Consequences** — Hệ quả positive/negative
6. **Jira link** — Nếu liên quan tới story

Template đầy đủ: xem `references/adr-template.md`
