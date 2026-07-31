---
id: domain-index
title: Domain Contract Index
status: Draft
version: "0.53"
owner: Product Owner
reviewers: []
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-28"
next_review: null
---

# Domain Contract & Glossary — Phase 0.2 (Complete — Phase 0.3 là sub-phase kế tiếp)

Thư mục này chứa Domain Contract cho từng khái niệm miền, mỗi file = 1 khái niệm, theo format quy định tại [04-domain-principles.md §4.3](../constitution/04-domain-principles.md). Glossary **hợp nhất vào** mỗi Domain Contract — không có file glossary riêng ([Chapter 4 §4.3](../constitution/04-domain-principles.md)).

## Registry prerequisite

[`context-map.yaml`](./context-map.yaml) là **authoritative registry** cho Business Capability + Domain Context identity/relationship ([Chapter 4 §4.2](../constitution/04-domain-principles.md), Locked). **Mọi `capability_id`/`domain_context_id` dùng trong một Domain Contract phải tồn tại sẵn ở đây trước** — Domain Contract không được tự định nghĩa capability/context mới. `context-map.yaml` phải tồn tại trước hoặc cùng lúc với Domain Contract đầu tiên tham chiếu tới nó.

## Conformance example

[`candle.md`](./candle.md) là **Domain Contract đầu tiên** — chứng minh registry ở trên resolve đúng đầu-cuối theo đúng template Chapter 4 §4.3, trước khi các concept khác được viết dựa trên hình dạng đó.

## Drafting packages

| Package | Nội dung | Trạng thái |
|---|---|---|
| **0.2-A — Domain foundation** | `context-map.yaml` (v0.3 — non-blocking documentation-reference fix) + `candle.md` (v0.4, không đổi ở vòng consolidation này) | Draft — **`Consolidated Stable`** (xem dưới) |
| **0.2-B — Data & analysis chain** | `swing.md`, `structure.md`, `regime.md`, `feature.md`, `context.md` | **Package 0.2-B1: `Consolidated Stable`** (xem dưới) — `swing.md` v0.2 Draft + `structure.md` v0.4 Draft, cả hai Clean qua đầy đủ hai vòng review độc lập. **Package 0.2-B2: `Consolidated Stable`** (xem dưới) — `regime.md` v0.2 Draft, Clean qua đầy đủ review, 0 finding. **Package 0.2-B3: `Consolidated Stable`** (xem dưới) — `feature.md` v0.2 Draft, Clean qua đầy đủ review (bao gồm narrow revision xử lý `RA-B3-MAJ-01`/`IRB-B3-MAJ-01`), 0 finding còn lại. **Package 0.2-B4: `Consolidated Stable`** (xem dưới) — `context.md` v0.2 Draft, tất cả finding resolved (`RA-B4-MAJ-01`/`IRB-B4-MAJ-01`/`IRB-B4-MAJ-02`/`IRB-B4-MAJ-03`/`RA-B4-MIN-02`/`IRB-ADR014-MAJ-01`/`IRB-ADR014-MAJ-02`/`IRB-ADR014-MIN-01`/`IRB-ADR014-MIN-02`/`IRB-B4-FINAL-MIN-01`), [ADR-014](../adr/ADR-014.md) **Approved** (Product Owner, 2026-07-30) là controlling authority. **Package 0.2-B (tổng thể) nay `Consolidated Stable`** — B1/B2/B3/B4 đều đạt. |
| **0.2-C — Decision & execution chain** | `instrument.md`, `venue.md`, `account.md`, `strategy.md` (Strategy Definition + Strategy Instance), `trade-intent.md`, `decision.md`, `risk.md`, `execution-intent.md`, `order.md`, `fill.md`, `position.md`, `replay-event.md` — decomposed thành 7 slice phụ thuộc (C1–C7, xem mục "Package 0.2-C decomposition" dưới đây) | [ADR-012](../adr/ADR-012.md) v0.3 và [ADR-013](../adr/ADR-013.md) v0.3 vẫn **`Approved`** (không đổi). **Package 0.2-C1 (Reference Foundation): `Consolidated Stable`** (xem dưới) — `instrument.md` v0.6 Draft + `venue.md` v0.3 Draft, ChatGPT Review A Clean, Independent Review B Clean with deferred limitations (Phase 1 implementation concerns, non-blocking), 0 blocking finding. **Package 0.2-C2 (Trading Account Foundation): `Consolidated Stable`** (xem dưới) — `account.md` v0.2 Draft, controlling architecture [ADR-012](../adr/ADR-012.md) v0.3 Approved (không sửa), ChatGPT bounded delta Review A Clean, Independent Review B Clean with deferred limitations (Phase 1 implementation concerns, non-blocking), 0 blocking finding. **Package 0.2-C3 (Strategy Foundation): `Consolidated Stable`** (xem dưới) — `strategy.md` v0.3 Draft, controlling architecture [ADR-013](../adr/ADR-013.md) v0.3 Approved (không sửa), ChatGPT final focused delta re-review Clean, Independent Review B final focused delta re-review Clean, 0 blocking finding. **Package 0.2-C4 (Trade Intent and Decision Foundation): `Consolidated Stable`** (xem dưới) — `decision.md` v0.3 Draft + `trade-intent.md` v0.2 Draft, controlling architecture [ADR-010](../adr/ADR-010.md) Approved (Decision Time Model) + Chapter 8 §8.4/§8.5 (Locked) + [ADR-013](../adr/ADR-013.md) v0.3 Approved (không sửa), ChatGPT final focused delta re-review Clean, Independent Review B final focused delta re-review Clean, 0 blocking finding. **Package 0.2-C5 (Risk Gateway and Execution Intent Foundation): `Consolidated Stable`** (xem dưới) — `risk.md` v0.3 Draft + `execution-intent.md` v0.2 Draft (không đổi), controlling architecture Chapter 8 §8.1.1/§8.2/§8.5 (Locked) + Chapter 9 §9.1 (Locked), ChatGPT final focused delta re-review Clean, Independent Review B final focused delta re-review Clean, 0 blocking finding. **Package 0.2-C6 (Order Foundation): `Consolidated Stable`** (xem dưới) — `order.md` v0.2 Draft, controlling architecture `execution-intent.md` §6a (`eligible_for_new_order_creation`, không sửa) + Chapter 8 §8.1.1/§8.2/§8.5 (Locked), ChatGPT bounded delta Review A Clean, Independent Delta Review B Clean, 0 blocking finding. **Package 0.2-C7 (Execution Result, Fill, Position and Replay Integration Foundation): `Consolidated Stable`** (xem dưới) — `execution-result.md` v0.3 Draft + `replay-event.md` v0.3 Draft + `fill.md` v0.3 Draft + `position.md` v0.3 Draft (hai file sau: reference-consistency-only, KHÔNG semantic change), controlling architecture `order.md` §8b (`eligible_for_execution_result_processing`, không sửa) + Chapter 8 §8.1.1/§8.2/§8.5 (Locked) + Chapter 7 §7.4 (Locked, Type 2 Projection), bounded correction v0.2 đóng bốn Major finding, second bounded correction (v0.2→v0.3) đóng `C7-DELTA-MAJ-01`, ChatGPT second bounded delta Review A Clean, Independent second bounded delta Review B Clean, 0 blocking finding. **Package 0.2-C (C1–C7, tổng thể) nay `Consolidated Stable`.** |

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

**Package 0.2-B4 (Context) — baseline dependency đã thỏa, sau đó Product Owner xác nhận scope authorization tường minh** ("Authorize Package 0.2-B4 minimal Context scope.") — B4 authoring đã bắt đầu (xem mục dưới).

**Context Map wording concern — đã xử lý ở Package 0.2-B4:** `context-map.yaml` từng mô tả `feature-engineering` (capability và context) bằng cụm "Feature/Signal" — ghi chú documentation-only đã ghi nhận tại `feature.md` §20. Vì `context-map.yaml` PHẢI đổi ở B4 (đăng ký quan hệ mới cho `context-projection`), wording đã được sửa thành "Feature" thuần túy (loại bỏ "/Signal"), đúng định nghĩa "Feature KHÔNG phải trade signal" — không tạo Signal capability/contract/relationship nào. Xem chi tiết tại mục Package 0.2-B4 dưới đây.

**Package 0.2-C vẫn chưa có artifact nào được author.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn **active và chưa hoàn tất**.

## Package 0.2-B4 đã đạt `Consolidated Stable`

**Phạm vi B4 (scope tối thiểu, đã Product Owner authorize):** điểm hội tụ có kiểm soát `Structure + Raw Regime + Feature → Market Context` — [`context.md`](./context.md) v0.2, `capability_id: context-aggregation` / `domain_context_id: context-projection` (đã đăng ký sẵn từ Package 0.2-A tại [`context-map.yaml`](./context-map.yaml) v0.9, forward-declared → authored ở v0.1, 10 relationship cho đúng bảy role mà `market_context` cần: Candle cadence/cutoff driver, Structure, hai Regime dimension, ba Feature type).

**Đúng một Context type — không mở rộng thành framework tổng quát:** `market_context` — aggregate `structure_orientation`; `volatility_regime_class`/`directional_persistence_regime_class`; `volatility_metric`/`directional_persistence_metric`/`distance_to_last_confirmed_swing`. Hai event type authoritative (`MarketContextSnapshot`, `MarketContextFactInvalidated`) + optional `MarketContextCurrentView`.

**Narrow architecture revision v0.1 → v0.2 — bốn finding:**

1. **`RA-B4-MAJ-01`/`IRB-B4-MAJ-01` (cùng một algorithmic defect):** Eligible Upstream Fact selection v0.1 (§8) có một bước filter (Currency) tham chiếu NGƯỢC kết quả của một bước SAU nó (Not-invalidated). **Sửa:** tách thành hai phase tuần tự, không tham chiếu ngược — Phase 1 (eligibility filtering, per-candidate độc lập) → Phase 2 (role-specific current selection, chỉ chạy trên tập survivor Phase 1).
2. **`IRB-B4-MAJ-02`:** `missing_input_policy` (§6) là chuỗi tự do, không pin giá trị canonical. **Sửa:** enum đóng, đúng một giá trị `NO_SNAPSHOT_WHEN_ANY_REQUIRED_ROLE_MISSING_OR_PENDING`, cấm tường minh null filling/stale fallback/partial snapshot/implementation-selected behavior. **Resolved technically — đóng.**
3. **`IRB-B4-MAJ-03`:** văn bản gốc [ADR-003](../adr/ADR-003.md) ("Feature Engine là điểm fan-in duy nhất") xung đột với thiết kế Context fan-in trực tiếp. **Sửa:** author [ADR-014](../adr/ADR-014.md) — narrow amendment (supersede có kiểm soát), phân biệt tường minh Feature computation fan-in vs Context snapshot aggregation, giữ nguyên toàn bộ quyết định Regime/Structure độc lập của ADR-003. **ADR-014 nay `status: Approved`** (Product Owner, 2026-07-30, sau ChatGPT + Claude narrow delta review Clean) — đúng [Chapter 11 §11.3](../constitution/11-adr-process.md), ADR-003 Approved vẫn bất biến byte-for-byte, không sửa trực tiếp; ADR-014 đã qua tối thiểu hai independent review trước khi Product Owner quyết định. **`IRB-B4-MAJ-03` governance-resolved kể từ 2026-07-30.**
4. **Non-blocking cleanup (bundled):** `MarketContextCurrentView` target-window selection (§13) làm rõ tường minh tiêu chí tie-break thứ hai (`window_start DESC`) khi hai window khác nhau cùng `window_end`.

**Lịch sử review đầy đủ:**

1. Author self-review v0.1: **hoàn tất** (35 attack scenario).
2. ChatGPT Review A + Independent Review B (baseline v0.1) → 4 finding: `RA-B4-MAJ-01`/`IRB-B4-MAJ-01` (cùng một algorithmic defect — Structure selection circular dependency), `IRB-B4-MAJ-02` (`missing_input_policy` chưa machine-pinned), `IRB-B4-MAJ-03` (ADR-003 fan-in conflict).
3. Narrow architecture revision (v0.1 → v0.2) xử lý đúng 4 finding trên — chỉ sửa `context.md`.
4. **ChatGPT Review A final package delta (trên `context.md` v0.2):** Clean — Blocker 0, Major 0, Minor 0, Suggestion 0.
5. **Independent Review B final package review (trên `context.md` v0.2):** semantic/architecture integration clean; phát hiện `IRB-B4-FINAL-MIN-01` (MANIFEST `compatible_adr_range` mâu thuẫn nội bộ với ADR-014 Approved/effective).
6. Narrow MANIFEST metadata correction xử lý đúng `IRB-B4-FINAL-MIN-01`.
7. **ChatGPT narrow MANIFEST delta:** Clean — Blocker 0, Major 0, Minor 0, Suggestion 0.
8. **Independent Review B narrow MANIFEST delta:** Clean — `IRB-B4-FINAL-MIN-01` Resolved, Blocker 0, Major 0, Minor 0, Suggestion 0 — **ready to record Consolidated Stable.**

**Kết luận consolidation:** toàn bộ chuỗi review trên, kết thúc bằng ChatGPT + Independent Review B narrow MANIFEST delta, cả hai **Clean**. **0 qualifying finding chưa xử lý** (finding ledger đầy đủ tại mục baseline dưới đây). Product Owner authorized: "Authorize Package 0.2-B4 consolidation as Consolidated Stable." (2026-07-30).

**Narrow traceability correction (`RA-B4-MIN-02`):** phiên bản trước của mục này (commit `f1ea03b`) gán nhầm `IRB-B4-MAJ-02` cho xung đột ADR-003 và `IRB-B4-MAJ-03` cho `missing_input_policy` — NGƯỢC với mapping authoritative của Independent Review B report. Đã sửa: `IRB-B4-MAJ-02` = `missing_input_policy` (resolved); `IRB-B4-MAJ-03` = ADR-003 fan-in conflict (**governance-resolved** — ADR-014 Approved 2026-07-30). Metadata/reference-only — không đổi semantic/algorithm/version nào.

**ADR-014 narrow review correction (v0.1 → v0.2) — đóng `IRB-ADR014-MAJ-01`/`IRB-ADR014-MAJ-02`/`IRB-ADR014-MIN-01`/`IRB-ADR014-MIN-02` (Independent Review B, trên `ADR-014.md` v0.1):**

1. **`IRB-ADR014-MAJ-01`:** ADR-014 v0.1 cấp quyền fan-in ở cấp LAYER (Feature Engine/Context Engine), không tường minh giới hạn theo Definition — có thể đọc rộng thành quyền chung không giới hạn. **Sửa:** thêm quy tắc "Definition-pinned direct fan-in" — fan-in trực tiếp CHỈ hợp lệ cho role/contract ID/contract version được chính Feature Definition hoặc Context Definition khai báo tường minh; canonical rule: "Layer capability does not authorize an input. The consuming Definition authorizes and pins the input."
2. **`IRB-ADR014-MAJ-02`:** Context prohibition list v0.1 chưa đủ. **Sửa:** mở rộng đầy đủ — cấm Risk/Account/Position/Execution conclusion, execution eligibility, order authority; cấm rename-conclusion-as-context-value; ví dụ payload cấm tuyệt đối (`risk_state`, `execution_allowed`, `position_size`, `order_eligible`).
3. **`IRB-ADR014-MIN-01`:** `context.md`'s "Quan hệ với ADR-003" gán stale finding ID (`RA-B4-MAJ-01`/`IRB-B4-MAJ-01`) cho xung đột ADR-003. **Sửa:** đúng phải là `IRB-B4-MAJ-03` — traceability-only, không đổi semantic.
4. **`IRB-ADR014-MIN-02`:** ghi nhận đầy đủ 6 risk (Coupling increase; Correction cascade; Definition-version mismatch; Duplicate temporal-alignment; Context scope creep; Feature scope creep) + mitigation, tường minh KHÔNG ngụ ý Product Owner đã accept ("reviewer-identified concerns... not Product Owner accepted risks while ADR-014 is Draft").

