---
id: 09-plugin-model
title: Plugin Model
version: "2.2"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-18"
next_review: null
depends_on: ["02-platform-invariants", "07-module-taxonomy", "08-event-model"]
---

# 9. Plugin Model

## 9.1 Plugin là gì — và thuộc phạm vi Module Taxonomy

**Plugin** là một **extension module**: runtime application component được thêm vào platform sau, có published boundary rõ ràng, và **không** được mặc định trở thành thành phần nội bộ của Decision Pipeline ([I-7](./02-platform-invariants.md)).

### Phạm vi Module Taxonomy — deployable unit, KHÔNG phải runtime instance

[Chapter 7 §7.0](./07-module-taxonomy.md) (Locked) định nghĩa module là *"runtime application component: thành phần có runtime responsibility và published boundary rõ ràng (**deployable** service, process, hoặc in-process component **được vận hành độc lập**)"*.

Áp dụng cho plugin:

| Đối tượng | Có thuộc Module Taxonomy? |
|---|---|
| **Plugin Definition / Package** — deployable/executable implementation unit | **CÓ** — có primary taxonomy type + entry trong `module-registry.yaml` |
| **Strategy Instance** — cấu hình runtime bound vào một deployable unit, KHÔNG được vận hành độc lập | **KHÔNG** — là runtime configuration/execution identity, không phải architecture module |

*Đây là **làm rõ trong phạm vi wording sẵn có** của Ch7 §7.0 (chữ "deployable" và "được vận hành độc lập"), KHÔNG phải định nghĩa lại Chapter 7 đã Locked. Nếu reviewer đánh giá đây là redefinition chứ không phải clarification, thì bắt buộc mở **ADR** sửa Chapter 7 — Chapter 9 không được tự làm.*

**Plugin Definition KHÔNG phải artifact riêng nằm ngoài taxonomy.** Mỗi plugin (ở tầng Definition/Package):
- phải có **một primary taxonomy type** trong 3 loại của Chapter 7 (Compute Engine / Projection / Runtime Service) — Strategy Plugin điển hình là **Compute Engine** (suy diễn domain information thành output, không sở hữu external side effect);
- được đăng ký trong **`/docs/architecture/module-registry.yaml`** cùng mọi module khác ([Chapter 7 §7.5](./07-module-taxonomy.md)).

**KHÔNG tạo plugin registry riêng** — làm vậy sẽ có hai nguồn cho cùng một sự thật "component nào tồn tại và thuộc loại gì" (vi phạm [I-12](./02-platform-invariants.md)).

## 9.2 Plugin tương tác qua published contract

Plugin **chỉ** được tương tác qua **published contract**: versioned event · query/read contract · command contract ([I-7](./02-platform-invariants.md)). Cấm gọi trực tiếp implementation nội bộ hoặc mutable state của module khác; cấm truy cập storage thuộc module khác.

**KHÔNG phát biểu plugin "mặc định là consumer của Event Bus":**
- Về **authority**: [Chapter 8 §8.1](./08-event-model.md) (Locked) khóa rằng transport/broker cụ thể KHÔNG phải source of truth — authority nằm ở durable append-only event log. Nói plugin "consume Event Bus" là mô tả plugin theo **transport**, không theo **contract**.
- Về **phạm vi**: I-7 đã được siết ở Chapter 7 review — không phải plugin nào cũng cần là event consumer; một plugin chỉ cần **query/read contract** là hợp lệ. Ép mọi plugin thành event-bus consumer là ràng buộc thừa.

## 9.3 Ba identity KHÔNG được đồng nhất

`Plugin Definition ≠ Strategy Definition ≠ Strategy Instance`. Đây là ranh giới bắt buộc vì [ADR-010](../adr/ADR-010.md) (Approved) đã khóa evidence của Decision gồm **strategy/model version** *và* **strategy instance** *và* **configuration version** như ba thứ riêng biệt.

| Identity | Bản chất | Thuộc về |
|---|---|---|
| **Plugin Definition / Package** | Implementation extension đã version hóa | Architecture — đăng ký `module-registry.yaml`, có primary taxonomy type (§9.1) |
| **Strategy Definition** | Domain-level strategy semantics/philosophy; tham chiếu plugin implementation version | Domain Contract ([Chapter 4](./04-domain-principles.md)) |
| **Strategy Instance** | Runtime instance đã cấu hình của một Strategy Definition: instance identity · parameters · Input Contract · configuration · lifecycle riêng | Strategy Domain Contract |

