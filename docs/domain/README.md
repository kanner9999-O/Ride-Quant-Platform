---
id: domain-index
title: Domain Contract Index
status: Draft
version: "0.17"
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
| **0.2-B — Data & analysis chain** | `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md` | **Package 0.2-B1: `Consolidated Stable`** (xem dưới) — `swing.md` v0.2 Draft + `structure.md` v0.4 Draft, cả hai Clean qua đầy đủ hai vòng review độc lập. **Package 0.2-B2: `Consolidated Stable`** (xem dưới) — `regime.md` v0.2 Draft, Clean qua đầy đủ review, 0 finding. **Package 0.2-B3: `Consolidated Stable`** (xem dưới) — `feature.md` v0.2 Draft, Clean qua đầy đủ review (bao gồm narrow revision xử lý `RA-B3-MAJ-01`/`IRB-B3-MAJ-01`), 0 finding còn lại. **Package 0.2-B4** (`context.md`): baseline dependency đã thỏa, eligible cho Product Owner scope authorization, **chưa bắt đầu**. Package 0.2-B (tổng thể) **chưa `Consolidated Stable`** — B1/B2/B3 đạt, B4 chưa có artifact nào. |
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

## Package 0.2-B1 đã đạt `Consolidated Stable`

**Phạm vi B1:** hoàn thiện chuỗi `Candle → Swing → Structure` — [`swing.md`](./swing.md) v0.2 Draft, [`structure.md`](./structure.md) v0.4 Draft, cả hai `capability_id: market-structure` / `domain_context_id: market-structure-analysis` (đã đăng ký sẵn tại [`context-map.yaml`](./context-map.yaml) v0.5 Draft, không tạo capability/context mới).

**Lịch sử review đầy đủ — cả hai track độc lập, bốn vòng mỗi track:**

| Vòng | Baseline HEAD | ChatGPT Review A | Independent Review B |
|---|---|---|---|
| Initial | `5d46bacc8b...` | Swing: Revision required · Structure: Revision required · Context Map: Clean · **Package B1: Revision required** | Swing: Revision required · Structure: Revision required · Context Map: Clean với 1 minor documentation correction · **Package B1: Revision required** |
| Delta | `3813c60012...` | Swing v0.2: Clean với minor correction · Structure v0.2: Revision required · Context Map v0.5: Clean | Swing v0.2: Clean · Structure v0.2: Revision required · Context Map v0.5: Clean |
| Final delta | `7c789b6dbb...` | Swing v0.2: Clean · Structure v0.3: Clean · Context Map v0.5: Clean | Swing v0.2: Clean · Structure v0.3: Revision required · Context Map v0.5: Clean |
| **Final re-review** | `d6545de3fc...` | Swing v0.2: Clean · Structure v0.4: Clean · Context Map v0.5: Clean · **Package B1: Clean, 0 finding** | Swing v0.2: Clean · Structure v0.4: Clean · Context Map v0.5: Clean · Package integration: Clean · Backward consistency: `No conflict` · **0 qualifying finding · Package B1: consolidation-ready** |

Mỗi vòng "Revision required" đã được xử lý bằng một revision commit atomic riêng (authoring B1 → consolidated revision → revision-qualified Structure reference → final ordering correction), đều đã push lên `main`, đúng thứ tự lịch sử trên.

**Kết luận consolidation:** ChatGPT Review A final re-review và Independent Review B final re-review, cả hai trên baseline `d6545de3fc...` (`swing.md` v0.2, `structure.md` v0.4, `context-map.yaml` v0.5), đều **Clean**. Backward Consistency Check: `No conflict`. **0 qualifying finding chưa xử lý.**

## `Consolidated Stable` baseline — Package 0.2-B1

**Exact reviewed artifact baseline (pinned):**

```text
swing.md         v0.2   blob 5bbe666ff404209876a721b1e01cb9ac62011062
structure.md     v0.4   blob 78964dfb6852bbac3fa1e034d64b4fc8031c3fef
context-map.yaml v0.5   blob 0d87744e2a1ffdd592b05bdfbb0ef5dab85b5920
reviewed HEAD:   d6545de3fcc767e03f74fd0712ada792372d1c33
```

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A phía trên: authoring hoàn tất cho phạm vi B1; ChatGPT Review A hoàn tất; Independent Review B hoàn tất; mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để package kế tiếp (B2) bắt đầu planning — **không** ngụ ý Product Owner Approval, **không** ngụ ý Lock. `swing.md`, `structure.md`, `context-map.yaml` **vẫn giữ `status: Draft`**, `approved_by: null`, `approved_at: null` — artifact lifecycle và package lifecycle là hai trục tách biệt.