**KHÔNG đổi bất kỳ quyết định kiến trúc nào** — Feature computation vs Context aggregation, Regime/Structure độc lập không đổi. **Reviewer evidence (tại thời điểm v0.2 pre-approval):** ghi nhận Independent Review B là actor đã tìm ra 4 finding trên `ADR-014.md` v0.1; KHÔNG fabricate một actor thứ hai; `ADR-014.md`'s `frontmatter.reviewers` giữ nguyên `[]` tại thời điểm đó — một tập hai-reviewer hợp lệ theo Chapter 11 §11.5 CHƯA được xác lập; bản sửa v0.2 CHƯA qua delta review (xem mục "ADR-014 atomic approval" dưới đây cho trạng thái hiện tại).

## `Consolidated Stable` baseline — Package 0.2-B4

**Exact reviewed artifact baseline (pinned):**

```text
context.md         v0.2   Draft   blob f9274d5749768151748b9dfa2713118a4fd77791
context-map.yaml    v0.9   Draft   blob 8ac18383b6ec378f6ef2664e2141f033370277d2
ADR-014 (controlling architecture)   v0.2   Approved   blob b2e5757102c360756f1649c93fa8cb61bf931f69
MANIFEST (registry baseline reviewed)   v9.48   blob e5000a290698cb3d990d8a0835e3c2e077ddcd90
reviewed HEAD:    cae2b4b115db93ba5f76bcbf28b41c03362789eb
```

**ADR-003 (historical, immutable):** embedded document `status: Approved`, blob `d40182eb336a6d9e70644f2c17fb36ddaa347e55`, byte-for-byte unchanged; current authoritative lifecycle state `Superseded by ADR-014` (MANIFEST).

**Dependency không đổi trong suốt B4:** `candle.md` v0.4 Draft, `swing.md` v0.2 Draft (blob `5bbe666ff404209876a721b1e01cb9ac62011062`), `structure.md` v0.4 Draft (blob `78964dfb6852bbac3fa1e034d64b4fc8031c3fef`), `regime.md` v0.2 Draft (blob `edd1584377f1db84269e7b1dfdd4926d0ce01c70`), `feature.md` v0.2 Draft (blob `2262adf9253ea20c8d817d1066f50c4353d2d35d`) — tất cả giữ nguyên byte-for-byte từ baseline trước.

**Finding ledger — tất cả resolved:**

```text
RA-B4-MAJ-01 / IRB-B4-MAJ-01   — Resolved (Structure selection two-phase pipeline, context.md v0.2 §8)
IRB-B4-MAJ-02                  — Resolved (missing_input_policy closed enum, context.md v0.2 §6/§9)
IRB-B4-MAJ-03                  — Resolved technically and through ADR-014 governance approval (2026-07-30)
RA-B4-MIN-02                   — Resolved (traceability correction, commit f1ea03b delta)
IRB-ADR014-MAJ-01              — Resolved (Definition-pinned direct fan-in rule, ADR-014 v0.2)
IRB-ADR014-MAJ-02              — Resolved (Context prohibition list đầy đủ, ADR-014 v0.2)
IRB-ADR014-MIN-01              — Resolved (traceability correction trong context.md)
IRB-ADR014-MIN-02              — Resolved (6 risk + mitigation ghi nhận, Product Owner accepted 2026-07-30)
IRB-B4-FINAL-MIN-01             — Resolved (MANIFEST compatible_adr_range/generated_at correction)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A: authoring hoàn tất cho phạm vi B4; ChatGPT Review A hoàn tất; Independent Review B hoàn tất; mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để package kế tiếp (0.2-C) bắt đầu planning — **không** ngụ ý Product Owner Approval cho `context.md`/`context-map.yaml`, **không** ngụ ý Lock, **không** đóng OQ nào, **không** authorize Live. `context.md` **vẫn giữ `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`**; `context-map.yaml` **vẫn giữ `version: "0.9"`, `status: Draft`** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package 0.2-C — baseline dependency đã thỏa** (ADR-012/ADR-013 Approved, ADR dependency gate open từ trước) — eligible cho Product Owner scope authorization tường minh, tương tự cơ chế đã áp dụng cho B1–B4. **Chưa bắt đầu, chưa author, KHÔNG được authorize bởi transaction này.**

**Package 0.2-C vẫn chưa có artifact nào được author.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn **active và chưa hoàn tất** — Package 0.2-B (tổng thể: A + B1 + B2 + B3 + B4) nay đều `Consolidated Stable`, nhưng Phase 0.2 chỉ hoàn tất khi 0.2-C cũng đạt tương đương, đúng roadmap Chapter 14.

## ADR-014 atomic approval and ADR-003 supersession (2026-07-30)

**Product Owner quyết định:** "Approve ADR-014." (2026-07-30). Đúng [Chapter 11 §11.6](../constitution/11-adr-process.md) — atomic documentation change: ADR-014 `Draft → Approved`, `approved_by: Product Owner`, `approved_at: "2026-07-30"`, `reviewers: [ChatGPT, Claude]`, `last_review: "2026-07-30"`; MANIFEST ghi nhận ADR-003 current authoritative lifecycle state `Superseded`/`superseded_by: ADR-014` VÀ ADR-014 `Approved`/`supersedes: ADR-003` cùng một change.

**Review evidence (delta review trên `ADR-014.md` v0.2, thỏa Chapter 11 §11.5):**

- **ChatGPT** (role `AI Technical Architect`): narrow delta review — Clean, Blocker 0, Major 0, Minor 0, Suggestion 0.
- **Claude** (role `AI Technical Architect`): narrow delta review, độc lập — Clean, Blocker 0, Major 0, Minor 0, Suggestion 0.

Bốn finding lịch sử `IRB-ADR014-MAJ-01`/`MAJ-02`/`MIN-01`/`MIN-02` (Independent Review B, trên v0.1) được bảo toàn làm review history trong `ADR-014.md`, không bị xóa. Reviewer REVIEW — không APPROVE; Product Owner là authority duy nhất approve/reject.

**Risk acceptance:** Product Owner chấp nhận sáu residual risk đã ghi nhận trong ADR-014 (Coupling increase; Correction cascade; Definition-version mismatch; Duplicate temporal-alignment implementation; Context scope creep; Feature scope creep), có điều kiện theo đúng mitigation đã pin cho từng risk — không risk nào ngoài sáu risk này, không mitigation nào bị suy yếu/xóa.

**ADR-003 supersession:** `docs/adr/ADR-003.md` **giữ nguyên byte-for-byte** (Chapter 11 §11.3) — không sửa, embedded `status: Approved` vĩnh viễn. Current authoritative lifecycle state (sống tại MANIFEST theo I-12) chuyển `Superseded` bởi ADR-014. Hai trục tách biệt, không mâu thuẫn: embedded document status = `Approved` (immutable); current authoritative lifecycle state = `Superseded`. **ADR-014 nay là controlling authority.**

**B4 blocker transition:** `IRB-B4-MAJ-03` (ADR-003 fan-in conflict) **governance-resolved** kể từ 2026-07-30. Package 0.2-B4 chuyển: `Draft`, architecture blocker cleared, technical review clean — tại thời điểm transaction này, **KHÔNG** `Approved`/`Locked`/`Consolidated Stable`/`completed`; B4 vẫn cần một transaction package delta review/consolidation riêng trước khi đạt `Consolidated Stable`. **Cập nhật:** transaction consolidation riêng đó đã diễn ra cùng ngày 2026-07-30 — xem mục "Package 0.2-B4 đã đạt `Consolidated Stable`" ở trên.

**Không tuyên bố hoàn thành hay approval ở bất kỳ mức nào ngoài phạm vi ADR-014:** `context.md`/`feature.md`/`regime.md`/`swing.md`/`structure.md`/`context-map.yaml` vẫn `status: Draft`. Không Approve/Lock/Consolidate Package 0.2-B4; không đóng OQ-002/OQ-003; không authorize Live. Package 0.2-C **vẫn chưa có artifact nào được author**. Phase 0.2 vẫn **active và chưa hoàn tất**.

## Package 0.2-C decomposition (2026-07-30)

**Product Owner authorized:** "Authorize Package 0.2-C scope definition and minimal authoring." — cho phép khóa decomposition dự kiến cho Package 0.2-C, và mở + author minimal slice đầu tiên (C1). Decomposition dưới đây là **planning baseline**, KHÔNG phải thiết kế runtime-module cuối cùng cho Phase 0.2 — một review sau này có thể xác định các điều chỉnh narrow cần thiết. **Chỉ C1 được author trong transaction này** — C2–C7 đòi hỏi Product Owner authorization RIÊNG, từng slice một, không tự động mở khi C1 hoàn tất.

```text
0.2-C1 — Reference Foundation
  instrument.md
  venue.md

0.2-C2 — Trading Account Foundation
  account.md
  ADR-012 integration

0.2-C3 — Strategy Foundation
  strategy.md
  Strategy Definition
  Strategy Instance
  ADR-013 integration

0.2-C4 — Decision Contract
  trade-intent.md
  decision.md

0.2-C5 — Risk Gateway Contract
  risk.md
  execution-intent.md

0.2-C6 — Order & Execution Contract
  order.md
  fill.md

0.2-C7 — Position & Replay Contract
  position.md
  replay-event.md
```

**Dependency direction đã pin:**

```text
Instrument + Venue
  → Account
  → Strategy
  → Trade Intent / Decision
  → Risk / Execution Intent
  → Order / Fill
  → Position / Replay