**Quy tắc:**
- Một Strategy Definition được thực thi qua **một** Strategy Plugin / canonical implementation đã đăng ký.
- **Một Strategy Plugin phục vụ được NHIỀU Strategy Instance.**
- **Strategy Instance KHÔNG phải module mới** và **KHÔNG tạo `module-registry` entry mới** chỉ vì khác parameters.

*Vì sao bắt buộc tách:* nếu "mỗi strategy = một plugin", thì `BTC-15m-conservative`, `BTC-1h-aggressive`, `ETH-15m-paper` — cùng dùng `ride-strategy-negation v2.1` nhưng khác tham số — sẽ thành 3 module riêng, 3 registry entry, 3 plugin version. Architecture registry phình theo runtime instance, và mất khả năng trả lời câu hỏi cơ bản: *"hai instance này có đang dùng cùng một implementation không?"*

### Runtime identity & evidence — Strategy Instance

Vì Strategy Instance nằm ngoài `module-registry` (§9.1), nó vẫn phải có identity/state authority riêng, nếu không [I-1](./02-platform-invariants.md) và [ADR-010](../adr/ADR-010.md) không tái dựng được Decision:

1. **Instance identity ổn định** qua restart/redeploy — không được sinh lại ID mới khi process khởi động lại.
2. **Đổi plugin version hoặc configuration** phải tạo **binding mới hoặc instance version mới** — KHÔNG mutate ngầm một identity đang chạy.
3. **Decision evidence phải resolve chính xác**: `strategy_instance` · `configuration version` · `plugin implementation version` đã dùng lúc tính Decision (ba thứ ADR-010 đã tách riêng).
4. **State transition của instance** (created · activated · paused · stopped · retired) là **authoritative event** trong event log (§9.8), không phải trạng thái ngầm suy từ registry hay config file.

Schema/representation cụ thể thuộc **Strategy Domain Contract**; Constitution khóa yêu cầu.

**Strategy-level philosophy KHÔNG được nâng thành Platform Invariant** — ranh giới đã khóa ở [Chapter 2](./02-platform-invariants.md): triết lý của một chiến lược cụ thể thuộc metadata của chính nó.

**Thẩm quyền schema/format:** thuộc Domain Contract / registry tương ứng, **KHÔNG hardcode tên file hay format trong Constitution** (bài học từ I-2 field list, I-13 state machine, ADR-008).

## 9.4 Decision Advisor — plugin tham gia Decision Pipeline

Một plugin (kể cả AI module) muốn **tham gia Decision Pipeline** phải được khai báo và kiểm soát như **Strategy Plugin hoặc Decision Advisor** (I-7), và khi đó chịu **toàn bộ** ràng buộc đã Locked ở Chapter 8 + ADR-010:

| Ràng buộc | Nguồn |
|---|---|
| Không gọi trực tiếp Exchange API; mọi intent qua Risk Gateway | [I-4](./02-platform-invariants.md) |
| Event Decision phải khai báo `event_class: decision` trong Event Contract | [Ch8 §8.4](./08-event-model.md) |
| Bắt buộc mang `decision_time` (effective axis) — `effective_time` prohibited | [ADR-010](../adr/ADR-010.md) |
| Bắt buộc mang `decision_context_cursor` hợp lệ (đủ 5 field canonical) | [Ch8 §8.5.1](./08-event-model.md) |
| Tuân relational invariants, gồm `cursor.recorded_time ≤ DecisionEvent.recorded_time` | [Ch8 §8.5.2](./08-event-model.md) |
| Append-and-Revalidate khi có registry transition | [ADR-010 §2.6](../adr/ADR-010.md) |

**Không có ngoại lệ cho AI module.** Việc một plugin dùng mô hình học máy không thay đổi bất kỳ ràng buộc nào ở trên — [I-1](./02-platform-invariants.md) vẫn yêu cầu decision tái dựng được từ immutable evidence (gồm model/strategy version, configuration version).

## 9.5 Decision-time visibility — áp cho MỌI plugin sinh authoritative output

*Mục này KHÔNG chỉ áp cho Decision Advisor.* Bất kỳ plugin nào sinh ra authoritative output tham gia decision-relevant path — Strategy Plugin · Feature/Signal plugin · Risk-context plugin · plugin sinh input cho Decision — đều phải tuân, vì [I-3](./02-platform-invariants.md) chống look-ahead ở **mọi** compute path, không riêng bước cuối.

`Published contract compliance ≠ Decision-time visibility compliance`. Một query hoàn toàn hợp lệ theo I-7 vẫn có thể phá [I-2](./02-platform-invariants.md)/[I-3](./02-platform-invariants.md)/[I-5](./02-platform-invariants.md) nếu nó trả về "current state" không bị giới hạn bởi cursor:

