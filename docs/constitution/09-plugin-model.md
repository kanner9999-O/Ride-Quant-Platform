---
id: 09-plugin-model
title: Plugin Model
version: "2.9"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-24"
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
| **Plugin Definition** — logical extension identity, taxonomy type + trách nhiệm (xem 4 tầng bên dưới) | **CÓ** — có primary taxonomy type + entry trong `module-registry.yaml` |
| **Strategy Instance (hosted)** — cấu hình runtime bound vào một deployable unit, chạy **bên trong** Strategy Engine, không có deploy/restart/scale/published-boundary riêng | **KHÔNG** — là runtime configuration/execution identity, không phải architecture module; không tạo `module-registry` entry |
| **Strategy Instance (independently operated)** — có process/pod riêng, deploy/restart/scale riêng, health/failure boundary riêng | **Bản thân instance: KHÔNG.** Instance, dù được deploy độc lập, **không tự tạo `module-registry` entry** chỉ vì có deployment/scale riêng. Nếu việc deploy độc lập đó tạo ra một **runtime module type/definition mới** với published responsibility riêng (ví dụ `strategy-plugin-runtime`), thì **module type đó** — không phải từng instance — có entry trong `module-registry.yaml`. `strategy_instance_id` luôn khác `module_id`; identity/lifecycle của instance luôn authoritative trong **event log** (§9.8), bất kể hosted hay independently operated |

*Đây là **làm rõ trong phạm vi wording sẵn có** của Ch7 §7.0 (chữ "deployable" và "được vận hành độc lập"), KHÔNG phải định nghĩa lại Chapter 7 đã Locked. Nếu reviewer đánh giá đây là redefinition chứ không phải clarification, thì bắt buộc mở **ADR** sửa Chapter 7 — Chapter 9 không được tự làm.*