```

Mỗi slice phụ thuộc slice trước nó theo đúng thứ tự trên — C2 (Account) cần Instrument/Venue (C1) đã tồn tại (Position/Order sau này scope theo Account, đúng [ADR-007](../adr/ADR-007.md)); C3 (Strategy) cần Account (C2, [ADR-012](../adr/ADR-012.md) integration) và [ADR-013](../adr/ADR-013.md) (Strategy Definition Version); v.v.

## Package 0.2-C1 đã đạt `Consolidated Stable`

**Phạm vi C1 (scope tối thiểu, đã Product Owner authorize):** hai Domain Contract nền tảng — [`instrument.md`](./instrument.md) v0.6 (Logical Instrument + TradableListing subordinate concept + `ActiveListingReservation` pair-scoped authority subject) và [`venue.md`](./venue.md) v0.3 (Logical Venue, không đổi từ vòng thứ ba) — `capability_id: market-reference` / `domain_context_id: instrument-venue-reference` (đã đăng ký sẵn từ Package 0.2-A tại [`context-map.yaml`](./context-map.yaml) v0.10, forward-declared → authored; **không tạo capability/context mới**).

**Không author ở C1 (đúng authorization boundary):** Account; Strategy; Decision; Risk; Position; Order; Fill; Trade Intent; Execution Intent; Replay Event — tất cả thuộc Package 0.2-C2–C7, chưa authorize.

**Instrument — tóm tắt (v0.2):** identity venue-neutral (`instrument_id`, opaque) cho một sản phẩm giao dịch, tách bạch KHỎI raw venue symbol. Scope identity bất biến: `instrument_identity_ref` (opaque discriminator bắt buộc, đóng `RA-C1-MAJ-01`)/`base_asset_ref`/`quote_asset_ref` (opaque reference, KHÔNG author Asset như Domain Contract riêng)/`instrument_type` (enum đóng `SPOT`/`PERPETUAL`/`FUTURE` — `OPTION` reserved-not-authored)/`contract_expiry_ref` (khi FUTURE)/`settlement_type` (bắt buộc khi FUTURE/PERPETUAL). Bốn event: `InstrumentRegistered` (nay correctable — original hoặc same-scope replacement), `InstrumentMetadataRevised` (forward-looking, PATCH semantics `EXPLICIT_PATCH_WITH_CLEAR_SET`), `InstrumentStatusChanged` (REGISTERED→ACTIVE↔SUSPENDED→RETIRED), `InstrumentFactInvalidated` (correction, nay có thể target initial fact). Cộng **TradableListing** — subordinate concept (không phải file riêng), gắn MỘT Logical Instrument với MỘT Venue, identity `(instrument_id, venue_id, listing_id)`, mang venue symbol/tick/lot/min-notional/session reference/listing status, bốn event riêng (`TradableListingCreated`/`MetadataRevised`/`StatusChanged`/`FactInvalidated`) — cùng correction/PATCH semantics như Instrument.

**Venue — tóm tắt (v0.2):** identity ổn định (`venue_id`, opaque) cho một địa điểm giao dịch, tách bạch KHỎI production/sandbox endpoint, API credential, adapter instance (deferred, Phase 1). Scope identity: `venue_identity_ref` (opaque discriminator bắt buộc, đóng `RA-C1-MAJ-01`)/`venue_type` (enum đóng `CENTRALIZED_EXCHANGE`/`DECENTRALIZED_EXCHANGE`/`BROKER`)/`jurisdiction_ref` (optional). Sở hữu reference concept: timezone, default trading calendar/session policy, default precision policy — venue-neutral, không giả định 24/7 (đúng [ADR-007](../adr/ADR-007.md)). Bốn event: `VenueRegistered` (nay correctable), `VenueMetadataRevised` (PATCH semantics), `VenueOperationalStatusChanged`, `VenueFactInvalidated` (nay có thể target initial fact).

**TradableListing ownership decision:** subordinate concept trong `instrument.md` (không phải file C1 riêng) — venue-neutral Instrument sở hữu product semantics; venue-specific TradableListing sở hữu trading constraints (symbol/increment/session). Quyết định tường minh, không để ambiguous.

**Bitemporal/correction rules (cả `instrument.md` và `venue.md`):** mọi metadata mang `effective_time`/`recorded_time`; **forward-looking revision** (thay đổi thật theo thời gian, fact cũ vẫn hợp lệ lịch sử) tách bạch tường minh khỏi **correction** (`*FactInvalidated` + replacement, sửa sai sót quá khứ) — không gộp hai khái niệm; Historical Replay dùng đúng metadata có hiệu lực TẠI cursor, không dùng giá trị hiện tại; no look-ahead; Current View (`InstrumentCurrentView`/`TradableListingCurrentView`/`VenueCurrentView`) no-row trước fact đầu tiên, `view_state` chỉ `VALID`/`PENDING_CORRECTION`, non-authoritative, fold algorithm deterministic đã pin tường minh (v0.2).

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất** (20 attack scenario).
- ChatGPT Review A: **hoàn tất** — 3 finding Major (`RA-C1-MAJ-01`, `RA-C1-MAJ-02`, `RA-C1-MAJ-03`), 0 Minor. Đóng qua narrow correction v0.2.
- Independent Review B (vòng 1, đánh giá v0.2): **hoàn tất** — 4 finding Major (`IRB-C1-MAJ-01`, `IRB-C1-MAJ-02`, `IRB-C1-MAJ-03`, `IRB-C1-MAJ-04`), 0 Minor. Đóng qua narrow correction v0.3.
- Independent Review B (vòng 2, đánh giá v0.3): **hoàn tất** — 4 finding Major (`IRB-C1-V03-MAJ-01`, `IRB-C1-V03-MAJ-02`, `IRB-C1-V03-MAJ-03`, `IRB-C1-V03-MAJ-04`), 0 Minor. Đóng qua narrow correction v0.4.
- Independent Review B (vòng 3, đánh giá v0.4): **hoàn tất** — 1 finding Major (`IRB-C1-V04-MAJ-01`), 0 Minor. Đóng qua bounded final correction v0.5.
- Independent Review B (vòng 4, đánh giá v0.5): **hoàn tất** — 1 finding Major (`IRB-C1-V05-MAJ-01`), 0 Minor. Đóng qua narrow correction v0.6 (transaction này).
- Narrow correction (v0.6, 2026-07-30): **hoàn tất** — finding Major duy nhất đã đóng, 34 attack scenario, author self-review lần sáu hoàn tất.
- ChatGPT Review A (trên `instrument.md` v0.6/`venue.md` v0.3): **Clean** — 0 blocking finding.
- Independent Review B (trên `instrument.md` v0.6/`venue.md` v0.3): **Clean with deferred limitations** — deferred limitations là Phase 1 implementation concern (runtime worker ownership, transaction boundaries, retry/backoff, monitoring/escalation, operational recovery orchestration), non-blocking cho walking-skeleton readiness, xem "Deferred limitations" dưới. 0 blocking finding.
- Consolidation: **hoàn tất (transaction này)** — Product Owner authorized: "Package 0.2-C1 consolidation transaction" (2026-07-30). **Package 0.2-C1 nay `Consolidated Stable`.**

**Package 0.2-C1 narrow correction thứ nhất — tóm tắt (v0.2, 2026-07-30):** đóng `RA-C1-MAJ-01` (thêm `instrument_identity_ref`/`venue_identity_ref` — opaque discriminator bắt buộc); đóng `RA-C1-MAJ-02` (pin canonical `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET`); đóng `RA-C1-MAJ-03` (pin canonical `initial_fact_correction_policy: INVALIDATE_INITIAL_FACT_AND_REGISTER_NEW_SUBJECT_WHEN_SCOPE_CHANGES`). `OPTION` bị loại khỏi `instrument_type` active enum, reserved-not-authored.

**Package 0.2-C1 narrow correction thứ hai — tóm tắt (v0.3, 2026-07-30):** đóng `IRB-C1-MAJ-01` (thêm `pending_correction_class` đóng — `AWAITING_SAME_SUBJECT_REPLACEMENT`/`TERMINAL_SCOPE_INVALIDATION`); đóng `IRB-C1-MAJ-02` (TradableListing eligibility đối xứng Instrument/Venue RETIRED, derived `eligibility_state`); đóng `IRB-C1-MAJ-03` (thêm `ActiveListingReservation` pair-scoped authority subject + `ActiveListingReserved`/`ActiveListingReservationReleased`/`ActiveListingActivationRejected`); đóng `IRB-C1-MAJ-04` (pin `status_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER`, thuật toán 5-phase).

**Package 0.2-C1 narrow correction thứ ba — tóm tắt (v0.4, 2026-07-30):** đóng `IRB-C1-V03-MAJ-01` (v0.3 `ActiveListingReserved` ↔ activation event có chu trình causal; thêm `ActiveListingActivationRequested` làm pre-arbitration request tường minh, chuỗi causal tuyến tính request→grant/reject→activation event); đóng `IRB-C1-V03-MAJ-02` (`TradableListingCurrentView` Bước 4–5 v0.3 dùng `InstrumentCurrentView`/`VenueCurrentView` làm input — mâu thuẫn với chính quy tắc "not authority"; v0.4 reconstruct trực tiếp từ authoritative Instrument/Venue event stream); đóng `IRB-C1-V03-MAJ-03` (reservation fact trước đây không correctable; thêm `ActiveListingReservationFactInvalidated` + `supersedes_fact_ref`); đóng `IRB-C1-V03-MAJ-04` (pin `reservation_fold_order_policy: RECORDED_VISIBILITY_THEN_EFFECTIVE_ORDER`, thuật toán 5-phase).

**Package 0.2-C1 bounded final correction — tóm tắt (v0.5, 2026-07-30):** đóng `IRB-C1-V04-MAJ-01` (`ActiveListingActivationRequested` v0.4 thiếu stable logical identity — `event_id` đổi mỗi physical record, không dedup/idempotent được dưới ingress retry/redelivery). Thêm `activation_request_id` — opaque, ổn định, KHÔNG bằng `event_id`, KHÔNG regenerate khi retry, vĩnh viễn bind đúng một `(instrument_id, venue_id, listing_id, requested_target_status)`; cùng ID với scope khác → reject (không phải correction/retry/request mới). Pin `activation_request_idempotency_policy: STABLE_ID_SAME_PAYLOAD_IS_IDEMPOTENT` — exact retry idempotent, changed-payload reject. `ActiveListingActivationRequested` không có correction lineage riêng (không metadata-patchable) — intent sai dùng ID mới. `ActiveListingReserved`/`ActiveListingActivationRejected`/`TradableListingCreated`/`TradableListingStatusChanged(ACTIVE)` thêm `activation_request_id` bắt buộc, exactly-one-outcome nay keyed theo logical ID (không chỉ event ref); outcome type (grant/reject) bất biến, đảo type cần invalidate + ID mới. Thêm "Request dedup và replay algorithm" (7 bước) tại `instrument.md` §16. Bounded — không đổi activation arbitration structure/reservation correction lineage/parent reconstruction/bitemporal folding hiện có. `venue.md` **không đổi** — không nội dung normative nào bị chạm; không cross-reference nào lệch số (không chèn section top-level mới). `instrument_id`/`venue_id`/`listing_id` **không đổi tên, không đổi shape** xuyên suốt cả bốn vòng correction.

**Package 0.2-C1 narrow correction thứ năm — tóm tắt (v0.6, 2026-07-30):** đóng `IRB-C1-V05-MAJ-01` (một `ActiveListingActivationRequested` fact có thể pass ingress validation, được ghi nhận authoritative, rồi sau đó phát hiện SAI thực tế — v0.5 không có append-only invalidation, không có replay exclusion/classification, canonical semantic payload chưa liệt kê đầy đủ). Thêm `ActiveListingActivationRequestFactInvalidated` — CHỈ target `ActiveListingActivationRequested`, KHÔNG có `supersedes_fact_ref`/replacement dưới cùng `activation_request_id` (giữ nguyên quyết định bounded "request immutable" của v0.5). Pin canonical request validity `VALID`/`TERMINALLY_INVALID` — invalidation visible ⟹ TERMINALLY_INVALID vĩnh viễn, không quay lại VALID. Định nghĩa hệ quả deterministic theo ba trường hợp thời điểm: chưa có outcome (cấm outcome mới); có rejection (rejection giữ nguyên historical evidence); có grant chưa activation (grant hết hiệu lực cho activation mới, `ActiveListingReservationReleased` reason MỚI `REQUEST_INVALIDATION` giải phóng reservation, tách bạch reservation state history khỏi activation authorization eligibility); có grant VÀ activation đã ghi nhận (tái dùng cơ chế `TradableListingFactInvalidated`/`ActiveListingReservationReleased` đã có sẵn — KHÔNG phát minh cơ chế thứ hai, không tự động cascade). `ActiveListingReserved`/`ActiveListingActivationRejected`/`TradableListingCreated`/`TradableListingStatusChanged(ACTIVE)` thêm invariant: request tham chiếu phải visible và VALID tại cursor — không rewrite causation lịch sử. "Request dedup và replay algorithm" mở rộng 7→10 bước. Liệt kê đầy đủ canonical semantic payload: `requested_by_ref` là semantic (phải khớp chính xác), `request_reason` (field mới) loại khỏi idempotency equality; `source_identity`/`causation_refs`/`related_event_refs` làm rõ không phải business request scope. `venue.md` **không đổi** — không nội dung normative nào bị chạm. `instrument_id`/`venue_id`/`listing_id`/`event_id` **không đổi tên, không đổi shape** xuyên suốt cả năm vòng correction.

**Kết luận consolidation:** ChatGPT Review A (Clean) và Independent Review B (Clean with deferred limitations — Phase 1 implementation concern, không blocking) trên `instrument.md` v0.6/`venue.md` v0.3, **0 finding còn lại chưa xử lý** (finding ledger đầy đủ, cả năm vòng narrow correction, tại mục baseline dưới đây). Product Owner authorized: "Package 0.2-C1 consolidation transaction" (2026-07-30).

## `Consolidated Stable` baseline — Package 0.2-C1

**Exact reviewed artifact baseline (pinned):**

```text
instrument.md       v0.6   Draft   blob 81651f6a19a3f22fa7a924173f14b02e6467c8e0
venue.md            v0.3   Draft   blob 0ffb9e64bcb7dec108edea0bc9c3af3a162b40d9
context-map.yaml     v0.10   Draft   blob 05bd2ba5bd72888d8ef206eb2ea088d03c1f50f3
MANIFEST (registry baseline reviewed)   v9.55   blob 381010a8c47ece07fdd1be8820129a8953ef33c3
reviewed HEAD:    ddc790864b3ee50a1ad402dc26146970e2791ed4
```

**Finding ledger — tất cả resolved qua năm vòng narrow correction (v0.2–v0.6):**

```text
RA-C1-MAJ-01                — Resolved (instrument_identity_ref/venue_identity_ref, instrument.md v0.2)
RA-C1-MAJ-02                — Resolved (revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET, v0.2)
RA-C1-MAJ-03                — Resolved (initial_fact_correction_policy, v0.2)
IRB-C1-MAJ-01                — Resolved (pending_correction_class, v0.3)
IRB-C1-MAJ-02                — Resolved (TradableListing eligibility đối xứng Instrument/Venue, v0.3)
IRB-C1-MAJ-03                — Resolved (ActiveListingReservation pair-scoped authority, v0.3)
IRB-C1-MAJ-04                — Resolved (status_fold_order_policy 5-phase, v0.3)
IRB-C1-V03-MAJ-01            — Resolved (ActiveListingActivationRequested phá vỡ chu trình causal, v0.4)
IRB-C1-V03-MAJ-02            — Resolved (authoritative parent reconstruction thay Current View, v0.4)
IRB-C1-V03-MAJ-03            — Resolved (ActiveListingReservationFactInvalidated correction lineage, v0.4)
IRB-C1-V03-MAJ-04            — Resolved (reservation_fold_order_policy 5-phase, v0.4)
IRB-C1-V04-MAJ-01            — Resolved (activation_request_id logical identity/idempotency, v0.5)
IRB-C1-V05-MAJ-01            — Resolved (ActiveListingActivationRequestFactInvalidated, canonical semantic payload, v0.6)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** runtime worker ownership; transaction boundaries; retry/backoff; monitoring và escalation; operational recovery orchestration. Đây là các mối quan tâm triển khai runtime (Phase 1 — Engineering/Plugin Model), KHÔNG phải Domain Contract semantic gap — Package 0.2-C1 pin RULE (identity, correction lineage, bitemporal fold, arbitration authority boundary), không pin MECHANISM triển khai cụ thể, đúng nguyên tắc defer đã nhất quán xuyên suốt `instrument.md` §23/§24. Các mối quan tâm này có thể tiếp tục evolve từ implementation evidence khi Phase 1 thực sự bắt đầu — không block walking-skeleton readiness ở Phase 0.2.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A: authoring hoàn tất cho phạm vi C1; ChatGPT Review A hoàn tất (Clean); Independent Review B hoàn tất (Clean with deferred limitations); mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để package kế tiếp (0.2-C2) bắt đầu planning — **không** ngụ ý Product Owner Approval cho `instrument.md`/`venue.md`, **không** ngụ ý Lock, **không** đóng OQ nào, **không** authorize Live, **không** thay đổi Constitution. `instrument.md` **vẫn giữ `version: "0.6"`, `status: Draft`, `approved_by: null`, `approved_at: null`**; `venue.md` **vẫn giữ `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package 0.2-C2 — baseline dependency đã thỏa** (Instrument/Venue reference data nay `Consolidated Stable`) — Product Owner đã authorize scope tối thiểu ("Package 0.2-C2 — Trading Account Foundation"), xem mục "Package 0.2-C2" dưới đây cho chi tiết authoring.

**Package 0.2-C3–C7 vẫn chưa có artifact nào được author.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn **active và chưa hoàn tất** — Package 0.2-A/B (tổng thể)/C1 nay đều `Consolidated Stable`, nhưng Phase 0.2 chỉ hoàn tất khi toàn bộ 0.2-C (C1–C7) cũng đạt tương đương, đúng roadmap Chapter 14.

**Không tuyên bố hoàn thành hay approval ở bất kỳ mức nào (mục C1):** `instrument.md`/`venue.md`/`context.md`/`feature.md`/`regime.md`/`swing.md`/`structure.md`/`context-map.yaml` `status: Draft`; không Product Owner Approve; không Lock; không đóng OQ-002/OQ-003; không authorize Live; không sửa ADR nào.

## Package 0.2-C2 đã đạt `Consolidated Stable`

**Phạm vi C2 (scope tối thiểu, đã Product Owner authorize):** một Domain Contract — [`account.md`](./account.md) v0.2 (Trading Account identity, boundary binding, environment, lifecycle tối thiểu, credential-reference boundary) — `capability_id: account-management` / `domain_context_id: account-reference` (capability/context **MỚI**, đăng ký lần đầu tại [`context-map.yaml`](./context-map.yaml) v0.11 — Account KHÔNG thuộc phạm vi `market-reference`/`instrument-venue-reference` của Package 0.2-C1).

**Controlling architecture — [ADR-012](../adr/ADR-012.md) v0.3 `Approved`** (đã có sẵn từ 2026-07-28, KHÔNG sửa/re-author/bump trong transaction này): Account-to-Boundary Cardinality — exactly-one-boundary Trading Account. `account.md` CHỈ implement field/invariant mà ADR-012 §2 yêu cầu (canonical `account_boundary_ref` model §2.1, venue boundary §2.2, broker_account boundary §2.3, scope rules §2.4), KHÔNG lặp lại toàn văn ADR, KHÔNG tự quyết architecture mới ngoài phạm vi đã khóa.

**Baseline conflict đã giải quyết (2026-07-30):** authorization ban đầu giả định `ADR-012.md` chưa tồn tại ("next repository-consistent Draft version") — thực tế `ADR-012.md` đã Approved v0.3 từ 2026-07-28, quyết định đúng lãnh thổ mà task yêu cầu (account identity/venue boundary/secret separation). Đã STOP, báo cáo conflict, chờ Product Owner quyết định. Product Owner decision: treat ADR-012 v0.3 Approved làm controlling architecture, KHÔNG modify/re-author/bump/replace/reinterpret, không cần ADR mới — chỉ author `account.md`.

**Account — tóm tắt (v0.2):** identity ổn định (`account_id`, opaque, globally unique, KHÔNG encode venue/owner/environment/credential/account type, KHÔNG derive từ scope) cho một trading account — một `account_id` có đúng một `account_boundary_ref`/`environment` bất biến, nhưng một cặp boundary/environment CÓ THỂ chứa nhiều `account_id` phân biệt (v0.2, đóng `C2-MAJ-01`). Scope identity bất biến: `account_boundary_ref` (`{boundary_type: venue | broker_account, boundary_id}`, required/immutable, đúng ADR-012 §2.1)/`environment` (enum đóng `PAPER`/`LIVE`, required/immutable — chỉ phân biệt domain value, KHÔNG authorize Live execution của platform). Bốn event: `AccountRegistered` (original hoặc same-scope replacement), `AccountMetadataRevised` (forward-looking, PATCH semantics `EXPLICIT_PATCH_WITH_CLEAR_SET`, whitelist `credential_reference`/`display_name`), `AccountStatusChanged` (lifecycle tối thiểu `ACTIVE`↔`SUSPENDED`→`CLOSED`, ba state, CLOSED terminal cho forward transition nhưng correctable append-only qua correction lineage, v0.2 đóng `C2-MAJ-02`), `AccountFactInvalidated` (correction, có thể target initial fact — METADATA_ERROR same-subject / SCOPE_ERROR new-subject, đúng ADR-012 §2.1 "rebinding = tạo Account khác"). Cộng `AccountCurrentView` (optional read model, non-authoritative, latest-state, KHÔNG cursor-addressable, `view_state`/`pending_correction_class`, fold algorithm "visible-valid-head per slice" v0.2 đóng `C2-MAJ-03`).

**Credential/secret boundary (I-11):** Account chỉ giữ `credential_reference` — opaque reference tới external secure credential binding (Vault/KMS, Phase 1) — TUYỆT ĐỐI KHÔNG raw secret (API key/private key/token/password) trong payload, snapshot, log, hay replay artifact nào. Chỉ Exchange Adapter/Custody-Signing Service dùng credential trực tiếp (I-11).

**Downstream reference contract (Package 0.2-C3–C7, chưa author):** `account_id`/`venue_id` (chỉ có mặt khi boundary_type=venue, ABSENT khi broker_account)/`environment`/`account_status` — bốn field, resolve TRỰC TIẾP từ authoritative Account event stream TẠI cursor; `AccountCurrentView` latest-state KHÔNG BAO GIỜ là input hợp lệ (không cursor-addressable); cache chỉ chấp nhận khi VỪA cursor-addressable VỪA provably equivalent tại đúng cursor (v0.2, đóng `C2-MAJ-04`, I-12). `account.md` KHÔNG author semantics của Strategy/Decision/Risk/Execution Intent/Order/Fill/Position.

**Học từ Package 0.2-C1, đóng trước (không chờ review round phát hiện):** `pending_correction_class` (VALID/PENDING_CORRECTION phân biệt AWAITING_SAME_SUBJECT_REPLACEMENT/TERMINAL_SCOPE_INVALIDATION) pin ngay từ v0.1; `revision_policy: EXPLICIT_PATCH_WITH_CLEAR_SET` cho metadata revision pin ngay từ v0.1; `AccountCurrentView` pin "KHÔNG BAO GIỜ authority" ngay từ v0.1, siết chặt hơn ở v0.2. Account KHÔNG có multi-party arbitration (khác `ActiveListingReservation` của Instrument) — không cần activation-request-identity/idempotency machinery.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** cơ chế credential reference cụ thể (Vault/KMS binding); runtime worker ownership; transaction boundaries; retry/backoff; monitoring/escalation; operational recovery orchestration; Broker Account Boundary Domain Contract riêng; onboarding/KYC/broker approval workflow; PAPER→LIVE promotion workflow (đổi environment = Account mới); billing, multi-tenant IAM, organization/tenant model (Chapter 6 §6.4: "Account ≠ Tenant"); custody system implementation.

**Package 0.2-C2 bounded correction — tóm tắt (v0.2, 2026-07-30):** đóng `C2-MAJ-01` (account_id sai khi derive từ boundary+environment, collapse nhiều Account hợp lệ; sửa thành opaque, globally unique, gán tại AccountRegistered, không derive từ scope); đóng `C2-MAJ-02` (làm rõ CLOSED chỉ terminal cho forward transition, correction append-only vẫn hợp lệ kể cả sửa một CLOSED fact sai; thêm `supersedes_fact_ref` còn thiếu vào payload AccountStatusChanged); đóng `C2-MAJ-03` (fold algorithm thay bằng quy tắc chung "visible-valid-head per slice" — group theo correction lineage/effective-time slice, loại fact invalidate visible, slice invalidate chưa replacement KHÔNG đóng góp gì, total-order effective_time/recorded_time/event_id ASC, dùng chung cho metadata PATCH và status fold); đóng `C2-MAJ-04` (pin một quy tắc downstream authority duy nhất — resolve từ authoritative stream tại cursor, AccountCurrentView latest-state không bao giờ là input, cache chỉ chấp nhận khi cursor-addressable VÀ provably equivalent; venue_id xác nhận ABSENT khi broker_account). ADR-012 không đổi, byte-for-byte.

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất.**
- ChatGPT Review A + Independent Review B (v0.1): 4 finding Major (`C2-MAJ-01`–`C2-MAJ-04`), đóng qua bounded correction v0.2.
- Bounded correction (v0.2): **hoàn tất** — cả 4 finding Major đã đóng, author self-review lần hai hoàn tất.
- ChatGPT bounded delta Review A (trên `account.md` v0.2): **Clean** — 0 blocking finding.
- Independent Review B (trên `account.md` v0.2): **Clean with deferred limitations** — deferred limitations là Phase 1 implementation concern (credential binding implementation, runtime worker ownership, transaction boundaries, retry/backoff, monitoring/recovery, Broker Account Boundary details, onboarding/KYC, PAPER→LIVE promotion, custody/IAM/billing), non-blocking, xem "Deferred limitations" ở trên. 0 blocking finding.
- Consolidation: **hoàn tất (transaction này)** — Product Owner authorized: "Package 0.2-C2 consolidation transaction" (2026-07-30). **Package 0.2-C2 nay `Consolidated Stable`.**

**Kết luận consolidation:** ChatGPT bounded delta Review A (Clean) và Independent Review B (Clean with deferred limitations — Phase 1 implementation concern, không blocking) trên `account.md` v0.2, **0 finding còn lại chưa xử lý** (finding ledger đầy đủ — 4 finding qua vòng bounded correction — tại mục baseline dưới đây). Product Owner authorized: "Package 0.2-C2 consolidation transaction" (2026-07-30).

## `Consolidated Stable` baseline — Package 0.2-C2

**Exact reviewed artifact baseline (pinned):**

```text
account.md              v0.2   Draft      blob 9fd2d0fb3235343d52c3435df3f1c7e08dd22781
ADR-012.md (controlling architecture)  v0.3   Approved   blob 59eec21774478fc862e120d8a0f9285dc24eb720
context-map.yaml         v0.11  Draft      blob 8eec5ee689f257a2e13bb8023175a58bbe175ad0
MANIFEST (registry baseline reviewed)  v9.58  blob c4c1357f66f4d0521988bf29f4c8511dac8fe8fd
reviewed HEAD:    730c07c26c2917b6599e5faf213bdaf6f96b703d
```

**Finding ledger — tất cả resolved qua bounded correction (v0.1 → v0.2):**

```text
C2-MAJ-01   — Resolved (account_id opaque/globally unique, không derive từ boundary+environment, account.md v0.2 §1)
C2-MAJ-02   — Resolved (CLOSED terminal chỉ cho forward transition, correction append-only vẫn hợp lệ, supersedes_fact_ref thêm vào AccountStatusChanged, v0.2 §5/§11)
C2-MAJ-03   — Resolved (fold algorithm "visible-valid-head per slice" dùng chung metadata/status, v0.2 §7)
C2-MAJ-04   — Resolved (một quy tắc downstream authority duy nhất, AccountCurrentView latest-state không bao giờ là input, cache chỉ chấp nhận khi cursor-addressable + provably equivalent, v0.2 §7/§13)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** cơ chế credential binding cụ thể (Vault/KMS); runtime worker ownership; transaction boundaries; retry/backoff; monitoring và operational recovery; Broker Account Boundary chi tiết (chỉ opaque reference ở v0.2); onboarding/KYC; PAPER→LIVE promotion workflow; custody, multi-tenant IAM, billing. Đây là các mối quan tâm triển khai runtime (Phase 1), KHÔNG phải Domain Contract semantic gap — `account.md` pin RULE (identity, boundary, environment, lifecycle, correction lineage, downstream authority), không pin MECHANISM triển khai cụ thể, đúng nguyên tắc defer đã nhất quán xuyên suốt `account.md` §14/§16. Không mở rộng thành Domain Contract semantic mới.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A: authoring + bounded correction hoàn tất cho phạm vi C2; ChatGPT bounded delta Review A hoàn tất (Clean); Independent Review B hoàn tất (Clean with deferred limitations); mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để package kế tiếp (0.2-C3) bắt đầu planning — **không** ngụ ý Product Owner Approval cho `account.md`, **không** ngụ ý Lock, **không** sửa ADR-012, **không** đóng OQ nào, **không** authorize Live, **không** thay đổi Constitution. `account.md` **vẫn giữ `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte không đổi**; `ADR-012.md` **vẫn giữ `version: "0.3"`, `status: Approved`, byte-for-byte không đổi** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package 0.2-C3 — baseline dependency đã thỏa** (Trading Account Foundation nay `Consolidated Stable`) — Product Owner đã authorize scope tối thiểu ("Package 0.2-C3 — Strategy Foundation v0.1"), xem mục "Package 0.2-C3" dưới đây cho chi tiết authoring. **Nay `Consolidated Stable`** (2026-07-30).

**Package 0.2-C4–C7 vẫn chưa có artifact nào được author.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn **active và chưa hoàn tất** — Package 0.2-A/B (tổng thể)/C1/C2 nay đều `Consolidated Stable`, nhưng Phase 0.2 chỉ hoàn tất khi toàn bộ 0.2-C (C1–C7) cũng đạt tương đương, đúng roadmap Chapter 14.

## Package 0.2-C3 đã đạt `Consolidated Stable`

**Phạm vi C3 (scope tối thiểu, đã Product Owner authorize):** một Domain Contract — [`strategy.md`](./strategy.md) v0.3 Draft (Strategy Definition Version + Strategy Instance, MỘT file định nghĩa cả hai concept theo quyết định tổ chức tài liệu của Product Owner — KHÔNG tạo `strategy-definition.md`/`strategy-instance.md` riêng) — `capability_id: strategy-management` / `domain_context_id: strategy-definition` (capability/context **MỚI**, đăng ký lần đầu tại [`context-map.yaml`](./context-map.yaml) v0.13 — Strategy KHÔNG thuộc phạm vi `account-management`/`account-reference` của Package 0.2-C2; **không đổi trong micro-correction này**).

**Package 0.2-C3 micro-correction — tóm tắt (v0.3, 2026-07-30):** đóng đúng một finding Major `C3-DELTA-MAJ-01` (repository-wide shape consistency) — hai vị trí còn sót lại trong `strategy.md` khai báo `instrument_selection_ref` là scalar `string` sau khi v0.2 đã pin shape object (`StrategyInstanceCurrentView.scope` §9, C4 downstream reference contract §10) — cả hai thay bằng đúng object `{instrument_id, venue_id, listing_id}` đã pin tại §5/§6. Shape nay nhất quán tại tất cả sáu vị trí trong tài liệu. Thuần shape-consistency — không đổi eligibility semantics, identity, lifecycle, correction/replay semantics, hay bốn trục evidence. `context-map.yaml` **không đổi** — không có capability/context/relationship semantic nào bị chạm.

**Controlling architecture — [ADR-013](../adr/ADR-013.md) v0.3 `Approved`** (đã có sẵn từ trước, KHÔNG sửa/re-author/bump trong transaction này): Strategy Definition Version — Independent Evidence Axis. `strategy.md` CHỈ implement field/invariant mà ADR-013 §2 yêu cầu (bốn trục evidence độc lập §2.1, capability/instrument-class vs. concrete instrument §2.2, immutable-pin không mutable-latest §2.3, Strategy Instance pin đủ bốn trục §2.4, rebuilt-artifact-identity §2.5), KHÔNG lặp lại toàn văn ADR, KHÔNG tự quyết architecture mới ngoài phạm vi đã khóa. Không có baseline conflict — `strategy.md` chưa tồn tại trước transaction này, đúng expected state.

**Strategy Definition Version — tóm tắt (v0.1):** identity qua `strategy_definition_version_id` (opaque, globally unique, immutable, gán tại `StrategyDefinitionVersionRegistered`, KHÔNG derive từ nội dung — áp dụng bài học `C2-MAJ-01` ngay từ đầu); `strategy_definition_id` là scope field nhóm nhiều Version bất biến (family identity, KHÔNG phải subject/registration event riêng). TOÀN BỘ payload (thesis, `supported_scope`, `required_input_contracts`, `decision_rule_ref`, `explanation_contract_ref`, `downstream_output_capability`) bất biến — KHÔNG có PATCH/metadata-revision event cho subject này (khác Account/Instrument/Venue), đúng ADR-013 §2.3 cấm mutable-latest tường minh. Correction (`StrategyDefinitionVersionFactInvalidated`) LUÔN LUÔN đăng ký ID mới — KHÔNG có same-ID replacement path. KHÔNG có "current/latest Definition" read model — chỉ một validity-check non-authoritative (`GetStrategyDefinitionVersionValidity`) cho một ID cụ thể đã biết.

**Strategy Instance — tóm tắt (v0.1):** identity qua `strategy_instance_id` (opaque, globally unique, immutable). Pin ĐỦ bốn trục evidence độc lập không proxy nhau (`strategy_definition_version_ref`/`plugin_version_ref`/`configuration_version_ref`/`package_build_artifact_ref`) cộng `account_id` (đúng một Account) và `instrument_selection_ref` (ownership pin về Instance, KHÔNG về Configuration Version, đúng yêu cầu "một quy tắc ownership duy nhất"). `environment` KHÔNG lưu riêng — luôn resolve qua `account_id` → Account event stream tại cùng cursor (tránh duplicate source of truth, I-12). Lifecycle tối thiểu ba state (`ACTIVE`/`PAUSED`/`RETIRED`, RETIRED terminal cho forward transition nhưng correctable append-only, `supersedes_fact_ref` có mặt ngay từ v0.1 trên `StrategyInstanceStatusChanged` — áp dụng bài học `C2-MAJ-02` ngay từ đầu). Cộng `StrategyInstanceCurrentView` (optional read model, non-authoritative, latest-state, KHÔNG cursor-addressable, `view_state`/`pending_correction_class`, fold algorithm "visible-valid-head per slice" — áp dụng bài học `C2-MAJ-03`/`C2-MAJ-04` ngay từ đầu, không chờ review round phát hiện).

**Downstream reference contract (Package 0.2-C4, chưa author):** chín field — `strategy_instance_id`/`strategy_definition_id`/`strategy_definition_version_id`/`plugin_version_ref`/`configuration_version_ref`/`package_build_artifact_ref`/`account_id`/`environment` (derived)/`instrument_selection_ref` — resolve TRỰC TIẾP từ authoritative event stream (Strategy Instance, Strategy Definition Version, Account) TẠI cùng cursor; `StrategyInstanceCurrentView` latest-state KHÔNG BAO GIỜ là input hợp lệ. `strategy.md` KHÔNG author semantics của Trade Intent/Decision/Risk/Execution Intent/Order/Fill/Position (Package 0.2-C4–C7).

**Học từ Package 0.2-C2, đóng trước (không chờ review round phát hiện):** opaque identity không derive từ scope/nội dung (`C2-MAJ-01`-style); `supersedes_fact_ref` có mặt ngay từ v0.1 trên mọi event correctable, correction lineage cho phép sửa cả terminal-state fact (`C2-MAJ-02`-style); fold algorithm "visible-valid-head per slice" pin ngay từ v0.1 (`C2-MAJ-03`-style); một quy tắc downstream authority duy nhất — Current View không bao giờ authority, cache chỉ chấp nhận khi cursor-addressable + provably equivalent (`C2-MAJ-04`-style). Khác biệt so với Account: Strategy Definition Version/Strategy Instance registration KHÔNG có mutable metadata tách biệt — TOÀN BỘ scope bất biến, nên correction chỉ có MỘT hình thức (invalidate + ID mới), đơn giản hơn model METADATA_ERROR/SCOPE_ERROR hai lớp của Account.

**Package 0.2-C3 bounded correction — tóm tắt (v0.2, 2026-07-30):** đóng đúng bốn finding Major và hai finding Minor consolidated từ ChatGPT Review A + Independent Review B trên baseline v0.1: `C3-MAJ-01` (`instrument_selection_ref` v0.1 là opaque string chưa pin shape; v0.2 pin `{instrument_id, venue_id, listing_id}` — đúng một TradableListing cụ thể, resolve từ authoritative C1 history tại cùng cursor, không tạo Selection aggregate); `C3-MAJ-02` (thêm Definition Version validity vào computation eligibility — invalidation không tự động pause/retire Instance, lịch sử giữ nguyên, cần Instance mới cho Version đã sửa); `C3-MAJ-03` (thêm Account eligibility ACTIVE vào computation eligibility — SUSPENDED/CLOSED không tự động mutate Instance, không author Order/Position/recovery behavior); `C3-MAJ-04` (pin bốn trục evidence phải persistently resolvable tại cursor — không resolvable ⟹ ineligible, không mutable-latest/fallback/proxy); `C3-MIN-01` (thắt chặt `strategy_definition_id` — gán tại Version đầu tiên của gia đình, không tái sử dụng cho gia đình khác, không family aggregate/registration event/version graph/approval workflow); `C3-MIN-02` (thêm MỘT normative derived rule `eligible_for_new_computation`, hợp nhất sáu điều kiện cùng cursor, tại `strategy.md` §9a — thuộc Strategy eligibility ONLY). ADR-013 không đổi, byte-for-byte.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** schema/versioning scheme cụ thể cho Plugin Version/Configuration Version/Package-Build-Artifact; multi-instrument set/universe/dynamic selection (v0.2 chỉ pin single-listing); xác minh tự động instrument nằm trong `supported_scope`; registry/retention infrastructure cụ thể đảm bảo persistent resolvability bốn trục evidence; runtime worker ownership; transaction boundaries; retry/backoff; monitoring/escalation; operational recovery orchestration; broker/parity-validation gate trước Live (chạm nhưng không đóng OQ-002); retention/resolvability horizon cụ thể cho Instance đã RETIRED; `display_name` revision mechanism.

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất.**
- ChatGPT Review A + Independent Review B (v0.1): 4 finding Major (`C3-MAJ-01`–`C3-MAJ-04`) + 2 finding Minor (`C3-MIN-01`/`C3-MIN-02`), đóng qua bounded correction v0.2.
- Bounded correction (v0.2): **hoàn tất** — cả 6 finding đã đóng, author self-review lần hai hoàn tất.
- ChatGPT delta Review A + Independent Review B (trên `strategy.md` v0.2): tìm thấy `C3-DELTA-MAJ-01` (shape consistency), đóng qua micro-correction v0.3.
- Micro-correction (v0.3): **hoàn tất** — finding đã đóng, author self-review lần ba hoàn tất.
- ChatGPT final focused delta re-review (trên `strategy.md` v0.3): **Clean** — 0 blocking finding.
- Independent Review B final focused delta re-review (trên `strategy.md` v0.3): **Clean** — 0 blocking finding.
- Consolidation: **hoàn tất (transaction này)** — Product Owner authorized: "Package 0.2-C3 consolidation transaction" (2026-07-30). **Package 0.2-C3 nay `Consolidated Stable`.**

**Kết luận consolidation:** ChatGPT final focused delta re-review (Clean) và Independent Review B final focused delta re-review (Clean) trên `strategy.md` v0.3, **0 finding còn lại chưa xử lý** (finding ledger đầy đủ — 6 finding qua vòng bounded correction v0.1→v0.2, 1 finding qua vòng micro-correction v0.2→v0.3 — tại mục baseline dưới đây). Product Owner authorized: "Package 0.2-C3 consolidation transaction" (2026-07-30).

## `Consolidated Stable` baseline — Package 0.2-C3

**Exact reviewed artifact baseline (pinned):**

```text
strategy.md              v0.3   Draft      blob c2cadc464bc8baecff41ff8079461ec0d5dfaccc
ADR-013.md (controlling architecture)  v0.3   Approved   blob 02df931143f8408c61d19ee2c91d2d355d5deb1d
context-map.yaml         v0.13  Draft      blob 5f32edd625f4b66e179dff752d45b301642d76fd
MANIFEST (registry baseline reviewed)  v9.62  blob fa585d2f0aee1274b6bd308f0519f409efe20fce
reviewed HEAD:    922723e459ea6418d66d9cacbd83d849844c6958
```

**Finding ledger — tất cả resolved qua bounded correction (v0.1 → v0.2) và micro-correction (v0.2 → v0.3):**

```text
C3-MAJ-01       — Resolved (instrument_selection_ref pin {instrument_id, venue_id, listing_id}, resolve same-cursor C1 history, không Selection aggregate, v0.2)
C3-MAJ-02       — Resolved (Definition Version VALID required cho computation mới, không auto-cascade Instance lifecycle, §9a, v0.2)
C3-MAJ-03       — Resolved (Account ACTIVE required cho computation mới, không auto-cascade Instance lifecycle, §9a, v0.2)
C3-MAJ-04       — Resolved (bốn trục evidence phải resolvable tại cursor, unresolvable ⟹ ineligible, không proxy, §9a/§11, v0.2)
C3-MIN-01       — Resolved (strategy_definition_id gán tại Version đầu gia đình, không tái sử dụng cross-family, §1, v0.2)
C3-MIN-02       — Resolved (unified rule eligible_for_new_computation, sáu điều kiện AND cùng cursor, §9a/§12, v0.2)
C3-DELTA-MAJ-01 — Resolved (instrument_selection_ref shape consistency — §9/§10 sửa object, đồng nhất sáu vị trí, v0.3)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** schema/versioning scheme cụ thể cho Plugin Version/Configuration Version/Package-Build-Artifact; multi-instrument set/universe/dynamic selection; xác minh tự động instrument nằm trong `supported_scope`; registry/retention infrastructure cụ thể đảm bảo persistent resolvability bốn trục evidence; runtime worker ownership; transaction boundaries; retry/backoff; monitoring/escalation; operational recovery orchestration; broker/parity-validation gate trước Live (chạm nhưng không đóng OQ-002); retention/resolvability horizon cụ thể cho Instance đã RETIRED; `display_name` revision mechanism. Đây là các mối quan tâm triển khai runtime (Phase 1), KHÔNG phải Domain Contract semantic gap — `strategy.md` pin RULE (identity, evidence axes, correction lineage, computation eligibility, downstream authority), không pin MECHANISM triển khai cụ thể, đúng nguyên tắc defer đã nhất quán xuyên suốt `strategy.md` §14/§16. Không mở rộng thành Domain Contract semantic mới.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A: authoring + bounded correction + micro-correction hoàn tất cho phạm vi C3; ChatGPT final focused delta re-review hoàn tất (Clean); Independent Review B final focused delta re-review hoàn tất (Clean); mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để package kế tiếp (0.2-C4) bắt đầu planning — **không** ngụ ý Product Owner Approval cho `strategy.md`, **không** ngụ ý Lock, **không** sửa ADR-013, **không** đóng OQ nào, **không** authorize Live, **không** thay đổi Constitution. `strategy.md` **vẫn giữ `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte không đổi**; `ADR-013.md` **vẫn giữ `version: "0.3"`, `status: Approved`, byte-for-byte không đổi**; `context-map.yaml` **vẫn giữ `version: "0.13"`, `status: Draft`, byte-for-byte không đổi** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package lifecycle states (pinned tại transaction này):**

```text
Package 0.2-C1:    Consolidated Stable
Package 0.2-C2:    Consolidated Stable
Package 0.2-C3:    Consolidated Stable
Package 0.2-C4–C7: unauthorized, unauthored
```

**Package 0.2-C4 — baseline dependency đã thỏa** (Strategy Foundation nay `Consolidated Stable`) — Product Owner đã authorize scope tối thiểu ("Package 0.2-C4 — Trade Intent and Decision Foundation v0.1"), xem mục "Package 0.2-C4" dưới đây cho chi tiết authoring. **Nay `Consolidated Stable`** (2026-07-31).

**Package 0.2-C5–C7 vẫn chưa có artifact nào được author.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn **active và chưa hoàn tất** — Package 0.2-A/B (tổng thể)/C1/C2/C3 nay đều `Consolidated Stable`, nhưng Phase 0.2 chỉ hoàn tất khi toàn bộ 0.2-C (C1–C7) cũng đạt tương đương, đúng roadmap Chapter 14.

## Package 0.2-C4 đã đạt `Consolidated Stable`

**Phạm vi C4 (scope tối thiểu, đã Product Owner authorize):** hai Domain Contract — [`decision.md`](./decision.md) v0.3 Draft (Decision + DecisionEvaluationAttempt) và [`trade-intent.md`](./trade-intent.md) v0.2 Draft (Trade Intent, **không đổi trong micro-correction này**) — HAI concept riêng biệt, HAI file riêng — `capability_id: decision-management` / `domain_context_id: strategy-decision` (đăng ký tại [`context-map.yaml`](./context-map.yaml) v0.14, không đổi).

**Controlling architecture:** [ADR-010](../adr/ADR-010.md) **Approved** (Decision Time Model) + [Chapter 8 §8.2.1/§8.4/§8.4.1/§8.5](../constitution/08-event-model.md) (Locked) + [ADR-013](../adr/ADR-013.md) v0.3 Approved (qua `strategy.md`) — không sửa/re-author/bump ADR nào.

**Package 0.2-C4 bounded correction — tóm tắt (v0.2, 2026-07-31):** đóng đúng sáu finding Major consolidated từ ChatGPT Review A + Independent Review B trên baseline v0.1: `C4-MAJ-01` (bỏ `trade_intent_outcome`/`SUPPRESSED_DUPLICATE` khỏi Decision evidence — duplicate handling nay là idempotency behavior, không phải Decision result); `C4-MAJ-02` (derivation Decision→Trade Intent nay idempotent qua `originating_decision_id` là unique key trên toàn bộ TradeIntentIssued VALID, canonical `trade_intent_derivation_idempotency_policy: ONE_VALID_INTENT_PER_ORIGINATING_DECISION`, trade-intent.md §10 — không unstated cross-stream atomicity, Phase 1 phải recover deterministic từ Decision LONG/SHORT valid); `C4-MAJ-03` (thêm correction lineage cho DecisionRecorded — `decision_id` vẫn bất biến/globally-unique per-fact, nhưng logical computation key `(strategy_instance_id, decision_context_cursor)` nay CÓ THỂ có nhiều DecisionRecorded qua invalidate + same-key replacement mang decision_id MỚI + `supersedes_fact_ref`, visible-valid-head per logical key, decision.md §8/§11); `C4-MAJ-04` (thêm `DecisionEvaluationAttempt`/`DecisionEvaluationAttemptRecorded`, decision.md §2/§4 — MỌI lần thử đánh giá kể cả ineligible/missing-input/failed nay là authoritative fact tường minh, đóng cơ chế "no event when ineligible" của v0.1, bốn outcome đóng: DECIDED/INELIGIBLE/INPUT_UNAVAILABLE/FAILED_BEFORE_EVALUATION); `C4-MAJ-05` (thêm invariant thứ tự — `TradeIntentIssued.effective_time >= originating Decision.decision_time`, `recorded_time` strict causal, trade-intent.md §3/§9); `C4-MAJ-06` (thêm `eligible_for_new_risk_evaluation` origin-validity rule, trade-intent.md §6a). ADR-010/ADR-013 không đổi, byte-for-byte.

**Package 0.2-C4 micro-correction — tóm tắt (v0.3, 2026-07-31):** đóng đúng hai finding Major consolidated từ ChatGPT delta Review A + Independent Review B trên baseline v0.2: `C4-DELTA-MAJ-01` (loại bỏ `resulting_decision_id` khỏi `DecisionEvaluationAttempt`/`DecisionEvaluationAttemptRecorded` — attempt DECIDED và Decision nay liên hệ MỘT CHIỀU DUY NHẤT qua `DecisionRecorded.causation_refs`, loại bỏ circular append-order dependency; query chiều ngược dùng cơ chế đã có, `GetDecisionForComputation` hoặc reverse causation_refs lookup, KHÔNG event/field mới); `C4-DELTA-MAJ-02` (tách `evaluation_attempt_id` — identity cá nhân một lần thử — khỏi logical computation key `(strategy_instance_id, decision_context_cursor)` — nhiều attempt CÓ THỂ chia sẻ cùng key kể cả outcome khác nhau, ví dụ `FAILED_BEFORE_EVALUATION` rồi retry `DECIDED`; idempotency nay scoped theo `evaluation_attempt_id`, canonical `decision_evaluation_attempt_idempotency_policy: STABLE_ATTEMPT_ID_SAME_PAYLOAD_IS_IDEMPOTENT`; nhiều attempt DECIDED cùng key phải resolve/reuse cùng một Decision qua `decision_computation_idempotency_policy` ở tầng Decision, không tạo hai Decision head trừ khi correction lineage cho phép). `trade-intent.md` **không đổi** — không có cross-reference nào cần sửa.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** Stream Registry/Input Contract/canonical Audit Stream implementation cụ thể; preservation-fact Event Contract cụ thể cho registry-transition-retired-stream edge case; nguồn cụ thể của reference-series fact (EMA hay contract khác); `evaluation_timing = INTRABAR`; `rule_family` khác `PRICE_CROSSES_REFERENCE_SERIES`; chính sách hết hạn Trade Intent cụ thể; `EXIT`/`FLAT`/`CLOSE`/`REDUCE` intent_type; implementation technology cho Decision→Trade Intent recovery (retry queue/outbox/message-broker); granular exception sub-taxonomy cho `FAILED_BEFORE_EVALUATION`; correction lineage riêng cho `DecisionEvaluationAttempt`; attempt lifecycle/scheduler/retry workflow.

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất.**
- ChatGPT Review A + Independent Review B (v0.1): 6 finding Major (`C4-MAJ-01`–`C4-MAJ-06`), đóng qua bounded correction v0.2.
- Bounded correction (v0.2): **hoàn tất** — cả 6 finding đã đóng, author self-review lần hai hoàn tất.
- ChatGPT delta Review A + Independent Review B (trên v0.2): 2 finding Major (`C4-DELTA-MAJ-01`/`C4-DELTA-MAJ-02`), đóng qua micro-correction v0.3.
- Micro-correction (v0.3): **hoàn tất** — cả 2 finding đã đóng, author self-review lần ba hoàn tất.
- ChatGPT final focused delta re-review (trên v0.3): **Clean** — 0 blocking finding.
- Independent Review B final focused delta re-review (trên v0.3): **Clean** — 0 blocking finding.
- Consolidation: **hoàn tất (transaction này)** — Product Owner authorized: "Package 0.2-C4 consolidation transaction" (2026-07-31). **Package 0.2-C4 nay `Consolidated Stable`.**

**Kết luận consolidation:** ChatGPT final focused delta re-review (Clean) và Independent Review B final focused delta re-review (Clean) trên `decision.md` v0.3 + `trade-intent.md` v0.2, **0 finding còn lại chưa xử lý** (finding ledger đầy đủ — 6 finding qua bounded correction v0.1→v0.2, 2 finding qua micro-correction v0.2→v0.3 — tại mục baseline dưới đây). Product Owner authorized: "Package 0.2-C4 consolidation transaction" (2026-07-31).

## `Consolidated Stable` baseline — Package 0.2-C4

**Exact reviewed artifact baseline (pinned):**

```text
decision.md              v0.3   Draft      blob e2a26320200d350ace3da0247235bb14cef12509
trade-intent.md          v0.2   Draft      blob e7a306abc53ba482ff1249af1dda2829c4c82fa7
ADR-010.md (controlling architecture)  Approved   blob 80b1807f9b99f2a83bfbdbdbd90672bd9ff06759
ADR-013.md (controlling architecture, qua strategy.md)  v0.3   Approved   blob 02df931143f8408c61d19ee2c91d2d355d5deb1d
context-map.yaml         v0.14  Draft      blob e7ad311419f54a60625ce05f37b0c0c8e982fafb
MANIFEST (registry baseline reviewed)  v9.66  blob ace9979897f793c1f2c52b543294e0a07d665835
reviewed HEAD:    2f338f54d19a1eaaf1280061e418793337de7a5e
```

**Finding ledger — tất cả resolved qua bounded correction (v0.1 → v0.2) và micro-correction (v0.2 → v0.3):**

```text
C4-MAJ-01        — Resolved (bỏ trade_intent_outcome/SUPPRESSED_DUPLICATE khỏi Decision, duplicate handling nay là idempotency behavior, v0.2)
C4-MAJ-02        — Resolved (derivation Decision→Trade Intent idempotent qua originating_decision_id unique key, trade_intent_derivation_idempotency_policy, v0.2)
C4-MAJ-03        — Resolved (correction lineage cho DecisionRecorded, decision_id mới + supersedes_fact_ref, visible-valid-head per logical key, v0.2)
C4-MAJ-04        — Resolved (thêm DecisionEvaluationAttempt/DecisionEvaluationAttemptRecorded, mọi lần thử là authoritative fact, v0.2)
C4-MAJ-05        — Resolved (invariant thứ tự effective/recorded-time giữa Trade Intent và Decision gốc, v0.2)
C4-MAJ-06        — Resolved (thêm eligible_for_new_risk_evaluation origin-validity rule, v0.2)
C4-DELTA-MAJ-01  — Resolved (loại bỏ resulting_decision_id, Attempt→Decision liên hệ một chiều qua causation_refs, v0.3)
C4-DELTA-MAJ-02  — Resolved (tách evaluation_attempt_id khỏi logical computation key, idempotency per-attempt-identity, v0.3)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** Stream Registry/Input Contract/canonical Audit Stream implementation cụ thể; preservation-fact Event Contract cụ thể cho registry-transition-retired-stream edge case; nguồn cụ thể của reference-series fact (EMA hay contract khác); `evaluation_timing = INTRABAR`; `rule_family` khác `PRICE_CROSSES_REFERENCE_SERIES`; chính sách hết hạn Trade Intent cụ thể; `EXIT`/`FLAT`/`CLOSE`/`REDUCE` intent_type; implementation technology cho Decision→Trade Intent recovery; granular exception sub-taxonomy cho `FAILED_BEFORE_EVALUATION`; correction lineage riêng cho `DecisionEvaluationAttempt`; attempt lifecycle/scheduler/retry workflow. Đây là các mối quan tâm triển khai runtime (Phase 1), KHÔNG phải Domain Contract semantic gap — `decision.md`/`trade-intent.md` pin RULE (identity, evidence axes, correction lineage, computation eligibility, evaluation-attempt disposition, downstream authority), không pin MECHANISM triển khai cụ thể. Không mở rộng thành Domain Contract semantic mới.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A: authoring + bounded correction + micro-correction hoàn tất cho phạm vi C4; ChatGPT final focused delta re-review hoàn tất (Clean); Independent Review B final focused delta re-review hoàn tất (Clean); mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để package kế tiếp (0.2-C5) bắt đầu planning — **không** ngụ ý Product Owner Approval cho `decision.md`/`trade-intent.md`, **không** ngụ ý Lock, **không** sửa ADR-010/ADR-013, **không** đóng OQ nào, **không** authorize Live, **không** thay đổi Constitution. `decision.md` **vẫn giữ `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte không đổi**; `trade-intent.md` **vẫn giữ `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte không đổi**; `ADR-010.md`/`ADR-013.md` **vẫn giữ trạng thái Approved, byte-for-byte không đổi**; `context-map.yaml` **vẫn giữ `version: "0.14"`, `status: Draft`, byte-for-byte không đổi** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package lifecycle states (pinned tại transaction này):**