```
1. Cursor pin frontier 1000
2. Plugin gọi query PositionProjection.getCurrentExposure()
3. Projection đã xử lý tới frontier 1010
4. Plugin tạo Decision nhưng attach cursor 1000
→ schema hợp lệ, nhưng Decision đã đọc state TỪ TƯƠNG LAI so với cursor
```

**Decision Advisor KHÔNG được đọc ambient/current mutable state.** Mọi event/query/read dependency dùng để tạo Decision phải:
1. được khai báo trong **Input Contract** hoặc một immutable decision-dependency contract;
2. được resolve **tại hoặc trước** `decision_context_cursor`;
3. **pin projection implementation version/schema/configuration** khi đọc derived state ([Chapter 7 §7.4](./07-module-taxonomy.md) — projection rebuild cần pin đủ);
4. có evidence đủ để **Replay tái tạo đúng snapshot đã đọc** (I-5: Replay không gọi lại mutable source).

**Query/read contract tham gia Decision Pipeline phải hỗ trợ cursor-bounded hoặc snapshot-bounded semantics.** Query không chứng minh được knowledge boundary → **cấm dùng để tạo authoritative Decision**.

Với projection dùng cho Decision: kết quả phải chỉ ra **source frontier/cursor · projection version/schema/config · freshness/criticality state**; **cấm lấy "latest" ngầm**.


## 9.6 Plugin Contract — nhóm thông tin bắt buộc khai báo

Chapter 9 sở hữu **sự tồn tại và ý nghĩa** của các nhóm khai báo dưới đây; [Chapter 10](./10-compatibility-capability-contract.md) sở hữu **thuật toán compatibility** trên chúng. Không có các nhóm này thì các kiểm tra mà [I-7 Verification](./02-platform-invariants.md) đã khóa (network ACL · authorization scope · event schema compatibility · command authorization · capability declaration) **không thực hiện được**.

| Nhóm | Ý nghĩa |
|---|---|
| **Identity** | plugin id · kind · implementation reference · primary module type (§9.1) |
| **Contract surface** | published inputs / outputs — event, query/read, command contract mà plugin dùng và phát (§9.2) |
| **Permission boundary** | quyền plugin được cấp; không được vượt (xem phân tầng bên dưới) |
| **Decision participation** | plugin có tham gia Decision Pipeline không — quyết định việc áp §9.4 |
| **Lifecycle class** | plugin thuộc lớp lifecycle nào (§9.8) |
| **Required capabilities** | capability plugin đòi hỏi từ platform — Chapter 10 khớp |

Schema/format cụ thể thuộc registry/Domain Contract, không hardcode ở Constitution.

**Permission boundary — phân tầng thẩm quyền** (nếu chỉ khai báo mà không có enforcement/verification thì đây chỉ là mô tả, không phải ranh giới an toàn):

| Tầng | Thuộc về |
|---|---|
| **Declaration** — quyền plugin *yêu cầu* | Plugin Contract; đăng ký cùng plugin identity (§9.1) |
| **Grant** — quyền plugin *thực sự được cấp* | Deployment/authorization configuration, versioned; **không** suy từ declaration (plugin không tự cấp quyền cho mình) |
| **Enforcement (runtime)** — chặn khi vượt quyền | Runtime authority tương ứng: Risk Gateway với execution intent ([I-4](./02-platform-invariants.md)) · Exchange Adapter/Signing Service với credential ([I-11](./02-platform-invariants.md)) · contract/API authorization với query & command |
| **Verification** — chứng minh không bypass | Đúng bộ kiểm đã khóa ở [I-7 Verification](./02-platform-invariants.md): network ACL · API authorization scope · event schema compatibility · command authorization · capability declaration · không truy cập storage module khác |

**Ràng buộc bắt buộc:** `granted ⊆ declared`; plugin vượt quyền là **integrity violation** → fail-safe theo [I-6](./02-platform-invariants.md). **Plugin KHÔNG bao giờ được cấp quyền truy cập trực tiếp exchange credential** — I-11 (Locked) giới hạn quyền đó cho Exchange Adapter/Custody-Signing Service, không có ngoại lệ cho plugin.

## 9.7 Versioning & compatibility — thuộc Chapter 10

Mỗi plugin có version độc lập với platform version; cập nhật một plugin không ảnh hưởng plugin khác.

**Quy tắc versioning/compatibility cụ thể** (SemVer, `schemaVersion`, capability declaration, Capability Matrix, hành vi khi không khớp) **thuộc [Chapter 10](./10-compatibility-capability-contract.md)** — Chapter 9 chỉ tuyên bố *tính độc lập*, không định nghĩa lại cơ chế. *(Lưu ý dependency: Chapter 10 khai báo `depends_on: [09-plugin-model]`, nên Chapter 9 KHÔNG được tham chiếu ngược vào chi tiết của Chapter 10 để tránh vòng.)*