**Nguyên tắc phân loại:** `Strategy Instance identity ≠ Module identity` trong **mọi** trường hợp, kể cả khi instance được vận hành độc lập. Registry chỉ sở hữu **registered module type/definition** — **không bao giờ** sở hữu runtime instance fact ([I-12](./02-platform-invariants.md), [§9.8](#98-lifecycle--tách-architecture-identity-khỏi-runtime-state)). Một module type có thể host/deploy **nhiều** Strategy Instance độc lập với nhau; tạo thêm hoặc retire instance là **operational action** ghi nhận trong event log, **không** phải architecture registry change và **không** cần sửa `module-registry.yaml`. Chỉ khi kiến trúc thật sự tạo ra một **module type mới** có published boundary/responsibility riêng (không chỉ một deployment/instance mới của module type đã có) mới cần thêm entry `module-registry` — đó là architecture change, thuộc diện **ADR Required** nếu là type/capability mới (§9.10).

**Plugin Definition KHÔNG phải artifact riêng nằm ngoài taxonomy.** Mỗi **Plugin Definition**:
- phải có **một primary taxonomy type** trong 3 loại của Chapter 7 (Compute Engine / Projection / Runtime Service) — Strategy Plugin điển hình là **Compute Engine** (suy diễn domain information thành output, không sở hữu external side effect);
- được đăng ký trong **`/docs/architecture/module-registry.yaml`** cùng mọi module khác ([Chapter 7 §7.5](./07-module-taxonomy.md)).

**KHÔNG tạo plugin registry riêng** — làm vậy sẽ có hai nguồn cho cùng một sự thật "component nào tồn tại và thuộc loại gì" (vi phạm [I-12](./02-platform-invariants.md)).

### Bốn tầng identity trong "Plugin" — không được gộp

"Plugin" không phải một identity phẳng. Bốn tầng sau phải tách rõ, kể cả khi cùng nằm dưới một taxonomy entry:

| Tầng | Bản chất | Ổn định qua |
|---|---|---|
| **Plugin Definition** | Stable logical identity + taxonomy type + trách nhiệm (bảng trên) | Toàn bộ vòng đời plugin |
| **Plugin Version** | Immutable semantic implementation release (SemVer) | Một release |
| **Package / Build Artifact** | Immutable executable bytes + content identity (content hash); có thể **nhiều** artifact/platform cho cùng một Plugin Version | Một build |
| **Plugin Runtime** | Deployment/process/replica identity đang chạy | Một deployment instance |

`module-registry.yaml` đăng ký **Plugin Definition** (logical identity, taxonomy type) — không đăng ký binary hay replica. **Decision evidence phải pin rõ Plugin Version** dùng để tạo Decision; không được lẫn với content hash của Package/Build Artifact hay với Plugin Runtime replica cụ thể đã xử lý request. Promote/rollback ([§9.8](#98-lifecycle--tách-architecture-identity-khỏi-runtime-state), [§9.10](#910-khi-nào-cần-adr--tách-architecture-change-khỏi-operational-action)) phải nói rõ tác động ở tầng nào: đổi **Plugin Version** là contract-relevant (có thể ADR Required nếu đổi published contract); chuyển **Plugin Runtime** sang replica khác là operational (không ADR).

**Pin Plugin Version là CẦN, chưa ĐỦ để tái dựng exact implementation đã chạy.** Một Plugin Version có thể có nhiều Package/Build Artifact (theo target platform, hoặc do rebuild), mỗi artifact có content hash riêng. Nếu Decision evidence chỉ biết Plugin Version, Replay không trả lời được: artifact nào thực sự xử lý Decision, platform nào, build nào, checksum nào phải materialize để verify. **Plugin Version ≠ Build Artifact, nhưng reference một mình Plugin Version không đủ nếu nó không resolve duy nhất tới exact artifact đã chạy.**

**Bắt buộc:** Decision evidence phải pin Plugin Version **đồng thời** truy được một cách bất biến tới exact Package/Build Artifact hoặc immutable release manifest đã exact-pin — gồm artifact content identity/checksum, target platform/runtime, build identity, và dependency/runtime environment cần thiết cho deterministic replay ([Chapter 8 §8.1.1](./08-event-model.md): referenced authoritative artifact phải có immutable content identity và persistently resolvable). Hai mô hình hợp lệ, không hardcode schema:
- **Mô hình A — Decision pin trực tiếp artifact:** `plugin_definition_id` · `plugin_version` · `artifact_content_hash`.
- **Mô hình B — Version manifest bất biến:** `plugin_version` trỏ tới một **immutable release manifest** exact-pin artifact theo từng target platform; Decision/run evidence phải pin đủ target/runtime discriminator để resolve duy nhất qua manifest đó.

Schema cụ thể thuộc registry/Domain Contract; Chapter 9 chỉ khóa yêu cầu resolvability.

## 9.2 Plugin tương tác qua published contract

Plugin **chỉ** được tương tác qua **published contract**: versioned event · query/read contract · command contract ([I-7](./02-platform-invariants.md)). Cấm gọi trực tiếp implementation nội bộ hoặc mutable state của module khác; cấm truy cập storage thuộc module khác.

**KHÔNG phát biểu plugin "mặc định là consumer của Event Bus":**
- Về **authority**: [Chapter 8 §8.1](./08-event-model.md) (Locked) khóa rằng transport/broker cụ thể KHÔNG phải source of truth — authority nằm ở durable append-only event log. Nói plugin "consume Event Bus" là mô tả plugin theo **transport**, không theo **contract**.
- Về **phạm vi**: I-7 đã được siết ở Chapter 7 review — không phải plugin nào cũng cần là event consumer; một plugin chỉ cần **query/read contract** là hợp lệ. Ép mọi plugin thành event-bus consumer là ràng buộc thừa.

## 9.3 Ba identity KHÔNG được đồng nhất

`Plugin Definition ≠ Strategy Definition ≠ Strategy Instance`. Đây là ranh giới bắt buộc vì [ADR-010](../adr/ADR-010.md) (Approved) đã khóa evidence của Decision gồm **strategy/model version** *và* **strategy instance** *và* **configuration version** như ba thứ riêng biệt.

| Identity | Bản chất | Thuộc về |
|---|---|---|
| **Plugin Definition** | Logical extension identity, taxonomy type + trách nhiệm (4 tầng đầy đủ ở [§9.1](#91-plugin-là-gì--và-thuộc-phạm-vi-module-taxonomy)) | Architecture — đăng ký `module-registry.yaml`, có primary taxonomy type (§9.1) |
| **Strategy Definition** | Domain-level strategy semantics/philosophy; tham chiếu **Plugin Version** (§9.1) của implementation nó dùng | Domain Contract ([Chapter 4](./04-domain-principles.md)) |
| **Strategy Instance** | Runtime instance đã cấu hình của một Strategy Definition: instance identity · parameters · Input Contract · configuration · lifecycle riêng | Strategy Domain Contract |

*`Package/Build Artifact` và `Plugin Runtime` không nằm trong bảng ba-identity này — chúng đã được định nghĩa đầy đủ ở 4 tầng của §9.1 và không phải cấp domain/runtime instance mà bảng này mô tả.*

**Quy tắc:**
- Một Strategy Definition **có thể** có **nhiều** implementation/Plugin Version cùng tồn tại — authoritative · shadow · experimental · migration ([Chapter 3](./03-engineering-principles.md) Locked cho phép các lớp này song song).
- Trong một **authoritative execution/parity scope**, đúng **một** implementation version là authoritative; mỗi Strategy Instance **pin** implementation version cụ thể của nó.
- Shadow/experimental/migration implementation **KHÔNG được** phát sinh authoritative Decision trước khi qua parity validation và promotion. "Canonical" là **authority status trong scope**, không phải cardinality "chỉ được tồn tại một implementation".
- **Một Plugin Version của một Plugin Definition có thể phục vụ nhiều Strategy Instance.**
- **Strategy Instance KHÔNG phải module mới** và **KHÔNG tạo `module-registry` entry mới** — kể cả khi được vận hành độc lập (§9.1: registry sở hữu module type/definition, không bao giờ sở hữu instance fact).

*Vì sao bắt buộc tách:* nếu "mỗi strategy = một plugin", thì `BTC-15m-conservative`, `BTC-1h-aggressive`, `ETH-15m-paper` — cùng dùng `ride-strategy-negation v2.1` nhưng khác tham số — sẽ thành 3 module riêng, 3 registry entry, 3 plugin version. Architecture registry phình theo runtime instance, và mất khả năng trả lời câu hỏi cơ bản: *"hai instance này có đang dùng cùng một implementation không?"*

### Runtime identity & evidence — Strategy Instance

**Strategy Instance identity không được lấy từ `module-registry`** ([§9.1](#91-plugin-là-gì--và-thuộc-phạm-vi-module-taxonomy): registry sở hữu module type/definition — kể cả khi instance được vận hành bởi một module type độc lập, registry **không bao giờ** sở hữu `strategy_instance_id` hay state của instance đó). Vì vậy Strategy Instance vẫn phải có identity/state authority riêng, nếu không [I-1](./02-platform-invariants.md) và [ADR-010](../adr/ADR-010.md) không tái dựng được Decision:

1. **Instance identity ổn định** qua restart/redeploy — không được sinh lại ID mới khi process khởi động lại.
2. **Đổi plugin version hoặc configuration** phải tạo **binding mới hoặc instance version mới** — KHÔNG mutate ngầm một identity đang chạy.
3. **Decision evidence phải resolve chính xác**: `strategy_instance` · `configuration version` · **`Plugin Version`** đã dùng lúc tính Decision (ba thứ ADR-010 đã tách riêng) — **và** đủ để resolve tới exact Package/Build Artifact đã chạy theo yêu cầu ở §9.1.
4. **State transition của instance** (created · activated · paused · stopped · retired) là **authoritative event** trong event log (§9.8), không phải trạng thái ngầm suy từ registry hay config file.

5. **Lifecycle transition KHÔNG được hủy hoặc vô hiệu hóa evidence của Decision đã tính.** Pause/stop/retire một instance là **operational state change**, không phải xóa lịch sử:
   - Decision đã tính vẫn phải **tái dựng được đầy đủ** với đúng instance identity + plugin version + configuration đã dùng ([I-1](./02-platform-invariants.md)).
   - Instance identity **không được tái sử dụng** cho một instance khác sau khi retire ([Chapter 6 §6.1](./06-identity-model.md): ID không tái dùng). Hai điều kiện bắt buộc để rule này thi hành được:
     - **Uniqueness scope phải khai báo tường minh** trong Strategy Domain Contract (global · per-Account · per-Strategy-Definition...) — Ch6 §6.1 cấm mặc định global. Nếu scope hẹp hơn global, mọi reference đi qua boundary phải **qualified** đủ để resolve duy nhất.
     - **Retention/resolvability horizon phải khai báo:** identity đã retire phải resolve được **trong toàn bộ replay/audit horizon platform cam kết** ([Chapter 8 §8.1.1](./08-event-model.md) — persistently resolvable, hết horizon phải có explicit retention/archive policy). Không có horizon thì "không tái dùng" không kiểm chứng được sau vài năm.
   - Nếu retire/stop khiến một Decision đang in-flight không thể hoàn tất đường bình thường, áp **cùng nguyên tắc** với [ADR-010 §2.6](../adr/ADR-010.md) (Approved): ghi immutable preservation/rejection fact mang đủ evidence, **không** xóa hay ghi đè Decision gốc, và **không** cấp execution eligibility.

Schema/representation cụ thể thuộc **Strategy Domain Contract**; Constitution khóa yêu cầu.

**Strategy-level philosophy KHÔNG được nâng thành Platform Invariant** — ranh giới đã khóa ở [Chapter 2](./02-platform-invariants.md): triết lý của một chiến lược cụ thể thuộc metadata của chính nó.

**Thẩm quyền schema/format:** thuộc Domain Contract / registry tương ứng, **KHÔNG hardcode tên file hay format trong Constitution** (bài học từ I-2 field list, I-13 state machine, ADR-008).

## 9.4 Decision Advisor — plugin tham gia Decision Pipeline

Một plugin (kể cả AI module) muốn **tham gia Decision Pipeline** phải được khai báo và kiểm soát như **Strategy Plugin hoặc Decision Advisor** (I-7). Bảng dưới đây **tóm tắt các ràng buộc trực tiếp quan trọng nhất** đã Locked ở Chapter 8 + ADR-010; **không thay thế toàn bộ Chapter 8 và ADR-010**:

| Ràng buộc | Nguồn |
|---|---|
| Không gọi trực tiếp Exchange API; mọi intent qua Risk Gateway | [I-4](./02-platform-invariants.md) |
| Event Decision phải khai báo `event_class: decision` trong Event Contract | [Ch8 §8.4](./08-event-model.md) |
| Bắt buộc mang `decision_time` (effective axis) — `effective_time` prohibited | [ADR-010](../adr/ADR-010.md) |
| Bắt buộc mang `decision_context_cursor` hợp lệ (đủ 5 field canonical) | [Ch8 §8.5.1](./08-event-model.md) |
| Tuân relational invariants, gồm `cursor.recorded_time ≤ DecisionEvent.recorded_time` | [Ch8 §8.5.2](./08-event-model.md) |
| Append-and-Revalidate khi có registry transition | [ADR-010 §2.6](../adr/ADR-010.md) |
| **Decision-time visibility** — mọi input/query phải cursor-bounded, cấm đọc ambient/current state | **§9.5 (bắt buộc, không tùy chọn)** |

**Bảng trên là điều kiện CẦN, chưa ĐỦ:** một Decision Advisor thỏa hết 6 dòng trên nhưng vi phạm §9.5 vẫn phá [I-2](./02-platform-invariants.md)/[I-3](./02-platform-invariants.md) — schema hợp lệ, cursor hợp lệ, nhưng đọc state từ tương lai so với chính cursor nó khai. **§9.5 là ràng buộc bắt buộc của mục này**, không phải khuyến nghị đặt ở nơi khác.

**Không có ngoại lệ cho AI module** — dùng ML/LLM không nới bất kỳ dòng nào ở trên. [I-1](./02-platform-invariants.md) vẫn đòi model/strategy version + configuration version trong evidence.

## 9.5 Decision-time visibility — áp cho plugin trong decision-relevant path

**Phạm vi chính xác:** mục này áp cho **mọi plugin sinh authoritative output nằm trong decision-relevant path** — Strategy Plugin · Feature/Signal plugin · Risk-context plugin · bất kỳ plugin nào sinh input cho Decision. Lý do: [I-3](./02-platform-invariants.md) chống look-ahead ở **mọi** compute path, không riêng bước cuối.

**Ngoài phạm vi:** plugin chỉ sinh output **không** tham gia decision-relevant path (ví dụ reporting/notification thuần túy, observability projection) không chịu ràng buộc cursor-bounded ở mục này.

### Decision-relevance là thuộc tính CONTRACT, không suy ra lúc runtime

Decision-relevance phải là **thuộc tính authoritative được khai báo** trong Plugin Contract (`Decision participation`, §9.6), **KHÔNG** phải thứ suy ra từ việc ai đó tình cờ tiêu thụ output. Nếu để phân loại "theo đường dữ liệu thực tế" thì cùng một plugin, cùng một version, cùng một output sẽ **đổi ràng buộc theo hành vi của consumer** — evidence yêu cầu thay đổi hồi tố, không audit được, và consumer có thể lặng lẽ kéo một plugin chưa đủ điều kiện vào Decision Pipeline.

**Quy tắc bắt buộc:**
- **CẤM** dùng output của một plugin **chưa được khai báo decision-relevant** làm input cho authoritative Decision. Vi phạm là **integrity violation** → fail-safe [I-6](./02-platform-invariants.md), **không** tự động nâng cấp plugin.
- Muốn tái sử dụng output đó cho Decision: phải **promote plugin thành decision-relevant** — đây là **contract change** (versioned). Promote bắt buộc verify đủ 4 điều kiện của §9.5 trước khi có hiệu lực: (1) mọi input/query của plugin cursor-bounded hoặc snapshot-bounded; (2) không đọc ambient/current mutable state; (3) projection version/schema/config được pin khi đọc derived state; (4) evidence đủ để Replay tái tạo đúng snapshot đã đọc (I-5). Đồng thời thuộc diện **ADR Required** nếu đổi Decision Pipeline topology (§9.10).
- **CẤM silent reclassification**: không có đường nào biến một plugin thành decision-relevant mà không qua contract change.
- **Promotion chỉ có hiệu lực tại một explicit, authoritative activation boundary** — không phải ngay khi contract change được ghi. Verify đủ 4 điều kiện ở trên là **precondition**, không phải activation tự thân. Tại boundary đó, một **validated compatibility set** phải đồng bộ atomic, gồm:
  - Plugin Contract version (đã khai báo decision-relevant);
  - Input Contract version (đã pin dependency/output contract mới theo quy tắc subordinate artifact ở trên);
  - published contract references liên quan;
  - permission grant version tương ứng ([§9.6](#96-plugin-contract--nhóm-thông-tin-bắt-buộc-khai-báo));
  - required capability/compatibility result ([Chapter 10](./10-compatibility-capability-contract.md));
  - runtime implementation/deployment version;
  - **exact Package/Build Artifact content identity đã qua parity/compatibility validation** — hoặc, nếu dùng immutable release manifest, **manifest version/content identity + target platform/runtime discriminator** đủ để resolve duy nhất tới artifact đó ([§9.1](#91-plugin-là-gì--và-thuộc-phạm-vi-module-taxonomy): Plugin Version một mình không đủ để xác định exact artifact).

  **Chỉ trùng Plugin Version là không đủ để activation eligible** — runtime implementation thực tế đang chạy tại boundary phải resolve duy nhất tới đúng artifact đã nằm trong compatibility set được validate; artifact khác (kể cả rebuild cùng Plugin Version) là **mixed-build activation**, không phải cùng một validated snapshot.

  **Trước boundary:** output KHÔNG được dùng cho authoritative Decision, dù Plugin Contract đã tuyên bố decision-relevant. **Sau boundary:** mọi Decision phải pin đúng promoted snapshot ở trên — không được lẫn phần cũ/phần mới, và **exact artifact hash ghi trong Decision evidence phải khớp artifact đã có trong compatibility set được validate** (evidence đúng sau khi chạy không tự chứng minh artifact đó từng được phép hoạt động tại activation — hai việc khác nhau). **Partial promotion hoặc mixed-version/mixed-build activation** (ví dụ: Plugin Contract đã decision-relevant nhưng Input Contract chưa pin dependency mới; consumer đã đọc output trong khi Plugin Contract vẫn khai `decision_participation: false`; hoặc runtime đang chạy artifact khác artifact đã parity-validate dù cùng Plugin Version) → **integrity violation, fail-safe** [I-6](./02-platform-invariants.md).

  Cơ chế fencing/transaction/deployment-coordinator cụ thể cho boundary này có thể **defer sang Phase 1 design spec**; **atomic semantic của boundary phải khóa ngay ở Chapter 9**, không defer.

*Cách hiểu đúng câu "đường dữ liệu thực tế": nó dùng để **phát hiện vi phạm** (một consumer đang kéo output ngoài phạm vi vào Decision), KHÔNG phải để **tự động hợp thức hóa** plugin đó.*

`Published contract compliance ≠ Decision-time visibility compliance`. Một query hoàn toàn hợp lệ theo I-7 vẫn có thể phá [I-2](./02-platform-invariants.md)/[I-3](./02-platform-invariants.md)/[I-5](./02-platform-invariants.md) nếu nó trả về "current state" không bị giới hạn bởi cursor:

```
1. Cursor pin frontier 1000
2. Plugin gọi query PositionProjection.getCurrentExposure()
3. Projection đã xử lý tới frontier 1010
4. Plugin tạo Decision nhưng attach cursor 1000
→ schema hợp lệ, nhưng Decision đã đọc state TỪ TƯƠNG LAI so với cursor
```

**Decision Advisor KHÔNG được đọc ambient/current mutable state.** Mọi event/query/read dependency dùng để tạo Decision phải nằm dưới authority của **Input Contract** mà `decision_context_cursor` pin — **không có authority ngang hàng nào khác**:
1. được khai báo trong **Input Contract**, hoặc trong một **subordinate immutable artifact được chính Input Contract exact-pin** (query/read dependency contract · projection snapshot contract · model/config reference set). Subordinate artifact **không được tự mở rộng input scope**; đổi reference của nó **bắt buộc bump version của Input Contract**;
2. được resolve **tại hoặc trước** `decision_context_cursor`, kể cả khi resolve gián tiếp qua subordinate artifact;
3. **pin projection implementation version/schema/configuration** khi đọc derived state ([Chapter 7 §7.4](./07-module-taxonomy.md) — projection rebuild cần pin đủ);
4. có evidence đủ để **Replay tái tạo đúng snapshot đã đọc** (I-5: Replay không gọi lại mutable source).

**Không tồn tại quan hệ "Input Contract HOẶC decision-dependency contract".** Một dependency contract chỉ có authority nếu nó nằm dưới, và được exact-pin bởi, Input Contract mà cursor pin. Nếu không, nó là **hidden input**: replay từ `decision_context_cursor` chỉ có nghĩa vụ resolve tới Input Contract, dependency contract nằm ngoài exact input scope sẽ không có root path bắt buộc để tái dựng — bất kể nó có immutable hay không. Nếu có nhu cầu thật sự cho nhiều peer input authority, đó là thay đổi mô hình canonical cursor của Chapter 8 và phải qua **ADR** — Chapter 9 không được tự tạo mô hình đó bằng prose.

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

Mỗi plugin có version identity và release lifecycle độc lập với platform version và với plugin khác.

**Independent versioning ≠ zero downstream impact.** Một update vẫn có thể ảnh hưởng dependent consumers qua: event/query/command contract · output semantics · capability · permission · freshness/latency · dependency graph · resource contention. Downstream impact **phải** được đánh giá bằng compatibility/capability/dependency rules của [Chapter 10](./10-compatibility-capability-contract.md) — không được giả định an toàn ngầm chỉ vì versioning độc lập.

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

Bảng này **không tạo authority mới** — mỗi dòng trỏ về enforcement/verification đã tồn tại. Pattern nào chưa có cột phải này thì là *khuyến nghị*, không phải rule thi hành được.

| Pattern | Vi phạm | Phát hiện / chặn bởi |
|---|---|---|
| Plugin gọi trực tiếp Exchange API | [I-4](./02-platform-invariants.md) | I-7 Verification: static dependency scan · network ACL · credential audit; runtime: Risk Gateway (mọi intent phải qua) |
| Plugin đọc trực tiếp database/storage của module khác | [I-7](./02-platform-invariants.md) | I-7 Verification: kiểm truy cập storage module khác · network ACL |
| Plugin đọc "current/latest state" không cursor-bounded khi tạo authoritative output | [I-2](./02-platform-invariants.md)/[I-3](./02-platform-invariants.md)/[I-5](./02-platform-invariants.md) | §9.5: query/read contract phải cursor/snapshot-bounded — query không chứng minh được knowledge boundary bị **từ chối**; I-5 self-contained replay test |
| Plugin được cấp quyền dùng exchange credential trực tiếp | [I-11](./02-platform-invariants.md) | §9.6 Grant layer (`granted ⊆ declared`) · I-11 access-control audit · Exchange Adapter/Signing Service là boundary duy nhất |
| Tạo `module-registry` entry mới cho mỗi Strategy Instance | §9.1, §9.3 | Registry review khi thay đổi `module-registry.yaml` (thuộc diện ADR Required — §9.10) |
| Mutate ngầm plugin version/config của instance đang chạy | §9.3 | §9.3: đổi version/config bắt buộc tạo binding/instance version mới; Decision evidence phải resolve đúng version đã dùng |
| Suy trạng thái runtime của plugin từ `module-registry` status | [I-12](./02-platform-invariants.md) | §9.8: runtime lifecycle facts chỉ authoritative trong event log |

| Nâng strategy-level philosophy thành Platform Invariant | [Chapter 2](./02-platform-invariants.md) | Chapter 2 mở đầu: ranh giới Platform Invariant vs Strategy-level Philosophy |
| Dùng output của plugin **chưa khai báo decision-relevant** làm input cho Decision | §9.5 | §9.6 Decision participation declaration · §9.5: consumer phải kiểm khai báo trước khi dùng làm Decision input |

**Anti-pattern thuộc phạm vi GOVERNANCE (không phải runtime enforcement):**

| Pattern | Vấn đề | Phát hiện bởi |
|---|---|---|
| Bắt mở ADR cho mọi activate/pause instance | Biến operational action thành architecture decision → không vận hành được | **Governance/process review** theo §9.10 + [Governance §4b](./00-governance.md) — đây là lỗi **quy trình**, không có cơ chế runtime nào phát hiện được |

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