```text
Package 0.2-C1:    Consolidated Stable
Package 0.2-C2:    Consolidated Stable
Package 0.2-C3:    Consolidated Stable
Package 0.2-C4:    Consolidated Stable
Package 0.2-C5–C7: unauthorized, unauthored
```

**Package 0.2-C5 nay `Consolidated Stable`** — Product Owner đã authorize scope tối thiểu ("Package 0.2-C5 — Risk Gateway and Execution Intent Foundation v0.1"), sau đó một bounded correction (v0.2, đóng consolidated Review A + Independent Review B findings C5-MAJ-01..06), một micro-correction (v0.3, đóng `C5-DELTA-MAJ-01` — evidence availability versus unit compatibility separation), và cuối cùng một consolidation transaction (Product Owner authorized: "Package 0.2-C5: Consolidated Stable") — xem mục "Package 0.2-C5" dưới đây cho chi tiết.

**Package 0.2-C6 nay `Consolidated Stable`. Package 0.2-C7 nay authored (chưa `Consolidated Stable`), xem mục "Package 0.2-C7" dưới đây.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn **active và chưa hoàn tất** — Package 0.2-A/B (tổng thể)/C1/C2/C3/C4/C5/C6 nay đều `Consolidated Stable`, nhưng Phase 0.2 chỉ hoàn tất khi toàn bộ 0.2-C (C1–C7) cũng đạt tương đương, đúng roadmap Chapter 14.