## 9.8 Lifecycle — tách architecture identity khỏi runtime state

**Phân chia thẩm quyền (mỗi loại sự thật một nguồn — [I-12](./02-platform-invariants.md)):**

| Loại sự thật | Authority |
|---|---|
| Plugin/module identity · taxonomy type · capabilities/responsibilities · implementation reference | `module-registry.yaml` ([Chapter 7 §7.5](./07-module-taxonomy.md)) |
| Installable version · immutable content identity · compatibility declaration | Artifact version/package reference — nếu được event hoặc cursor tham chiếu thì phải thỏa **Referenced Authoritative Artifact rules** ([Chapter 8 §8.1.1](./08-event-model.md)) |
| **Runtime lifecycle facts** — installed/deployed · instance created · activated/paused/deactivated · promoted/rolled back · retired | **Authoritative event log** ([I-12](./02-platform-invariants.md): runtime facts → event log) |
| Strategy Instance state | Strategy Domain Contract |

**`module-registry.yaml` KHÔNG phải nguồn runtime truth** cho "plugin nào đang active tại thời điểm nào" — suy trạng thái runtime từ registry status là vi phạm I-12.

## 9.9 Forbidden patterns — bảng đối chiếu nhanh

| Pattern | Vi phạm |
|---|---|
| Plugin gọi trực tiếp Exchange API | [I-4](./02-platform-invariants.md) |
| Plugin đọc trực tiếp database/storage của module khác | [I-7](./02-platform-invariants.md) |
| Plugin đọc "current/latest state" không bị cursor ràng buộc khi tạo authoritative output | [I-2](./02-platform-invariants.md)/[I-3](./02-platform-invariants.md)/[I-5](./02-platform-invariants.md) (§9.5) |
| Plugin được cấp quyền dùng exchange credential trực tiếp | [I-11](./02-platform-invariants.md) (§9.6) |
| Tạo `module-registry` entry mới cho mỗi Strategy Instance | §9.1, §9.3 |
| Mutate ngầm plugin version/config của một instance đang chạy | §9.3 (phải tạo binding/version mới) |
| Suy trạng thái runtime của plugin từ `module-registry` status | [I-12](./02-platform-invariants.md) (§9.8) |
| Bắt mở ADR cho mọi activate/pause instance | §9.10 (operational action, không phải architecture change) |
| Nâng strategy-level philosophy thành Platform Invariant | [Chapter 2](./02-platform-invariants.md), §9.3 |

## 9.10 Khi nào cần ADR — tách architecture change khỏi operational action

**ADR Required** ([Governance §4b](./00-governance.md)):
- thêm một plugin **type/capability mới**;
- thay đổi **published contract**;
- thay đổi **module dependency graph**;
- thay đổi **Decision Pipeline topology**;
- thay đổi **authority/permission model**;
- thay đổi **lifecycle semantics** khó đảo ngược.

**KHÔNG mặc định cần ADR** (là operational action, đi qua lifecycle/quality/approval gate tương ứng):
- tạo một Strategy Instance từ plugin **đã approved**;
- activate / pause / stop instance theo lifecycle đã khóa;
- promote / rollback version theo deployment policy **đã approved**;
- operational disable do **kill switch / fail-safe** ([I-6](./02-platform-invariants.md), [I-8](./02-platform-invariants.md));
- uninstall version không còn reference và thỏa retention policy.

*Vì sao phải tách:* Strategy Plugin mặc định tham gia Decision Pipeline, nên câu "activation ảnh hưởng Decision Pipeline → ADR Required" sẽ biến **bật/tắt một strategy instance** thành thủ tục mở ADR — không vận hành được. Governance chỉ đòi ADR cho **architecture decision**, không phải mọi runtime operation.

**Không giải quyết ngầm OQ-002:** Strategy Lifecycle Gate (Backtest=YES + Paper=YES trước khi lên Live) vẫn `Open` và thuộc **Quality Gates/Strategy Lifecycle** — Chapter 9 KHÔNG được đóng nó bằng cách tuyên bố "mọi activation cần ADR".

**Ràng buộc bảo toàn evidence:** thay đổi version hoặc trạng thái của một plugin đang tham gia Decision Pipeline **không được làm mất evidence của Decision đã tính** — Decision đã tồn tại vẫn phải tái dựng được với đúng plugin version đã dùng ([I-1](./02-platform-invariants.md)). Protocol cụ thể (drain, activation boundary, in-flight handling) thuộc **Phase 1 design spec**.