## Package 0.2-B2 đã đạt `Consolidated Stable`

**Phạm vi B2:** bắt đầu chuỗi `Candle → Raw Regime → Feature`, song song và độc lập hoàn toàn với `Candle → Swing → Structure` ([ADR-003](../adr/ADR-003.md)) — [`regime.md`](./regime.md) v0.2 Draft, `capability_id: market-regime` / `domain_context_id: raw-regime-analysis` (đã đăng ký sẵn từ Package 0.2-A tại [`context-map.yaml`](./context-map.yaml) v0.6, không đổi trong toàn bộ B2). Hai dimension: **Volatility**, **Directional Persistence**.

**Lịch sử review đầy đủ:**

1. ChatGPT Review A + Independent Review B (baseline v0.1) → 4 finding: `RA-B2-MIN-01`/`IRB-B2-MIN-03` (Current View ambiguity: no-row vs `UNAVAILABLE`, một correction chung), `IRB-B2-MAJ-01` (candle evidence normalization thiếu), `IRB-B2-MAJ-02` (invalidation envelope binding thiếu).
2. Narrow revision (v0.1→v0.2) xử lý đúng 4 finding trên — chỉ sửa `regime.md`; `context-map.yaml`/`swing.md`/`structure.md` không đổi.
3. **ChatGPT Review A (trên `regime.md` v0.2):** Clean — Blocker 0, Major 0, Minor 0.
4. **Independent Review B narrow delta (trên `regime.md` v0.2):** `IRB-B2-MAJ-01` resolved, `IRB-B2-MAJ-02` resolved, `IRB-B2-MIN-03` resolved — Blocker 0, Major 0, Minor 0, Suggestion 0. `regime.md` v0.2: Clean. Package 0.2-B2 integration: Clean. **Package 0.2-B2: consolidation-ready.**

**Kết luận consolidation:** ChatGPT Review A và Independent Review B narrow delta, cả hai trên baseline `78479ab088...` (`regime.md` v0.2, `context-map.yaml` v0.6 không đổi), đều **Clean**. **0 qualifying finding chưa xử lý.**

## `Consolidated Stable` baseline — Package 0.2-B2

**Exact reviewed artifact baseline (pinned):**

```text
regime.md         v0.2   blob edd1584377f1db84269e7b1dfdd4926d0ce01c70
context-map.yaml  v0.6   blob 5447f91435b5ffdc01424988f29e0d9d5ad76f99
reviewed HEAD:    78479ab088b1a32c580c9a729a53333896b952b3
```