## Package 0.2-C5 — Risk Gateway and Execution Intent Foundation `Consolidated Stable`

**Phạm vi C5 (scope tối thiểu, đã Product Owner authorize):** hai Domain Contract — [`risk.md`](./risk.md) v0.3 Draft (RiskEvaluation + RiskEvaluationAttempt) và [`execution-intent.md`](./execution-intent.md) v0.2 Draft (Execution Intent, không đổi trong micro-correction này) — HAI concept riêng biệt, HAI file riêng, đúng yêu cầu "Risk and Execution Intent must remain separate concepts" — `capability_id: risk-management` / `domain_context_id: risk-gateway` (capability/context **MỚI**, đăng ký lần đầu tại [`context-map.yaml`](./context-map.yaml) v0.17 — Risk/Execution Intent KHÔNG thuộc phạm vi `decision-management`/`strategy-decision` của Package 0.2-C4).

**v0.2 — bounded correction (đóng consolidated Review A + Independent Review B findings, sáu Major):** (1) `C5-MAJ-01` — sửa thứ tự Attempt EVALUATED: bounded policy computation PHẢI hoàn tất TRƯỚC KHI `RiskEvaluationAttemptRecorded(EVALUATED)` ghi (trước đây văn bản mô tả sai thứ tự "Attempt ghi trước rồi engine chạy," mâu thuẫn ngữ nghĩa EVALUATED); thêm recoverable-append-gap invariant cho khoảng trống Attempt→RiskEvaluation. (2) `C5-MAJ-02` — thêm `evidence_availability` (bảy khóa đóng, năm giá trị đóng ban đầu) làm mọi ref/scalar evidence field trở thành conditional, loại bỏ khả năng NON_EVALUABLE bundle yêu cầu field không tồn tại. (3) `C5-MAJ-03` — thêm bounded v0.1 unit model (`unit_evidence`) — mọi Risk arithmetic PHẢI cùng currency với TradableListing quote asset, mismatch → `NON_EVALUABLE`/`INCOMPATIBLE_EVIDENCE_UNIT`, KHÔNG FX conversion. (4) `C5-MAJ-04` — `approved_quantity` PHẢI strictly positive sau floor-rounding trên cả `risk.md` VÀ `execution-intent.md` — bằng 0 → `REJECTED`/`QUANTITY_ROUNDS_TO_ZERO`, zero Execution Intent. (5) `C5-MAJ-05` — pin domain số học chính xác cho mọi scalar input, disclose bounded `quantity_precision` maximum = 18 (không có repository-wide bound sẵn có, chọn tường minh v0.1); exposure âm chặn tại domain-validation, KHÔNG bypass cap. (6) `C5-MAJ-06` — `eligible_for_new_order_creation` mở rộng đủ NĂM điều kiện transitive (Decision→Trade Intent→RiskEvaluation→Execution Intent). Sizing algorithm mở rộng từ sáu bước thành mười ba bước deterministic (§5c risk.md).

