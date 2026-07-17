---
id: responsibility-matrix
status: In Review
owner: Product Owner
created_at: "2026-07-16"
---
# Responsibility Matrix (RACI)

R = Responsible (trực tiếp làm) · A = Accountable (chịu trách nhiệm cuối) · C = Consulted · I = Informed

| Công việc | Product Owner | AI Technical Architect | Software Engineer |
|---|:-:|:-:|:-:|
| Requirement Discovery | A | R | I |
| Architecture Decision (ADR) | A | R | C |
| Documentation | A | R | I |
| Coding | I | C | R |
| Code Review | I | R | C |
| Architecture Review (đổi kiến trúc) | I | R | C |
| Final Approve | A | C | I |

**Lưu ý:** khi có nhiều người cùng giữ role "AI Technical Architect" hoặc "Software Engineer", cột này áp dụng cho role, không phân biệt ai trong nhóm đó — trách nhiệm cụ thể theo module xem [Module Owner trong team.yaml](./team.yaml).