**Dependency không đổi trong suốt B2:** `candle.md` v0.4, `swing.md` v0.2, `structure.md` v0.4 — cả ba giữ nguyên byte-for-byte từ baseline Package 0.2-B1.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A: authoring hoàn tất cho phạm vi B2; ChatGPT Review A hoàn tất; Independent Review B hoàn tất; mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để package kế tiếp (B3) bắt đầu planning — **không** ngụ ý Product Owner Approval, **không** ngụ ý Lock, **không** đóng OQ nào, **không** authorize Live. `regime.md` **vẫn giữ `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package 0.2-B3 (Feature) — baseline dependency đã thỏa, sau đó Product Owner xác nhận scope authorization tường minh** ("Authorize Package 0.2-B3 minimal Feature scope.") — B3 authoring đã bắt đầu (xem mục dưới). **Package 0.2-B4** (`context.md`) tương tự **chưa bắt đầu**.

## Package 0.2-B3 đã đạt `Consolidated Stable`

**Phạm vi B3 (scope tối thiểu, đã Product Owner authorize):** điểm fan-in có kiểm soát `Candle/Swing/Raw Regime → Feature`, đúng [ADR-003](../adr/ADR-003.md) — [`feature.md`](./feature.md) v0.2 Draft, `capability_id: feature-engineering` / `domain_context_id: feature-engineering` (đã đăng ký sẵn từ Package 0.2-A tại [`context-map.yaml`](./context-map.yaml) v0.7, không đổi trong toàn bộ B3). Đúng **ba founding feature type**: `volatility_metric` (dual-path Candle/Regime pinned), `directional_persistence_metric` (dual-path pinned, thống kê thuần túy, không mã hóa Bullish/Bearish, không tiêu thụ Structure orientation), `distance_to_last_confirmed_swing` (Candle làm giá tham chiếu + SwingConfirmed, effective-time-safe Eligible Swing selection).

**Semantic ổn định đã pin (không restate toàn bộ contract):** subject identity năm field; đúng một upstream path (Candle hoặc Regime) mỗi Feature Definition; input normalization deterministic; correction lineage append-only; không Feature-to-Feature dependency; `FeatureCurrentView` no-row / `VALID` / `PENDING_CORRECTION`; Eligible Swing selection effective-time-safe (ordered filter pipeline trước total order, §9a); không phải Strategy signal hay Context snapshot; không ADR mới.

**Lịch sử review đầy đủ:**

1. Author self-review v0.1 (authoring) → 1 gap tự phát hiện và tự sửa trước commit (thiếu concrete canonical policy value).
2. ChatGPT Review A + Independent Review B (baseline v0.1) → 2 finding: `RA-B3-MAJ-01`, `IRB-B3-MAJ-01` — cùng một defect (effective-time look-ahead trong eligible-Swing selection cho `distance_to_last_confirmed_swing`), một correction.
3. Narrow revision (v0.1 → v0.2) xử lý đúng 2 finding trên — chỉ sửa `feature.md`; `context-map.yaml`/`candle.md`/`swing.md`/`structure.md`/`regime.md` không đổi.
4. **ChatGPT Review A final delta (trên `feature.md` v0.2):** `RA-B3-MAJ-01` resolved — Blocker 0, Major 0, Minor 0, Suggestion 0; `feature.md` v0.2: Clean.
5. **Independent Review B narrow delta (trên `feature.md` v0.2):** `IRB-B3-MAJ-01` resolved — Blocker 0, Major 0, Minor 0, Suggestion 0; `feature.md` v0.2: Clean; Package 0.2-B3 integration: Clean. **Consolidation readiness: Ready.**

**Kết luận consolidation:** ChatGPT Review A final delta và Independent Review B narrow delta, cả hai trên baseline `ed88130302...` (`feature.md` v0.2, `context-map.yaml` v0.7 không đổi), đều **Clean**. **0 qualifying finding chưa xử lý.**

## `Consolidated Stable` baseline — Package 0.2-B3

**Exact reviewed artifact baseline (pinned):**

```text
feature.md        v0.2   blob 2262adf9253ea20c8d817d1066f50c4353d2d35d
context-map.yaml  v0.7   blob 3a93845abcf6efb7214939f8dc2e36d02bb39b65
reviewed HEAD:    ed8813030203cd9e5f779f54be752a3e94c4f68b
```

**Dependency không đổi trong suốt B3:** `candle.md` v0.4, `swing.md` v0.2, `structure.md` v0.4, `regime.md` v0.2 — tất cả giữ nguyên byte-for-byte từ baseline trước đó.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A: authoring hoàn tất cho phạm vi B3; ChatGPT Review A hoàn tất; Independent Review B hoàn tất; mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để package kế tiếp (B4) bắt đầu planning — **không** ngụ ý Product Owner Approval, **không** ngụ ý Lock, **không** đóng OQ nào, **không** authorize Live. `feature.md` **vẫn giữ `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package 0.2-B4 (Context) — baseline dependency đã thỏa** — eligible cho Product Owner scope authorization tường minh, tương tự cơ chế đã áp dụng cho B3 ("Authorize Package 0.2-B3 minimal Feature scope."). **Chưa bắt đầu, chưa author, và KHÔNG được authorize bởi transaction này.** Package 0.2-B (tổng thể) vẫn **chưa hoàn tất** cho tới khi B4 hoàn thành.

**Context Map wording concern — deferred, non-blocking:** `context-map.yaml` mô tả `feature-engineering` (capability và context) bằng cụm "Feature/Signal" — ghi chú documentation-only đã ghi nhận tại `feature.md` §20, cạnh định nghĩa "Feature KHÔNG phải trade signal" ở đầu tài liệu. **Không phải executable finding**, không chặn consolidation này. `context-map.yaml` **không đổi** trong transaction này — không tạo OQ mới cho việc này (không thuộc phạm vi governance-level OQ).

**Package 0.2-C vẫn chưa có artifact nào được author.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn **active và chưa hoàn tất**.

## Danh sách dự kiến (Package 0.2-A + 0.2-B)

candle.md → swing.md → structure.md → regime.md → feature.md → context.md
