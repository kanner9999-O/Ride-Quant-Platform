---
id: domain-index
title: Domain Contract Index
status: Draft
version: "0.10"
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
| **0.2-A — Domain foundation** | `context-map.yaml` (v0.3 — non-blocking documentation-reference fix) + `candle.md` (v0.4, không đổi ở vòng consolidation này) | Draft — **`Consolidated Stable`** (xem dưới) |
| **0.2-B — Data & analysis chain** | `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md` | **Đã bắt đầu — B1 candidate Draft, final narrow correction.** `swing.md` v0.2 Draft (verdict: **Clean**, không đổi) + `structure.md` v0.4 Draft (đóng IRB-FD-STR-MAJ-01 + IRB-FD-STR-MIN-01, 2 finding cuối từ Independent Review B final delta). Sẵn sàng cho ChatGPT Review A final re-review + Independent Review B final re-review. `regime.md`, `feature.md`, `context.md` (B2/B3/B4) **chưa bắt đầu**. Package 0.2-B **chưa `Consolidated Stable`** (xem dưới). |
| **0.2-C — Decision & execution chain** | `strategy.md` (Strategy Definition + Strategy Instance), `decision.md`, `risk.md`, `position.md`, `replay-event.md`, cộng các concept chưa có trong danh sách gốc: account, venue, instrument, order, fill, trade-intent, execution-intent | [ADR-012](../adr/ADR-012.md) v0.3 và [ADR-013](../adr/ADR-013.md) v0.3 nay **`Approved`** (Product Owner, 2026-07-28) — **ADR dependency gate is now open.** Package 0.2-C is authorized to begin planning and authoring, subject to its normal package scope authorization and review workflow. **No Package 0.2-C artifact is authored in this transaction.** |

**Thứ tự dự kiến trong từng package không đổi** so với kế hoạch gốc (theo dependency đã chốt ở [ADR-003](../adr/ADR-003.md) và [07-module-taxonomy.md](../constitution/07-module-taxonomy.md)); Package 0.2-C được liệt kê đầy đủ hơn danh sách gốc vì danh sách gốc thiếu Account/Order/Execution/Venue/Instrument.

## Package 0.2-A đã đạt `Consolidated Stable` — Package 0.2-B được mở khóa để bắt đầu authoring

**`Consolidated Stable` nghĩa là:**

- author self-review hoàn tất;
- ChatGPT Review A hoàn tất;
- Independent Review B hoàn tất;
- consolidation hoàn tất;
- không còn qualifying finding nào chưa xử lý so với baseline của package.

**Package 0.2-A đã đạt đủ cả năm điều kiện trên**, qua hai vòng review đầy đủ:

1. ChatGPT Review A + Independent Review B (baseline gốc) → consolidated thành `context-map.yaml` v0.1→v0.2, `candle.md` v0.2→v0.3.
2. ChatGPT Review A re-review + Independent Review B delta review (baseline v0.2/v0.3) → consolidated thành `candle.md` v0.3→v0.4 (F-CND-MAJ-01).
3. **ChatGPT Review A final re-review: Clean. Independent Review B final delta: Clean với đúng 1 Suggestion không-blocking.** Backward Consistency Check: `No conflict`. **0 qualifying finding chưa xử lý.**

Suggestion không-blocking đã được incorporate trong chính transaction này: `context-map.yaml` v0.2→v0.3 — sửa cross-reference "chi tiết semantic tại candle.md §11" (không chính xác) thành "chi tiết correction/recompute và classification semantics tại candle.md §§10–11" — **thuần túy sửa tài liệu tham chiếu, không đổi semantic** (provider/consumer/contract_id/relationship_type/model_influence/translation_policy/consumer_obligation giữ nguyên).

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status.** Mọi artifact cấu thành (`context-map.yaml`, `candle.md`, chính README này) **vẫn giữ `status: Draft`**. Package 0.2-A **không** được Product Owner Approve, **không** Lock. Phase 0.2 **không** được coi là hoàn tất chỉ vì Package 0.2-A đạt Consolidated Stable — Package 0.2-B và 0.2-C vẫn chưa có artifact nào.