**v0.3 — micro-correction (đóng `C5-DELTA-MAJ-01`, consolidated Review A + Independent Review B findings trên baseline v0.2):** `evidence_availability` (§5b2) tách biệt hoàn toàn khỏi `unit_evidence` compatibility (§5b1) — hai khái niệm KHÁC NHAU trước đây bị gộp vào cùng một enum 5-giá-trị (`AVAILABLE`/`MISSING`/`INVALID`/`UNRESOLVABLE`/`INCOMPATIBLE_UNIT`), khiến `INCOMPATIBLE_UNIT` KHÔNG BAO GIỜ hợp lệ được set bởi thuật toán (mâu thuẫn với invariant "NON_EVALUABLE ⟺ ít nhất một khóa != AVAILABLE"). `evidence_availability` nay chỉ còn bốn giá trị (`AVAILABLE`/`MISSING`/`INVALID`/`UNRESOLVABLE`). `result = NON_EVALUABLE` nay pin đúng hai nhánh loại trừ lẫn nhau: Branch A — availability failure (≥1 khóa != AVAILABLE → `REQUIRED_EVIDENCE_UNAVAILABLE`/`RISK_POLICY_EVIDENCE_UNAVAILABLE`, unit comparison không chạy); Branch B — compatibility failure (TẤT CẢ khóa = AVAILABLE, unit equality invariant fail → `INCOMPATIBLE_EVIDENCE_UNIT`, mọi resolved ref/value vẫn có mặt). Thuật toán deterministic (§5c) không đổi thứ tự — chỉ pin lại rõ ràng tính loại-trừ-lẫn-nhau. Thêm Scenario 19 (price base mismatch). `execution-intent.md` không đổi, blob preserved.

**Controlling architecture:** [`trade-intent.md`](./trade-intent.md) v0.2 Draft §6a (`eligible_for_new_risk_evaluation`, không sửa) + [Chapter 8 §8.1.1/§8.2/§8.5](../constitution/08-event-model.md) (Locked, Referenced Authoritative Artifact + canonical Replay Cursor — tái sử dụng nguyên vẹn cho `risk_context_cursor`, KHÔNG tạo schema gần giống) + [Chapter 9 §9.1](../constitution/09-plugin-model.md) (Locked, bốn lớp Plugin identity áp dụng platform-wide cho bốn trục risk evidence) — không sửa/re-author/bump ADR/Constitution nào. `risk.md`/`execution-intent.md` ÁP DỤNG LẠI (KHÔNG sao chép cơ học) ba semantic pattern đã proven qua C4's hai vòng correction: (1) KHÔNG circular reference giữa Attempt và RiskEvaluation (đóng trước lớp lỗi `C4-DELTA-MAJ-01`-style, ngay từ v0.1); (2) `evaluation_attempt_id` tách biệt logical computation key (đóng trước lớp lỗi `C4-DELTA-MAJ-02`-style, ngay từ v0.1); (3) origin-uniqueness/idempotency + origin-validity rule cho downstream package (đúng pattern `originating_decision_id`/`eligible_for_new_risk_evaluation` đã proven tại `trade-intent.md`).

