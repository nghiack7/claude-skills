---
name: workflow
description: >
  This skill should be used when the user asks about "workflow", "quy trình", "solution template",
  "viết solution", "commit format", "branch naming", "implementation doc", "docs/stories",
  "tạo solution", "tạo doc", or needs guidance on engineering workflow from sprint planning to merge,
  solution writing, commit conventions, or implementation documentation.
---

# Engineering Workflow

Quy trình phát triển bắt buộc cho toàn bộ team engineering.

## Workflow tổng quan

```
Sprint Planning
    |
    v
Viết Solution trên Jira Story ---- FE + BE cùng viết nếu liên quan cả hai
    |
    v
Solution Review & Approve
    |
    v
Tạo branch: feature/<STORY-KEY>-description
    |
    v
Code + Viết docs/stories/ song song
    |   Commit: <type>(<scope>): message <STORY-KEY> <TASK-KEY>
    |                |
    |                v
    |         Có thay đổi solution? ---- Cập nhật Jira Story + docs
    |
    v
Tạo MR (code + docs) -> Code Review (dựa trên solution)
    |
    v
Merge
```

---

## 1. Solution Review (Sau Sprint Planning)

- Sau sprint planning, mỗi engineer **viết solution** vào **Jira story** (KHÔNG phải trên task).
- Nếu story liên quan cả FE và BE, **cả hai engineer cùng viết solution** — phải thông suốt end-to-end.
- Solution phải được **review và approve** trước khi bắt đầu code.
- Solution trên Jira story là **baseline cho code review** — code khác solution mà chưa cập nhật = reject MR.

### Rule: KHÔNG ref gì ở local

Solution trên Jira phải là tài liệu độc lập, reviewer/BA/PO đọc được ngay:

- Không ref local path như `/Users/...`, repo-local file, branch chưa push, hay file chỉ tồn tại trên máy engineer.
- Nếu cần dẫn chứng code, dùng GitLab URL hoặc MR URL.
- Nếu cần dẫn Jira, dùng Jira story/task URL.
- Nếu cần dẫn tài liệu, dùng Confluence/GitLab/Jira attachment URL.

### Solution template

Khi engineer cần viết solution, đọc và output nội dung từ `references/solution-template.md`.

Solution bao gồm các phần chính:
- Bối cảnh & Overview
- **Diagrams** (bắt buộc — xem bảng bên dưới)
- Frontend (nếu có): UI flow, components, API calls
- Backend (nếu có): endpoints, request/response, business logic, DB changes
- Contract FE ↔ BE (bắt buộc khi story liên quan cả hai)
- Ảnh hưởng & Rủi ro

### Solution Review Checklist

Reviewer **phải check tất cả** trước khi approve solution:

- [ ] **Edge cases:** Liệt kê rõ các trường hợp biên, không chỉ happy path (empty data, concurrent requests, partial failure, ...)
- [ ] **Error handling:** Mỗi API call / external dependency có xử lý lỗi rõ ràng (retry? fallback? propagate error?)
- [ ] **Data flow:** Rõ ràng data đi từ đâu → transform thế nào → lưu ở đâu → trả về gì
- [ ] **Diagram match text:** Diagram phản ánh đúng logic trong text, không vẽ cho có
- [ ] **Performance:** Có concern về volume/load không? Nếu có, đã address chưa? (batch size, pagination, indexing, caching)
- [ ] **Breaking changes:** Có ảnh hưởng tới API contract / data format hiện tại không? Migration plan?
- [ ] **Cross-repo impact:** Nếu story span nhiều repo, đã mô tả rõ phần nào thuộc repo nào chưa?

**Rule:** Solution không pass checklist = KHÔNG được approve. Engineer sửa lại rồi review lần nữa.

### Diagram requirements

| Diagram | Bắt buộc khi | Ví dụ |
|---------|-------------|-------|
| **Flow Diagram** | Mọi story | Logic xử lý, user flow, decision tree |
| **Sequence Diagram** | Có 2+ components tương tác | FE↔BE, service↔service, service↔queue |
| **ER Diagram** | Thay đổi data model | Thêm field, tạo collection mới |
| **State Diagram** | Feature có nhiều trạng thái | Order status flow, subscription lifecycle |

Dùng Mermaid syntax để vẽ trực tiếp trong Jira/Markdown.

---

## 2. Git Branching & Commit Convention

### Branch Naming

Dùng **story key** làm branch name (KHÔNG dùng task key):

```
feature/PROJ-123-short-description
bugfix/PROJ-123-short-description
hotfix/PROJ-123-short-description
```

### Commit Message — Conventional Commits

Format: `<type>(<scope>): <mô tả ngắn> <STORY-KEY> <TASK-KEY>`