Package 0.2-B **được authorize để bắt đầu authoring** kể từ transaction trước — Package 0.2-B1 (swing.md + structure.md) là artifact đầu tiên thực sự được author (xem mục dưới).

## Package 0.2-B1 — `structure.md` v0.4, final narrow correction; `swing.md` v0.2 và `context-map.yaml` v0.5 Clean, không đổi

**Phạm vi B1:** hoàn thiện chuỗi `Candle → Swing → Structure` — [`swing.md`](./swing.md) v0.2, [`structure.md`](./structure.md) v0.4, cả hai `capability_id: market-structure` / `domain_context_id: market-structure-analysis` (đã đăng ký sẵn tại [`context-map.yaml`](./context-map.yaml) v0.5, không tạo capability/context mới).

**Lịch sử review đầy đủ:**

1. ChatGPT Review A + Independent Review B clean-room (trên baseline v0.1) → consolidated thành `swing.md` v0.1→v0.2 (3 Major), `structure.md` v0.1→v0.2 (3 Major), `context-map.yaml` v0.4→v0.5 (1 Minor).
2. ChatGPT Review A delta + Independent Review B delta (trên baseline v0.2) — verdict: `swing.md` **Clean**; `context-map.yaml` **Clean**; `structure.md` **Revision required** — 2 Major (D-B1-STR-MAJ-01, D-B1-STR-MAJ-02) → xử lý thành `structure.md` v0.2→v0.3.
3. **Independent Review B final delta (trên baseline v0.3)** — phát hiện 2 finding cuối trên `structure.md`: **IRB-FD-STR-MAJ-01** (một câu trong §6a mâu thuẫn với chính lexicographic rule đã khai — nói "bỏ qua tiêu chí 5, chuyển thẳng tiêu chí 6" khi tiêu chí 3/4 đã phân biệt được, thay vì dừng lại đúng tại 3/4), **IRB-FD-STR-MIN-01** (§9 còn sót identifier `relevant_swing_selection_policy` lỗi thời của 4-tier order v0.2, chưa cập nhật theo 8-tiêu-chí v0.3).
4. **Final narrow correction này** xử lý đúng 2 finding cuối — chỉ sửa `structure.md` (v0.3→v0.4): thay thế câu mâu thuẫn bằng thuật toán chuẩn tường minh + 3 ví dụ minh họa (đóng IRB-FD-STR-MAJ-01); xóa identifier lỗi thời, §9 nay chỉ tham chiếu normative tới §6a — đúng MỘT canonical identifier duy nhất (đóng IRB-FD-STR-MIN-01). `swing.md` và `context-map.yaml` **giữ nguyên byte-for-byte** (đã Clean).

**Trạng thái review:**

- Author self-review (baseline v0.4, sau final correction): **hoàn tất** — xem CHANGELOG, 20 self-review scenario.
- ChatGPT Review A final re-review + Independent Review B final re-review (trên `structure.md` v0.4): **CHƯA diễn ra.**
- Consolidation: **chưa diễn ra** ở vòng này (chờ final re-review).

**Package 0.2-B (và do đó B1) CHƯA đạt `Consolidated Stable`** — điều kiện đó đòi hỏi cả hai vòng review độc lập hoàn tất và 0 qualifying finding, đúng định nghĩa đã khóa ở mục Package 0.2-A phía trên. `structure.md` v0.4 sẵn sàng để chuyển sang ChatGPT Review A final re-review + Independent Review B final re-review; `swing.md` v0.2 và `context-map.yaml` v0.5 đã Clean, không cần review thêm.

**Không tuyên bố hoàn thành hay approval ở bất kỳ mức nào:** `swing.md`/`structure.md`/`context-map.yaml` `status: Draft`; không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-B2/B3/B4 (`regime.md`, `feature.md`, `context.md`) **chưa bắt đầu**. Package 0.2-C **vẫn chưa có artifact nào được author**. Phase 0.2 vẫn active và chưa hoàn tất.

## Danh sách dự kiến (Package 0.2-A + 0.2-B)

candle.md → swing.md → structure.md → regime.md → feature.md → context.md