**RiskEvaluation — tóm tắt (v0.2):** `risk_evaluation_id` (opaque, globally unique, immutable). Logical computation key `(trade_intent_id, risk_context_cursor)` — `risk_context_cursor` TÁI SỬ DỤNG nguyên vẹn Chapter 8 §8.5.1 Replay Cursor shape như PAYLOAD field (KHÔNG envelope-level ADR-010 field — `event_class: decision` KHÔNG áp dụng, chỉ riêng cho `decision.md`'s `DecisionRecorded`). `RiskEvaluationAttempt` (subject riêng): `attempt_outcome ∈ {EVALUATED, INELIGIBLE, FAILED_BEFORE_EVALUATION}` — MỌI lần thử ĐỀU ghi nhận, KHÔNG absence-based; `EVALUATED` CHỈ ghi SAU KHI computation hoàn tất trọn vẹn (v0.2). Precondition: `eligible_for_new_risk_evaluation == true` (trade-intent.md §6a) — false → attempt INELIGIBLE, KHÔNG RiskEvaluation. `evidence_availability` (bảy khóa đóng, bốn giá trị đóng — v0.3, tách biệt khỏi unit compatibility) gate mọi ref/scalar evidence field (bốn trục risk evidence + ba evidence fact) thành conditional. Bounded v0.1 unit model (`unit_evidence`, v0.2) — mọi currency PHẢI khớp TradableListing quote asset; `result = NON_EVALUABLE` pin hai nhánh loại trừ lẫn nhau (Branch A availability, Branch B compatibility, v0.3). Sizing bounded deterministic (`sizing_method: FIXED_RISK_BUDGET_NOTIONAL`) — mười ba bước tuần tự (v0.2: validate eligibility, resolve evidence, resolve availability/unit, domain validation, account active, environment=PAPER, equity >= risk budget, projected exposure <= max notional, floor-round, zero-check) → `approved_quantity` strictly positive khi APPROVED. `result: APPROVED | REJECTED | NON_EVALUABLE` — chín reason code đóng (v0.2: thêm `QUANTITY_ROUNDS_TO_ZERO`, `RISK_POLICY_EVIDENCE_UNAVAILABLE`, `INCOMPATIBLE_EVIDENCE_UNIT`). Correction lineage: `risk_evaluation_id` bất biến per-fact, logical key hỗ trợ invalidate + same-key replacement (`supersedes_fact_ref`), visible-valid-head per logical key.

**Execution Intent — tóm tắt (v0.2):** `execution_intent_id` (opaque, globally unique, immutable), origin từ ĐÚNG MỘT RiskEvaluation APPROVED (`originating_risk_evaluation_id`, unique key, `execution_intent_derivation_idempotency_policy`). `account_id`/`instrument_selection_ref`/`direction`/`approved_quantity`/`quantity_unit` PHẢI khớp chính xác RiskEvaluation gốc — KHÔNG tự tính lại/thay đổi; `approved_quantity` PHẢI strictly positive (v0.2). `execution_action: OPEN_EXPOSURE` (v0.1, duy nhất). Lifecycle tối thiểu ba state (`ISSUED`/`WITHDRAWN`/`EXPIRED`), `supersedes_fact_ref` từ v0.1. Time ordering: `effective_time >= risk_evaluation_time`, `recorded_time > RiskEvaluationRecorded.recorded_time`. `eligible_for_new_order_creation` (v0.2: đủ NĂM điều kiện transitive, đóng `C5-MAJ-06`) — khi Trade Intent hoặc RiskEvaluation gốc invalidate/supersede, Execution Intent liên quan mất eligibility cho Order creation mới mà KHÔNG tự động xóa/rewrite.

**Cardinality:** `RiskEvaluation.result = APPROVED` → zero hoặc một Execution Intent; `REJECTED`/`NON_EVALUABLE` → zero luôn luôn.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** Stream Registry/Input Contract implementation cụ thể; nguồn cụ thể của evidence fact (Account/Ledger contract cho equity/exposure); cơ chế cụ thể resolve `evidence_availability`/`unit_evidence` (v0.2); `sizing_method` khác `FIXED_RISK_BUDGET_NOTIONAL`; correction lineage riêng cho `RiskEvaluationAttempt`; granular exception sub-taxonomy cho `FAILED_BEFORE_EVALUATION`; implementation technology cho RiskEvaluation→Execution Intent recovery; `environment = LIVE` policy support (v0.1 CHỈ PAPER); CLOSE/REDUCE execution_action; chính sách hết hạn Execution Intent cụ thể; `quantity_precision` maximum = 18 là disclosed v0.1 judgment call, rà soát lại nếu về sau có repository-wide bound authoritative.

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất.**
- ChatGPT Review A + Independent Review B (baseline v0.1): **hoàn tất** — sáu Major finding (`C5-MAJ-01`..`C5-MAJ-06`) consolidated.
- Bounded correction commit (v0.1 → v0.2), Product Owner authorized: **hoàn tất** — đóng toàn bộ sáu finding.
- ChatGPT delta Review A + Independent Review B delta review (trên v0.2): **hoàn tất** — một Major finding (`C5-DELTA-MAJ-01`, evidence availability versus unit compatibility conflation) consolidated.
- Micro-correction commit (v0.2 → v0.3), Product Owner authorized: **hoàn tất** — đóng `C5-DELTA-MAJ-01`. `execution-intent.md` không đổi.
- ChatGPT final focused delta re-review (trên v0.3): **Clean** — 0 blocking finding.
- Independent Review B final focused delta re-review (trên v0.3): **Clean** — 0 blocking finding.
- Consolidation: **hoàn tất (transaction này)** — Product Owner authorized: "Package 0.2-C5: Consolidated Stable". **Package 0.2-C5 nay `Consolidated Stable`.**

**Kết luận consolidation:** ChatGPT final focused delta re-review (Clean) và Independent Review B final focused delta re-review (Clean) trên `risk.md` v0.3 + `execution-intent.md` v0.2, **0 finding còn lại chưa xử lý** (finding ledger đầy đủ — 6 finding qua bounded correction v0.1→v0.2, 1 finding qua micro-correction v0.2→v0.3 — tại mục baseline dưới đây). Product Owner authorized: "Package 0.2-C5: Consolidated Stable".

## `Consolidated Stable` baseline — Package 0.2-C5

**Exact reviewed artifact baseline (pinned):**

```text
risk.md                  v0.3   Draft      blob 1deb39f49c82f8b138c0dc3f65250b876c1839ab
execution-intent.md      v0.2   Draft      blob afc0c1fe7bdd2f285403dff29c71849ab66af70c
context-map.yaml         v0.17  Draft      blob 59f11a2cee142c533280a33060c21f69f3fc50cf
MANIFEST (registry baseline reviewed)  v9.70  
reviewed HEAD:    55b9cb842de91825a7335a6563c35a690c926fe4
```

**Finding ledger — tất cả resolved qua bounded correction (v0.1 → v0.2) và micro-correction (v0.2 → v0.3):**

```text
C5-MAJ-01        — Resolved (sửa thứ tự Attempt EVALUATED — computation hoàn tất TRƯỚC, Attempt EVALUATED ghi SAU, recoverable append gap, v0.2)
C5-MAJ-02        — Resolved (thêm evidence_availability bảy khóa đóng, mọi ref/scalar evidence field conditional, v0.2)
C5-MAJ-03        — Resolved (thêm bounded v0.1 unit model, mismatch → NON_EVALUABLE/INCOMPATIBLE_EVIDENCE_UNIT, v0.2)
C5-MAJ-04        — Resolved (approved_quantity strictly positive sau floor-rounding, QUANTITY_ROUNDS_TO_ZERO, v0.2)
C5-MAJ-05        — Resolved (pin domain số học cho mọi scalar input, quantity_precision maximum = 18 disclosed, v0.2)
C5-MAJ-06        — Resolved (eligible_for_new_order_creation mở rộng đủ năm điều kiện transitive, v0.2)
C5-DELTA-MAJ-01  — Resolved (tách evidence_availability khỏi unit compatibility, hai nhánh NON_EVALUABLE loại trừ lẫn nhau, v0.3)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** Stream Registry/Input Contract implementation cụ thể; nguồn cụ thể của evidence fact (Account/Ledger contract cho equity/exposure); cơ chế cụ thể resolve `evidence_availability`/`unit_evidence`; `sizing_method` khác `FIXED_RISK_BUDGET_NOTIONAL`; correction lineage riêng cho `RiskEvaluationAttempt`; granular exception sub-taxonomy cho `FAILED_BEFORE_EVALUATION`; implementation technology cho RiskEvaluation→Execution Intent recovery; `environment = LIVE` policy support (v0.1 CHỈ PAPER); CLOSE/REDUCE execution_action; chính sách hết hạn Execution Intent cụ thể; `quantity_precision` maximum = 18 là disclosed v0.1 judgment call, rà soát lại nếu về sau có repository-wide bound authoritative. Đây là các mối quan tâm triển khai runtime (Phase 1), KHÔNG phải Domain Contract semantic gap — không mở rộng thành Domain Contract semantic mới.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A: authoring + bounded correction + micro-correction hoàn tất cho phạm vi C5; ChatGPT final focused delta re-review hoàn tất (Clean); Independent Review B final focused delta re-review hoàn tất (Clean); mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để package kế tiếp (0.2-C6) bắt đầu planning — **không** ngụ ý Product Owner Approval cho `risk.md`/`execution-intent.md`, **không** ngụ ý Lock, **không** sửa ADR nào, **không** đóng OQ nào, **không** authorize Live, **không** thay đổi Constitution. `risk.md` **vẫn giữ `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte không đổi**; `execution-intent.md` **vẫn giữ `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte không đổi**; `context-map.yaml` **vẫn giữ `version: "0.17"`, `status: Draft`, byte-for-byte không đổi** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package lifecycle states (pinned tại transaction này):**

```text
Package 0.2-C1:    Consolidated Stable
Package 0.2-C2:    Consolidated Stable
Package 0.2-C3:    Consolidated Stable
Package 0.2-C4:    Consolidated Stable
Package 0.2-C5:    Consolidated Stable
Package 0.2-C6–C7: unauthorized, unauthored
```

**Package 0.2-C6 baseline dependency đã thỏa, eligible cho Product Owner scope authorization — CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này.** Package 0.2-C7 gate chưa mở. OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất.

## Package 0.2-C6 — Order Foundation `Consolidated Stable`

**Phạm vi C6 (scope tối thiểu, đã Product Owner authorize):** một Domain Contract — [`order.md`](./order.md) v0.2 Draft (Order + OrderCreationAttempt + OrderSubmissionRequest) — ba concept trong MỘT file, đúng quyết định tổ chức "prefer một bounded contract chứa cả creation và submission-request semantics" — `capability_id: execution-management` / `domain_context_id: order-management` (capability/context **MỚI**, đăng ký lần đầu tại [`context-map.yaml`](./context-map.yaml) v0.18, không đổi trong bounded correction này — Order KHÔNG thuộc phạm vi `risk-management`/`risk-gateway` của Package 0.2-C5). MỘT relationship edge đã đăng ký (không đổi): `risk-gateway` (execution-intent) → `order-management` (order), `published_language`, contract `execution-intent-issued`.

**Controlling architecture:** [`execution-intent.md`](./execution-intent.md) v0.2 Draft §6a (`eligible_for_new_order_creation`, không sửa) + [Chapter 8 §8.1.1/§8.2/§8.5](../constitution/08-event-model.md) (Locked, Referenced Authoritative Artifact + canonical Replay Cursor — tái sử dụng nguyên vẹn cho `order_context_cursor`/`submission_context_cursor`, KHÔNG tạo schema gần giống) — không sửa/re-author/bump ADR/Constitution nào. `order.md` ÁP DỤNG LẠI (KHÔNG sao chép cơ học) bốn semantic pattern đã proven qua C4/C5's các vòng correction: (1) KHÔNG circular reference giữa Attempt và Order; (2) `order_creation_attempt_id` tách biệt logical creation key; (3) `attempt_outcome = CREATED` chỉ ghi sau khi computation hoàn tất trọn vẹn (đóng trước lớp lỗi `C5-MAJ-01`-style, ngay từ v0.1); (4) `FAILED_BEFORE_CREATION` tường minh retryable.

**v0.2 — bounded correction (đóng consolidated Review A + Independent Review B findings, ba Major):** (1) `C6-MAJ-01` — thêm `supersedes_fact_ref` vào `OrderCreated.payload` (thiếu trong v0.1 dù correction prose đã yêu cầu); pin convention direct-predecessor-fact-targeting (đối xứng `risk.md` §10 — trỏ TRỰC TIẾP predecessor `OrderCreated`, KHÔNG trỏ `OrderFactInvalidated`); thêm mười invariant correction lineage; sửa fold algorithm dựng EXPLICIT chain theo `supersedes_fact_ref`. (2) `C6-MAJ-02` — cho phép `OrderFactInvalidated` target `OrderSubmissionRequested` (invalidate-only); sửa fold algorithm loại trừ request đã invalidate khỏi lifecycle/duplicate-suppression/C7 readiness; request MỚI CÓ THỂ append sau nếu eligible lại. (3) `C6-MAJ-03` — `eligible_for_execution_result_processing` nay dùng TRỌN VẸN `eligible_for_new_order_creation` (bao gồm điều kiện `ExecutionIntent.current_status == ISSUED`, trước đây bị bỏ sót) VÀ pin CHÍNH XÁC `current_status == SUBMISSION_REQUESTED`.

**Order — tóm tắt (v0.2):** `order_id` (opaque, globally unique, immutable). Logical creation key = `originating_execution_intent_id` (không có cursor component — 1:1 giữa Execution Intent và visible-valid-head Order, khác pattern (trade_intent_id, cursor) của RiskEvaluation). `OrderCreationAttempt` (subject riêng): `attempt_outcome ∈ {CREATED, INELIGIBLE, FAILED_BEFORE_CREATION}` — MỌI lần thử ĐỀU ghi nhận. Precondition: `eligible_for_new_order_creation == true` (execution-intent.md §6a) — false → attempt INELIGIBLE, KHÔNG Order. Scope bất biến copy nguyên vẹn từ Execution Intent gốc — `quantity` LUÔN CHÍNH XÁC bằng `approved_quantity` gốc, KHÔNG resize/clamp/round. v0.1 pin ba giá trị đơn: `order_action=OPEN_EXPOSURE`, `order_type=MARKET`, `environment=PAPER`. Correction lineage (v0.2): `order_id` bất biến per-fact, logical key hỗ trợ invalidate + explicit same-key replacement chain (`supersedes_fact_ref` trỏ trực tiếp predecessor fact, mười invariant đầy đủ), visible-valid-head per logical key (đối xứng RiskEvaluation, khác ExecutionIntent's invalidate-only).

**OrderSubmissionRequest — tóm tắt (v0.2):** `submission_request_id` (opaque, per-fact identity), derivation/idempotency key = `order_id` (KHÔNG một individual submission-attempt identity riêng — walking skeleton không cần). `target_environment=PAPER` — KHÔNG chứng minh venue acceptance/execution/Fill. Lifecycle tối thiểu năm state (`UNSEEN`/`CREATED`/`SUBMISSION_REQUESTED`/`WITHDRAWN`/`EXPIRED`), `supersedes_fact_ref` từ v0.1 trên `OrderStatusChanged`. **v0.2:** CÓ THỂ bị invalidate (invalidate-only, không same-ID replacement bắt buộc) — request mới CÓ THỂ append sau nếu eligible lại.

**Hai derived eligibility rule (v0.2):** `eligible_for_new_submission_request(order_id, C)` (§8a order.md) — visible-valid-head + `current_status=CREATED` + `eligible_for_new_order_creation` (đầy đủ năm điều kiện) + chưa có submission request VALID (chưa invalidate) tại C. `eligible_for_execution_result_processing(order_id, C)` (§8b order.md, đóng `C6-MAJ-03`) — visible-valid-head + `eligible_for_new_order_creation` đầy đủ năm điều kiện + đúng một submission request VALID + `current_status == SUBMISSION_REQUESTED` (chính xác, không chỉ "khác WITHDRAWN/EXPIRED") — future C7 readiness boundary, KHÔNG author Fill semantics.

**Cardinality:** một Execution Intent eligible → zero hoặc một Order (visible-valid-head).

**Deferred limitations (Phase 1 implementation concern, non-blocking):** Stream Registry/Input Contract implementation cụ thể; chính sách hết hạn Order cụ thể; lý do WITHDRAWN cụ thể; reference price cho PAPER simulation evidence (v0.1 chủ động omit — Order không tự tính toán gì); granular exception sub-taxonomy cho `FAILED_BEFORE_CREATION`; individual submission-attempt identity riêng; correction lineage riêng cho `OrderCreationAttempt` (`OrderSubmissionRequested` nay CÓ correction — invalidate-only, v0.2); implementation technology cho Execution Intent→Order và Order→Submission recovery.

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất.**
- ChatGPT Review A + Independent Review B (baseline v0.1): **hoàn tất** — ba Major finding (`C6-MAJ-01`/`C6-MAJ-02`/`C6-MAJ-03`) consolidated.
- Bounded correction commit (v0.1 → v0.2), Product Owner authorized: **hoàn tất** — đóng toàn bộ ba finding.
- ChatGPT bounded delta Review A (trên v0.2): **Clean** — 0 blocking finding.
- Independent Delta Review B (trên v0.2): **Clean** — 0 blocking finding.
- Consolidation: **hoàn tất (transaction này)** — Product Owner authorized: "Package 0.2-C6: Consolidated Stable". **Package 0.2-C6 nay `Consolidated Stable`.**

**Kết luận consolidation:** ChatGPT bounded delta Review A (Clean) và Independent Delta Review B (Clean) trên `order.md` v0.2, **0 finding còn lại chưa xử lý** (finding ledger đầy đủ — ba finding qua bounded correction v0.1→v0.2, tại mục baseline dưới đây). Product Owner authorized: "Package 0.2-C6: Consolidated Stable".

## `Consolidated Stable` baseline — Package 0.2-C6

**Exact reviewed artifact baseline (pinned):**

```text
order.md                 v0.2   Draft      blob 94ec87593834362292dc3379068e99ef12d86412
context-map.yaml         v0.18  Draft      blob d87428e9919005a2cd7f7b282c92f710e5aed382
reviewed HEAD:    2c655c18aa976278c9b4f75cbe0b6aae202e5223
```

**Finding ledger — tất cả resolved qua bounded correction (v0.1 → v0.2):**

```text
C6-MAJ-01  — Resolved (thêm supersedes_fact_ref vào OrderCreated.payload, pin direct-predecessor-fact-targeting đối xứng risk.md §10, mười invariant correction lineage, fold algorithm dựng explicit chain)
C6-MAJ-02  — Resolved (OrderFactInvalidated cho phép target OrderSubmissionRequested, invalidate-only, fold algorithm loại trừ request đã invalidate khỏi mọi fold)
C6-MAJ-03  — Resolved (eligible_for_execution_result_processing dùng trọn vẹn eligible_for_new_order_creation, pin chính xác current_status == SUBMISSION_REQUESTED)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** Stream Registry/Input Contract implementation cụ thể; chính sách hết hạn Order cụ thể; lý do WITHDRAWN cụ thể; reference price cho PAPER simulation evidence (chủ động omit — Order không tự tính toán gì); granular exception sub-taxonomy cho `FAILED_BEFORE_CREATION`; individual submission-attempt identity riêng; correction lineage riêng cho `OrderCreationAttempt`; implementation technology cho Execution Intent→Order và Order→Submission recovery. Đây là các mối quan tâm triển khai runtime (Phase 1), KHÔNG phải Domain Contract semantic gap — không mở rộng thành Domain Contract semantic mới.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A: authoring + bounded correction hoàn tất cho phạm vi C6; ChatGPT bounded delta Review A hoàn tất (Clean); Independent Delta Review B hoàn tất (Clean); mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để package kế tiếp (0.2-C7) bắt đầu planning — **không** ngụ ý Product Owner Approval cho `order.md`, **không** ngụ ý Lock, **không** sửa ADR nào, **không** đóng OQ nào, **không** authorize Live, **không** thay đổi Constitution. `order.md` **vẫn giữ `version: "0.2"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte không đổi**; `context-map.yaml` **vẫn giữ `version: "0.18"`, `status: Draft`, byte-for-byte không đổi** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package lifecycle states (pinned tại transaction này):**

```text
Package 0.2-C1:    Consolidated Stable
Package 0.2-C2:    Consolidated Stable
Package 0.2-C3:    Consolidated Stable
Package 0.2-C4:    Consolidated Stable
Package 0.2-C5:    Consolidated Stable
Package 0.2-C6:    Consolidated Stable
Package 0.2-C7:    unauthorized, unauthored
```

**Package 0.2-C7 baseline dependency đã thỏa, eligible cho Product Owner scope authorization — CHƯA bắt đầu, CHƯA author, KHÔNG được authorize bởi transaction này.** OQ-002/OQ-003 vẫn `Open`. Không authorize Live ở bất kỳ hình thức nào. Phase 0.2 vẫn active và chưa hoàn tất. KHÔNG Fill/Position semantics nào được author.

## Package 0.2-C7 — Execution Result, Fill, Position and Replay Integration Foundation `Consolidated Stable`

**Phạm vi C7 (scope tối thiểu, đã Product Owner authorize):** bốn Domain Contract — [`execution-result.md`](./execution-result.md) v0.3 Draft (ExecutionResultComputation + PaperExecutionObservation + ExecutionResultProcessingAttempt + ExecutionResult), [`fill.md`](./fill.md) v0.3 Draft (Fill), [`position.md`](./position.md) v0.3 Draft (Position, derived projection), [`replay-event.md`](./replay-event.md) v0.3 Draft (ReplayStateProjection, integration-only) — bốn context (không đổi từ authoring) CÙNG capability `execution-management` (`execution-result-management`/`fill-management`/`position-management`/`replay-integration`, [`context-map.yaml`](./context-map.yaml) v0.19, không đổi trong toàn bộ C7 — computation identity/PaperExecutionObservation sống trong `execution-result.md`, cùng context, KHÔNG cần registration mới).

**Controlling architecture:** [`order.md`](./order.md) v0.2 Draft §8b (không sửa) + Chapter 8 §8.1.1/§8.2/§8.5 (Locked) + Chapter 7 §7.4 (Locked, Type 2 Projection).

**v0.2 — bounded correction (đóng consolidated Review A + Independent Review B findings, bốn Major):** (1) `C7-MAJ-01` — thêm `PaperExecutionObservation` (entity MỚI) — durable, immutable record của simulation evidence VÀ output; `ExecutionResult` nay CHỈ copy `result_type` từ Observation, KHÔNG tự computation; thứ tự corrected: computation → Observation → Attempt PROCESSED → Result; hai recoverable gap tường minh. (2) `C7-MAJ-02` — Fill economics nay BẮT BUỘC copy CHÍNH XÁC từ Observation (field `execution_observation_id`) — KHÔNG độc lập quan sát/recompute, kể cả khi recovery. (3) `C7-MAJ-03` — loại bỏ hoàn toàn ngôn ngữ "cặp bắt buộc"/"atomic-adjacent" giữa ExecutionResult và Fill correction — thay bằng continuing eligibility rule `eligible_as_position_contributing_fill` (fill.md §6) đánh giá LIÊN TỤC tại mọi cursor, KHÔNG phụ thuộc thời điểm cleanup. (4) `C7-MAJ-04` — Position projection nay có `projection_status ∈ {EVALUABLE, NON_EVALUABLE}` (position.md §1/§2) — khi > 1 eligible Fill lineage cùng Position key, projection trả `NON_EVALUABLE`/`UNSUPPORTED_MULTIPLE_FILL_LINEAGES` VÀ `contributing_fill_refs`, KHÔNG silently chọn/aggregate/report FLAT sai.

**v0.3 — second bounded correction (đóng `C7-DELTA-MAJ-01`, consolidated Review A + Independent Review B findings trên baseline v0.2):** logical computation key cũ `(submission_request_id, observation_cursor)` KHÔNG authoritatively phân biệt được initial computation / authorized correction computation / illegal rerun tại cursor mới / orphan Observation chờ Attempt. Thêm `ExecutionResultComputation` (entity MỚI, execution-result.md §2) + `ExecutionResultComputationAuthorized` (event MỚI, §5) — identity authoritative đại diện ĐÚNG MỘT authorized computation lifecycle, `computation_purpose ∈ {INITIAL, CORRECTION}`. INITIAL: tối đa MỘT computation cho mỗi `submission_request_id`, BẤT KỂ cursor. CORRECTION: bắt buộc `predecessor_execution_result_ref` + `correction_authorization_ref`, tối đa MỘT trực tiếp cho mỗi predecessor — cấm fork. `PaperExecutionObservation` logical identity nay = `execution_result_computation_id` (KHÔNG còn cursor-compound key). Thứ tự corrected: `ExecutionResultComputationAuthorized` → computation hoàn tất → Observation → Attempt PROCESSED → Result. `fill.md`/`position.md` chỉ nhận reference-consistency edits (remap `execution-result.md §N` citations theo numbering mới) — KHÔNG semantic change, `C7-MAJ-02`/`C7-MAJ-03`/`C7-MAJ-04` KHÔNG reopen. `replay-event.md` v0.3: `ReplayState(C)` fold thêm `execution_result_computation_lineage`, mười hai cursor mốc (C0–C11, thay mười mốc cũ).

**ExecutionResult/ExecutionResultComputation/PaperExecutionObservation — tóm tắt (v0.3):** `execution_result_computation_id` (opaque, immutable, `computation_purpose ∈ {INITIAL, CORRECTION}`) — identity authoritative cho authorization/idempotency. `execution_observation_id` (opaque, immutable, logical identity = `execution_result_computation_id`) — durable evidence (bốn trục: policy/configuration/build/deterministic-input refs) + output (`result_type`, `executed_quantity`, `execution_price`). `execution_result_id` (logical result key = `submission_request_id`, không đổi xuyên suốt C7) — `result_type` COPY CHÍNH XÁC từ Observation.

**Fill — tóm tắt (v0.3, KHÔNG semantic change từ v0.2):** `fill_id` (opaque, immutable). Logical Fill key = `execution_result_id`. Economics (`fill_quantity`/`fill_price`/`price_currency`/`quantity_unit`) BẮT BUỘC = Observation economics CHÍNH XÁC, qua `execution_observation_id`. `eligible_as_position_contributing_fill(fill_id, C)` (§6) — continuing cursor-bound validity rule, nguồn sự thật DUY NHẤT cho Position, KHÔNG `FillCurrentView`.

**Position — tóm tắt (v0.3, KHÔNG semantic change từ v0.2):** PROJECTION deterministic dẫn xuất từ `eligible_as_position_contributing_fill`. `projection_status ∈ {EVALUABLE, NON_EVALUABLE}` — zero eligible Fill → EVALUABLE FLAT; một → EVALUABLE LONG/SHORT; nhiều → NON_EVALUABLE, `UNSUPPORTED_MULTIPLE_FILL_LINEAGES`, `contributing_fill_refs` đầy đủ.

**Replay Integration — tóm tắt (v0.3):** `ReplayState(C)` fold `execution_result_computation_lineage` + `paper_execution_observation_lineage` + `fill_continuing_eligibility` (tách biệt khỏi Fill stream riêng) + `derived_position` (phản ánh `projection_status`). Mười hai cursor mốc (C0–C11) — bao gồm "sau computation authorization"/"sau correction computation authorized" (minh chứng `C7-DELTA-MAJ-01`), "Result invalidation TRƯỚC Fill invalidation" (minh chứng `C7-MAJ-03`), "nhiều eligible Fill lineage" (minh chứng `C7-MAJ-04`).

**Deferred limitations (Phase 1 implementation concern, non-blocking):** Stream Registry/Input Contract implementation cụ thể; cơ chế/thuật toán PAPER simulation cụ thể; granular exception sub-taxonomy; correction lineage riêng cho `ExecutionResultComputation`/Attempt/Observation (append-only đủ — correction dùng computation identity MỚI thay vì sửa fact cũ); partial-fill semantics (deferred hoàn toàn); multiple-Fill-per-Position-key aggregation formula (deferred — formally trả `NON_EVALUABLE` thay vì silently sai); Position cache/materialization cụ thể; implementation technology cho mọi recovery gap; replay execution technology cụ thể.

**Trạng thái review:**

- Author self-review (authoring, v0.1): **hoàn tất.**
- ChatGPT Review A + Independent Review B (baseline v0.1): **hoàn tất** — bốn Major finding (`C7-MAJ-01`..`C7-MAJ-04`) consolidated.
- Bounded correction commit (v0.1 → v0.2), Product Owner authorized: **hoàn tất** — đóng toàn bộ bốn finding.
- ChatGPT bounded delta Review A + Independent Review B delta review (trên v0.2): **hoàn tất** — một Major finding delta (`C7-DELTA-MAJ-01`, computation identity binding) consolidated.
- Second bounded correction commit (v0.2 → v0.3), Product Owner authorized: **hoàn tất** — đóng `C7-DELTA-MAJ-01`.
- ChatGPT second bounded delta Review A (trên v0.3): **Clean** — 0 blocking finding.
- Independent second bounded delta Review B (trên v0.3): **Clean** — 0 blocking finding.
- Consolidation: **hoàn tất (transaction này)** — Product Owner authorized: "Package 0.2-C7: Consolidated Stable". **Package 0.2-C7 nay `Consolidated Stable`.**

**Kết luận consolidation:** ChatGPT second bounded delta Review A (Clean) và Independent second bounded delta Review B (Clean) trên `execution-result.md`/`replay-event.md`/`fill.md`/`position.md` v0.3, **0 finding còn lại chưa xử lý** (finding ledger đầy đủ — bốn finding qua bounded correction v0.1→v0.2, một finding qua second bounded correction v0.2→v0.3 — tại mục baseline dưới đây). Product Owner authorized: "Package 0.2-C7: Consolidated Stable".

## `Consolidated Stable` baseline — Package 0.2-C7

**Exact reviewed artifact baseline (pinned):**

```text
execution-result.md      v0.3   Draft      blob e5cbb0ee3e3b9083920c03318e3f0dd726247304
fill.md                   v0.3   Draft      blob a4a2c473086ef8495c4106b75d632a7af09ae3fc
position.md                v0.3   Draft      blob 808a3e6041af7a5521094318924fa3682be9cefa
replay-event.md            v0.3   Draft      blob f429d31c0f8ec42e2859f5658edd8a3dedf58b64
context-map.yaml          v0.19  Draft      (unchanged toàn bộ C7)
reviewed HEAD:    c671b987aedc1f4ac9d74597a1c111ae0c98683e
```

**Finding ledger — tất cả resolved qua bounded correction (v0.1 → v0.2) và second bounded correction (v0.2 → v0.3):**

```text
C7-MAJ-01        — Resolved (PaperExecutionObservation entity mới, durable simulation evidence + output, corrected ordering, v0.2)
C7-MAJ-02        — Resolved (Fill economics bắt buộc copy chính xác từ Observation, v0.2)
C7-MAJ-03        — Resolved (eligible_as_position_contributing_fill continuing eligibility rule, thay ngôn ngữ "cặp bắt buộc", v0.2)
C7-MAJ-04        — Resolved (Position projection_status EVALUABLE/NON_EVALUABLE, UNSUPPORTED_MULTIPLE_FILL_LINEAGES, v0.2)
C7-DELTA-MAJ-01  — Resolved (ExecutionResultComputation entity mới, computation identity thay cursor làm điểm neo authorization/idempotency, v0.3)
```

**Final totals:** Blocker 0, Major 0, Minor 0, Suggestion 0.

**Deferred limitations (Phase 1 implementation concern, non-blocking):** Stream Registry/Input Contract implementation cụ thể; cơ chế/thuật toán PAPER simulation cụ thể; granular exception sub-taxonomy; correction lineage riêng cho `ExecutionResultComputation`/Attempt/Observation (append-only đủ); partial-fill semantics (deferred hoàn toàn); multiple-Fill-per-Position-key aggregation formula (deferred); Position cache/materialization cụ thể; implementation technology cho mọi recovery gap; replay execution technology cụ thể. Đây là các mối quan tâm triển khai runtime (Phase 1), KHÔNG phải Domain Contract semantic gap — không mở rộng thành Domain Contract semantic mới.

**`Consolidated Stable` là package lifecycle/readiness state — KHÔNG phải document approval status**, đúng định nghĩa đã khóa ở mục Package 0.2-A: authoring + bounded correction + second bounded correction hoàn tất cho phạm vi C7; ChatGPT second bounded delta Review A hoàn tất (Clean); Independent second bounded delta Review B hoàn tất (Clean); mọi qualifying finding đã xử lý; artifact đã review được pin chính xác; package đủ ổn định để toàn bộ Package 0.2-C (C1–C7) coi là hoàn tất tương đương — **không** ngụ ý Product Owner Approval cho `execution-result.md`/`fill.md`/`position.md`/`replay-event.md`, **không** ngụ ý Lock, **không** sửa ADR nào, **không** đóng OQ-002/OQ-003, **không** authorize Live, **không** thay đổi Constitution, **không** declare Phase 0.2 complete. `execution-result.md`/`replay-event.md`/`fill.md`/`position.md` **vẫn giữ `version: "0.3"`, `status: Draft`, `approved_by: null`, `approved_at: null`, byte-for-byte không đổi**; `context-map.yaml` **vẫn giữ `version: "0.19"`, `status: Draft`, byte-for-byte không đổi** — artifact lifecycle và package lifecycle là hai trục tách biệt.

**Package lifecycle states (pinned tại transaction này):**

```text
Package 0.2-C1:    Consolidated Stable
Package 0.2-C2:    Consolidated Stable
Package 0.2-C3:    Consolidated Stable
Package 0.2-C4:    Consolidated Stable
Package 0.2-C5:    Consolidated Stable
Package 0.2-C6:    Consolidated Stable
Package 0.2-C7:    Consolidated Stable
```

**Package 0.2-C (C1–C7, tổng thể) nay `Consolidated Stable`.** Package 0.2-A/B/C tất cả `Consolidated Stable`.

## Phase 0.2 — Complete (Product Owner decision, 2026-07-31)

```text
Phase 0.2:
  Complete

Completed baseline:
  95fdb01ea662e741fa08f4c2d79727cc13c1a54a

Next active sub-phase:
  Phase 0.3
```

Phase 0: `not Approved`. Phase 1: `not Authorized`. Domain artifacts: remain `Draft`, not Approved, not Locked. OQ-002/OQ-003: remain `Open`. Live: remains `Unauthorized`. `Consolidated Stable`/`Complete` là package/sub-phase lifecycle state — KHÔNG document approval, KHÔNG Phase 0 Approval Gate, KHÔNG Phase 1 authorization.

## Danh sách dự kiến (Package 0.2-A + 0.2-B)

candle.md → swing.md → structure.md → regime.md → feature.md → context.md

## Danh sách dự kiến (Package 0.2-C)

instrument.md → venue.md → account.md → strategy.md → trade-intent.md → decision.md → risk.md → execution-intent.md → order.md → execution-result.md → fill.md → position.md → replay-event.md
