---
id: domain-index
title: Domain Contract Index
status: Draft
version: "0.2"
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-28"
next_review: null
---

# Domain Contract & Glossary — Phase 0.2 (đang tiến hành, chưa hoàn tất)

Thư mục này chứa Domain Contract cho từng khái niệm miền, mỗi file = 1 khái niệm, theo format quy định tại [04-domain-principles.md §4.3](../constitution/04-domain-principles.md). Glossary **hợp nhất vào** mỗi Domain Contract — không có file glossary riêng ([Chapter 4 §4.3](../constitution/04-domain-principles.md)).

## Registry prerequisite

[`context-map.yaml`](./context-map.yaml) là **authoritative registry** cho Business Capability + Domain Context identity/relationship ([Chapter 4 §4.2](../constitution/04-domain-principles.md), Locked). **Mọi `capability_id`/`domain_context_id` dùng trong một Domain Contract phải tồn tại sẵn ở đây trước** — Domain Contract không được tự định nghĩa capability/context mới. `context-map.yaml` phải tồn tại trước hoặc cùng lúc với Domain Contract đầu tiên tham chiếu tới nó.

## Conformance example

[`candle.md`](./candle.md) là **Domain Contract đầu tiên** — chứng minh registry ở trên resolve đúng đầu-cuối theo đúng template Chapter 4 §4.3, trước khi các concept khác được viết dựa trên hình dạng đó.

## Drafting packages

| Package | Nội dung | Trạng thái |
|---|---|---|
| **0.2-A — Domain foundation** | `context-map.yaml` (6 capability/context: Instrument/Venue Reference, Market Data, Market Structure, Market Regime, Feature Engineering, Context Aggregation) + `candle.md` | Draft — author self-review xong, **chưa** Consolidated Stable (xem dưới) |
| **0.2-B — Data & analysis chain** | `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md` | Chưa bắt đầu |
| **0.2-C — Decision & execution chain** | `strategy.md` (Strategy Definition + Strategy Instance), `decision.md`, `risk.md`, `position.md`, `replay-event.md`, cộng các concept chưa có trong danh sách gốc: account, venue, instrument, order, fill, trade-intent, execution-intent | Chưa bắt đầu — chặn bởi [ADR-012](../adr/ADR-012.md) và [ADR-013](../adr/ADR-013.md) (cả hai đang `Draft`, chưa Approved) |

**Thứ tự dự kiến trong từng package không đổi** so với kế hoạch gốc (theo dependency đã chốt ở [ADR-003](../adr/ADR-003.md) và [07-module-taxonomy.md](../constitution/07-module-taxonomy.md)); Package 0.2-C được liệt kê đầy đủ hơn danh sách gốc vì danh sách gốc thiếu Account/Order/Execution/Venue/Instrument.

## Package 0.2-B không được bắt đầu dựa trên authority của 0.2-A cho tới khi 0.2-A đạt `Consolidated Stable`

**`Consolidated Stable` nghĩa là:**

- author self-review hoàn tất;
- ChatGPT Review A hoàn tất;
- Independent Review B hoàn tất;
- consolidation hoàn tất;
- không còn qualifying finding nào chưa xử lý so với baseline của package.

Trạng thái hiện tại của Package 0.2-A: **author self-review hoàn tất**, ba review còn lại **chưa diễn ra**. Package 0.2-A **không** được coi là Product Owner approve/lock, và Phase 0.2 **không** được coi là hoàn tất chỉ vì Package 0.2-A tồn tại.

## Danh sách dự kiến (Package 0.2-A + 0.2-B)

candle.md → swing.md → structure.md → regime.md → feature.md → context.md
