---
id: 09-plugin-model
title: Plugin Model
version: "1.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["02-platform-invariants", "07-module-taxonomy"]
---

# 9. Plugin Model

- **Strategy = Plugin.** Mỗi strategy có `strategy.json`/metadata riêng chứa: strategy-level philosophy, tham số, version riêng.
- **AI Module:** mặc định là consumer thuần túy của Event Bus. Nếu muốn tham gia Decision Pipeline, phải implement như một **Decision Advisor** — chịu sự gatekeeping của Risk Gateway giống mọi strategy khác (I-4, I-7), không có ngoại lệ.
- **Versioning độc lập theo từng plugin:** Platform version độc lập với version của từng strategy. Cập nhật một plugin không ảnh hưởng plugin khác.