**Ví dụ:**
```
feat(orders): add order validation API PROJ-123 PROJ-124
fix(auth): handle expired token refresh PROJ-123 PROJ-125
refactor(sync): extract retry logic PROJ-200 PROJ-201
```

| Type | Khi nào dùng |
|------|-------------|
| `feat` | Thêm feature mới |
| `fix` | Sửa bug |
| `refactor` | Refactor code, không thay đổi behavior |
| `docs` | Chỉ thay đổi documentation |
| `test` | Thêm hoặc sửa test |
| `chore` | Build, CI, dependency, config |
| `perf` | Cải thiện performance |
| `style` | Format code, không thay đổi logic |

Quy tắc:
- `scope` là module/area bị ảnh hưởng (khuyến khích)
- Story key **bắt buộc** trong mọi commit
- Task key **bắt buộc** nếu commit thuộc về task cụ thể
- Breaking changes thêm `!` sau scope: `feat(api)!: change response format PROJ-123 PROJ-124`

---

## 3. Cập nhật Solution khi có thay đổi

Trong quá trình code, nếu solution thay đổi so với ban đầu:
- Cập nhật lại trên Jira story (ghi rõ: thay đổi gì, lý do, impact)
- Cập nhật doc trong `docs/stories/` tương ứng
- Reviewer dựa trên solution **mới nhất** trên Jira để review code

---

## 4. Implementation Documentation

Mỗi repo có `docs/stories/` chứa implementation doc **riêng cho repo đó**. Doc này là bản breakdown cụ thể — full solution nằm trên Jira story.

### Mục đích
- Story span nhiều repo (microservice) → mỗi repo cần doc riêng mô tả phần của mình
- Ghi lại **key decisions** implementation mà solution trên Jira không cover chi tiết
- Nằm cùng MR với code, viết song song trong quá trình code

### Quy tắc
- Doc nằm trong `docs/stories/` của repository
- **Luôn mention story key** ở header để link về Jira story chính
- Giữ doc ngắn gọn — chỉ ghi những gì specific cho repo này, không repeat solution
- Nếu story chỉ ảnh hưởng 1 repo và solution trên Jira đã đủ chi tiết → doc có thể rất ngắn (context + changes list)

### Cấu trúc
```
repository/
├── docs/
│   ├── stories/                    <- Implementation docs theo story
│   │   ├── PROJ-123-feature-name.md
│   │   └── PROJ-456-another-feature.md
│   └── ...                         <- Các loại doc khác (ADR, runbook, ...)
├── src/
└── ...
```

### Implementation doc template

Khi engineer cần viết implementation doc, đọc và output nội dung từ `references/implementation-doc-template.md`.

---

## 5. Checklist cho Engineer

- [ ] Đã viết solution trên Jira story (theo format chuẩn, có diagrams)
- [ ] Solution đã được review/approve
- [ ] Branch name dùng story key
- [ ] Commit messages follow Conventional Commits + mention story key và task key
- [ ] Solution trên Jira đã cập nhật nếu có thay đổi
- [ ] Implementation doc trong `docs/stories/` được viết song song với code, nằm cùng MR
- [ ] Doc mention story key

---

## 6. Trách nhiệm

| Vai trò | Trách nhiệm |
|---------|-------------|
| Engineer | Viết solution, code theo solution, cập nhật khi thay đổi, viết docs |
| Reviewer | Review solution trước khi code bắt đầu, review code dựa trên solution |
| Tech Lead | Đảm bảo team follow quy trình, spot-check docs quality |
| PM/PO | Đảm bảo story có đủ context để engineer viết solution |

---

## 7. Anti-patterns

- Viết solution trên Jira task thay vì Jira story.
- Bắt đầu code trước khi solution được review/approve.
- Chỉ mô tả happy path, bỏ qua edge cases và failure modes.
- Vẽ diagram không khớp text hoặc thiếu diagram cho flow chính.
- Ref local file/path trong solution khiến reviewer không truy cập được.
- Code khác solution nhưng không cập nhật Jira story và implementation doc.
- Dùng task key làm branch name thay vì story key.
- Commit thiếu story key/task key.
- Copy full Jira solution vào `docs/stories/` thay vì chỉ ghi phần implementation specific của repo.

---

## 8. Ghi nhớ

- Jira story giữ full solution và là source of truth cho review.
- `docs/stories/` giữ implementation notes theo từng repo, nằm cùng MR với code.
- Nếu output solution hoặc implementation doc, phải đọc template tương ứng trong `references/` trước khi viết.
- Nếu có thay đổi trong lúc code, cập nhật cả Jira story và doc repo trước khi MR review.
