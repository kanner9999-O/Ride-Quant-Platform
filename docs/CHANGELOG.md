# Changelog — Ride Quant Platform Docs

Format dựa theo [Keep a Changelog](https://keepachangelog.com/), áp dụng cho toàn bộ `/docs`.

## [Unreleased] — Chapter 10 v2.4 (ChatGPT review round 4: **0 Blocker · 2 Major · 0 Minor · 0 Suggestion mới**)

Không có phản biện; 2 finding chấp nhận toàn bộ. **0 Blocker lần đầu ở Chapter 10.**

### Fixed — Major 1: authority designation đã version hóa nhưng Compatibility Result chưa pin designation đã dùng
- **Lại là propagation gap** — cùng lớp lỗi với vòng 8 của Chapter 9 (§9.1 khóa exact artifact nhưng §9.5 activation set không pin). v2.3 khóa ở §10.4.3 rằng designation của canonical authority phải version hóa + governance phê duyệt, nhưng §10.4.1 provenance không bắt result pin designation nào đã được dùng. Hệ quả: `T1: designation D1 → authority X trả lời "policy nào active"` · result ghi `policy=compat-v3 · boundary=T1 · eligible=true` · sau đó đổi sang `D2 → authority Y` → audit có thể dùng D2 **tái diễn giải** applicability tại T1, kết luận đổi hồi tố.
- **Sửa §10.4.1:** thêm vào danh sách pin bắt buộc — **canonical authority designation version cho policy identity/version** · **canonical authority designation version cho runtime applicability trong subject scope** · **authoritative applicability/activation fact hoặc frontier đã resolve tại evaluation boundary** (bằng chứng policy thực sự active trong scope lúc đánh giá). Ghi rõ vì sao exact-pin policy artifact là chưa đủ: *"policy content là gì"* và *"policy đó có authority + đang active trong scope lúc đánh giá không"* là **hai fact khác nhau**. Khóa thêm: **designation đổi về sau KHÔNG được làm thay đổi cách diễn giải một Compatibility Result lịch sử**. Bổ sung designation version vào điều kiện invalid-result.

### Fixed — Major 2: Capability Matrix mới là execution-mode readiness matrix, chưa bao phủ capability semantics của chính Chapter 10
- §10.2 đã tách 3 loại capability (Business · Required platform · Provided contract) nhưng §10.8 chỉ ghi execution mode → Matrix không trả lời được subject có năng lực cụ thể nào, năng lực nào declared, năng lực nào validated, requirement nào đang được đáp ứng. Một component có thể `Live = validated` trong khi thiếu `cursor-bounded historical projection` hoặc `multi-venue routing`; provider bỏ một provided capability mà ô `Live = validated` vẫn đứng nguyên — snapshot dù bất biến vẫn quá thô để giải thích readiness.
- **Sửa §10.8:** Matrix có **hai chiều** — **capability assertions** (required platform capability · provided contract capability · business-capability implementation mapping khi liên quan) và **execution-mode readiness** (Backtest · Replay · Paper Trading · Live). **Execution-mode readiness là projection/kết luận dẫn xuất từ capability assertion**, không phải cờ độc lập. Mỗi validated mode readiness phải exact-pin hoặc resolve tới capability requirement set · provider capability set · Compatibility Result/evidence · policy/evaluator/boundary. **`Live = validated` là invalid nếu không resolve được tập capability requirement/provider evidence làm căn cứ.** Mở rộng §10.8.1: rule declared ≠ validated áp cho **cả capability assertion lẫn execution-mode readiness**, không chỉ mode.
- **Vẫn không đóng OQ-002** — chỉ bảo đảm "Live readiness" có nghĩa kỹ thuật đầy đủ trước khi Quality Gate dùng nó.

### Checklist
- Ch10 v2.4 · 16 heading đúng thứ tự §10.1→§10.9 (+ 10.3.1 · 10.4.1→10.4.4 · 10.8.1 · 10.8.2), không mục nào bị nuốt/trùng · **0 tham chiếu §10.x gãy** · **0 cấu trúc peer authority** · version file ↔ MANIFEST đồng bộ.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 5 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 v2.3 (ChatGPT review round 3: **1 Blocker · 1 Major · 0 Minor · 0 Suggestion mới**)

Không có phản biện; 2 finding chấp nhận toàn bộ.

### Fixed — Blocker: Compatibility Policy vẫn có competing authority qua cấu trúc "A hoặc B"
- **Đây là lặp lại đúng lớp lỗi peer authority mà Chapter 9 đã mất hai vòng để loại bỏ** (`Input Contract HOẶC decision-dependency contract`), lần này ở tầng policy. v2.2 ghi identity authority là "Policy Contract **hoặc** registry", và runtime activation thuộc "**event/configuration** authority" — cả hai đều cho phép hai nguồn cùng trả lời một loại sự thật. Hệ quả: `Policy Contract: v3 active` vs `registry: v2 active`, hoặc `event log: POLICY_V3_ACTIVATED` vs `config: active_policy = v2` — evaluator chọn được nguồn thuận lợi, cùng một subject cho ra hai kết luận eligibility trái ngược, phá I-12 và phá chính evaluation provenance vừa khóa ở §10.4.1.
- **Sửa §10.4.3 mục 3-4:** khóa **cardinality**, không chọn technology — mỗi loại policy fact, trong mỗi declared scope, **đúng một canonical authority**. Identity/definition/version: **cấm** tồn tại Contract và registry như hai peer source. Runtime applicability: configuration **có thể** là desired-state input, event log **có thể** là recorded transition, nhưng **chỉ một nguồn là canonical current/historical truth**; nguồn còn lại không được tự tạo competing activation fact. **Designation phải version hóa + governance phê duyệt**; thiếu designation hoặc có nhiều peer authority → **policy reference invalid** → `eligible = false` (I-6), reason ghi *invalid*/*không resolve được*. Mô hình cụ thể defer Phase 1. Cập nhật dòng authority tương ứng ở §10.1.
- **Siết thêm (Claude chủ động, cùng lớp lỗi):** hai chỗ còn dùng "Domain Contract / registry" cho tên capability/schema đã đổi thành "registry/Contract được designate cho **chính loại khai báo đó** — mỗi loại đúng một, không phải lựa chọn giữa nhiều nguồn", để pattern này không tái phát ở vòng sau.

### Fixed — Major: Capability Matrix là input authoritative nhưng chưa có authority, version, provenance
- §10.8 đã pin subject scope tốt, nhưng chưa nói ai sở hữu Matrix, entry là declaration hay validated result, ai được ghi "supports Live", Matrix có version/content identity không, update ghi đè hay tạo version mới, gate pin được snapshot nào. Rule chống self-certification đã áp rất chặt cho Compatibility Result **nhưng chưa áp cho Capability Matrix** — một plugin tự khai `Live = YES` đi thẳng vào input của lifecycle gate mà chưa có evaluator, policy, evidence hay approval.
- **Sửa — thêm §10.8.1:** tách **Declared support** (component tuyên bố thiết kế hỗ trợ mode nào — **không tự tạo eligibility**) khỏi **Validated capability/readiness** (đã đánh giá bằng policy/evidence, mới được dùng làm căn cứ readiness); hai lớp không được gộp trong cùng một ô "supports: yes". Validated entry phải pin: subject identity/version/artifact/config · evaluation policy/result hoặc evidence reference · evaluator/verification authority (quyền đánh giá là **grant**, không tự nhận) · validation boundary/time · immutable matrix version hoặc source frontier.
- **Thêm §10.8.2:** Matrix phải là **versioned resolvable artifact** hoặc **projection của authoritative source đã designate** (nếu projection thì phải chỉ ra source frontier/version như mọi projection dùng cho quyết định — Ch7 §7.4). Update **không được ghi đè lịch sử**; **gate phải pin đúng snapshot đã dùng tại thời điểm đánh giá**, không đọc "matrix hiện tại" (nếu không, kết luận của gate đổi hồi tố theo trạng thái sau này); reference không resolve được về version/frontier cụ thể → không dùng làm input cho gate, xử lý theo §10.4.2.
- **Không đóng OQ-002:** ghi rõ §10.8.1/§10.8.2 chỉ bảo đảm thứ đưa sang lifecycle gate không phải một bảng mutable tự khai; *khi nào* được lên Live vẫn thuộc OQ-002/Quality Gates.

### Checklist (áp bài học v2.2 — grep toàn bộ heading, không chỉ phần vừa thêm)
- Ch10 v2.3 · 16 heading đúng thứ tự §10.1→§10.9 (+ 10.3.1 · 10.4.1→10.4.4 · 10.8.1 · 10.8.2), không mục nào bị nuốt/trùng · **0 tham chiếu §10.x gãy** (10 ref đều tồn tại) · **0 cấu trúc peer authority "A hoặc B"** còn lại · 0 hardcode technology/tên file.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 4 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 v2.2 (ChatGPT review round 2: **1 Blocker · 2 Major · 1 Minor · 0 Suggestion mới**)

Reviewer đã rút lại nhận định sai về metadata Chapter 9 ở vòng trước — repo đã đồng bộ đầy đủ quyết định Lock của Kanner. Không có phản biện nào ở vòng này; 4 finding chấp nhận toàn bộ.

### Fixed — Blocker: Compatibility policy/rule-set được pin nhưng chưa có authority/identity/lifecycle
- v2.1 bắt Compatibility Result pin `compatibility policy/rule-set version` (§10.4.1) nhưng toàn chapter không định nghĩa policy đó là artifact gì, ai sở hữu identity, ai được tạo version, nằm registry nào, có immutable content identity không, version transition thành authoritative bằng cách nào, rule-set nào active cho scope nào. Provenance có **field** nhưng chưa có **gốc**: hai result cùng ghi nhãn `compat-v2` vẫn có thể chạy hai bộ luật khác nhau, và một result có thể tự khai `policy_version` không tồn tại rồi thành vé activation. **Đúng cùng lớp lỗi "pin một thứ chưa được định nghĩa đầy đủ" đã gặp ở v1.0** — lần này ở tầng policy thay vì tầng result.
- **Sửa — thêm §10.4.3:** Compatibility Policy là **versioned immutable authoritative artifact** với 7 yêu cầu: stable logical identity + immutable version/content identity (**exact-pin**, cấm nhãn version tự do) · declared scope (result ngoài scope policy nó viện dẫn = invalid) · identity/definition authority thuộc **Compatibility Policy Contract/registry được governance phê duyệt** (Constitution khóa yêu cầu, không tự tạo registry, không hardcode tên file; ghi rõ **Chapter 10 là luật cấp cao, không tự động trở thành runtime policy artifact**) · runtime activation/applicability là **runtime fact** thuộc event/configuration authority theo I-12 · lifecycle transition authoritative, **cấm mutate nội dung dưới cùng version identity** · historical content immutable + resolvable theo horizon · **evaluator chỉ được dùng policy version đã được grant cho scope đó** (nối tiếp rule chống self-certification). Thêm dòng authority tương ứng vào bảng §10.1. Nêu **phương án thay thế** được chấp nhận: exact-pin version của Chapter 10 + tập format-specific rules, miễn có root path authoritative và machine-resolvable.

### Fixed — Major
- **"Historical Compatibility Result giữ nguyên vĩnh viễn" lệch retention horizon model:** §10.4 chỉ yêu cầu resolvable trong horizon cam kết, còn Chapter 8 dùng mô hình "persistently resolvable trong committed horizon, hết horizon → explicit retention/archive policy". "Không mutate lịch sử" và "giữ object online vô hạn" là hai việc khác nhau; Constitution không nên cam kết infinite retention. **Sửa:** bỏ từ "vĩnh viễn"; thêm **§10.4.4** — result và policy version là immutable (không sửa/ghi đè/hồi tố) · phải resolve trong toàn bộ replay/audit horizon cam kết · sau horizon tuân explicit retention/archive policy · nếu archive thì reference lịch sử vẫn phải có cách xử lý đúng theo policy đã công bố, không được thành dangling reference im lặng.
- **Thiếu compatibility direction chưa được khóa thành hành vi:** §10.3.1 nói "contract phải khai báo chiều bắt buộc; không khai báo thì không suy diễn mặc định" — đúng nguyên tắc nhưng chưa khóa hệ quả, nên mỗi team vẫn tự chọn mặc định riêng (backward / unknown-nhưng-vẫn-cho-minor / invalid). **Sửa:** contract trong phạm vi compatibility evaluation mà không khai báo chiều bắt buộc → **invalid declaration** → không được chứng nhận compatible → `eligible = false` theo I-6, reason ghi *khai báo invalid*/*không đủ policy*, **không** ghi *đã chứng minh không tương thích*. Cho phép contract tuyên bố **tường minh** là không cam kết chiều nào — nhưng phải là declaration, không phải field vắng mặt.

### Fixed — Minor
- **Capability Matrix pin `configuration/profile` nhưng profile name có thể trỏ tới mutable config:** `live-default` hôm nay bật Live, tuần sau cùng profile đó có thể đã đổi → entry không còn resolve đúng snapshot đã đánh giá. **Sửa §10.8:** phải pin **configuration/profile identity + immutable configuration version hoặc content identity**, không chỉ tên profile.

### Fixed — lỗi biên tập nội bộ (Claude tự phát hiện khi verify)
- Khi chèn §10.4.3, thao tác `str_replace` đã **nuốt mất header §10.4.2**, làm phần Reason classification dangling dưới §10.4.4 và sai thứ tự. Phát hiện qua grep header sau khi sửa; đã khôi phục header đúng vị trí (sau §10.4.1, trước §10.4.3) và xóa khối bị nhân đôi. **Bài học quy trình:** sau mỗi lần chèn tiểu mục mới, phải grep lại toàn bộ heading để xác nhận thứ tự và không mất mục — không chỉ kiểm nội dung vừa thêm.

### Checklist
- Ch10 v2.2 · §10.1→§10.9 liên tục · §10.4.1→§10.4.4 đủ 4 tiểu mục, đúng thứ tự, không trùng lặp · **0 tham chiếu §10.x gãy** (§10.4 · 10.4.1 · 10.4.2 · 10.4.3 · 10.4.4 · 10.7 · 10.9 đều tồn tại) · 0 occurrence "vĩnh viễn" · 0 hardcode tên file/registry · Compatibility Policy có authority row trong §10.1.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 3 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 v2.1 (ChatGPT review round 1: **1 Blocker · 3 Major · 1 Minor · 0 Suggestion mới**)

### Note — phản biện một điểm phi kỹ thuật trong review
Review kết luận *"GitHub metadata Chapter 9: vẫn cần atomic transition phản ánh quyết định"*. **Điểm này không đúng với trạng thái repo:** commit `cec4f1e` (trước commit Chapter 10 v2.0) đã thực hiện atomic transition — `09-plugin-model.md` trên `main` hiện là `version: 2.9 · status: Locked · approved_by: Kanner · approved_at: 2026-07-24`, MANIFEST ghi `**Locked**`, CHANGELOG có entry `[Milestone]`. Đã fetch lại remote `main` để xác minh trước khi ghi note này. Reviewer có thể đã đọc snapshot Ch9 cũ hơn `cec4f1e`. Không có hành động nào cần thực hiện thêm cho Chapter 9. **5 finding kỹ thuật còn lại: chấp nhận toàn bộ, không phản biện.**

### Fixed — Blocker: Compatibility Result pin subject nhưng không pin evaluation provenance
- v2.0 yêu cầu result immutable + pin input + kết luận nhị phân, nhưng **không** yêu cầu pin rule-set/evaluator. Cùng một bộ input có thể cho kết luận ngược nhau dưới hai compatibility rule-set khác nhau — result chỉ ghi `inputs + eligible=true` không trả lời được luật nào đã áp, ai đánh giá, người đánh giá có thẩm quyền không, result sinh trước hay sau rule transition. Vì Ch9 §9.5 dùng result này để **mở activation boundary**, thiếu provenance biến nó thành **"vé eligible" tự chứng nhận**.
- **Sửa — thêm §10.4.1:** result phải pin bất biến subject scope · input references · **compatibility policy/rule-set version** · **evaluator module identity** · **evaluator implementation version + exact artifact/manifest** · evaluation time/boundary · result + reason + evidence refs. Result không resolve được evaluator identity/artifact/rule-set/scope thì **không hợp lệ và không được đưa vào validated compatibility set**. Ghi rõ đây cùng nguyên tắc Ch3 §3.1 (Locked): parity phải pin implementation version + configuration + **policy version** + contract, không chỉ pin dữ liệu vào.
- **Chống self-certification:** component đang được đánh giá không mặc định tự cấp eligibility cho chính nó; **registry membership là identity, KHÔNG phải grant** — quyền đánh giá phải qua đúng phân tầng Declaration → Grant → Enforcement → Verification của Ch9 §9.6 với `granted ⊆ declared`. Self-evaluation chỉ hợp lệ khi authorization model cho phép tường minh + có independent verification.

### Fixed — Major
- **Trigger "provider đổi contract/capability mà consumer đang pin" gây revalidation hồi tố:** wording cũ có thể bị đọc thành "provider publish version mới → activation lịch sử phải xét lại", phá immutable reference và independent versioning. **Sửa §10.5:** trigger đúng là **transition của binding/resolution**, không phải sự tồn tại của version mới — consumer đổi pinned reference · active binding resolve sang version/artifact khác · artifact/contract đã pin bị explicit revoke hoặc mất resolvability · permission/capability grant đổi · compatibility policy đổi · runtime đổi exact artifact · startup. Ghi rõ: provider publish version mới **KHÔNG** phải trigger; **historical Compatibility Result giữ nguyên vĩnh viễn**, đánh giá mới sinh result mới cho boundary mới, không hồi tố.
- **Schema compatibility delegation từ Ch8 §8.6 chưa đủ semantic để triển khai nhất quán:** v2.0 chỉ định nghĩa breaking change theo contract surface chung, chưa khóa các trường hợp schema evolution phổ biến — hai team cùng nói "SemVer nghiêm ngặt" vẫn phân loại ngược nhau (thêm required field không default: minor hay major?). **Thêm §10.3.1** semantic độc lập format: định nghĩa backward/forward compatibility và breaking theo **chiều mà contract yêu cầu** · nguyên tắc tối thiểu cho optional/required element, remove/rename/type/nullability/default/đổi ý nghĩa, enum expansion/contraction theo từng chiều, deprecated-rồi-gỡ · hai điều cấm suy diễn: `schema_version` bump không tự chứng minh compatibility, major bump không tự làm thay đổi trở nên an toàn. Rules theo format cụ thể (JSON Schema/Avro/Protobuf) defer Domain Contract/Phase 1.
- **Unknown impact bị ghi thành proved incompatibility:** §10.7 nói không resolve được tập consumer thì "kết quả là incompatible" — đúng về hành vi chặn, sai về semantic, và mâu thuẫn nhẹ với kết luận nhị phân ở §10.4. **Thêm §10.4.2:** eligibility vẫn nhị phân, nhưng **reason classification bắt buộc phân biệt** *đã chứng minh tương thích* · *đã chứng minh không tương thích* · *không đủ evidence* · *khai báo invalid* · *reference không resolve được* · *policy mismatch*. Quy tắc: không chứng minh được tương thích → `eligible = false` (fail-safe I-6) **nhưng không được ghi thành "đã chứng minh không tương thích"** — chặn đúng mà ghi sai lý do là mất explainability (I-1). Sửa §10.7 tương ứng.

### Fixed — Minor
- **Capability Matrix chưa pin version/artifact scope:** v2.0 nói Matrix ghi nhận "với mỗi module/plugin", nhưng capability đổi theo Plugin Version, artifact/target platform và configuration/profile — gắn ở logical level tạo declaration quá rộng. **Sửa §10.8:** mỗi entry phải pin subject identity đủ cụ thể (Definition · **Plugin Version** · artifact/target discriminator khi capability phụ thuộc build/platform · configuration/profile khi phụ thuộc config); **cấm suy capability của mọi version/artifact chỉ từ Plugin Definition** — trái yêu cầu exact-artifact eligibility Ch9 §9.5.

### Đánh giá của reviewer về §10.4/§10.5
Claude nêu lo ngại hai section này có thể lấn Phase 1. Reviewer kết luận §10.4 là **semantic invariant**, đúng chỗ ở Constitution; §10.5 đúng ý tưởng nhưng cần khóa theo **state transition ảnh hưởng binding**, không theo hành động "provider đổi" nói chung — đã sửa đúng hướng đó.

### Checklist
- Ch10 v2.1 · §10.1→§10.9 liên tục (+ §10.3.1 · §10.4.1 · §10.4.2) · **0 tham chiếu §10.x gãy** (§10.4 · §10.4.1 · §10.4.2 · §10.7 đều tồn tại) · 0 hardcode tên/schema · 0 authority mới · historical result bất biến, không hồi tố.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 2 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 10 (Compatibility & Capability Contract) v2.0 — Claude tự review (**2 Blocker · 5 Major · 2 Minor · 1 Suggestion**)

Chapter 10 v1.0 viết 2026-07-16, **trước khi** Chapter 2-9 được Locked, dài 32 dòng — chưa hấp thụ bất kỳ model nào đã khóa từ đó. Self-review đối chiếu toàn bộ Chapter 2/3/4/7/8/9 Locked.

### Fixed — Blocker
- **`compatibility result` là thứ Chapter 9 (Locked) pin nhưng Chapter 10 chưa định nghĩa tồn tại:** Ch9 §9.5 khóa `required capability/compatibility result` là thành phần của validated compatibility set tại activation boundary, nhưng v1.0 chỉ nói "Plugin Loader kiểm tra lúc startup" — kết quả kiểm tra sống trong bộ nhớ, không pin được. Thêm **§10.4**: compatibility result phải bất biến · có content identity + resolvable trong replay/audit horizon (thỏa Referenced Authoritative Artifact rules Ch8 §8.1.1) · pin đủ input đã đánh giá (Plugin Version · exact artifact/manifest + target discriminator · contract refs · capability requirement set · version phía cung cấp) · kết luận nhị phân trong phạm vi đã khai báo, không có trạng thái "một phần" ngầm. Cấm suy lại từ trạng thái runtime; đánh giá lại sinh result mới, không hồi tố hợp thức hóa activation đã xảy ra.
- **Hardcode module/capability name + schema format, tạo authority cạnh tranh với Ch4 và Ch7 (Locked):** khối JSON dùng `StructureEngine` (module identity → thuộc `module-registry.yaml`, Ch7 §7.5) và `SWING_STRENGTH/BOS/CHOCH` (capability/domain concept → Ch4 §4.2 khóa mọi `capability_id` phải tồn tại sẵn trong `context-map.yaml`; Domain Contract còn không được tự đặt). Đây đúng lớp lỗi Ch9 §9.3 đã khóa ("không hardcode tên file hay format trong Constitution" — bài học I-2 field list, I-13 state machine, ADR-008). Xóa toàn bộ khối JSON; thay bằng **§10.1 bảng ranh giới thẩm quyền** trỏ mọi identity về registry sở hữu nó.

### Fixed — Major
- **"capability" bị dùng cho 3 khái niệm khác nhau:** Business Capability (Ch4, có version theo Ch3 §3.1) · Required platform capability (Ch9 §9.6) · Provided contract capability. Gộp phẳng thì so khớp mất nghĩa. Thêm **§10.2** tách 3 loại + authority của từng loại; reference tới capability chưa đăng ký = invalid declaration.
- **`schemaVersion` xung đột Ch8 §8.2.5 (Locked):** Ch8 khóa `schema_version` **không** phải proxy cho Event Contract version, hai trục tiến hóa độc lập; v1.0 gộp thành một trục và viết sai canonical field name. **§10.3** khóa 3 trục độc lập (Event Contract version · `schema_version` · Plugin Version), cấm dùng trục này làm proxy trục kia.
- **SemVer không nói áp cho tầng identity nào:** Ch9 khóa 4 tầng Definition/Version/Artifact/Runtime. **§10.3** khóa SemVer áp cho **Plugin Version**, và định nghĩa breaking change theo **published contract surface** (không theo internal implementation); cấm bump major "cho an toàn" khi contract surface không đổi. Bỏ cách nói "mỗi Engine" (bỏ sót Projection + Runtime Service của Ch7).
- **Dangling delegation — ba chapter Locked trỏ vào khoảng trống:** Ch3 §Engineering Foundation nói SemVer schema/capability "đã có **đầy đủ**" ở Ch10 · Ch8 §8.6 delegate schema versioning/compatibility · Ch9 §9.7 delegate SemVer, capability declaration, Capability Matrix, hành vi khi không khớp **và** downstream impact rules. v1.0 không có định nghĩa breaking change, không có dependency impact rule nào. **§10.1** liệt kê tường minh các delegation nhận được; **§10.6** (hành vi khi không khớp) và **§10.7** (downstream impact assessment) lấp đúng phần còn trống.
- **"Plugin Loader" là authority mới đặt bằng prose:** không thuộc taxonomy nào của Ch7, không có trong registry, nhưng được giao quyền chặn — trái phân tầng Declaration/Grant/Enforcement/Verification đã khóa ở Ch9 §9.6. **§10.1** khóa: Chapter 10 KHÔNG tạo authority mới, Constitution không đặt tên component, enforcement đi qua đúng phân tầng Ch9.

### Fixed — Minor
- **Capability Matrix có nguy cơ đóng ngầm OQ-002:** v1.0 nói Matrix "dùng làm tiêu chí readiness cho production", trong khi Ch9 §9.10 khóa không đóng ngầm OQ-002 (vẫn `Open`, thuộc Quality Gates/Strategy Lifecycle). Danh sách của v1.0 (Replay/Live/Backtest/Multi-Exchange) cũng lệch OQ-002 (Backtest + Paper Trade) và lệch execution mode canonical Ch3 §3.1. **§10.8**: Ch10 sở hữu cấu trúc/semantic của Matrix, execution mode canonical thuộc Ch3 §3.1, Matrix là **input** cho lifecycle gate chứ không phải bản thân gate — "hỗ trợ Live" ≠ "được phép lên Live".
- **`depends_on` thiếu:** chỉ khai `09-plugin-model` dù nội dung chạm trực tiếp Ch2 (I-6, I-7 verification), Ch3 (execution mode, authoritative implementation), Ch4 (capability registry), Ch7 (module registry/taxonomy), Ch8 (schema/contract version). Bổ sung đủ 6, đồng bộ MANIFEST.

### Fixed — Suggestion
- **"fail-fast lúc startup" chưa nối vào I-6:** I-6 (Locked) là fail-safe **theo scope**, phạm vi nhỏ nhất nhưng đủ. **§10.6** diễn đạt lại theo I-6, ghi rõ không mặc định dừng toàn platform vì một plugin không critical, cũng không thu hẹp scope tới mức để ảnh hưởng lan ra ngoài. Thêm: cấm degrade ngầm (tự bỏ capability/hạ version/chạy với subset = mixed-state activation) · mọi từ chối phải để lại evidence resolvable (I-1) · không khớp không tự động là việc cần ADR.

### Added — §10.5 điểm đánh giá bắt buộc
Startup-only là không đủ. Bắt buộc đánh giá tại tối thiểu: đăng ký Plugin Version/artifact mới · **activation boundary** của decision-relevance promotion (Ch9 §9.5) · runtime deployment đổi artifact/target **kể cả rebuild cùng Plugin Version** (nếu không, mixed-build activation mà Ch9 vừa khóa là integrity violation sẽ không có điểm phát hiện) · provider đổi contract/capability mà consumer đang pin · startup.

### Checklist
- Ch10 v2.0 · §10.1→§10.9 liên tục · **0 tham chiếu §10.x gãy** · grep xác nhận 0 hardcode (`StructureEngine` · `SWING_STRENGTH/BOS/CHOCH` · `Plugin Loader` · `schemaVersion`) · mọi link target tồn tại · 0 authority mới được tạo · OQ-002 không bị đóng ngầm.

### Note
- Đây là **self-review của Claude**, chưa qua ChatGPT. Không tự tuyên bố Approve. Chờ ChatGPT review round 1 và Product Owner Approve/Lock.

## [Milestone] — 2026-07-24 — 🔒 Chapter 9 (Plugin Model) LOCKED

**Product Owner (Kanner) xác nhận Approve & Lock** Chapter 9 v2.9, theo khuyến nghị reviewer (ChatGPT round 9: 0 Blocker · 0 Major · 0 Minor · 0 Suggestion, Consolidation Review + Backward Consistency Check toàn bộ Chapter 0-8 đạt).

`status: In Review → Locked` · `approved_by: null → Kanner` · `approved_at: null → 2026-07-24`.

### Quy mô công việc
Chapter 9 trải qua **10 revision** (v2.0 Claude tự review → v2.9), tương ứng **9 vòng review ChatGPT** (round 1-9) sau vòng self-review ban đầu. Các model đã khóa:

- **Identity — 4 tầng tách biệt:** Plugin Definition (logical/taxonomy) ≠ Plugin Version (immutable release) ≠ Package/Build Artifact (immutable bytes + content hash) ≠ Plugin Runtime (deployment/replica); Strategy Definition ≠ Strategy Instance, khớp ba-thứ-tách-riêng của ADR-010 (strategy/model version · instance · configuration version).
- **Module Taxonomy:** registry chỉ sở hữu module type/definition, không bao giờ sở hữu Strategy Instance runtime fact (hosted hay independently operated); `strategy_instance_id ≠ module_id`; lifecycle instance authoritative trong event log (I-12).
- **Strategy cardinality:** một Strategy Definition có thể có nhiều implementation (authoritative/shadow/experimental/migration), đúng một authoritative trong mỗi execution/parity scope — khớp Chapter 3 Locked.
- **Decision input authority:** Input Contract là root authority duy nhất mà `decision_context_cursor` pin; dependency contract chỉ có hiệu lực như subordinate immutable artifact exact-pinned, không còn peer authority/hidden-input path.
- **Decision-relevance promotion:** contract declaration (không suy runtime) · cấm silent reclassification · 4 điều kiện visibility precondition · authoritative atomic activation boundary với validated compatibility set (Plugin Contract version · Input Contract version · published refs · permission grant version · capability result · runtime deployment version · **exact Package/Build Artifact hoặc immutable manifest + target discriminator**) · mixed-version/mixed-build activation = integrity violation, fail-safe I-6.
- **Permission boundary 4 tầng:** Declaration · Grant · Enforcement (runtime) · Verification; `granted ⊆ declared`; plugin không bao giờ được cấp exchange credential trực tiếp (I-11).
- **Versioning:** độc lập với platform/plugin khác nhưng "independent versioning ≠ zero downstream impact" — impact đánh giá qua Chapter 10.
- **Governance/runtime split:** forbidden-pattern table tách rõ phần runtime-enforceable (có cột phát hiện/chặn) khỏi phần thuộc governance/process; ADR Required giới hạn đúng architecture change, không chặn operational action (§9.10).

### Deferred sang Phase 1 design spec
Fencing/transaction mechanism cho activation boundary · deployment coordinator · artifact retention/archive protocol cụ thể · Capability Matrix/compatibility algorithm chi tiết (Chapter 10 sở hữu).

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5, 6, 7, 8, **9** + ADR-005 → ADR-010.

**Next Milestone:** Chapter 10 — Compatibility & Capability Contract.

## [v0.1] — 2026-07-16 (Phase 0, đang tiến hành, chưa release chính thức)

### Added
- Constitution 15 chương (00-governance → 14-roadmap), tách thành docs-as-code.
- Platform Invariants I-1 → I-11.
- Domain Principles, Time Model, Identity Model, Module Taxonomy.
- Event Model, Plugin Model, Compatibility & Capability Contract.
- ADR Process, Approval Gates, Quality Gates, Roadmap.
- MANIFEST.md (lockfile ghim version/status toàn bộ docs).
- ADR-001 (Event Sourcing), ADR-002 (Strategy Isolation), ADR-003 (Regime Engine Split) — ghi hồi tố các quyết định đã chốt qua thảo luận nhưng chưa từng thành file.
- ADR-004 → ADR-005: Governance Model v1 (Tri-party 3/3 + Blocking/Non-blocking + Challenge Round + Devil's Advocate).
- Folder structure: constitution/, adr/, domain/, architecture/, research/, meeting-notes/, templates/.

### Changed
- ADR-005 rev.2: đơn giản hóa Governance sau review của ChatGPT — bỏ luật 3/3 (Product Owner là approve authority duy nhất), bỏ Blocking/Non-blocking (thay bằng Concern/Risk/Recommendation), bỏ Devil's Advocate, gọn Challenge Round thành 1 field "Scale check" trong ADR template thay vì một quy trình riêng.
- Document status enum mở rộng: Not Started → Draft → In Review → Revision Requested → Approved → Locked (+ Deprecated/Superseded), thay cho "Debating".
- Thêm metadata chuẩn cho mọi file: owner, reviewers, approved_by, last_review, next_review.

### Open
- OQ-001: Data Retention Policy & Access Control Model — chưa quyết, cần trước Phase 1.
- Toàn bộ Constitution vẫn ở trạng thái `In Review`, chưa có Approval chính thức từ Product Owner.

## [Unreleased] — sau ChatGPT review round 3 (chuẩn bị Lock Chapter 0)

### Changed
- Tách vai trò **Product Owner** và **Chief Architect** thành 2 role độc lập (trước đó gộp chung) — cho phép delegate Chief Architect cho người khác trong tương lai mà không ảnh hưởng quyền Product Owner.
- Đổi "Architecture Discussion" → "Architecture Review" trong Decision Workflow (chuyên nghiệp hơn, ngụ ý có output/concern/recommendation).
- Decision Workflow: thêm trạng thái "ADR Accepted" trước "ADR Locked" (tách trạng thái quyết định khỏi hành động đóng băng tài liệu).
- `scale_check` template: thêm field `reason_if_no` — bắt buộc điền nếu `decision_still_valid: NO` nhưng vẫn quyết định tiến hành.
- **Single Source of Truth nâng thành Platform Invariant I-12** (trước đó chỉ là một rule trong Governance — tự mâu thuẫn với chính nguyên tắc SSOT nếu định nghĩa nó ở 2 nơi).
- Xóa cụm "Blocking Objection" còn sót trong lý giải của ADR-005 (khái niệm này đã bị loại bỏ khỏi Governance, không nên còn xuất hiện như đang tồn tại).

### Backlog (v1.1, Medium Priority — chưa làm ngay theo đề xuất ChatGPT)
- BL-001: `review_status` machine-readable trong metadata.
- BL-002: `Traceability` — related_constitution/related_domain/related_engine trong ADR frontmatter.

## [Unreleased] — sau ChatGPT review round 4 (9.8/10, recommend LOCK Chapter 0)

### Added
- **ADR Scope Rule (4b)** — bảng ADR Required / Optional / Not Required, tránh "cái gì cũng phải ADR".
- `created_at`, `approved_at` vào metadata mọi file (tách khỏi `last_review`).
- Ghi chú **Decision ≠ Documentation** (hệ quả của I-12) — mỗi loại tài liệu chỉ làm đúng 1 việc.

### Changed
- Tách quy tắc xung đột Product Owner/Chief Architect ra khỏi bảng Roles thành mục riêng **2b. Conflict Resolution**.
- Đổi "Technical Architect #1/#2" → "AI Technical Architect (ChatGPT)" / "(Claude)" — bỏ đánh số, future-proof cho AI khác tham gia sau này.
- ADR-005: sửa câu cảm tính "không có phản đối kỹ thuật nào đủ mạnh" → lý do kỹ thuật cụ thể (Trade-off accepted vì...).
- 11-adr-process.md: xác nhận ADR dùng chung Document Lifecycle (Mục 7) thay vì viết thêm "ADR Lifecycle" riêng — phát hiện: `Deprecated`/`Superseded` đã tồn tại sẵn ở đó, ChatGPT backlog item này thực ra đã được giải quyết, chỉ cần trỏ tham chiếu.

### Backlog (giữ nguyên, chưa làm)
- DoD cho từng Chapter (sẽ áp dụng bắt đầu từ Chapter 1 — Vision).
- BL-001, BL-002 (không đổi từ round trước).

## [Unreleased] — mở rộng Team Governance (chuẩn bị scale 1 → nhiều người)

### Added
- **`/docs/team/`** — tầng mới tách biệt hoàn toàn khỏi Constitution: `team.yaml` (gán Người/AI ↔ Role), `roles.md`, `responsibility-matrix.md` (RACI), `onboarding.md`.
- Role mới trong Governance: **Module Owner** (tránh 1 người ôm hiểu toàn bộ hệ thống khi Phase 3 bắt đầu).

### Changed
- **Sửa lỗi kiến trúc thật:** bảng Roles ở `00-governance.md` trước đó ghi thẳng "User"/"ChatGPT"/"Claude" — vi phạm chính nguyên tắc Role-vs-Person. Sửa thành: Constitution chỉ định nghĩa Role, việc gán Người/AI cụ thể chuyển sang `/team/team.yaml`.
- **Giữ nguyên vị trí ngang hàng giữa ChatGPT và Claude** (cả hai đều là "AI Technical Architect", không phân cấp) — phản đối đề xuất đặt Claude làm cấp dưới "Lead Technical Architect (ChatGPT)", vì sẽ làm mất giá trị 2 góc nhìn độc lập phản biện lẫn nhau đã chứng minh hiệu quả qua nhiều vòng review.
- Xác nhận: rule "Engineer không được tự đổi kiến trúc" không phải rule mới — đã được bao phủ bởi 4b (ADR Scope Rule), chỉ làm rõ áp dụng cho MỌI contributor.

### Note
- Toàn bộ thay đổi trong mục này **không chặn việc Lock Chapter 0** — theo đúng logic Role-vs-Person, nội dung `/team` nằm ngoài phạm vi Constitution.

## [Unreleased] — ADR-006: quyết định Product Owner đầu tiên khi 2 AI bất đồng

### Added
- **ADR-006** (Approved) — Product Owner quyết: ChatGPT và Claude giữ vai trò AI Technical Architect **ngang hàng**, khác nhau ở `focus` (ChatGPT: Discovery/consistency-check; Claude: Documentation/Implementation), không có hierarchy. Đây là ADR đầu tiên đạt trạng thái `Approved` chính thức từ Product Owner (các ADR-001~003 là ghi hồi tố, ADR-004 Superseded, ADR-005 vẫn `In Review`).
- `team.yaml` cập nhật field `focus` cho ChatGPT/Claude khớp ADR-006.

## [Milestone] — 2026-07-16 — 🔒 Chapter 0 (Governance) LOCKED

Product Owner chính thức Approve + Lock:
- `constitution/00-governance.md` → `Locked`
- `adr/ADR-005.md` (Lean Governance Model) → `Locked`
- `adr/ADR-006.md` (ChatGPT/Claude ngang hàng) → `Locked`

Từ thời điểm này, **ADR Immutable Rule có hiệu lực** với cả 3 file trên: không sửa trực tiếp, mọi thay đổi phải qua ADR mới (ADR-007+). Đây là mốc khóa chính thức đầu tiên của Ride Quant Platform — kết thúc ~5-6 vòng phản biện giữa Product Owner, ChatGPT, Claude.

**Next Milestone:** Chapter 1 — Vision.

## [Unreleased] — Vision v2.0 (soạn cùng ChatGPT) + ADR-007

### Added
- **ADR-007** (Locked) — chốt phạm vi Vision Phase 0-3: nội bộ (không multi-tenant/RBAC ngay) + crypto only (không đa tài sản ngay), nhưng kiến trúc chừa chỗ mở rộng qua `Account` first-class entity.
- `06-identity-model.md`: thêm `AccountID`, ghi rõ Account là entity first-class từ Phase 0.2 theo ADR-007.
- Vision v2.0: nội dung phong phú hơn nhiều từ bản soạn cùng ChatGPT (Core Beliefs, Product Principles, Non-Goals, Out of Scope, North Star), chuẩn hóa lại frontmatter khớp schema chung, thêm Mục 1.1 "Current Scope" phân biệt rõ Phase 0-3 vs Long-term Vision.

### Changed
- OQ-001: từ `Open` → `Partially Resolved` — hướng đã chốt (single-operator now, multi-tenant-ready later), thiết kế RBAC cụ thể vẫn mở nhưng không còn chặn Phase 1.

### Fixed (phát hiện khi review)
- Bản Vision nháp ban đầu (từ ChatGPT) ngầm định multi-tenant SaaS (Target Users nhiều nhóm độc lập) và bỏ mất phạm vi Crypto — mâu thuẫn với toàn bộ kiến trúc đã thiết kế (Position Ledger, Risk Gateway, I-9 Numerical Precision giả định crypto). Đã làm rõ qua ADR-007 trước khi hợp nhất vào 01-vision.md.

## [Unreleased] — Vision review round 2 (ChatGPT phản biện Claude)

### Fixed (Claude tự nhận sai lý luận, quyết định vẫn đúng)
- Issue #1 (Target Users): Claude từng suy luận "Target Users nhiều persona → ngầm định multi-tenant" — ChatGPT chỉ ra đây là 2 khái niệm tách biệt (Target Users = persona thiết kế tính năng, Deployment Model = hạ tầng chạy). Quyết định ở ADR-007 (nội bộ trước, chừa chỗ multi-tenant) vẫn đúng, chỉ sửa lại lý luận/câu chữ trong Vision (không mở ADR mới vì ADR-007 đã Locked và nội dung quyết định không đổi).
- Vision 1.3/1.5: thêm 2 câu rõ ràng (theo đề xuất chính xác của ChatGPT) — Ride ban đầu cho cá nhân/1 team, kiến trúc chừa chỗ multi-workspace/multi-tenant sau; Ride ban đầu cho Crypto, kiến trúc asset-agnostic để mở rộng sau.

### Changed
- Giảm overlap Vision/Mission/Long-term Vision (ChatGPT Issue #3): Mission (1.4) chỉ còn "What Ride does", bỏ câu trùng với Core Beliefs.
- Thêm Product Principle **"Everything Must Be Measurable"** (ChatGPT Issue #4) — đối xứng với tagline mở đầu (Explainable, Measurable, Continuously Improving), trước đó thiếu.
- Mở rộng BL-002 (Traceability, backlog) — thêm chiều Principle → ADR → Architecture theo đề xuất ChatGPT, không tạo backlog item mới trùng lặp.

## [Unreleased] — Vision review round 3 (ChatGPT, "Approve with required changes")

### Fixed — Critical
- **V2-01 (semantic error trong Parity/Reproducible):** Vision từng viết "cùng 1 kết quả bất kể execution mode" — SAI, vì execution outcome (fill, slippage, latency) được phép khác nhau giữa Live/Backtest/Paper. Sửa đúng bản chất: Parity nằm ở tầng **Decision** (phải giống nhau với cùng input/config/state), không phải tầng **Execution Result**. Bài học: paraphrase lại một Invariant (I-2) ở nơi khác có rủi ro làm sai lệch bản chất kỹ thuật — nhắc lại đúng tinh thần I-12.

### Fixed — Major
- **V2-02 (quá nhiều chi tiết implementation trong Vision):** gỡ bỏ chi tiết `AccountID`/Capability Matrix gate cụ thể khỏi Vision — chuyển thành **OQ-002** (Strategy Lifecycle Gate) trong Manifest, chỉ giữ nguyên tắc cấp cao "Research Before Capital".
- **V2-03 (1.1 và 1.3 lặp nhau):** 1.3 Product Positioning rút gọn chỉ còn phát biểu định vị sản phẩm, không lặp lại bảng Current Scope đã có ở 1.1.
- **V2-04 (Target Users phòng thủ quá mức):** bỏ ví dụ VSCode và lời giải thích tranh luận giữa 2 AI — không cần thiết cho người đọc Vision, lịch sử đã lưu ở ADR-007 + CHANGELOG.
- **V2-05 (Measurable chưa nối xuống đo lường):** thêm câu ràng buộc outcome ở Success Definition phải chuyển hóa thành leading/lagging indicators, KHÔNG nhét KPI chi tiết vào Vision — chuyển thành **OQ-003** (Product Metrics) trong Manifest.

### Added
- **OQ-002, OQ-003** trong MANIFEST.md — 2 chi tiết implementation được "trục xuất" khỏi Vision đúng chỗ, không mất thông tin, chỉ đổi nơi lưu.

### Note
- ChatGPT: "Approve with required changes — sau commit này, Approve & Lock Chapter 1, không cần thêm vòng rewrite lớn."

## [Unreleased] — Vision v2.2: Product Positioning phân tầng Identity/Capability (Product Owner trực tiếp yêu cầu)

### Changed
- 1.3 Product Positioning: tách "Quant Trading Platform" và "Trading Operating System" đang đứng ngang hàng (nối bằng "và") thành 2 tầng rõ ràng — **Identity** (Trading Operating System) và **Core Capability** (strategy-agnostic Quant Trading Platform) — khớp với cách câu mở đầu chương đã định danh Ride từ đầu.

## [Unreleased] — Vision v2.3: bỏ lặp Identity ở 1.3

### Changed
- Bỏ nhãn "Identity" khỏi 1.3 (đã tuyên bố ở câu mở đầu chương) — 1.3 giờ chỉ còn "Core Capability", trỏ ngược lại Identity đã nêu, tránh lặp.

## [Milestone] — 2026-07-17 — 🔒 Chapter 1 (Vision) LOCKED

Product Owner chính thức Approve + Lock `constitution/01-vision.md` (v2.3), sau 3 vòng review (ChatGPT + Claude) qua Vision v2.0 → v2.1 → v2.2 → v2.3.

Từ thời điểm này, **ADR Immutable Rule có hiệu lực** với `01-vision.md`: không sửa trực tiếp, mọi thay đổi phải qua ADR mới.

**Đã Locked tới nay:** Chapter 0 (Governance), Chapter 1 (Vision), ADR-005, ADR-006, ADR-007.

**Next Milestone:** Chapter 2 — Platform Invariants.

## [Unreleased] — Platform Invariants v2.0 (ChatGPT review: "Revision Requested" → xử lý toàn bộ)

### Fixed — Blocker
- **I-8 (Kill Switch):** câu cũ quá tuyệt đối ("circuit breaker 1 sàn không ảnh hưởng sàn khác") tạo lỗ hổng naked exposure cho strategy arbitrage/hedge đa sàn. Sửa: per-exchange isolation ở tầng hạ tầng vẫn giữ, nhưng Risk Gateway phải được phép pause/unwind cross-exchange khi có dependency/exposure thật.

### Fixed — Major
- **I-2 (Parity → Decision Parity):** thiếu Paper Trading mode, và là NGUỒN GỐC của lỗi semantic đã sửa ở Vision V2-01 — tôi từng sửa bản sao (Vision) mà quên sửa bản gốc (I-2). Nay sửa đúng tại nguồn: Parity ở tầng Decision, không phải Execution Result, đủ cả 4 mode.
- **I-3 (No Repaint → No Repaint/No Look-Ahead):** event immutability (append-only) KHÔNG tự động đảm bảo No Repaint — engine vẫn có thể look-ahead bias nếu không phân biệt provisional/confirmed. Bổ sung rõ.
- **I-6 (Fail-Safe → Fail-Safe by Scope):** "1 engine lỗi → dừng toàn platform" quá rộng, phá isolation, giảm availability. Thêm khái niệm blast radius/scope (symbol/strategy/account/exchange/platform).
- **I-10 (Idempotency Key → Idempotent Execution Effect):** idempotency key tự thân không đảm bảo exactly-once economic effect (exchange có thể nhận lệnh nhưng response thất lạc...). Yêu cầu reconciliation trước khi retry.

### Fixed — Minor
- I-1: mở rộng evidence cần capture (config version, code/build version, risk policy version, correlation chain...).
- I-5: mở rộng từ "external data" thành "decision-time observable dependency" (bao gồm cả feature flags, risk limits, config, model artifact — không chỉ nguồn ngoài).
- I-7: thay "Core Engine" (thuật ngữ không tồn tại trong Module Taxonomy) bằng contract cụ thể (versioned event/query/command contract).
- I-9: phân biệt giá trị authoritative (bắt buộc decimal) vs phân tích không-authoritative (float được phép, có boundary conversion).
- I-12: "Event Bus" chỉ là transport, sửa thành "durable append-only event log" làm authority; làm rõ "1 nguồn sự thật" = 1 authoritative source PER SCOPE, không phải 1 database duy nhất toàn platform.

### Changed
- Toàn bộ 12 invariant viết lại theo cấu trúc Statement/Required guarantees/Prohibited behavior/Scope/Verification — đủ để triển khai và test, thay vì mỗi invariant chỉ 1 dòng.

## [Unreleased] — Platform Invariants v2.1 (ChatGPT review round 2: "Approve with required changes")

### Fixed — Blocker
- **I-12 tự mâu thuẫn SSOT:** bản v2.0 gọi MANIFEST.md/Decision Log/Domain Model là "bản sao dẫn xuất có thể rebuild từ event log" — SAI, mâu thuẫn trực tiếp với Governance đã Locked (MANIFEST.md là authoritative cho document status, Domain Model là authoritative cho domain concept, không phải projection của event log). Sửa: phân biệt rõ authoritative source theo từng loại concept (runtime→event log, document status→MANIFEST, ADR→architecture decision, Domain Contract→domain concept), chỉ Projection/cache/index/dashboard mới là derived representation.

### Fixed — Major
- **I-6:** thêm rõ Fail-Safe by Scope KHÔNG được chặn risk-reducing action (cancel, reduce-only, close, hedge, controlled unwind) — chỉ chặn action làm TĂNG exposure.
- **I-2:** Verification đổi từ "decision hash comparison" (dễ fail sai do lẫn runtime metadata như DecisionID/timestamp/trace ID) sang "canonical semantic-decision hash" — chỉ hash payload nghiệp vụ, loại trừ metadata vận hành.

### Fixed — Minor
- I-1: Verification không còn dựa vào "1 decision ngẫu nhiên" — yêu cầu 100% trace-completeness cho production, CI sample-based cho volume lớn, audit định kỳ.
- I-5: cho phép immutable content-addressed reference + checksum cho dependency lớn (model artifact, calendar dataset) thay vì bắt buộc inline toàn bộ; cấm reference dạng mutable ("latest-model").
- I-11: siết least privilege — chỉ Exchange Adapter/Custody-Signing Service giữ raw secret, Execution Engine chỉ tương tác qua contract trừ khi cùng trust boundary.
- I-8: đổi "pause hoặc unwind" (nghe như nghĩa vụ) thành "pause/cancel/hedge/reduce/controlled unwind theo risk policy" (được phép, không phải bắt buộc luôn unwind) — tránh khóa lỗ/mất hedge khi xử lý vội.

## [Unreleased] — Platform Invariants v2.2 (ChatGPT review round 3, fetch trực tiếp GitHub blob SHA `252cd63`)

### Fixed — Major
- **I-11:** Required Guarantees và Verification từng nói NGƯỢC NHAU (Guarantee: Execution không đọc secret; Verification: xác nhận Execution có quyền đọc) — lỗi do sửa 1 phần không đồng bộ. Sửa Verification khớp Guarantee, đổi "read secret store" → "use credential" (KMS/signing service có thể ký mà không lộ raw secret).
- **I-5:** "immutable content-addressed reference" không tự động đảm bảo Replay offline được (artifact có thể chỉ nằm ở remote store). Tách rõ 2 giai đoạn: Replay preparation (được resolve artifact qua mạng) vs Replay execution (bắt buộc network-free) — verification đổi thành "self-contained replay test" sau khi materialize.
- **I-9:** Verification cũ vô tình hợp thức hóa "exchange price → float → decimal → Ledger", mất precision không phục hồi được. Sửa: giá trị authoritative (price/quantity/fee/balance) phải parse trực tiếp từ lossless representation, KHÔNG BAO GIỜ qua float ở bất kỳ bước nào; float chỉ dành cho analytical output, qua explicit quantization boundary khi thành financial intent.

### Fixed — Minor
- I-8: sửa câu ví dụ mâu thuẫn đại từ ("exchange lỗi" và "hoạt động bình thường" cùng câu) — làm rõ 2 chân hedge nằm trên 2 exchange khác nhau.
- I-4: Verification mở rộng — static import scan không đủ, thêm runtime test (`ExecutionIntentAccepted` phải trace tới `RiskApproved`), network-policy test, credential audit.
- I-7: Verification mở rộng — thêm network ACL, API authorization scope, event schema compatibility, command authorization, capability declaration, kiểm tra truy cập storage module khác.
- I-2: bỏ hardcode field list (strategy_instance, instrument...) khỏi Verification — nguy cơ tự vi phạm I-12 nếu Decision Contract đổi sau này. Trỏ về "Decision Contract authoritative" ở `/docs/domain/` (chưa tạo, sẽ có ở Phase 0.2).
- I-3: bổ sung yêu cầu test bitemporal (effective/event time vs knowledge/recorded time) cho trường hợp data correction, trỏ về Time Model.

### Added
- **BL-003** (Manifest) — Invariant Conformance Matrix, thuộc Architecture/Engineering Phase (không phải Constitution), chỉ làm khi module/contract thật tồn tại.
- **OQ-004** (Manifest) — Time Model (Chapter 5) cần bổ sung bitemporal, xử lý khi Chapter 5 vào vòng review riêng.

### Note
- ChatGPT: "Sau khi ba Major được sửa, Chapter 2 đủ điều kiện Approve & Lock." Không thêm Motivation/Examples/Severity vào 12 invariant (tránh phình tài liệu) — giữ nguyên khuyến nghị này.

## [Unreleased] — Platform Invariants v2.4 (ChatGPT review round 4, fetch blob SHA `657e33b`)

### Fixed — Major
- **I-1:** Statement cũ tự mâu thuẫn — đòi evidence "capture tại decision time" nhưng Required Guarantees lại yêu cầu "execution outcome" (chỉ tồn tại SAU decision time). Sửa: tách decision inputs (frozen tại decision time) khỏi subsequent outcomes (capture khi được quan sát), nối bằng causation/correlation chain.
- **I-10:** Statement cũ ngầm định quan hệ 1 execution intent → 1 client order (số ít), không hỗ trợ order slicing, TWAP/VWAP, cancel-replace, multi-venue routing — có thể khóa sai Execution model. Sửa: 1 intent → nhiều child order/execution attempt hợp lệ, miễn tổng economic effect không vượt quá intent đã approved; mỗi child order truy vết được về intent gốc.

### Fixed — Minor
- I-5: "Replay chỉ đọc event" chưa khớp việc Replay còn đọc immutable artifact bundle — làm rõ Replay execution đọc cả event lẫn artifact đã materialize+checksum.
- I-8: Verification cũ chỉ nói "pause", hẹp hơn Guarantee (cho phép pause/cancel/hedge/reduce/unwind) — mở rộng Verification khớp đủ các action.
- I-12: terminology không nhất quán ("Domain Contract" ở Required Guarantees vs "Domain Model" ở Scope) — ironic vì đây là invariant về SSOT. Chuẩn hóa dùng "Domain Contract" xuyên suốt.

### Cross-check (Claude tự xác nhận, không phải từ ChatGPT)
- Fix I-1 (causation chain) và fix I-10 (ExecutionIntentID → nhiều ChildOrderID) phải nhất quán với nhau — đã xác nhận: I-10 sinh nhiều child order, I-1 phải trace được toàn bộ qua đúng 1 causation chain. Hai fix củng cố lẫn nhau, không mâu thuẫn.

### Note
- I-3/Chapter 5 boundary: ChatGPT xác nhận ví dụ bitemporal hiện tại trong I-3 Verification là đúng kỹ thuật, không cần bỏ — chỉ nhắc khi review Chapter 5 phải giữ thuật ngữ khớp hoàn toàn với I-3.

## [Unreleased] — Platform Invariants v2.5 (ChatGPT review round 5, fetch blob SHA `a8879aa`)

### Fixed — Major
- **I-6:** Statement cũ "không phát sinh exposure mới" mâu thuẫn trực tiếp với Required Guarantees cho phép hedge (hedge luôn tăng GROSS exposure dù giảm NET risk). Sửa: phân biệt risk-increasing action (bị cấm) vs risk-reducing action theo risk model authoritative (được phép, kể cả khi tăng gross exposure) — ví dụ cụ thể: long 1 BTC exchange A, hedge short 1 BTC exchange B → net ~0 nhưng gross tăng gấp đôi, vẫn hợp lệ vì risk model xác nhận giảm net risk.

### Fixed — Minor
- I-7: Statement cũ "mọi module mới" quá rộng so với Scope thật (chỉ Plugin) — có thể vô tình áp cho Exchange Adapter, Custody/Signing Service, event storage, schema registry... không phải module nào cũng nên mặc định là Event Bus consumer. Thu hẹp về đúng phạm vi Plugin/extension module.

### Note
- 4 vòng liên tiếp (v2.0→v2.5): số vấn đề mới phát hiện giảm dần (6 → 4 → 5 → 2+3 → 1+1) — tín hiệu hội tụ rõ ràng, không phải vòng lặp tìm lỗi vô hạn.

## [Unreleased] — Platform Invariants v3.0: thêm I-13 State Transition Integrity (ChatGPT đề xuất, ⭐⭐⭐⭐⭐)

### Added
- **I-13 — State Transition Integrity:** invariant còn thiếu thật — mọi entity có vòng đời trạng thái (Position, Order, Risk Decision, Strategy Instance, Portfolio, Session) chỉ được chuyển state qua transition đã khai báo tường minh, không tồn tại illegal transition, terminal state không nhận thêm transition. Khác I-3 (No Repaint — trục thời gian) ở chỗ I-13 kiểm soát trục cấu trúc đồ thị trạng thái — 2 invariant độc lập, không trùng.
- Tự sửa trước khi thêm: KHÔNG hardcode state machine cụ thể (OPEN/PARTIAL/CLOSED...) vào Platform Invariants — chỉ dùng làm ví dụ minh họa, danh sách state/transition thật phải sống ở Domain Contract (`/docs/domain/`, Phase 0.2 chưa bắt đầu) — áp dụng đúng bài học từ lỗi I-2 (hardcode field list) đã sửa trước đó, tránh vi phạm I-12.
- Cập nhật `team/onboarding.md`: 12 → 13 Invariant.

### Version bump note
- Bump lên 3.0 (không phải patch nhỏ) vì đây là thêm invariant mới, thay đổi số lượng nguyên tắc bất biến của Constitution — khác các lần sửa nội dung/wording trước (2.0→2.5).

## [Unreleased] — Platform Invariants v3.1 (ChatGPT review I-13, round 1)

### Fixed — Major
- **I-13 "terminal state = zero outbound transition":** quá tuyệt đối — thực tế nhiều domain có correction/reconciliation/supersession hợp lệ sau terminal (Order REJECTED được supersede, Position CLOSED nhận late fill, Session CLOSED được reopen). Đây vẫn là một dạng hardcode state machine rule (dù không hardcode danh sách state) — lặp lại đúng loại lỗi đã sửa ở I-2. Sửa: Domain Contract tự khai báo state nào "strictly terminal" (zero outbound thật) vs state có correction/supersession path riêng.
- **I-13 "không mutate trực tiếp field trạng thái":** mâu thuẫn với I-12 (Projection/materialized view được phép tồn tại và rebuild). Sửa: phân biệt rõ "Authoritative state transition" (phải qua event) vs "Derived state projection update" (được phép, miễn rebuild được từ event).

### Fixed — Minor
- Ví dụ Prohibited behavior đổi từ state cụ thể (`OPEN→CLOSED→PARTIAL`) sang trừu tượng (`StateA→StateC`) — tránh gây hiểu lầm đó là canonical Position state trong khi Constitution chủ trương không hardcode domain.
- Scope: sửa "Domain Model" → "Domain Contract" cho nhất quán thuật ngữ (I-12 đã canonical hóa "Domain Contract").

## [Milestone] — 2026-07-18 — 🔒 Chapter 2 (Platform Invariants) LOCKED

Product Owner chính thức Approve + Lock `constitution/02-platform-invariants.md` (v3.1, 13 invariant: I-1 → I-13), sau **6 vòng review liên tiếp** giữa ChatGPT và Claude (v1.0 → v2.0 → v2.1 → v2.2 → v2.3 → v2.4 → v2.5 → v3.0 → v3.1). Đây là chapter trải qua nhiều vòng phản biện nhất từ đầu dự án — số vấn đề mới phát hiện mỗi vòng giảm dần rõ rệt, xác nhận hội tụ thật trước khi khóa.

Từ thời điểm này, **ADR Immutable Rule có hiệu lực** với `02-platform-invariants.md`: không sửa trực tiếp, mọi thay đổi phải qua ADR mới.

**Đã Locked tới nay:** Chapter 0 (Governance), Chapter 1 (Vision), Chapter 2 (Platform Invariants), ADR-005, ADR-006, ADR-007.

**Next Milestone:** Chapter 3 — Engineering Principles.

## [Unreleased] — Chapter 3 (Engineering Principles) v1.1 — Claude tự review trước khi gửi ChatGPT

### Added
- **ADR-008** (Approved, hồi tố) — Phân bổ ngôn ngữ Python (lõi logic)/Go (biên hệ thống), Rust reserved cho tương lai. Quyết định này tồn tại từ Session 1 nhưng chưa từng thành ADR — cùng loại lỗi với ADR-001~003, phát hiện khi tự review Chapter 3.

### Fixed
- Tham chiếu "Parity Principle (I-2)" đã lỗi thời — I-2 đổi tên thành "Decision Parity" qua các vòng review Chapter 2. Cập nhật khớp tên hiện tại.
- "Go/Rust không được chứa logic nghiệp vụ" gây hiểu lầm cả 2 đang active — làm rõ Rust chỉ reserved, chưa dùng.
- **Phát hiện quan trọng:** thêm cảnh báo tường minh — Risk Gateway viết Go không vi phạm I-2 Decision Parity, MIỄN Backtest/Replay/Paper/Live gọi qua cùng 1 Risk Gateway service instance, không viết risk-check Python "rút gọn" riêng cho backtest (lỗi kinh điển trong lịch sử hệ thống trading thật).

### Changed
- Thêm cross-reference tránh trùng lặp (I-12): Testing Convention → trỏ Chapter 13 (coverage/tier); Versioning → trỏ Chapter 10 (SemVer engine schema); Documentation Convention → trỏ Governance §7-9 (metadata/lifecycle).
- Thêm Mục 3.3 Backlog: hiệu năng Backtest Engine Python ở scale lớn (vectorization/Ray/Dask) — nêu từ Session 1, chưa từng được ghi lại chính thức ở đâu.

## [Unreleased] — Chapter 3 v1.2 (ChatGPT review round 1, fetch blob SHA `87250fb`)

### Fixed — Major
- **Ngôn ngữ bị "đóng đinh" vào Principle:** Chapter 3 v1.1 lặp lại nguyên nội dung ADR-008 (Python=X, Go=Y, Rust=Z) — 2 nguồn cùng nói 1 quyết định công nghệ, sẽ lệch nhau khi công nghệ đổi. Sửa: Chapter 3 chỉ giữ nguyên tắc trừu tượng ("One Canonical Business Logic Implementation" — không đổi theo công nghệ), trỏ về ADR-008 cho quyết định cụ thể, không lặp lại.
- **"1 Risk Gateway service instance" quá literal:** giống lỗi đã sửa ở I-10 (1 intent → nhiều child order) — "instance" ngầm cấm horizontal scaling/HA/replica. Sửa thành "cùng 1 canonical implementation (Risk Decision Contract)", có thể chạy dưới nhiều replica miễn cùng codebase.

### Fixed — Minor
- Naming example đổi từ domain-specific (`SWING_CREATED`, `REGIME_UPDATED`) sang trừu tượng (`ENTITY_CREATED`, `ORDER_FILLED`, `POSITION_CLOSED`) — Chapter 3 là engineering convention chung, không nên ví dụ bằng domain cụ thể.
- Backlog 3.3 đổi từ nêu sẵn giải pháp (Polars/Ray/Dask) sang đúng thứ tự problem→benchmark→evaluate — tránh Constitution hint solution trước khi đo vấn đề thật.

## [Unreleased] — Chapter 3 v1.3 (ChatGPT review round 2, fetch blob SHA `572f8bc`)

### Fixed — Blocker
- **Mâu thuẫn với Governance đã Locked:** Chapter 3 khẳng định "mọi convention change bắt buộc ADR" — nhưng Governance §4b (ADR Scope Rule, đã Locked) đã phân loại ADR Required/Optional/Not Required. Câu cũ vô tình tạo luật governance riêng, ghi đè Chapter 0 (vi phạm hierarchy Constitution). Đây là lỗi tồn tại từ bản thảo đầu tiên, không ai (kể cả Claude) nhận ra qua nhiều vòng review trước — chỉ lộ ra khi đối chiếu trực tiếp với Governance đã Locked. Sửa: Engineering Foundation tuân theo đúng phân loại ADR Scope Rule, không tự đặt luật cứng hơn.

### Fixed — Major
- **Risk Gateway "không được chứa business logic" tự mâu thuẫn:** ngay sau đó lại yêu cầu Risk Gateway có canonical Risk Policy implementation (exposure limit, approve/reject, risk-increasing detection...) — chính là business logic. Sửa: phân biệt Strategy/Decision domain logic (không được rò rỉ khỏi Decision Engine) với Risk Policy logic (Risk Gateway sở hữu hợp lệ, đây đúng là bounded context của nó).
- **"Đúng một implementation duy nhất" quá tuyệt đối:** không cho phép shadow implementation, blue/green deployment, migration, experimental implementation — các pattern hợp lệ trong thực tế. Sửa: phân biệt "authoritative implementation" (được phép phát sinh Decision chính thức) với "implementation khác tồn tại song song" (được phép tồn tại, không phát sinh authoritative Decision cho tới khi qua parity validation + promote).

### Fixed — Minor
- Label "trừu tượng, không domain-specific" không khớp ví dụ thật (`ORDER_FILLED`, `IStructureEngine`, `SwingDTO` vẫn domain-specific) — sửa label thành "minh họa cụ thể cho Ride, không phải canonical domain vocabulary bắt buộc".
- Bỏ cách gom "Research (Backtest/Replay/Paper) vs Production (Live)" — không khớp cách I-2 (Locked) liệt kê 4 mode ngang hàng, và Paper Trading về bản chất gần Production hơn Research (dùng live data/clock/execution simulator). Dùng liệt kê trung tính: Backtest, Replay, Paper Trading, Live.

## [Unreleased] — Chapter 3 v1.4 (ChatGPT review round 3, fetch blob SHA `c1102e2`) + Chapter 12 addition

### Fixed — Major
- **"Bounded context" dùng trước khi Chapter 4 (Domain Principles) canonical hóa nó:** Chapter 3 chỉ khai báo `depends_on: [02-platform-invariants]` nhưng nội dung dựa vào khái niệm "bounded context" — thuộc quyền sở hữu của Chapter 4 chưa Locked. Tạo dependency ngầm không khai báo + rủi ro Chapter 4 định nghĩa khác giả định của Chapter 3. Sửa: đổi thành "business capability/responsibility ownership" — trung lập, không cần sửa lại kể cả sau khi Chapter 4 Lock.
- **Risk parity bị gọi nhầm là "hệ quả trực tiếp của I-2":** I-2 (Locked) chỉ định nghĩa parity ở tầng Decision, không tự động bao gồm Risk Action. Gọi Risk parity là hệ quả của I-2 = âm thầm mở rộng phạm vi 1 invariant đã Locked mà không qua ADR. Sửa: tách rõ — Strategy/Decision tuân thủ I-2; Risk là yêu cầu bổ sung của Chapter 3 + I-1, không mở rộng định nghĩa I-2.

### Fixed — Minor
- "Cùng version/config cho mọi execution mode" quá tuyệt đối — không cho phép canary/experiment hợp lệ (Paper chạy canary version, Backtest thử config mới, Replay tái dựng version cũ). Sửa: chỉ bắt buộc đồng bộ version/config khi THỰC SỰ tuyên bố parity hoặc tái dựng cùng run identity; ngoài phạm vi đó được phép khác nhau, miễn không tuyên bố parity sai.

### Added
- **Chapter 12 §12.1 — Backward Consistency Check:** hệ thống hóa bài học "rà ngược chapter cũ khi có luật mới Locked" thành bước lặp lại được trong Approval Gate — đặt ở Chapter 12 (vẫn `In Review`, sửa trực tiếp được) thay vì Governance (đã `Locked`, cần ADR mới nếu sửa) theo đúng đề xuất ChatGPT.

## [Milestone] — 2026-07-18 — 🔒 Chapter 3 (Engineering Principles) LOCKED

Product Owner chính thức Approve + Lock `constitution/03-engineering-principles.md` (v1.4), sau 4 vòng review liên tiếp (v1.0 → v1.1 → v1.2 → v1.3 → v1.4). Vòng cuối đạt 0 Blocker/Major/Minor — chỉ còn 2 Suggestion không chặn Lock (giữ nguyên "authoritative output", chưa cần rút ví dụ ra Domain Contract vì Domain Contract chưa tồn tại).

Từ thời điểm này, **ADR Immutable Rule có hiệu lực** với `03-engineering-principles.md`: không sửa trực tiếp, mọi thay đổi phải qua ADR mới.

**Đã Locked tới nay:** Chapter 0 (Governance), Chapter 1 (Vision), Chapter 2 (Platform Invariants), Chapter 3 (Engineering Principles), ADR-005, ADR-006, ADR-007, ADR-008.

**Next Milestone:** Chapter 4 — Domain Principles.

## [Unreleased] — Chapter 4 (Domain Principles) v2.0 — Claude tự review trước khi gửi ChatGPT

### Fixed
- **Lời hứa chưa giữ:** Chapter 3 (Locked) nói "bounded context sẽ được canonical hóa ở Chapter 4" — nhưng Chapter 4 bản cũ hoàn toàn không nhắc tới khái niệm này. Thêm §4.3 **Business Capability** (tên canonical được chọn thay vì "bounded context" để nhất quán với ngôn ngữ Chapter 3 đã dùng): định nghĩa, ranh giới (single responsibility), quy tắc giao tiếp (chỉ qua published contract, nhất quán I-4/I-7).
- **Domain Contract template thiếu state machine:** I-13 (Locked) yêu cầu Domain Contract sở hữu state machine của từng entity, nhưng ví dụ YAML cũ không có field này. Thêm `state_machine` (states/transitions/terminal_states) vào template.
- **Thuật ngữ "Domain Model" vs "Domain Contract" tự mâu thuẫn:** I-12 (Locked) đã canonical hóa "Domain Contract" — nhưng chính Chapter 4 (chapter sở hữu khái niệm) vẫn viết "Domain Model = Domain Contract" và "Glossary hợp nhất với Domain Model". Chuẩn hóa toàn bộ về "Domain Contract".
- Thêm khai báo type/precision cho giá trị tài chính trong `schema` (liên kết I-9).
- "Domain Modeling trước UX Blueprint": bỏ tự khẳng định thứ tự độc lập, trỏ về Roadmap (Chapter 14) — nơi thứ tự này đã được liệt kê, tránh 2 nguồn cùng khẳng định 1 trình tự.

## [Unreleased] — Chapter 4 v2.1 (ChatGPT review round 1, fetch blob SHA `b1ac6db`) + Chapter 14 v1.1

### Fixed — Blocker
- **Ubiquitous Language áp dụng toàn cục làm mất context boundary:** "1 thuật ngữ = 1 nghĩa duy nhất TOÀN dự án" mâu thuẫn với việc canonical hóa bounded-context. Nếu giữ, hệ thống trượt dần thành global shared domain model (capability mất tính độc lập). Sửa: 1 thuật ngữ = 1 nghĩa canonical TRONG mỗi Domain Context; cùng từ được phép khác nghĩa giữa context, namespace rõ + Context Map (ví dụ Position ở Execution vs Portfolio).

### Fixed — Major
- **Business Capability ≠ Bounded Context ≠ Module bị đồng nhất:** §4.3 viết lại phân biệt 3 boundary với quan hệ 1..n (Capability 1─1..n Context 1─1..n Module), mapping 1:1 ở giai đoạn đầu nhưng không đóng đinh vĩnh viễn. Đặc biệt: giữ đúng cách Chapter 3 (Locked) đã dùng "Business Capability" — tránh semantic drift NGƯỢC lên chapter đã Locked (điểm Claude phản biện, Product Owner chốt wording dung hòa).
- **Mở rộng vai trò Module Owner đã Locked:** Chapter 4 bản cũ nói capability "do Module Owner phụ trách" — nhưng Governance định nghĩa Module Owner cho module cụ thể, capability có thể gồm nhiều module. Sửa: không mặc định Module Owner = Capability Owner; Domain Contract ownership theo metadata tài liệu; role Capability Owner (nếu cần) phải qua ADR.
- **Dependency thiếu + vòng tròn với Roadmap:** frontmatter thiếu `03-engineering-principles`; §4.4 lấy Roadmap (downstream, chưa Locked, đang có rule mâu thuẫn Governance) làm nguồn authoritative cho thứ tự. Sửa: thêm dependency, đưa nguyên tắc thứ tự vào chính Chapter 4, Roadmap chỉ tham chiếu (luồng 4→12→14 không ngược).

### Fixed — Minor
- Domain Contract template ép mọi concept cùng cấu trúc (schema/events/invariants/state_machine) — nhưng value object/policy/command... không phải cái nào cũng phát sinh event. Thêm field `kind` + phân biệt required/conditional; tách `events_emitted`/`events_consumed`.

### Fixed — Chapter 14 (Backward Consistency Check phát hiện)
- Roadmap chứa "ADR bắt buộc cho mọi định nghĩa Domain Concept / mọi quyết định kiến trúc" — mâu thuẫn Governance §4b (ADR Scope Rule: không phải mọi quyết định cần ADR). Sửa thành "ADR cho quyết định thuộc diện ADR Required". Đây đúng loại lỗi §12.1 Backward Consistency Check vừa thêm được sinh ra để bắt.

## [Unreleased] — Chapter 4 v2.2 (ChatGPT review round 2, fetch blob SHA `3a3b2ea`)

### Fixed — Major
- **Context Map dùng như nghĩa vụ nhưng chưa được định nghĩa:** §4.1 yêu cầu term đa nghĩa phải mô tả trong "Context Map" — nhưng không nói Context Map là gì/ở đâu/ai sở hữu → nguy cơ mỗi người tạo 1 kiểu, vi phạm I-12 (cùng thứ giải quyết Blocker lại tạo nguồn rải rác). Thêm §4.2 canonical hóa: authoritative source `/docs/domain/context-map.yaml`, field bắt buộc, không dùng section rải trong từng Contract.

### Fixed — Minor
- `schema: {} # required` ép mọi kind (kể cả policy/domain_service không có data representation) → sinh tài liệu giả. Sửa: schema required khi CÓ data representation; policy/domain_service dùng inputs/outputs/pre/postconditions.
- Cardinality `Domain Context 1─1..n Module` quá cứng (context ở giai đoạn modeling có thể chưa có module). Đổi `1..n` → `0..n`; thêm quy tắc shared technical module không sở hữu domain state của nhiều context.

### Added (Suggestion — chi phí gần 0, làm luôn)
- `capability_id`/`domain_context_id` là stable machine-readable ID (không phải display name) — display title đổi được mà không hỏng references/event metadata/dependency graph, tránh migration đau đớn sau này.

## [Unreleased] — Chapter 4 v2.3 (ChatGPT review round 3, fetch blob SHA `ebf3b78`)

### Fixed — Major
- **Context Map authoritative cho relationship nhưng KHÔNG cho identity của capability/context:** hai Domain Contract có thể khai `capability_id` mâu thuẫn nhau mà không có registry phân xử ID nào đúng — cùng loại vấn đề I-12 mà Context Map sinh ra để giải quyết, nhưng ở tầng node (định nghĩa) thay vì edge (quan hệ). Sửa: mở rộng context-map.yaml sở hữu 3 phần — capability registry + context registry + relationship map; mọi ID dùng trong Domain Contract phải tồn tại sẵn trong registry, không được tự định nghĩa ID chưa đăng ký.

### Fixed — Minor
- `upstream_context/downstream_context` bắt buộc cho mọi relationship — nhưng message flow direction ≠ model influence direction (một context publish event nhưng consume command từ context kia). Sửa: direction theo từng contract edge (provider/consumer + relationship_type); model_influence (DDD upstream/downstream) khai báo riêng khi cần.

## [Unreleased] — Chapter 4 v2.4 (ChatGPT review round 4 — chỉ Suggestion, không Blocker/Major/Minor)

### Added
- `status` cho relationship trong Context Map (Suggestion 1) — nhất quán với capabilities/contexts đã có status; cho phép deprecate 1 relationship mà không xóa lịch sử.
- **BL-004** (backlog): tách context-map.yaml thành nhiều file khi quá lớn (Suggestion 2) — KHÔNG làm ngay vì file chưa tồn tại, tránh giải quyết vấn đề chưa đo được (đúng nguyên tắc Chapter 3 đã thiết lập). Xử lý khi có dữ liệu thật ở Engineering Foundation/Phase 0.2.

## [Milestone] — 2026-07-18 — 🔒 Chapter 4 (Domain Principles) LOCKED

Product Owner chính thức Approve + Lock `constitution/04-domain-principles.md` (v2.4), sau 5 vòng (self-review + 4 vòng ChatGPT: v1.0 → v2.0 → v2.1 → v2.2 → v2.3 → v2.4). Chapter nền tảng cho toàn bộ `/docs/domain/` sau này — định nghĩa Ubiquitous Language (context-scoped), Context Map (authoritative registry cho capability/context/relationship), Domain Contract template, và phân biệt 3 boundary (Business Capability / Domain Context / Module).

Điểm đáng ghi nhớ: vòng self-review + review với ChatGPT đã giữ đúng lời hứa Chapter 3 (canonical hóa "Business Capability"), tuân thủ I-13 (state_machine trong Domain Contract), I-12 (Context Map authoritative), và Claude phản biện thành công 1 lần (giữ semantic "capability" của Chapter 3 khỏi bị drift ngược) — Product Owner chốt wording dung hòa.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4 + ADR-005, 006, 007, 008.

**Next Milestone:** Chapter 5 — Time Model (cần xử lý OQ-004: bitemporal effective/event time vs knowledge/recorded time).

## [Unreleased] — Chapter 5 (Time Model) v2.0 — Claude tự review

### Fixed — nghiêm trọng nhất
- **Thuật ngữ "Event Time" va nhau giữa Chapter 5 và I-3 (Locked):** I-3 viết "event_time của candle là 10:00" theo nghĩa *thời điểm dữ liệu nói về* (effective), nhưng Chapter 5 cũ định nghĩa Event Time = *thời điểm publish vào bus* (recorded) — candle khung 10:00 publish lúc 10:00:30 sẽ có 2 cách hiểu không tương thích, khiến look-ahead test của I-3 không biết so theo trục nào. Vì I-3 đã Locked, Chapter 5 hòa giải: canonical hóa cặp **Effective Time / Recorded Time**, khai báo cách gọi trong I-3 là alias tương thích (effective/event → Effective; knowledge/recorded → Recorded), không mâu thuẫn với nguyên văn I-3.

### Added
- **§5.1 Bitemporal Model** — giải quyết **OQ-004** (treo từ vòng review Chapter 2): 2 trục Effective/Recorded, correction là event mới (effective giữ nguyên, recorded mới), nhất quán I-3 append-only.
- **§5.3 Ngữ nghĩa Replay** — Replay Time trước đây chỉ có tên, không có định nghĩa vận hành. Nay định nghĩa rõ: Replay tại T = chỉ thấy event có recorded time ≤ T, bất kể effective time — nhìn theo trục effective để quyết visibility là look-ahead bias (khớp đúng ví dụ 10:00/10:03/10:07 trong I-3).
- **§5.4 Clock authority** — event_time do event log cấp phát, bất biến sau khi ghi; clock skew là vấn đề vận hành cần giám sát nhưng không thay đổi nguyên tắc ordering.

### Changed
- Bảng 4 mốc thời gian gắn rõ mỗi mốc thuộc trục nào (Market→Effective, Event→Recorded, Processing→vận hành, Replay→Recorded); Market Time với dữ liệu dạng khoảng (candle) = thời điểm bắt đầu khoảng.
- Thêm dependency `02-platform-invariants` vào frontmatter (chapter này tồn tại để phục vụ I-3/I-5 kiểm chứng được).

## [Unreleased] — Chapter 5 v2.1 (ChatGPT review round 1)

### Fixed — Major
- **Processing Time mâu thuẫn phân loại ngay trong bảng:** §5.2 viết "Processing Time không thuộc 2 trục" nhưng vẫn để chung bảng với các mốc bitemporal → gây hiểu lầm nó cũng dùng cho ordering/replay. Tách thành 2 bảng riêng: mốc bitemporal (Market/Event/Replay — authoritative cho ordering/replay/decision) vs mốc vận hành (Processing Time — chỉ observability, CẤM dùng cho ordering/replay/decision vì phá determinism I-2/I-3).

### Fixed — Minor
- Market Time ngầm định luôn có và luôn đáng tin — thực tế có thể vắng mặt/lệch (derived data nội bộ, sàn không gửi timestamp, clock sàn lệch). Làm rõ: khi đó Effective Time theo policy khai báo trong Domain Contract của nguồn, không mặc định luôn có Market Time.
- Thiếu xử lý out-of-order arrival (event đến trễ nhưng effective time cũ). Bổ sung: ordering/replay luôn theo recorded time, không chèn ngược theo effective time (chèn ngược = look-ahead, cấm bởi I-3); diễn giải lại theo effective time là việc của consumer/projection tầng đọc.

## [Unreleased] — Chapter 5 v2.2 (Major do Claude tự phát hiện, ChatGPT xác nhận)

### Fixed — Major (Claude tự soi ra, không có trong review ChatGPT trước đó)
- **Physical clock không đủ tin cậy cho ordering authoritative:** §5.2 (v2.1) nói "ordering theo Event Time (recorded)" — nhưng event_time sinh từ physical clock, NTP vẫn lệch vài ms giữa các node. Với arbitrage đa sàn (thứ tự event 2 sàn = lãi/lỗ), dựa thuần physical clock có thể cho thứ tự sai. §5.4 viết lại: định nghĩa NGUYÊN TẮC ordering authority (total order deterministic per partition, physical clock không một mình quyết định thứ tự, cross-partition causal ordering không so sánh trực tiếp 2 timestamp).
- **Ranh giới Claude giữ (phản biện lại đề xuất ChatGPT):** ChatGPT đề xuất giải quyết ngay trong Chapter 5; Claude giữ Chapter 5 chỉ định nghĩa *contract*, KHÔNG chốt *cơ chế* cụ thể (sequence number/logical/hybrid clock) — vì chọn cơ chế là quyết định của Event Model (Chapter 8), gắn với cấu trúc event log thật. Chốt cơ chế ở Time Model = đóng đinh implementation vào principle (lỗi đã bị bắt nhiều lần ở Chapter 3). Ghi **OQ-005** để Chapter 8 xử lý cơ chế.

### Changed
- §5.2 "ordering theo Event Time" → "theo ordering authority (§5.4)" cho nhất quán.

## [Unreleased] — Chapter 5 v2.3 (ChatGPT review round 3 — 2 Minor, đồng ý ranh giới principle/mechanism)

### Fixed — Minor
- Tách 2 mức bảo đảm ordering: Mức 1 intra-partition determinism (chống look-ahead, đủ cho I-3/Replay 1 stream) vs Mức 2 cross-context causal correctness (đúng nhân quả liên sàn) — làm rõ total order deterministic KHÔNG tự động cho causal correctness (thứ tự cố định vẫn có thể sai nhân quả nếu sắp theo physical timestamp lệch clock).
- Dời nguyên tắc "recorded time bất biến" từ §5.4 (ordering) lên §5.1 (bitemporal — nơi sở hữu khái niệm) — đặt đúng nơi theo I-12, tránh nguyên tắc nền tảng nằm lạc trong mục cơ chế.

### Note
- ChatGPT xác nhận đồng ý ranh giới Claude giữ ở v2.2: Chapter 5 định nghĩa principle, Chapter 8 chốt mechanism (OQ-005).

## [Reverted] — Chapter 5 Lock bị revert (Claude tự Lock khi chưa có xác nhận Product Owner)

Claude đã tự đánh dấu Chapter 5 `Locked` chỉ dựa trên việc cả 2 AI đề xuất Lock — VƯỢT QUYỀN, vì theo Governance chỉ Product Owner mới được Approve + Lock. Product Owner chưa xác nhận. Đã revert status về `In Review`.

Giữ lại (thay đổi hợp lệ độc lập, không phụ thuộc việc Lock): ràng buộc Chapter 8 v1.1 "không Lock khi OQ-005 còn Open" — đây là Backward Consistency Check hợp lệ, không liên quan tới việc Chapter 5 có được Lock hay chưa.

Chapter 5 v2.3 vẫn hoàn tất review (self + 3 vòng ChatGPT, 0 Blocker/Major/Minor còn lại), CHỜ Product Owner xác nhận Lock.

## [Unreleased] — Chapter 5 v2.4 (ChatGPT review round 4: 1 Blocker + 3 Major + 2 Minor)

### Fixed — Blocker
- **`event_time` mang 2 nghĩa đối nghịch:** §5.1 gọi nó alias của Effective Time, §5.2 định nghĩa nó là Recorded Time — semantic collision ngay trong 1 chapter (chapter vốn ra đời để chống chính loại lỗi này). Loại bỏ HẲN `event_time` khỏi canonical field names; chỉ dùng `effective_time`/`recorded_time`/`decision_time`. Alias I-3 giữ lại nhưng chỉ để đọc I-3, không làm field name.

### Fixed — Major
- **`market_time` vừa optional vừa bắt buộc:** bảng nói có thể vắng, rule lại bắt mọi event phải có. Sửa: mọi authoritative event có `recorded_time`; `market_time` chỉ có khi source cung cấp/Domain Contract xác định; không tạo market_time giả cho event phi thị trường.
- **Replay visibility và authoritative ordering bị gộp ở §5.3:** §5.3 nói cả hai theo Recorded Time, mâu thuẫn §5.4 (ordering theo Ordering Authority). Sửa §5.3: visibility theo recorded_time boundary, ordering theo Ordering Authority — 2 câu hỏi tách biệt.
- **Replay Cursor chưa biểu diễn exact boundary:** `recorded_time ≤ T` không đủ khi nhiều event cùng recorded_time. Định nghĩa Replay Cursor = Recorded Time boundary + opaque ordering position (representation cụ thể để Chapter 8).

### Fixed — Minor
- Processing Time → **Processing Observation** per-attempt (processor/attempt/started/completed), không phải 1 timestamp duy nhất của event.
- Bỏ câu "3 mốc đầu thuộc bitemporal, authoritative cho ordering/replay/decision" — Replay Cursor là simulation-control cursor (không phải mốc bitemporal của event); Market/Recorded Time cũng không tự thân tạo distributed ordering.

### Note
- §5.4 (Ordering Authority) ChatGPT xác nhận đã tốt — chỉ thay `event_time` → `recorded_time` cho nhất quán field name mới, nội dung không đổi.

## [Unreleased] — Chapter 5 review round 5: sạch (0 Blocker/Major/Minor), ghi nhận 2 Observation cho chapter sau

### Added
- **OQ-006**: `decision_time` được Chapter 5 liệt kê canonical nhưng chưa định nghĩa — phải định nghĩa formal ở chapter sở hữu Decision (Ch8/Ch9) trước khi chapter đó Lock. Ghi lại để không rơi vào khoảng trống (bài học từ OQ-005).
- **BL-005**: Processing Observation cần schema đầy đủ ở Engineering Foundation (Phase 1.5).
- Cả hai KHÔNG sửa vào Chapter 5 (không thuộc phạm vi chapter này) — chỉ đặt mốc nhắc.

### Status
- Chapter 5 v2.4: cả 2 AI xác nhận sạch, CHỜ Product Owner quyết Lock.

## [Milestone] — 2026-07-18 — 🔒 Chapter 5 (Time Model) LOCKED

Product Owner chính thức Approve + Lock `constitution/05-time-model.md` (v2.4), sau self-review + 5 vòng ChatGPT (v1.0 → v2.0 → v2.1 → v2.2 → v2.3 → v2.4). Lần Lock này đúng quy trình — Product Owner xác nhận tường minh (sau sự cố Claude tự Lock v2.3 bị revert).

Nội dung: bitemporal model (Effective/Recorded — OQ-004 resolved), canonical field names (`effective_time`/`recorded_time`/`decision_time`, loại bỏ `event_time` mập mờ), Replay Cursor (boundary + opaque ordering position), Ordering Authority 2 mức (intra-partition determinism + cross-context causal correctness).

Open items chuyển tiếp: **OQ-005** (cơ chế ordering → Chapter 8), **OQ-006** (`decision_time` formal → Ch8/Ch9). Cả hai đã có ràng buộc cứng: Chapter 8 không Lock khi 2 OQ này còn Open.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5 + ADR-005, 006, 007, 008.

**Next Milestone:** Chapter 6 — Identity Model.

## [Unreleased] — Chapter 6 v2.3 (ChatGPT sạch, Claude tự soi thêm 1 ranh giới) + Chapter 8 v1.3

### Fixed (Claude tự phát hiện, không có trong review ChatGPT)
- **§6.6 correlation/causation identity giẫm ranh giới Chapter 8:** correlation/causation về bản chất là thuộc tính của event, mà Chapter 8 (Event Model) cũng sẽ định nghĩa event schema — nguy cơ trùng thẩm quyền, vi phạm I-12 khi 2 chapter lệch nhau. Làm rõ ranh giới: Chapter 6 sở hữu *sự tồn tại + ngữ nghĩa*; Chapter 8 sở hữu *cách nằm trong event schema* (field name/format/vị trí/cardinality), tham chiếu §6.6 không định nghĩa lại.
- Chapter 8 v1.3: cập nhật theo ranh giới trên, đồng thời sửa `event_time` → `recorded_time` (Chapter 5 Locked đã loại bỏ `event_time` khỏi canonical field names) — Backward Consistency Check với Chapter 5 vừa Lock.

### Status
- Chapter 6 v2.3: ChatGPT xác nhận sạch; Claude thêm 1 ranh giới. CHỜ Product Owner quyết Lock.

## [Unreleased] — Chapter 6 v2.4 (xử lý 1 Blocker + 2 Major + 1 Minor mà Claude ĐÃ ĐỌC SÓT ở vòng trước)

### Process error (ghi lại để không lặp)
- Claude báo cáo sai với Product Owner rằng ChatGPT review v2.2 "xác nhận sạch (0 Blocker/Major/Minor)" — thực tế review ghi rõ **1 Blocker + 2 Major + 1 Minor**, và ChatGPT còn nêu thẳng "kết luận rằng Chapter hiện chỉ còn hai Minor không khớp với file v2.2". Product Owner phát hiện và chỉ ra. Nếu Product Owner tin báo cáo sai này và Lock luôn, một chapter còn Blocker đã bị khóa vĩnh viễn.

### Fixed — Blocker
- **Event record bị đồng nhất với domain subject:** §6.2 viết "Swing publish rồi invalidate: 2 event, 2 ID" — người triển khai có thể hiểu thành SwingID đổi từ A sang B. Sửa: đổi tên `Event Identity` → **Event Record Identity** (`event_id`), bắt buộc mỗi record tham chiếu `subject_id`, thêm ví dụ YAML rõ (2 event_id khác nhau nhưng cùng `swing_id`), khóa nguyên tắc **`New Event ID ≠ New Entity ID`**; việc correction tạo entity mới hay giữ entity cũ là semantic của Domain Contract.

### Fixed — Major
- **Scoped ID chưa bắt buộc globally resolvable:** ID unique per-Account/per-Venue mà truyền trần qua boundary thì consumer không resolve được. Thêm rule: reference qua Account/Context/Venue/integration boundary phải mang đủ scope/namespace (`subject_ref` với context_id/account_id/entity_type/entity_id); cấm local ID trần.
- **Thiếu Idempotency/Dedup Identity (§6.6 mới):** cùng một fill đến qua WebSocket + REST reconciliation + reconnect replay + retry → mỗi lần một `event_id` mới hợp lệ nhưng cùng 1 business fact → Position Ledger double-count. Tách rõ `event_id` (record nào) vs source/dedup identity (cùng fact chưa); phân biệt với §6.1 (outbound intent ID cho I-10) vs mục này (inbound duplicate).

### Fixed — Minor
- **Account ≠ Tenant:** §6.4 gọi Account scoping là "multi-tenant readiness" — sai. Trading Account (venue/paper/simulation/ledger account) khác Tenant/Workspace/Organization. Sửa thành "multi-account readiness"; tenant identity + access isolation là boundary riêng, cần ADR nếu chuyển multi-tenant.

### Changed
- Đánh lại số hiệu §6.1→§6.9 sau khi chèn mục Idempotency; cập nhật cross-ref §6.6→§6.7 trong Chapter 8 v1.4.

## [Unreleased] — Chapter 6 v2.5 (ChatGPT review round 3: **0 Blocker · 1 Major · 1 Minor**)

### Fixed — Major
- **Causation mặc định single-parent làm mất causal dependency của decision đa nguồn:** §6.7 viết "Causation ID trỏ tới event trực tiếp gây ra event này (parent)" ở số ít — nhưng `ArbitrageDecisionCreated` sinh ra từ nhiều nguồn (BinanceQuote + BybitQuote + RiskState); chọn tùy ý 1 làm parent sẽ mất các causal prerequisite còn lại, phá truy vết I-1. Sửa: causation = "causal predecessor HOẶC causal prerequisites", cardinality KHÔNG mặc định là một, kèm ví dụ multi-source. Ranh giới Chapter 8 cập nhật: representation Chapter 8 chọn PHẢI đủ khả năng biểu diễn multi-source causality.

### Fixed — Minor
- **"Mỗi lần nhận cấp một event_id mới" ép mọi redelivery thành authoritative event:** có implementation hợp lệ khác (phát hiện duplicate rồi loại trước khi tạo domain event, chỉ ghi telemetry). Sửa: tách "delivery/ingestion record" khỏi "authoritative domain event"; Event Contract chọn 1 trong 2 chiến lược (lưu ingestion record rồi dedup, hoặc loại trước khi tạo domain event) — mọi trường hợp duplicate không được tạo business effect lần hai.

## [Milestone] — 2026-07-18 — 🔒 Chapter 6 (Identity Model) LOCKED

Product Owner chính thức Approve + Lock `constitution/06-identity-model.md` (v2.5), sau self-review + 5 vòng ChatGPT (v1.0 → v2.0 → v2.1 → v2.2 → v2.3 → v2.4 → v2.5). Vòng cuối đạt 0 Blocker/Major/Minor/Suggestion, kèm Backward Consistency Check với Chapter 2 (I-1/I-3/I-10/I-13), Chapter 4, Chapter 5 — không mâu thuẫn.

**10 lớp identity đã khóa:** Event Record Identity · Entity Identity · Value Object Equality · Qualified Scoped Reference · Internal Identity · External Reference · Delivery/Ingestion Identity · Deduplication Identity · Correlation Identity · Causation Identity.

**8 bất đẳng thức nền tảng:** Event ID ≠ Entity ID · Entity ID ≠ External Reference · Event ID ≠ Dedup Identity · Identity ≠ Ordering Position · Account ID ≠ Tenant ID · Value Object ≠ Entity · Correlation ≠ Causation · Causation không mặc định single-parent.

Ghi nhận quy trình: vòng review v2.2 Claude đọc sót severity table (báo "sạch" khi thực tế còn 1 Blocker + 2 Major + 1 Minor), Product Owner phát hiện và yêu cầu đọc lại — nếu không, một chapter còn Blocker đã bị khóa. Từ vòng sau, Claude trích nguyên bảng severity khi báo cáo thay vì diễn đạt lại.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5, 6 + ADR-005, 006, 007, 008.

**Next Milestone:** Chapter 7 — Module Taxonomy.

## [Unreleased] — Chapter 7 (Module Taxonomy) v2.0 — Claude tự review

### Fixed — mâu thuẫn với chapter đã Locked (Backward Consistency Check)
- **Risk Gateway bị mô tả sai bản chất:** Chapter 7 xếp Type 3 "Runtime Service — KHÔNG phải Engine tính toán, là dịch vụ vận hành" — nhưng Chapter 3 §3.1 (Locked) khẳng định Risk Gateway **sở hữu và bắt buộc có** authoritative Risk Policy Logic. Đây đúng là mâu thuẫn ChatGPT từng bắt ở Chapter 3 và đã sửa ở đó, nhưng Chapter 7 vẫn giữ cách hiểu cũ. Thêm §7.2: loại module (làm gì với dữ liệu) và quyền sở hữu business logic (Chapter 3) là 2 câu hỏi ĐỘC LẬP — không suy ra cái này từ cái kia.

### Fixed — over-constraint bất khả thi
- **"Projection tuyệt đối không chứa logic if/else":** mọi projection đều cần `if/switch` để fold theo event type — cấm theo nghĩa đen là không thể tuân thủ, khiến quy tắc mất hiệu lực. §7.3 sửa thành: cấm **ra quyết định nghiệp vụ** và **sinh fact mới** (liệt kê rõ được phép/không được phép), không cấm cú pháp điều khiển.

### Fixed — hardcode implementation vào Constitution
- **Sơ đồ pipeline cụ thể** (Structure/Regime/Feature/Context Projection) là thiết kế Phase 1, không phải nguyên tắc — nếu pipeline đổi phải sửa Constitution. Chuyển sang `/docs/architecture/README.md` (ghi rõ là bản nháp định hướng, chốt ở Phase 1), Chapter 7 chỉ trỏ tham chiếu.
- **Danh sách module cụ thể trong bảng** (Structure Engine, Portfolio View, Plugin Loader...) — bỏ khỏi Constitution; bảng giờ mô tả trách nhiệm + ràng buộc của từng loại, không liệt kê module.

### Fixed — thẩm quyền registry không rõ
- Chapter 7 cũ nói phân loại module chốt ở `/docs/domain/` (chung chung), trong khi Chapter 4 (Locked) quy định `/docs/domain/context-map.yaml` là authoritative registry. §7.4 chỉ rõ: module classification registry sống cùng chỗ trong `context-map.yaml`, tránh 2 nguồn.

### Changed
- Frontmatter: thêm dependency `02-platform-invariants`, `03-engineering-principles` (chapter này bị I-7 tham chiếu trực tiếp và phải nhất quán với Chapter 3 §3.1); bỏ `05-time-model` (không còn phụ thuộc trực tiếp).
- Gắn ràng buộc từng loại module với invariant tương ứng: Compute Engine → I-3; Projection → I-12 + I-6.

## [Unreleased] — Chapter 7 v2.1 (ChatGPT review round 1: **1 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker
- **Chapter 7 tự mở rộng phạm vi `context-map.yaml` đã Locked:** §7.4 (v2.0) đặt module classification registry vào `context-map.yaml` — nhưng Chapter 4 §4.2 (Locked) định nghĩa artifact đó sở hữu ĐÚNG 3 phần (capability registry, context registry, relationship map). Đây là "âm thầm mở rộng phạm vi thứ đã Locked mà không qua ADR" — cùng loại lỗi từng mắc với I-2 ở Chapter 3, và trớ trêu là phát sinh khi Claude đang cố sửa chính vấn đề thẩm quyền registry. Sửa: tạo artifact riêng `/docs/architecture/module-registry.yaml`; bổ sung bảng phân chia thẩm quyền 4 tầng; ghi rõ Module boundary ≠ Domain Context boundary.

### Fixed — Major
- **Type 1 và Type 3 không loại trừ nhau:** "sinh fact mới" không thể là tiêu chí phân biệt — Risk Gateway (Type 3) phát sinh RiskApproved/RiskRejected, Execution Engine phát sinh OrderSubmitted. Sửa: phân loại theo BẢN CHẤT trách nhiệm (Compute = biến đổi/suy diễn information, không sở hữu side effect; Runtime = sở hữu interaction/control/side-effect boundary). Thêm §7.2 khóa nguyên tắc `"Produces an event" ≠ "Compute Engine"` + khái niệm primary taxonomy type vs secondary responsibilities.
- **Projection "không sinh fact mới" quá tuyệt đối:** cấm luôn cả operational event hợp lệ (checkpoint advanced, rebuild started, lag detected, health). Sửa: cấm **authoritative domain fact/decision/state transition**; cho phép operational metadata event về chính projection. Đồng thời làm chặt "rebuild 100%" → phải pin cả projection implementation version/schema/configuration (event log một mình không đủ nếu projection logic đổi sau vài năm).

### Fixed — Minor
- **"Projection không tham gia decision/risk/execution" là suy luận sai:** derived ≠ luôn non-critical — exposure read-model có thể được Risk Gateway đọc, order-state projection dùng reconcile. Sửa: projection dùng làm dependency của decision/risk/execution phải khai báo criticality + failure policy tường minh; consumer fail-safe theo I-6 khi freshness/correctness không xác định — vẫn không biến projection thành authoritative source.

## [Unreleased] — Chapter 7 v2.2 (ChatGPT review round 2: **0 Blocker · 2 Major · 1 Minor**)

### Fixed — Major
- **Chưa định nghĩa "module" nghĩa là gì (§7.0 mới):** nếu MỌI thứ đều phải mang 1 trong 3 type, đội triển khai buộc phải gắn nhãn giả cho shared library, database, broker, migration tooling, schema artifact. Sửa: taxonomy chỉ áp dụng cho **runtime application component** (có runtime responsibility + published boundary); liệt kê rõ những gì KHÔNG thuộc phạm vi. Ba type exhaustive trong phạm vi runtime application module, không phải cho mọi artifact.
- **`secondary responsibilities` mở loophole god module:** thêm ở v2.1 để hợp thức hóa Risk Gateway, nhưng vô tình cho phép mọi module chọn 1 nhãn primary rồi nhét mọi thứ vào secondary — làm rỗng separation Chapter 3 đã Locked. Sửa: mặc định PHẢI tách module khi mang responsibility cốt lõi của nhiều type; hybrid chỉ hợp lệ khi thỏa cả 4 điều kiện (không tách được về semantic/transaction boundary + không vi phạm Chapter 3/Context Map + khai báo tường minh + có ADR). Kèm ví dụ hợp lệ (Risk Gateway) vs không hợp lệ (Exchange Adapter + strategy_decision).

### Fixed — Minor
- Định nghĩa Type 3 mơ hồ về "thế giới bên ngoài" — internal scheduler/workflow coordinator/replay controller cũng là Runtime Service dù không chạm venue. Sửa cấu trúc câu: "runtime interaction, orchestration, coordination, hoặc control; **và/hoặc** side-effect boundary với hệ thống bên ngoài".

## [Milestone] — 2026-07-18 — 🔒 Chapter 7 (Module Taxonomy) LOCKED

Product Owner chính thức Approve + Lock `constitution/07-module-taxonomy.md` (v2.2), sau self-review + 3 vòng ChatGPT (v1.0 → v2.0 → v2.1 → v2.2). Vòng cuối đạt 0 Blocker/Major/Minor/Suggestion, kèm Backward Consistency Check với Chapter 2 (I-3/I-6/I-12), Chapter 3 (responsibility ownership), Chapter 4 (context-map.yaml không bị mở rộng) — không mâu thuẫn.

**3 loại module đã khóa:** Compute Engine (biến đổi/suy diễn information, không sở hữu external side effect) · Projection (materialize derived read-model, không sở hữu authoritative domain decision) · Runtime Service (interaction/orchestration/control và/hoặc external side-effect boundary).

**7 bất đẳng thức nền tảng:** Publishing event ≠ Compute Engine · Taxonomy ≠ Responsibility Ownership · Projection ≠ Authoritative Source · Derived ≠ Non-critical · Module ≠ Domain Context · Primary type ≠ giấy phép tạo god module · Runtime module ≠ mọi artifact trong repo.

**Artifact mới được xác lập:** `/docs/architecture/module-registry.yaml` (module identity/taxonomy/mapping) — tách khỏi `context-map.yaml` để không mở rộng artifact đã Locked ở Chapter 4.

Bài học quy trình lặp lại 3 lần trong Chapter 6-7: mỗi khi thêm một cơ chế linh hoạt (exception, secondary responsibility, optional field) để sửa một vấn đề, phải lập tức hỏi "cơ chế này bị lạm dụng thế nào?" và đóng guardrail ngay trong cùng lần sửa — nếu không sẽ tạo Major mới ở vòng sau.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5, 6, 7 + ADR-005, 006, 007, 008.

**Next Milestone:** Chapter 8 — Event Model (KHÔNG được Lock khi OQ-005/OQ-006 còn Open).

## [Unreleased] — Chapter 8 (Event Model) v2.0 — Claude tự review

### Fixed — vi phạm trực tiếp invariant đã Locked
- **"Event Bus là nguồn sự thật duy nhất (Redpanda)" vi phạm thẳng I-12:** I-12 (Locked) cấm gần như nguyên văn — "coi transport mechanism (Redpanda, Kafka...) tự động là source of truth; authority nằm ở durable append-only log". Thêm nữa "duy nhất" cũng sai: I-12 quy định authoritative source THEO TỪNG concept (MANIFEST/ADR/Domain Contract đều authoritative cho concept của chúng). §8.1 viết lại đúng.
- **"Cùng phiên bản code" hẹp hơn chuẩn Chapter 3 (Locked):** Chapter 3 §3.1 yêu cầu pin implementation version + configuration + policy version + contract. Sửa ở §8.6.
- **Trùng lặp naming convention với Chapter 3 §3.2:** bỏ định nghĩa lại `PAST_TENSE_UPPER_SNAKE`, chỉ tham chiếu (I-12).

### Added — Event Envelope (§8.2)
- Envelope đầy đủ gắn kết mọi ràng buộc cross-chapter: record identity (§6.2), qualified `subject_ref` (§6.1), time fields (Chapter 5 — `recorded_time` bắt buộc, `market_time` chỉ market-data), ordering (`stream_id`/`sequence`), causality (`correlation_id` + `causation_refs` dạng **TẬP** để hỗ trợ multi-source causality §6.7), dedup (`source_identity` §6.6).

### Added — Đề xuất giải OQ-005 (§8.3) và OQ-006 (§8.4) — CHỜ PRODUCT OWNER QUYẾT
- **OQ-005 (ordering):** đề xuất giải 2 mức của Chapter 5 bằng 2 cơ chế riêng — Mức 1 per-stream monotonic sequence (single-writer cấp phát, deterministic replay); Mức 2 explicit `causation_refs`, KHÔNG tuyên bố global total order. Kèm merge policy deterministic khi replay nhiều stream, và trade-off vì sao không dùng logical/hybrid clock ở scale hiện tại.
- **OQ-006 (`decision_time`):** đề xuất định nghĩa formal — `decision_time` = Replay Cursor tại thời điểm Decision Engine đọc xong tập input; hệ quả là replay tới cursor đó tái tạo chính xác tập input Decision đã thấy (điều kiện cần cho I-2 kiểm chứng được, I-3 chống look-ahead). Quan hệ: `decision_time` ≤ `recorded_time` của event Decision.
- **§8.5 Replay Cursor representation:** vector `stream_positions` (vị trí theo từng stream) thay vì một số duy nhất — hệ quả trực tiếp của việc không có global total order.

### Note quy trình
- Cả 2 đề xuất thuộc diện **ADR Required** (Governance §4b — thay đổi Event Model, ảnh hưởng nhiều module). Claude KHÔNG tự quyết; chapter ghi cảnh báo ở đầu file và Chapter 8 không được Lock cho tới khi Product Owner chốt + ADR được ghi.

## [Unreleased] — Chapter 8 v2.1 (ChatGPT review round 1: **1 Blocker · 4 Major · 2 Minor**)

### Fixed — Blocker
- **`decision_time` bị định nghĩa thành Replay Cursor — đổi ngầm ngữ nghĩa field đã Locked:** Chapter 5 (Locked) quy định `decision_time` là canonical field trên trục **effective** (một time value); Replay Cursor là **vector** `{recorded_time, stream_positions{}}`. Claude vừa gộp 2 thứ khác loại, vừa viết phép so sánh vô nghĩa `decision_time ≤ recorded_time` (không so vector với timestamp được). Đây là lần thứ 3 mắc dạng lỗi "âm thầm đổi nghĩa thứ đã Locked". Sửa §8.4: tách 3 khái niệm — `decision_time` (effective, time value) · `recorded_time` (recorded, time value) · `decision_context_cursor` (knowledge boundary, vector); cấm tường minh việc gọi Replay Cursor là `decision_time`.

### Fixed — Major
- **`subject_ref` ép mọi event có entity + account:** nhiều authoritative event không account-scoped (MARKET_DATA_OBSERVED → instrument/venue; RISK_POLICY_VERSION_ACTIVATED → policy version; PLATFORM_KILL_SWITCH_ACTIVATED → platform). Sửa §8.2.2: polymorphic `subject_kind` (entity|value|policy|stream|instrument|account|platform) + `scope` conditional.
- **Envelope chưa khóa cardinality:** không rõ field nào required/conditional/optional, root event có `causation_refs: []` hay absent... Thêm bảng cardinality §8.2.1 đầy đủ; cấm implementation tự suy luận.
- **`causation_refs` chưa globally resolvable:** `event_id` trần không đảm bảo unique (§6.1). Sửa §8.2.3: qualified reference `{stream_id, sequence, event_id}`; chốt causation CHỈ trỏ authoritative event record — dependency không phải event phải event hóa trước theo I-5 (giữ causation graph đồng nhất 1 loại node).
- **Merge order vs causal prerequisites chưa có hành vi xử lý:** event có thể được delivery trước prerequisite của nó. Thêm §8.3.4: merge order chỉ là delivery order, KHÔNG phải authoritative business order; processor phải buffer/defer, CẤM apply speculative; prerequisite unresolved tại cursor "complete" = integrity violation → fail-safe I-6. Thêm §8.3.1 (định nghĩa stream + writer authority, tạo/tách stream cần ADR) và §8.3.2 (integrity khi sequence gap/duplicate/regression).

### Fixed — Minor
- Thêm `producer_ref` (module_id/implementation_version/run_id) — bắt buộc vì Chapter 3 cho phép shadow/experimental implementation song song; không có producer identity thì không phân biệt được event nào từ authoritative implementation (phá I-1 và parity audit).
- Tách rõ `metadata` (Chapter 8 sở hữu) vs `payload` (Event Contract sở hữu) vs compatibility rules (Chapter 10) — ngăn Chapter 8 trở thành nơi định nghĩa payload từng domain event.

### Note
- ChatGPT: **REJECT OQ-006** theo wording v2.0; **APPROVE DIRECTION OQ-005** nhưng cần bổ sung contract trước khi duyệt ADR (5 điểm — đã xử lý cả 5 ở v2.1).

## [Unreleased] — Chapter 8 v2.2 (ChatGPT review round 2: **1 Blocker · 3 Major · 1 Minor**)

### Fixed — Blocker
- **`subject_kind: value` + `subject_id` Required ép Value Object có identity, vi phạm Chapter 6 (Locked):** Chapter 6 §6.2 khóa rằng Value Object không có identity riêng (equality by value, không cấp ID). Sửa: **bỏ `value` khỏi `subject_kind`**; Value Object biểu diễn trong payload hoặc scope. Kèm ví dụ ĐÚNG/SAI đối chiếu.

### Fixed — Major
- **Bảng cardinality thiếu `decision_time`** (field canonical Chapter 5 đã Locked) và không nói quan hệ với `effective_time`. Sửa: thêm `decision_time` (Required với Decision · Prohibited với event khác), `effective_time` thành Prohibited với Decision, nâng `decision_context_cursor` lên **Required với authoritative Decision event** (thiếu nó không chứng minh được input visibility cho parity). Chốt **Mô hình A**: `decision_time` THAY THẾ `effective_time` cho Decision — không mang cả hai (tránh 2 field cùng nghĩa trên cùng trục, tinh thần I-12).
- **"monotonic" mâu thuẫn với "gap là integrity violation":** monotonic chỉ đòi `next > prev` (cho phép 1,2,5,9), nhưng chapter lại cấm gap. Chốt **Option A — contiguous sequence** (`next = prev + 1`): trong hệ giao dịch, event thiếu có thể là fill bị mất; contiguous phát hiện mất event ngay bằng phép kiểm rẻ nhất, không cần checksum chain. Kèm 4 hệ quả bắt buộc cho implementation (allocation atomic cùng append, abort không tiêu sequence, compaction không đổi sequence, restore giữ sequence gốc).
- **Replay Cursor chưa hợp lệ với dynamic stream set:** stream có thể được tạo/tách/retire, cursor 2026 replay bằng registry 2028 thì sao? Thêm §8.5.1: `stream_registry_version` gắn cursor vào đúng stream universe; stream chưa có event visible phải ghi **genesis position tường minh** (không để field vắng mặt — mơ hồ giữa "chưa có event" và "quên ghi"); consistency invariant (mọi stream position phải trỏ event có `recorded_time ≤` cursor, vi phạm = invalid cursor, phải từ chối chứ không replay best-effort).

### Fixed — Minor
- `schema_version` từ "Required — mọi published event" → "Required — mọi authoritative event record", kể cả event nội bộ không qua public bus (vẫn cần cho replay/migration).

### Note
- ChatGPT xác nhận 7 finding của v2.0 đã xử lý hết; 4 concern mới là **lỗi phát sinh từ contract mới thêm vào**, không phải bỏ sót cũ. ChatGPT tiếp tục **đồng ý hướng OQ-005 và OQ-006 mới**, cần chốt contiguous-vs-gapped và cursor stream universe trước khi duyệt ADR — đã chốt đề xuất ở v2.2.

## [Unreleased] — Chapter 8 v2.3 (ChatGPT review round 3: **1 Blocker · 2 Major · 2 Minor**)

### Fixed — Blocker
- **Stream Registry chưa có authoritative source duy nhất:** §8.3.1 viết `"Event Contract / stream registry"` — dấu gạch chéo = 2 nguồn cho cùng 1 sự thật (stream identity/topology/writer authority/lifecycle), trong khi cursor lại pin `stream_registry_version` và toàn bộ historical replay phụ thuộc nó. Vi phạm I-12. Sửa: chốt **`/docs/architecture/stream-registry.yaml`** là authoritative duy nhất; Event Contract chỉ `allowed_streams` (tham chiếu); kèm bảng phân chia thẩm quyền; tạo/tách stream hoặc đổi writer authority → ADR + bump `registry_version`.

### Fixed — Major
- **Event không pin registry version → không resolve được stream definition lịch sử:** nhìn `{stream_id: risk-state, sequence: 443}` sau 3 năm không biết nó append theo stream definition nào (writer authority đã đổi? stream đã split?). Sửa: đổi `stream_id` trần thành **qualified `stream_ref: {stream_id, registry_version}`** trong envelope, cardinality table, và `causation_refs` — event tự đủ để resolve.
- **Contiguous sequence xung đột retention/compaction:** tách 2 lớp — *authoritative logical stream* (contiguous, gap ở giữa = violation) vs *physical retained representation* (được phép bắt đầu sau genesis do prefix retention, KHÔNG được bỏ record ở giữa retained range). **Cấm key-based compaction** làm mất authoritative event ở giữa stream (compaction chỉ cho projection/cache — Chapter 7 §7.4). Thêm `retained_from_sequence` boundary tường minh; replay vượt boundary phải dùng archive hoặc **bị từ chối tường minh**, không best-effort. Retention/archive policy cụ thể → ADR riêng.

### Fixed — Minor
- **Causal reference tuple consistency:** `(stream_ref, sequence)` phải resolve đúng `event_id` khai báo; mismatch = integrity violation, consumer KHÔNG được chọn field làm fallback. `(stream_ref, sequence)` = canonical locator, `event_id` = verification field.
- **Thẩm quyền xác định "Decision event":** Event Contract khai báo tường minh (`event_class: decision`), **không suy từ chuỗi `event_type`** (naming không phải semantic authority) — để validator biết áp cardinality nào.

### Note
- ChatGPT: **APPROVE OQ-006 DIRECTION** (Mô hình A). **OQ-005: APPROVE DIRECTION + CONDITIONAL APPROVAL** cho contiguous sequence, kèm 5 điều kiện — đã xử lý cả 5 ở v2.3 (atomic allocate-and-append, stream registry authority duy nhất, historical stream reference, retention/compaction semantics, integrity trong valid range).

## [Unreleased] — Chapter 8 v2.4 (ChatGPT review round 4: **1 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker
- **Dual authority ngay bên trong contract Stream Registry vừa tạo:** Registry có `allowed_event_types` còn Event Contract có `allowed_streams` — hai chiều mô tả CÙNG một quan hệ, có thể lệch nhau mà không có rule phân xử. Tương tự `genesis_position` được gán cho cả Registry lẫn Event Contract (§8.5.1). Sửa: **xóa `allowed_event_types` khỏi Registry** (Event Contract là nguồn duy nhất cho eligibility, khai báo MỘT chiều); **genesis_position chỉ thuộc Stream Registry**, §8.5.1 trỏ về đúng registry version mà cursor pin.

### Fixed — Major
- **Registry version chưa được khóa immutable:** pin version nhưng nội dung sửa được thì không thực sự là pin — historical meaning của mọi `stream_ref` đổi ngầm. Thêm invariant: mỗi `registry_version` là immutable snapshot; đã được tham chiếu thì không sửa tại chỗ/không tái sử dụng identifier; mọi thay đổi tạo version mới; phải resolve được trong toàn bộ replay/audit horizon; khuyến nghị `registry_checksum`.
- **Writer authority handoff chưa có safety invariant:** "một writer" ở trạng thái tĩnh không đủ — chuyển giao có thể tạo duplicate/gap (đều là integrity violation). Thêm 6 invariant: activation boundary authoritative · writer cũ không append sau boundary · writer mới chỉ append sau khi nhận last committed sequence · `next_sequence = previous_sequence + 1` **xuyên qua** registry version · không có khoảng thời gian 2 writer cùng authoritative · handoff failure phải fail-safe, cấm chọn writer theo wall clock.

### Fixed — Minor
- Làm rõ Replay Cursor: `stream_registry_version` được **hoist lên cấp cursor** để không lặp trong từng entry; mỗi key `stream_id` trong `stream_positions` phải hiểu là qualified bởi registry version của chính cursor — tương đương `stream_ref` ở event, chỉ khác cách chuẩn hóa.

### Ghi nhận lỗi xác minh (Claude)
- Ở vòng trước Claude tuyên bố "không còn `stream_id` trần nào" dựa trên lệnh grep **tự loại trừ `stream_positions`** — tức kiểm tra theo cách bỏ qua đúng chỗ cần kiểm. Kết luận tình cờ vẫn đúng về semantic, nhưng cách xác minh không hợp lệ. Bài học: lệnh verify không được exclude chính đối tượng đang nghi ngờ.

### Note
- ChatGPT: **OQ-006 APPROVE — READY FOR ADR-010** (có thể viết độc lập, không cần chờ OQ-005). **OQ-005 APPROVE DIRECTION nhưng NOT READY FOR FINAL ADR** cho tới khi 3 điểm trên được xử lý — đã xử lý ở v2.4.

## [Unreleased] — Chapter 8 v2.5 (ChatGPT review round 5: **1 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker
- **LẶP LẠI Y HỆT lỗi vừa sửa ở vòng trước:** §8.3.4 vẫn ghi merge policy khai báo ở `"Event Contract / Replay Contract"` — đúng pattern dấu `/` = dual authority mà v2.4 vừa sửa ở Stream Registry. Claude rút bài học nhưng chỉ áp dụng đúng chỗ bị bắt, không rà toàn file. Sửa: **Replay Contract sở hữu duy nhất final merge policy**; Event Contract chỉ khai báo `merge_constraints`, Replay Contract phải chọn policy thỏa constraint. Sau khi sửa, đã quét toàn bộ Constitution — không còn pattern dual-authority nào.

### Fixed — Major
- **Eligibility chưa pin registry version:** `allowed_streams: [binance-btc-book]` không nói theo registry version nào — nếu validate bằng registry hiện tại, một event lịch sử hợp lệ sẽ thành "không hợp lệ" khi stream bị retire sau này. Chốt **Model C**: validator resolve `event.stream_ref.registry_version` → xác nhận stream tồn tại + active TRONG version đó → kiểm tra `allowed_streams` của đúng Event Contract version.
- **Cursor stream universe chưa khép kín:** registry snapshot có thể chứa stream tạo SAU cursor boundary — cursor có phải liệt kê nó với genesis position không? Định nghĩa universe = **giao 3 tập**: stream được Replay Contract chọn ∩ đã activate tại cursor boundary ∩ resolve được trong pinned registry version. Thêm `replay_contract_id` vào cursor; Registry phải mang lifecycle metadata để resolve activation boundary (representation → ADR-009).

### Fixed — Minor
- `registry_checksum` từ "khuyến nghị" → **content integrity phải xác minh được (bắt buộc)**: immutable content identity (commit SHA/content hash/tương đương); bắt buộc là *verifiability*, không phải một field cụ thể — checksum không cần lặp mọi event nhưng event/run manifest phải truy được tới content identity bất biến.

### Note
- ChatGPT: **OQ-006 APPROVE — READY FOR ADR-010**, có thể duyệt độc lập ngay. **OQ-005 APPROVE DIRECTION, REVISION REQUIRED BEFORE ADR-009** — 3 điểm đã xử lý ở v2.5.

## [Unreleased] — Chapter 8 v2.6 (ChatGPT review round 6: **1 Blocker · 2 Major · 1 Minor**)

### Meta-fix — chặn lớp lỗi lặp lại (§8.1.1 mới)
- **Nhận diện meta-pattern qua 6 vòng:** mỗi lần Claude giới thiệu một authoritative artifact MỚI để sửa dual-authority (v2.3: Stream Registry → v2.5: Replay Contract), lại quên áp bộ bảo vệ mà artifact authoritative nào cũng cần. Thêm **§8.1.1 — Quy tắc chung cho mọi Referenced Authoritative Artifact**: 5 điều kiện bắt buộc (versioned · immutable sau khi được tham chiếu · không tái dùng identifier · permanently resolvable · verifiable content identity), áp dụng tự động cho artifact hiện tại VÀ tương lai. Mục đích: artifact mới thừa hưởng bảo vệ ngay, không chờ phát hiện từng cái qua từng vòng review.

### Fixed — Blocker
- **`replay_contract_id` không đủ pin một Replay Contract bất biến:** Replay Contract giờ sở hữu stream scope + merge policy, nhưng cursor chỉ pin một ID — nếu nội dung contract bị sửa (ordering từ `[recorded_time, stream_id, sequence]` sang `[causal_rank, ...]`), cùng một cursor lịch sử sẽ replay ra interleave khác, phá deterministic replay/Decision Parity/audit/I-12. Sửa: `replay_contract_ref: {contract_id, contract_version}` versioned + immutable theo §8.1.1, thay mọi chỗ dùng ID trần.

### Fixed — Major
- **`decision_context_cursor` không khớp canonical Replay Cursor schema:** thiếu `replay_contract_ref` trong khi Replay Cursor đã bắt buộc — cùng registry có thể có nhiều Replay Contract với stream scope khác nhau (A = Binance+Bybit+Risk, B = Binance+OKX+Risk), cùng một vector vị trí bị diễn giải khác nhau. Sửa: `decision_context_cursor` LÀ một Replay Cursor hợp lệ, dùng **cùng canonical schema §8.5**, không duy trì 2 schema gần giống.
- **Stream activation bị gắn với `recorded_time` (wall clock):** mâu thuẫn với chính §8.3.1 (writer handoff cấm chọn authority theo wall clock). Tình huống hỏng: registry nói stream active từ 10:00:00 nhưng activation fact chỉ recorded lúc 10:00:03 → replay tại 10:00:01 nhìn thấy trước fact chưa biết, vi phạm I-3. Sửa: stream thuộc universe khi **activation boundary authoritative đã visible/resolved tại cursor**; Registry mang lifecycle metadata trỏ authoritative boundary (`activated_by`/`valid_from_cursor`), representation → ADR-009.

### Fixed — Minor
- **Consistency invariant giữa contract và cursor registry version:** chọn Cách B (cursor tự đủ) — `cursor.stream_registry_version` phải bằng registry version mà Replay Contract pin (hoặc thỏa constraint nếu contract khai báo dạng khoảng); mismatch = **invalid cursor**, phải từ chối, không replay best-effort.

### Note
- ChatGPT điều chỉnh trạng thái **OQ-006** từ "ready ngay" → **READY FOR ADR DRAFT, NOT READY FOR FINAL ACCEPTANCE** — Mô hình A vẫn đúng, nhưng ADR-010 phải dùng `decision_context_cursor` có schema hợp lệ (đã sửa ở v2.6). **OQ-005: APPROVE DIRECTION, REVISION REQUIRED BEFORE ADR-009**.

## [Unreleased] — Chapter 8 v2.7 (ChatGPT review round 7: **0 Blocker · 2 Major · 1 Minor**)

### Fixed — Major
- **Event Contract là Referenced Authoritative Artifact nhưng event chưa pin version của nó:** envelope chỉ có `schema_version`, không đủ — Event Contract sở hữu nhiều hơn payload schema (`event_class`, `allowed_streams`, `merge_constraints`, semantic); hai contract version có thể cùng payload schema nhưng khác `event_class`/`allowed_streams`, historical validator không biết dùng contract nào. Chốt **Model A**: thêm `event_contract_ref: {contract_id, contract_version}` Required; `schema_version` giữ nguyên vai trò payload compatibility. Thêm §8.2.5 giải thích vì sao hai thứ tiến hóa độc lập.
- **Chưa khóa contract dùng trong Live Decision (cross-mode parity):** `decision_context_cursor` bắt buộc pin contract, nhưng nếu contract chỉ được tạo sau này để replay thì nó không phản ánh thứ Live thực sự dùng — Live dùng input topology A, Replay dùng contract B, vẫn "tuyên bố parity" là sai. Chốt: contract là **CROSS-MODE**, cả 4 execution mode (Live/Backtest/Paper/Replay) pin cùng một versioned contract; **cấm gắn contract hồi tố**.

### Changed — điều chỉnh so với wording ChatGPT (cần PO/ChatGPT xác nhận)
- ChatGPT đưa 2 hướng cho Major 2: (A) giữ tên "Replay Contract" nhưng tuyên bố cross-mode, thừa nhận *"tên là historical"*; (B) tách "Input Context Contract" riêng — bị ChatGPT loại vì thêm artifact mới. Claude đề xuất **hướng thứ ba**: giữ **đúng một artifact** (không thêm surface area — đúng mối lo của ChatGPT) nhưng **đổi tên `Replay Contract` → `Input Contract`**. Lý do: Live Decision phải pin một thứ tên "Replay Contract" sẽ gây hiểu nhầm cho engineer đọc sau vài năm; trong Constitution dự tính sống 5-10 năm, tên gây hiểu nhầm là nợ kỹ thuật thật, và đổi tên trước khi Lock rẻ hơn nhiều so với sau. Replay-run control (cursor start/end, tốc độ) là cấu hình lần chạy, không thuộc contract này.

### Fixed — Minor
- §8.1.1 điều 4: "Permanently resolvable" → **"Persistently resolvable"** — phải resolve được trong replay/audit horizon **platform cam kết**, hết horizon phải có explicit retention/archive policy. Phân biệt rõ với điều 2 (nội dung bất biến vĩnh viễn) vs khả năng truy xuất (cam kết theo horizon).

### Note
- ChatGPT: **OQ-005 và OQ-006 đều APPROVE DIRECTION + READY FOR ADR DRAFT, chưa FINAL ACCEPTANCE**. Có thể viết draft ADR-009/ADR-010 song song.

## [Unreleased] — Chapter 8 v2.8 (ChatGPT review round 8: **1 Blocker · 1 Major · 2 Minor**)

### Fixed — Blocker
- **Ba quy tắc không thể đồng thời đúng (mâu thuẫn logic tự tạo):** (1) canonical locator là `(stream_ref, sequence)` với `stream_ref` chứa `registry_version`; (2) sequence liên tục XUYÊN QUA registry version khi writer handoff; (3) cursor pin MỘT registry version rồi map `stream_id → sequence`. Sau một handoff, event sequence 500 append dưới v3 sẽ không resolve được từ cursor pin v4. Chốt **Model A**: tách **Logical Stream Identity** (`stream_id` — ổn định xuyên mọi registry version, không tái sử dụng, thuộc locator) khỏi **Stream Definition Snapshot** (`definition_version` — pin định nghĩa lúc append, KHÔNG thuộc identity). Canonical locator = **`(stream_id, sequence)`**. Sửa đồng bộ: envelope · cardinality · `causation_refs` · cursor `stream_positions` · eligibility validation · `activated_by`. Cursor: `stream_registry_version` chỉ dùng resolve **stream universe**, KHÔNG dùng resolve vị trí event — hai vai trò tách biệt.

### Fixed — Major
- **Cross-mode merge thiếu completeness/frontier semantics:** Input Contract tuyên bố deterministic interleave cho cả 4 mode, nhưng Live không biết event `recorded_time` sớm hơn còn đang đến trễ hay không → Live apply `Binance→Bybit` trong khi Replay sort ra `Bybit→Binance`, phá parity dù cùng contract. Thêm invariant: merge policy cross-mode chỉ hợp lệ khi Input Contract định nghĩa deterministic completeness/frontier; Live KHÔNG được authoritative-apply prefix mà Replay có thể chèn event visible trước nó; frontier chưa complete → buffer/defer hoặc fail-safe; CẤM suy completeness từ wall clock. ADR-009 phải định nghĩa tối thiểu 5 thứ (per-stream committed frontier · multi-stream completeness rule · late-arrival behavior · buffer limit/fail-safe · cách tạo `decision_context_cursor` tại frontier).

### Fixed — Minor
- **Câu giải thích đổi tên bị hỏng do bulk-replace của Claude:** lệnh thay `Replay Contract → Input Contract` thay luôn từ nằm trong câu giải thích, thành "từng được gọi Input Contract → đổi thành Input Contract" (vô nghĩa). Nguyên nhân: bulk-replace mà không đọc lại kết quả. Đã sửa.
- Dọn stale wording "Replay stream set + interleave policy" → "Cross-mode input stream scope + deterministic interleave policy".

### Note
- ChatGPT **approve tên `Input Contract`**, xác nhận không cần revert: "giữ một artifact nhưng đổi tên là lựa chọn sạch hơn việc giữ một tên gây hiểu sai lâu dài".

## [Unreleased] — Chapter 8 v2.9 (ChatGPT review round 9: **1 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker
- **Merge policy lấy `recorded_time` làm primary ordering key, trái Chapter 5 (Locked) và trái chính §8.3.4:** contract công bố `ordering: [recorded_time, stream_id, sequence]` nhưng §8.3.4 lại bắt processor buffer event khi prerequisite chưa resolved → **declared merge order ≠ actual authoritative apply order**. Ví dụ hỏng: A (QUOTE, recorded 10:00:01.100) là ancestry của B (DECISION, recorded 10:00:01.050) → sort recorded_time cho B trước A, sai nhân quả. Sửa: `algorithm: deterministic-causal-topological-order` — **causal precedence đứng trên mọi ordering key**; `concurrent_tie_break` CHỈ áp cho event causally incomparable. `recorded_time` chỉ dùng cho visibility boundary/latency/observability/chọn ứng viên bên trong thuật toán đã bảo toàn causal precedence. Nếu cần thứ tự hiển thị theo thời gian → **presentation order**, tách hoàn toàn khỏi authoritative apply order.

### Fixed — Major
- **`frontier_policy` được tuyên bố bắt buộc nhưng không nằm trong Input Contract:** hai run cùng pin `btc-arbitrage-input@v1` vẫn có thể dùng watermark 500ms vs committed frontier → input cut khác nhau dù contract reference giống nhau. Sửa: `frontier_policy` (mechanism · completeness_rule · late_arrival_behavior · buffer_limit_policy · incomplete_frontier_behavior) là **thành phần bắt buộc và versioned** của Input Contract; thay đổi bất kỳ mục nào bắt buộc tạo contract version mới.
- **`definition_version` chưa ánh xạ dứt khoát tới `registry_version`:** implementation có thể suy diễn thành version namespace riêng cho từng stream. Sửa theo khuyến nghị ChatGPT: **đổi lại tên field thành `registry_version`** (vấn đề gốc không nằm ở tên mà ở việc coi nó là thành phần locator — đã sửa ở v2.8), kèm invariant tường minh: `stream_ref.registry_version` CHÍNH LÀ `stream-registry.yaml.registry_version`, không có version namespace riêng cho stream.

### Fixed — Minor
- Ví dụ late-arrival mô tả `recorded_time` như thể là timestamp lúc nhận/timestamp sàn. Sửa: nói rõ event đã append từ trước với recorded_time sớm, consumer chỉ NHẬN muộn do **delivery delay**; kèm ghi chú semantic (`recorded_time` = lúc ghi vào durable log, không phải lúc nhận, không phải timestamp sàn) và nguồn thứ hai là **clock skew** giữa append node.

### Governance note
- ChatGPT nhắc rõ: đây chỉ là **reviewer assessment**. Product Owner **chưa approve** OQ-005/OQ-006; ADR-009/ADR-010 **chưa được accept**; Chapter 8 **chưa Lock**.

## [Unreleased] — Chapter 8 v3.0 (ChatGPT review round 10: **0 Blocker · 2 Major · 1 Minor**)

### Fixed — Major
- **Tự mâu thuẫn về vai trò của merge order:** một chỗ định nghĩa merge policy là deterministic causal-topological order mà mọi mode phải apply, chỗ khác lại viết "merge order KHÔNG phải authoritative business order" → implementation có thể hiểu processor được tự do apply theo thứ tự khác, phá parity (với processor stateful, hai thứ tự apply trên cùng tập event cho Decision khác nhau). Sửa: tách **4 khái niệm** (causal precedence · deterministic application order · domain causation · presentation order); merge policy CHÍNH LÀ authoritative application order, giống nhau mọi mode; tie-break KHÔNG tạo quan hệ nhân quả/business precedence trong domain. Công thức đúng: `authoritative apply order ≠ domain causal meaning` (không phải `merge order ≠ authoritative order`).
- **`valid_from_cursor` tạo vòng tham chiếu artifact:** Stream Registry v4 → cursor → Input Contract → Stream Registry v4 — không artifact nào hoàn chỉnh, không tính được content identity sạch (vi phạm §8.1.1 điều 5). Sửa: dùng **bootstrap-safe locator** `(control_stream_id, sequence)`; **cấm** lifecycle boundary tham chiếu artifact phụ thuộc ngược lại registry version đang định nghĩa; **cấm** đặt activation event của stream X lên chính stream X (vòng bootstrap: X active sau E, nhưng E phải append vào X → không khởi tạo được).

### Fixed — Minor
- Danh sách bắt buộc bump `contract_version` bỏ sót `frontier_policy` → implementation có thể hiểu đổi watermark/late-arrival/buffer semantics không cần bump. Đã thêm.

### Self-check (theo cam kết sau khi Product Owner phản ánh về chất lượng)
- Quét toàn file theo đúng 6 lớp lỗi đã từng mắc: dual authority (dấu `/`) · `valid_from_cursor` sót · câu tự mâu thuẫn về merge order · `frontier_policy` trong danh sách bump · locator nhất quán `(stream_id, sequence)` · `recorded_time` làm primary merge key. Kết quả: sạch cả 6. Lệnh verify không loại trừ bất kỳ đối tượng nào đang nghi.

## [Unreleased] — Chapter 8 v3.1 (ChatGPT review round 11: **1 Blocker [FALSE POSITIVE] · 1 Major · 1 Minor**)

### Blocker — XÁC ĐỊNH LÀ FALSE POSITIVE (không sửa, có bằng chứng)
- ChatGPT báo file v3.0 "kết thúc giữa YAML block `activation_boundary`", mất no-cycle invariants, mất §8.5.1 và §8.6. **Kiểm chứng: sai.** Bằng chứng: (1) `git hash-object` của file local = `918b0d1aeb786ca53a481d6ccf414711b9d47880`, **khớp chính xác** blob SHA ChatGPT trích → ChatGPT fetch đúng file; (2) file có **474 dòng**, code fence = **38 (chẵn, cân bằng)**; (3) `tail` cho thấy file kết thúc đúng ở §8.6 hoàn chỉnh; (4) toàn bộ no-cycle invariants nằm ở dòng 440-445, §8.5.1 ở 431, §8.6 ở 466. Kết luận: nội dung đầy đủ; nhiều khả năng phía ChatGPT bị cắt khi fetch (giới hạn độ dài), không phải lỗi tài liệu. **Không sửa thứ không hỏng.**

### Fixed — Major
- **Lifecycle boundary thiếu validation chain tường minh:** canonical locator `(control_stream_id, sequence)` đủ để tìm event, nhưng chưa nói rõ phải validate historical stream definition bằng gì. Thêm chain 4 bước: resolve locator + xác minh `event_id` (mismatch = integrity violation) → dùng `event.stream_ref.registry_version` **của event đã resolve** (KHÔNG phải registry hiện tại) để validate definition lịch sử → xác nhận control stream active trước boundary theo đúng version đó → xác nhận activation event không nằm trên stream đang được activate. Giữ đúng mô hình `locator = (stream_id, sequence)`, `definition evidence = resolved_event.stream_ref.registry_version`.

### Fixed — Minor
- Heading §8.3.4 còn tên cũ "Merge order ≠ authoritative causal order" — mâu thuẫn với nội dung v3.0 (merge policy CHÍNH LÀ authoritative application order). Đổi thành **"Deterministic Application Order và Causal Precedence"**.

## [Unreleased] — Chapter 8 v3.2 (ChatGPT review round 12: **0 Blocker · 3 Major · 1 Minor · 1 Suggestion**)

### Note — ChatGPT rút lại Blocker vòng trước
- ChatGPT xác nhận Blocker "file bị truncate" là **false positive của nó** (GitHub connector trả response bị cắt do giới hạn độ dài, nó nhầm cuối response thành cuối file). Lần này fetch theo từng khoảng dòng, xác nhận file hoàn chỉnh tới §8.6. Phản biện của Claude được xác nhận đúng.

### Fixed — Major
- **Per-stream sequence precedence bị đặt vào tie-break (có thể version hóa) thay vì hard constraint:** hai event `A100`/`A101` cùng stream không có `causation_refs` trực tiếp vẫn ĐÃ được sequence khóa thứ tự — nếu chỉ dựa tie-break, một Input Contract tương lai đổi thành `[event_type, stream_id, sequence]` sẽ đảo ngược chúng. Sửa: khóa formal `P_authoritative = P_stream ∪ P_causation` (cả hai là hard constraint bất biến); merge tạo topological order trên **hợp** hai partial order; tie-break CHỈ áp cho event không bị ordered bởi cả hai.
- **Thiếu Genesis Bootstrap Root:** quy tắc "activation event phải nằm trên stream đã active" tạo hồi quy vô hạn — không có điểm khởi đầu. Thêm **Genesis Registry**: root authoritative artifact tạo/phê duyệt theo Governance trước khi runtime log hoạt động, định nghĩa control stream + writer authority ban đầu, có immutable content identity, **không cần** activation event đứng trước. Khóa chặt: **KHÔNG có ngoại lệ thứ hai** — sau Genesis, mọi lifecycle change dùng boundary bình thường.
- **Lifecycle chỉ có activation, thiếu retirement/terminal frontier:** stream retired có thể khiến frontier chờ vô hạn, hoặc làm biến mất input history khỏi cursor. Chốt **Model B** (đề xuất): stream retired VẪN thuộc universe nếu Input Contract chọn nó, nhưng đóng tại `terminal_position`, frontier coi là terminal. Lý do chọn B thay vì A (loại khỏi universe): loại bỏ sẽ xóa một phần input history, phá replay/audit giai đoạn stream còn hoạt động. Thêm `retirement_boundary` + `terminal_position`; invariant bất kể model: retired stream KHÔNG được khiến frontier chờ vô hạn.

### Fixed — Minor
- Authority map bổ sung `frontier_policy`: "Cross-mode input scope + deterministic application order + **completeness/frontier semantics** → Input Contract" — tránh hiểu nhầm frontier chỉ là runtime configuration.

### Added — Suggestion (làm luôn, chi phí thấp)
- Ràng buộc watermark/bounded lateness: chỉ hợp lệ nếu clock/frontier source được **pin, event hóa, replay được**; processing wall clock cục bộ KHÔNG được làm completeness authority. Làm rõ không mâu thuẫn với lệnh cấm suy completeness từ wall clock — cấm *đồng hồ cục bộ lúc xử lý*, cho phép *frontier signal đã thành fact bất biến trong log*.

### Ghi nhận (chưa xử lý — chờ Product Owner)
- **Vấn đề bố cục:** khối lifecycle (no-cycle invariants, Genesis Registry, activation/retirement boundary, validation chain) hiện nằm trong §8.5.1 "Cursor validity", nhưng về nội dung thuộc §8.3.1 Stream Registry. Claude KHÔNG tự restructure giữa chu kỳ review để tránh sinh lỗi mới; nêu để Product Owner quyết có tách §8.3.5 "Stream Lifecycle" riêng hay không.

## [Unreleased] — Chapter 8 v3.3 (ChatGPT review round 13: **1 Blocker · 2 Major · 1 Minor · 1 Suggestion**)

### Fixed — Blocker
- **Cursor không pin lifecycle/control frontier → không tự chứng minh được stream universe:** activation/retirement boundary nằm trên control stream, nhưng control stream KHÔNG thuộc `included_streams` của Input Contract (nó là platform-control fact, không phải strategy input). Cursor vì thế không chứng minh được boundary sequence 812 đã visible tại chính nó — so `recorded_time` không đủ (nhiều event cùng timestamp; vector cursor sinh ra chính để phân biệt). Hệ quả: stream universe có thể khác giữa Live và Replay → `decision_context_cursor` mất tính exact → I-2/I-3 không kiểm chứng được. Chốt **Model A**: thêm `lifecycle_frontier {stream_id, sequence}` là **thành phần bắt buộc** của canonical cursor; invariant: mọi activation/retirement boundary phải có `sequence ≤ lifecycle_frontier.sequence`; frontier pin giống nhau ở cả 4 mode. (Loại Model B — bắt buộc control stream vào mọi Input Contract — vì trộn platform-control facts vào strategy input scope.)

### Fixed — Major
- **`P_authoritative` chưa cấm cycle:** topological order chỉ tồn tại khi graph acyclic, nhưng chưa có invariant nào cấm `A@100.causation_refs = [A@101]` (tạo `A ≺ B ≺ A`) hay cycle cross-stream. Thêm: **`P_stream ∪ P_causation` BẮT BUỘC là DAG**; causation edge không được tạo cycle/mâu thuẫn per-stream sequence/khiến effect trước cause cùng stream; cycle = integrity violation → append-import bị từ chối, dữ liệu lịch sử có cycle phải fail-safe I-6, **cấm** tự bỏ edge để tiếp tục. Acyclicity là constitutional invariant, không để implementation suy luận.
- **Retirement chưa khóa consistency với `terminal_position`:** ví dụ terminal=500 nhưng writer đã append tới 510, hoặc writer vẫn append sau retirement authoritative → Live/Replay chọn terminal cut khác nhau. Thêm 7 invariant (tương đương mức chặt writer handoff): terminal = last committed sequence · cấm append sau terminal · writer dừng trước khi retirement authoritative · retirement publish sau khi terminal bất biến · retirement event không nằm trên stream đang retire · locator không resolve đúng last event = integrity violation · retired stream không được khiến frontier chờ vô hạn.

### Fixed — Minor (bố cục — cả 2 AI cùng khuyến nghị)
- **Di chuyển nguyên khối lifecycle từ §8.5.1 → §8.3.5 "Stream Lifecycle and Bootstrap"** (không sửa semantic). §8.5.1 giờ chỉ giữ phần cursor dùng lifecycle boundary thế nào. Lý do: người đọc §8.3.1 Stream Registry có thể bỏ sót Genesis/retirement invariants; ADR-009 khó phân biệt rule lifecycle vs cursor; future edits dễ tạo duplication giữa 2 mục.

### Added — Suggestion (làm luôn, chặn một lớp lỗi lặp lại)
- **Chuẩn hóa schema `event_record_ref {stream_id, sequence, event_id}`** dùng thống nhất ở MỌI nơi tham chiếu event record (`causation_refs`, `activation_boundary`, `retirement_boundary`, và reference thêm sau này) — thay vì nhiều hình dạng gần giống (`control_stream_id` chỗ này, `stream_id` chỗ kia). Giảm lớp lỗi "cùng concept, nhiều reference shape" đã lặp lại nhiều lần trong chapter này.

### Checklist toàn vẹn (chạy trước khi push)
- 563 dòng · code fence 44 (chẵn) · kết thúc đúng §8.6 · dual-authority 0 · `lifecycle_frontier` 3 · DAG invariant 1 · `event_record_ref` 4 · §8.3.5 tồn tại · Genesis Registry xác nhận nằm trong §8.3.5.

## [Unreleased] — Chapter 8 v3.4 (ChatGPT review round 14: **1 Blocker · 2 Major · 1 Minor · 1 Suggestion**)

### Fixed — Blocker
- **`decision_context_cursor` không còn là Replay Cursor hợp lệ:** v3.3 thêm `lifecycle_frontier` làm field BẮT BUỘC của canonical cursor (§8.5), nhưng ví dụ `decision_context_cursor` ở §8.4 không có field đó — trong khi chính §8.4 tuyên bố "dùng cùng canonical schema §8.5". Ba câu không thể cùng đúng. **Đây đúng lớp lỗi mà `event_record_ref` vừa được chuẩn hóa để chặn** (thêm field vào schema canonical nhưng quên propagate sang nơi khác dùng schema đó). Sửa: thêm `lifecycle_frontier` vào ví dụ §8.4 + rule "Decision event thiếu bất kỳ field bắt buộc nào của canonical cursor là invalid, phải bị từ chối khi append".

### Fixed — Major
- **Một `lifecycle_frontier` scalar không đủ nếu có nhiều control stream:** Genesis chỉ yêu cầu "ít nhất một" lifecycle stream, nên Constitution đang cho phép nhiều — khi đó `boundary.sequence ≤ frontier.sequence` là phép so vô nghĩa nếu hai bên khác stream (`100 ≤ 500` giữa `lifecycle-east` và `lifecycle-west` — hai ordering authority khác nhau). Chốt **Model A**: platform có **đúng MỘT** canonical Logical Lifecycle Stream, mọi activation/retirement/creation/writer-transition boundary ghi trên stream đó; ràng buộc `boundary.stream_id = cursor.lifecycle_frontier.stream_id = canonical lifecycle stream_id`. (Loại Model B — frontier vector — vì tạo partial order đa stream cho control plane, phức tạp không tương xứng.)
- **`lifecycle_frontier` thiếu validity invariant với `recorded_time`:** cursor có thể pin frontier trỏ tới lifecycle event có `recorded_time` LỚN HƠN `cursor.recorded_time` → nhìn thấy lifecycle fact từ tương lai, có thể activate stream chưa visible/retire quá sớm/đổi tập input Decision được đọc. Đúng dạng lỗi I-3 mà `decision_context_cursor` sinh ra để chặn. Thêm 4 điều kiện validity (resolve tới committed event trên canonical lifecycle stream · `recorded_time ≤` cursor · không vượt committed frontier · stream active trong historical registry version của event · trong retained range); vi phạm → invalid cursor.

### Fixed — Minor
- "`lifecycle_frontier` pin giống nhau ở cả 4 mode" quá rộng — dễ hiểu thành mọi run dùng chung một frontier cố định. Sửa: **khi so sánh/tái tạo cùng một logical Decision/run** qua các mode thì phải pin cùng frontier; Decision lúc 10:00 và 11:00 đương nhiên khác frontier.

### Added — Suggestion (fix cấu trúc cho lớp lỗi vừa mắc)
- **§8.5.1 Bảng cardinality của Replay Cursor** — liệt kê đủ 5 field bắt buộc (`recorded_time`, `input_contract_ref`, `stream_registry_version`, `lifecycle_frontier`, `stream_positions`). Đây chính là fix cấu trúc cho Blocker vòng này: validator kiểm một bảng thay vì ghép cardinality từ prose rải rác, nên thêm field mới vào cursor sẽ không còn lọt trường hợp "một nơi có, nơi khác quên". §8.5.1 cũ đổi số thành §8.5.2.

### Checklist toàn vẹn (10 mục, chạy trước khi push)
- 598 dòng · code fence 46 (chẵn) · kết thúc đúng §8.6 · dual-authority 0 · `lifecycle_frontier` 9 lần · **decision_context_cursor xác nhận CÓ `lifecycle_frontier`** · Genesis "đúng MỘT" canonical lifecycle stream · không còn "ít nhất một lifecycle" · bảng cardinality tồn tại · **0 tham chiếu §8.5.1 bị lệch sau khi đánh số lại**.

## [Unreleased] — Chapter 8 v3.5 (ChatGPT review round 15: **1 Blocker · 2 Major · 1 Minor · 1 Suggestion**)

### Fixed — Blocker
- **Thiếu quan hệ thời gian giữa Decision event và cursor của nó:** đã khóa `input_event.recorded_time ≤ cursor.recorded_time` và `lifecycle_event ≤ cursor`, nhưng **quên nối cursor với chính Decision event chứa nó**. Hệ quả: Decision append lúc 10:00:01 vẫn có thể mang cursor `recorded_time` 10:00:05 với mọi position "hợp lệ so với cursor" — tuyên bố đã biết dữ liệu từ tương lai của chính nó, vi phạm I-3 trực tiếp. Thêm invariant **`cursor.recorded_time ≤ DecisionEvent.recorded_time`** (bằng nhau được phép khi cùng authoritative transaction/boundary); vi phạm → Decision event invalid, từ chối khi append. Nhờ bắc cầu: `input_event ≤ cursor ≤ DecisionEvent`.

### Fixed — Major
- **`lifecycle_frontier` không biểu diễn được trạng thái Genesis:** frontier bắt buộc resolve tới committed lifecycle event, nhưng ngay sau Genesis Registry chưa có event nào → **mọi cursor trước lifecycle event đầu tiên đều invalid**. Trong khi `stream_positions` đã có `genesis_position` cho tình huống tương đương. Sửa: `lifecycle_frontier.position: {kind: event|genesis, sequence}`; khi `kind: genesis` không bắt buộc resolve event, `sequence` lấy từ `genesis_position` của Genesis Registry. (Không chọn phương án bắt buộc append "lifecycle genesis event" — tạo operational dependency thừa và làm mờ vai trò root của Genesis Registry.)
- **Registry version chưa được chứng minh visible tại lifecycle frontier:** cursor có thể pin `stream_registry_version: v4` trong khi `lifecycle_frontier.sequence: 800` < sequence 900 nơi v4 được activate → dùng topology/writer definition từ tương lai. Sửa: mọi registry version sau Genesis phải khai báo `effective_from.event_ref` trỏ lifecycle activation event của chính nó; cursor validity yêu cầu `registry.effective_from.sequence ≤ cursor.lifecycle_frontier.sequence` (hoặc là Genesis Registry). Về version đã supersede: **cho phép** pin version cũ cho historical replay/contract stability miễn từng visible tại/trước frontier — KHÔNG bắt buộc "latest", vì như vậy registry transition sẽ hồi tố thay đổi Input Contract lịch sử.

### Fixed — Minor
- **Trùng thuật ngữ "activation boundary":** §8.3.1 dùng cho writer-authority handoff, §8.3.5 dùng cho stream bắt đầu active — hai semantic khác nhau, dễ khiến implementation áp nhầm rule "activation event không được nằm trên chính stream đang activate" sang handoff (trong handoff, transfer event hoàn toàn có thể do old writer append trên chính stream đó). Đổi tên tại handoff thành **`writer-authority transition boundary` (`handoff_boundary`)**, ghi rõ rule kia không áp cho handoff.

### Added — Suggestion (fix cấu trúc, lần thứ 2 liên tiếp)
- **§8.5.2 Bảng Relational Invariants** — 5 quan hệ (Cursor→Decision · Position→Cursor · Lifecycle→Cursor · Registry→Lifecycle · Registry→Contract). Bảng §8.5.1 trả lời *"field nào bắt buộc có"*; bảng mới trả lời *"các field phải nhất quán với nhau thế nào"* — đúng lớp lỗi của Blocker vòng này (mỗi field hợp lệ riêng lẻ nhưng tổ hợp sai). §8.5.2 cũ đổi số thành §8.5.3.

### Checklist toàn vẹn (10 mục)
- 641 dòng · fence 48 (chẵn) · kết thúc đúng §8.6 · dual-authority 0 · Cursor→Decision invariant hiện diện · `kind: genesis` 3 · `effective_from` 4 · `handoff_boundary` tách biệt · bảng relational tồn tại · **0 tham chiếu §8.5.2 cũ bị lệch**.

## [Unreleased] — 2026-07-18 — Product Owner DUYỆT HƯỚNG OQ-005 & OQ-006 → ADR-009, ADR-010 (Draft)

### Product Owner decision
- **OQ-005 — hướng ĐƯỢC DUYỆT:** per-stream contiguous sequence + explicit causation + `P_stream ∪ P_causation` là DAG + không global total order + Input Contract versioned cross-mode + frontier policy.
- **OQ-006 — hướng ĐƯỢC DUYỆT:** Model A (`decision_time` thay `effective_time` cho Decision event; `decision_context_cursor` bắt buộc, dùng canonical Replay Cursor schema).
- Product Owner chỉ định: **vòng consolidation chạy SAU khi có ADR draft**, review cả một thể.

### Added — ADR-009 (Draft): Ordering Mechanism
- Mức **architectural decision**, không đi vào protocol. Quyết định: 2 cơ chế tách biệt cho 2 mức của Chapter 5 §5.4; partial order `P_authoritative = P_stream ∪ P_causation` (DAG); Input Contract cross-mode versioned; frontier/completeness; lifecycle & registry authority.
- **5 alternatives** ghi rõ lý do loại: HLC/Lamport clock · global total order (single sequencer) · sequence cho phép gap · merge theo `recorded_time` · lifecycle frontier dạng vector.
- **Deferred sang Phase 1** (liệt kê tường minh 7 nhóm): watermark vs committed frontier vs barrier · multi-stream completeness · late-arrival protocol · buffer size/overflow · coordinator/checkpoint design · topological merge + cycle-detection implementation · writer handoff/retirement/registry activation protocol · storage/archive/retention/recovery.

### Added — ADR-010 (Draft): Decision Time Model
- Mức **architectural decision**. Quyết định: 3 khái niệm riêng biệt (`decision_time` effective · `recorded_time` recorded · `decision_context_cursor` knowledge boundary); Model A; cursor dùng canonical schema §8.5.1; relational invariant `input ≤ cursor ≤ DecisionEvent`; Event Contract là authority xác định Decision class.
- **4 alternatives** ghi rõ lý do loại, **bao gồm chính đề xuất sai ban đầu của Claude** (`decision_time` = Replay Cursor) — giữ lại trong ADR làm bản ghi lịch sử vì sao phương án đó bị bác.
- Ghi rõ **phụ thuộc ADR-009**: nếu ADR-009 bị bác hoặc đổi mô hình frontier, `decision_context_cursor` phải đánh giá lại.

### Changed
- MANIFEST: `compatible_adr_range` → ADR-001 ~ ADR-010; OQ-005/OQ-006 chuyển trạng thái sang "hướng đã được PO duyệt → ADR Draft, chờ review + accept".

### Trạng thái governance sau bước này
- ADR-009, ADR-010: **Draft** — chưa accept. Chapter 8: **In Review** v3.5. Chưa có gì được Lock.

## [Unreleased] — Review bộ ba (Chapter 8 v3.6 + ADR-009 + ADR-010): **2 Blocker · 2 Major · 1 Minor**

### Blocker 1 — XÁC ĐỊNH LÀ FALSE POSITIVE (một phần), kèm 1 ý đúng đã sửa
- ChatGPT khẳng định Product Owner **chưa từng** approve OQ-005/OQ-006 và MANIFEST đang ghi nhận quyết định không tồn tại. **Kiểm chứng: sai.** Product Owner đã duyệt hướng bằng lời trực tiếp trong phiên làm việc ("Tao duyệt OQ-005 và 006"). ChatGPT chỉ đọc GitHub, không thấy hội thoại → suy ra approval không tồn tại. Đây là false positive **cùng dạng** với vụ "file bị truncate" trước đó (kết luận từ dữ liệu nó không có quyền truy cập).
- **Ý ĐÚNG trong Blocker 1, đã sửa:** `resolves: [OQ-005]` / `resolves: [OQ-006]` trong ADR còn `Draft` là mâu thuẫn metadata — Draft chưa resolve được gì. Đổi thành **`addresses:`** kèm ghi chú "`resolves` chỉ có hiệu lực khi ADR được Accepted".
- **Làm rõ MANIFEST** để không ai hiểu nhầm nữa: tách bạch 3 tầng — (a) PO đã duyệt HƯỚNG (có nguồn, có ngày); (b) ADR = Draft, CHƯA accept; (c) OQ vẫn `Open` cho tới khi ADR được accept.

### Fixed — Blocker 2 (thật, nghiêm trọng)
- **`lifecycle_frontier` tồn tại 3 schema mâu thuẫn:** v3.5 đổi canonical thành `{stream_id, position: {kind, sequence}}` nhưng KHÔNG propagate sang: ví dụ §8.4, bảng cardinality §8.5.1, bảng relational §8.5.2, các phép so activation/registry. Schema cũ `{stream_id, sequence}` **không biểu diễn được** Genesis frontier — chính use case vừa thêm ở v3.5. Trớ trêu: bảng cardinality được tạo ra để chặn đúng lớp lỗi propagation này lại chính là chỗ chưa cập nhật. Đã chuẩn hóa 1 schema duy nhất và propagate 6 chỗ; bảng relational thêm điều kiện theo `kind` (genesis → registry phải là Genesis Registry; event → so `effective_from.event_ref.sequence ≤ position.sequence`).

### Fixed — Major
- **ADR-009 gộp Lamport Clock và HLC thành một alternative với rationale không chính xác:** hai cơ chế khác nhau. Tách thành 2 alternatives riêng — Lamport (bảo toàn chiều happened-before nhưng `L(A) < L(B)` KHÔNG chứng minh A gây ra B, không phân biệt causality với concurrency) và HLC (hữu ích cho temporal locality/observability nhưng clock timestamp không mang đủ domain evidence thay `causation_refs`). Thêm ghi chú: Lamport/HLC có thể bổ sung sau làm **metadata phụ**, không được thành domain causation authority nếu không có ADR mới.
- **ADR-010 phụ thuộc ADR-009 nhưng chỉ nằm trong prose:** thêm `depends_on: [ADR-009]` vào frontmatter + **§7 Acceptance gate** — ADR-010 không được rời `Draft`/`In Review` trước khi ADR-009 accept; nếu ADR-009 đổi semantic frontier/Input Contract/cursor/lifecycle boundary thì ADR-010 quay lại review. Review song song được, **accept thì không**.

### Fixed — Minor
- ADR-009 "cả 4 execution mode pin cùng contract" → làm rõ theo logical run: khi so sánh/tái tạo **cùng một logical Decision/run** thì mọi mode pin cùng Input Contract version; strategy/run khác nhau được dùng contract khác nhau.

### Checklist toàn vẹn
- 641 dòng · fence 48 (chẵn) · `position: {kind` 3 lần · **0 path cũ `lifecycle_frontier.sequence`** · `decision_context_cursor` xác nhận dùng `position: {kind: event}`.

## [Unreleased] — Consolidation round: Chapter 8 v3.7 + ADR-009 + ADR-010 + Ch11 v1.1 (**2 Blocker · 2 Major · 1 Minor**)

### Note — ChatGPT rút Blocker về PO approval
- ChatGPT xác nhận Blocker "PO chưa duyệt OQ-005/006" là false positive và đã rút lại. Product Owner đã duyệt hướng; ADR vẫn Draft chưa accept.

### Fixed — Blocker 1 (hậu quả trực tiếp của hybrid split)
- **Chapter 8 và ADR-009 công bố hai authority khác nhau:** Chapter 8 ghi "cơ chế do ADR-009 quyết định, ADR-009 PHẢI định nghĩa tối thiểu frontier/completeness/late-arrival/buffer/cursor-capture", trong khi ADR-009 lại defer chính những thứ đó sang Phase 1. Không thể accept ADR hay Lock Chapter khi chưa biết câu nào có hiệu lực. Sửa **5 chỗ** trong Chapter 8: ADR-009 khóa **architectural model + invariant**; **Phase 1 tạo design specification** cho mechanism; Phase 1 đổi semantic đã khóa trong ADR-009 → **follow-up ADR**, không sửa ngầm. Thêm **Phase 1 deliverable gate** vào ADR-009: implementation không được bắt đầu trước khi mechanism có design spec đã review.

### Fixed — Blocker 2
- **Cursor được phép pin registry version đã lỗi thời tại frontier mới:** rule cũ chỉ yêu cầu "đã từng visible trước frontier" → v3 (`effective_from` 900) vẫn hợp lệ tại frontier 1500 dù v4 (`effective_from` 1200) mới là authoritative. Cursor kết hợp *knowledge boundary mới* + *registry state cũ* (writer authority cũ, stream còn `active` dù v4 đã retire, thiếu `terminal_position`) → Live/Replay diễn giải khác stream universe hoặc chờ vô hạn trên stream đã retire. Định nghĩa **`active_registry_at(frontier)`** = registry có `effective_from` lớn nhất không vượt frontier; authoritative cursor **bắt buộc** dùng nó. Historical replay tự nhiên pin đúng registry lịch sử. Chạy registry cũ tại frontier mới phải phân loại là **counterfactual simulation** — không phải authoritative replay, không dùng làm parity evidence.

### Fixed — Major
- **Chapter 8 ghi sai trạng thái approval:** banner vẫn nói "CHƯA được Product Owner quyết" và heading §8.3/§8.4 vẫn "chờ Product Owner + ADR" — nay đã sai vì PO đã duyệt hướng. Sửa banner thành 3 tầng trạng thái + **lock gate 4 điều kiện** (ADR-009 accept · ADR-010 accept theo dependency gate · OQ chuyển Resolved · consolidation hoàn tất), ghi rõ *"ADR đã được ghi KHÔNG đủ — Draft là đã ghi nhưng chưa accept"*. Heading đổi thành "HƯỚNG ĐÃ ĐƯỢC PO DUYỆT · chờ ADR-00x accept".
- **Manifest dependency graph không khớp frontmatter Chapter 8:** Manifest thiếu `03-engineering-principles` và `07-module-taxonomy` → tooling/reviewer có thể bỏ qua deterministic checks (Ch3) và writer `module_id`/taxonomy checks (Ch7). Đã đồng bộ đủ 5 dependency.

### Fixed — Minor
- **`addresses`/`depends_on` chưa thuộc ADR metadata contract chuẩn:** thêm vào `templates/adr-template.md` và **Chapter 11 v1.1** bảng semantic 3 field — `addresses` (đang xử lý OQ, KHÔNG resolve) · `resolves` (chỉ hiệu lực khi ADR `Approved`/`Locked`) · `depends_on` (dependency phải Approved/Locked trước). Biến acceptance gate từ prose thành **machine-readable** dựa trên status lifecycle chuẩn.

### Checklist toàn vẹn
- 667 dòng · fence 52 (chẵn) · **0 câu "do ADR-009 quyết"** · `active_registry_at` 2 · banner 4-điều-kiện hiện diện · 2 heading "PO DUYỆT" · **0 path cũ `lifecycle_frontier.sequence`**.

## [Unreleased] — Consolidation round 2: Ch8 v3.8 · ADR-009 · Ch11 v1.2 (**2 Blocker · 2 Major · 2 Minor**)

### Fixed — Blocker
- **ADR-009 giữ rule registry YẾU hơn Chapter 8 vừa siết:** Chapter 8 v3.7 khóa `cursor.stream_registry_version = active_registry_at(frontier)`, nhưng ADR-009 §2.6 vẫn ghi "cursor chỉ dùng registry version đã visible tại frontier" — với v3(900)/v4(1200)/frontier 1500, ADR cho qua v3 còn Chapter bắt reject. Đã propagate rule mạnh sang ADR-009 + ghi hệ quả: registry activation làm mọi Input Contract pin registry cũ **không còn hợp lệ** cho authoritative Decision sau boundary đó.
- **`active_registry_at` không phải hàm total + unique:** (a) *không có ứng viên* — Genesis Registry không có `effective_from`, nên cursor `kind: genesis` (và giai đoạn sau Genesis nhưng chưa có post-Genesis registry) không resolve được; (b) *nhiều ứng viên* — schema không cấm 2 registry cùng `effective_from`. Sửa: định nghĩa 2 nhánh (base case → Genesis Registry; ngược lại → registry DUY NHẤT có effective_from lớn nhất ≤ frontier) + 4 invariant bảo đảm uniqueness (mỗi post-Genesis registry đúng một `effective_from` · không 2 registry chung `effective_from.event_ref` · activation event định danh chính xác registry được activate · duplicate/ambiguous = integrity violation → fail-safe I-6).

### Fixed — Major
- **Phase 1 deliverable gate khóa quá rộng:** "implementation KHÔNG được bắt đầu trước khi các mechanism deferred có design spec" có thể bị hiểu là chặn toàn bộ Phase 1 cho tới khi xong cả storage/archive/recovery — trong khi domain modeling, schema tooling, module skeleton không phụ thuộc. Sửa thành **per-capability gate** (frontier consumer ↔ frontier design; handoff ↔ handoff design; archive ↔ retention design...) + ghi rõ hạng mục độc lập không bị chặn.
- **Chapter 11 đổi semantic dưới cùng version — LỖI CỦA CLAUDE:** vòng trước Claude chạy `replace('version: "1.0"', '"1.1"')` nhưng Chapter 11 **vốn đã là 1.1**, nên lệnh **thất bại im lặng** và Claude báo cáo là đã bump. Kết quả: metadata contract mới (`addresses`/`resolves`/`depends_on` + acceptance gate) được thêm dưới cùng snapshot v1.1, khiến version không còn định danh được nội dung. Đã bump thật lên **v1.2** + cập nhật `last_review` + đồng bộ Manifest. *Lớp lỗi: string-replace giả định giá trị cũ mà không verify kết quả — lặp lại lần thứ 3.*

### Fixed — Minor
- Chapter 8 cross-mode wording rộng hơn ADR-009 ("mọi Decision run ở cả 4 mode phải pin cùng contract") — propagate nguyên clarification của ADR-009: chỉ áp khi **so sánh/tái tạo cùng một logical Decision/run**; strategy/run khác được dùng contract khác.
- MANIFEST mô tả OQ-005 còn theo mô hình cũ ("cơ chế cụ thể quyết định ở Chapter 8") — cập nhật theo hybrid split: Chapter 8 = invariant · ADR-009 = architectural model · Phase 1 = mechanism/design spec.

### Added — Backlog (Suggestion, làm SAU khi ADR accept)
- **BL-006:** sau khi ADR-009/010 accept, dọn decision history khỏi Chapter 8 (các đoạn "chọn Model A thay vì B", "vì sao chọn mô hình này") — rationale/alternatives đã ở ADR; Constitution chỉ giữ normative rule. Chưa làm bây giờ vì ADR chưa accept.

### Checklist toàn vẹn (8 mục)
- Ch8 676 dòng · fence 52 (chẵn) · `active_registry_at` có base case · ADR-009 có rule mạnh · Phase 1 gate per-capability · Ch11 = v1.2 · BL-006 ghi backlog · Manifest OQ-005 mô tả mới.

## [Unreleased] — Consolidation round 3: Ch8 v3.9 · Ch11 v1.3 · ADR-009 · ADR-010 (**2 Blocker · 3 Major · 1 Suggestion**)

### Fixed — Blocker
- **Bảng relational §8.5.2 vẫn dùng rule registry YẾU:** §8.3.1 đã khóa `cursor.registry = active_registry_at(frontier)` nhưng bảng validator authority tập trung vẫn chỉ kiểm `effective_from ≤ frontier` — cho qua cursor frontier 1500 pin v3 dù v4 active từ 1200. Hai validator mâu thuẫn ngay trong một chapter. Sửa: bảng dùng đúng `active_registry_at` (genesis → Genesis Registry; event → hàm total+unique), ghi rõ `effective_from ≤ frontier` chỉ là **điều kiện CẦN bên trong hàm**, không phải validity cuối cùng.
- **Input Contract vừa exact-pin vừa cho phép range:** §8.5 còn câu "hoặc thỏa registry constraint nếu contract khai báo dạng khoảng" — hai mô hình kiến trúc khác nhau. Range open-ended làm semantic của một **immutable** contract mở rộng trong tương lai **mà không bump version** (tự mâu thuẫn), và chưa định nghĩa: ai đưa registry tương lai vào range, chứng minh compatibility `included_streams` ra sao, chọn version nào khi nhiều match. Chốt **EXACT PIN cho v1**, bỏ range; ghi concern đã chấp nhận (**contract-version churn**) + lối thoát bằng follow-up ADR (immutable closed compatibility set · subset registry · capability-based constraint).

### Fixed — Major
- **`active_registry_at` chỉ áp cho cursor, chưa áp cho event lúc append:** event có thể pin registry **tương lai chưa active** (v4 active từ sequence 900 nhưng append ở frontier 800 vẫn pin v4 → future configuration knowledge) hoặc registry **đã supersede**. Khóa invariant `event.stream_ref.registry_version = active_registry_at(append_lifecycle_frontier)`; representation/evidence của append frontier → Phase 1.
- **Causation prerequisite ngoài Input Contract scope chưa có semantic:** B ∈ included_streams nhưng `B.causation_refs → A` với A ngoài scope — đọc A thì Input Contract không mô tả đúng input thật (**hidden input**, phá parity); không đọc A thì không xác nhận được prerequisite. Chốt: prerequisite là **payload/state dependency** → stream của nó BẮT BUỘC thuộc `included_streams` + cursor universe; prerequisite **ngoài scope** → chỉ verify identity/existence, **cấm** đọc payload và **cấm** dùng làm state-transition input.
- **Decision class có hai authority field:** Chapter 8 cho `event_class: decision` HOẶC `semantic_roles: [decision]`, ADR-010 chỉ khóa `event_class` → validator có thể phân loại khác nhau (ảnh hưởng `decision_time`, cấm `effective_time`, bắt buộc cursor, no-future validator). Chuẩn hóa **đúng một field canonical `event_class`**; `semantic_roles` là metadata **không authoritative**.

### Added — Suggestion
- **Chapter 11 v1.3 — transition `addresses → resolves` phải ATOMIC:** khi PO approve ADR, toàn bộ `status` · `addresses→[]` · `resolves→[OQ-x]` · `approved_by/at` · `MANIFEST OQ→Resolved` phải nằm trong **cùng một documentation change**. Nếu approve trước rồi sửa metadata sau, lần sửa đó **vi phạm ADR Immutable Rule**.

### Checklist (7 mục, dùng assert cho mọi replace)
- Ch8 v3.9 · Ch11 v1.3 · fence 54 (chẵn) · **0 câu range/constraint còn sót** · **0 chỗ `semantic_roles` còn là authority** · ADR-009 có exact pin · ADR-010 có `event_class` canonical.

## [Unreleased] — Consolidation round 4: Ch8 v4.0 · ADR-009 (**2 Blocker · 1 Major [chờ PO] · 1 Minor · 1 Suggestion**)

### Fixed — Blocker
- **Registry activation event thiếu pre-append boundary semantic (vòng tự kích hoạt):** registry v4 active tại chính event E@900 — nếu `append_lifecycle_frontier` hiểu là post-append (900) thì E phải validate bằng v4, mà v4 chỉ active vì E đã commit. Chốt: `append_lifecycle_frontier` = frontier committed **ngay TRƯỚC** append transaction; **registry activation event KHÔNG được validate bằng chính registry nó kích hoạt** (E dùng registry cũ, registry mới active TỪ E). Nếu E đồng thời chuyển writer: old writer append `E@n`, new writer từ `n+1`.
- **`causation_refs` gộp 2 semantic mà schema không phân biệt được:** v3.9 định nghĩa 2 loại prerequisite (payload/state dependency vs identity-only ngoài scope) nhưng dùng chung một field → ba quy tắc không thể cùng thực thi (external ref không thuộc cursor universe + mọi causation phải cursor-visible + mọi causation tạo precedence edge). Tách schema: **`causation_refs`** (authoritative prerequisite, tham gia `P_causation`, bắt buộc trong universe, causally closed) vs **`related_event_refs`** (identity/audit, KHÔNG tham gia `P_causation`, được phép ngoài universe, cấm đọc payload). Thêm cả hai vào bảng cardinality để tránh lỗi propagation quen thuộc.

### Added — §8.4.1: Decision "in-flight" qua registry transition — **CHỜ PRODUCT OWNER QUYẾT**
- Tình huống: Decision đọc xong input ở frontier 899 (cursor pin v3), registry v4 activate ở 900, Decision append ở 901 (envelope pin v4). Hai rule riêng lẻ đều đúng nhưng chưa có policy. Vì nó **thay đổi authoritative Decision history**, không để Phase 1 tự suy luận và **Claude không tự chọn**. Trình bày 2 phương án + đánh đổi: **A** (append rồi revalidate trước Risk/Execution, supersede/reject chứ không xóa) vs **B** (reject và recompute ngay tại append). ChatGPT nghiêng về A — recommendation, không phải quyết định.
- **Lock gate Chapter 8 nâng từ 4 → 5 điều kiện**, thêm: §8.4.1 phải có quyết định của Product Owner.

### Fixed — Minor
- **Chapter 8 và ADR-009 ghi "Concern đã chấp nhận"/"Chấp nhận đánh đổi" khi ADR vẫn Draft** — ghi nhận thay Product Owner. Sửa toàn bộ thành "**được GHI NHẬN trong Draft**; chỉ coi là accepted khi Product Owner approve ADR". Giữ đúng 3 tầng: *OQ direction approved ≠ ADR accepted ≠ từng tradeoff tự động được PO chấp nhận*.

### Added — Suggestion
- **Boundary conformance fixtures** trong ADR-009 (review/test artifact, KHÔNG phải authority mới): 6 case đánh đúng các lỗi relational boundary đã lặp nhiều vòng — registry activation `E@n` · lifecycle writer transition · Decision cut trước/append sau transition · state causation ngoài scope (reject) · identity-only ngoài scope (cho phép, không vào `P_causation`) · cursor pin stale/future registry (reject).

### Checklist (7 mục, assert cho mọi replace)
- Ch8 v4.0 · fence 58 (chẵn) · pre-append semantic hiện diện · `related_event_refs` 3 chỗ (gồm bảng cardinality) · §8.4.1 chờ PO · **0 chỗ "đã chấp nhận" còn sót** (cả Ch8 lẫn ADR-009) · ADR-009 có fixtures.

## [Unreleased] — 2026-07-18 — Product Owner QUYẾT §8.4.1: **Model A** (Ch8 v4.1 · ADR-009 · ADR-010)

### Product Owner decision
- **Decision "in-flight" qua registry transition → chọn Model A:** Decision có knowledge cut trước transition **vẫn được append** như immutable historical fact; trước Risk/Execution phải **revalidate** theo registry đang active; nếu stale/invalid thì ghi event **supersede/reject**, KHÔNG xóa/sửa Decision gốc.

### Added — ADR-010 §2.6 (chủ sở hữu quyết định)
- Ghi quyết định Model A + rationale + **4 guardrail bắt buộc**: (1) Decision được append KHÔNG tự động có execution eligibility · (2) Risk/Execution bị chặn tới khi revalidation thành công · (3) kết quả revalidation là **authoritative event**, không phải trạng thái ngầm · (4) cấm sửa/xóa Decision gốc.
- Rationale ghi rõ vì sao A: phân biệt *"Decision đã thực sự được tính bằng cut v3"* vs *"Decision còn đủ điều kiện thực thi dưới v4"* — phù hợp **I-1** (input/reasoning đã xảy ra phải lưu bất biến, không biến mất vì transition vài ms trước append) và **I-4** (Decision không tự thực thi, Risk Gateway là boundary hợp lý cho current-validity check).
- **Model B đưa vào bảng Alternatives** kèm lý do loại: mất bản ghi Decision đã tính; muốn giữ Explainability vẫn phải ghi computation-attempt fact → tiến gần A mà không có lợi thế semantic.
- **Ranh giới:** state machine `computed → revalidated → rejected/superseded` thuộc **Decision Domain Contract**, KHÔNG hardcode vào Constitution/ADR (theo I-13 + bài học Chapter 4).

### Fixed — Major (từ review v4.0)
- **ADR-009 §2.6 có wording ngầm chọn B:** "registry activation làm Input Contract cũ không hợp lệ cho Decision **sau boundary**" — "sau" không rõ là *knowledge cut* hay *append*. Nếu hiểu theo append thì đã ngầm chọn B. Sửa thành boundary chính xác: contract cũ không hợp lệ cho Decision có **knowledge cut SAU** boundary; Decision có **cut TRƯỚC nhưng append SAU** → áp dụng Model A theo ADR-010 §2.6. Thêm phân chia thẩm quyền: registry/frontier boundary → ADR-009; Decision lifecycle policy → ADR-010.
- **Quyết định A/B chưa có ADR ownership:** theo ADR Scope Rule, quyết định ảnh hưởng nhiều module + khó đảo ngược **bắt buộc** thành ADR. Ghi vào **ADR-010 §2.6** (tài liệu sở hữu Decision Time/Context) thay vì tạo ADR-011 — ADR-009 chỉ cross-reference.

### Changed
- **Chapter 8 §8.4.1** đổi từ "⚠️ CHỜ PO QUYẾT" → "Model A (PO quyết 2026-07-18)", giữ normative rule tại Chapter, rationale/alternatives ở ADR.
- **Lock gate điều kiện 4 hoàn thành:** còn lại 4 điều kiện — ADR-009 accept · ADR-010 accept theo dependency gate · OQ-005/006 → Resolved · consolidation review hoàn tất.
- **Fixtures ADR-009** mở rộng cho Model A: Decision stored + Risk blocked + bắt buộc revalidation result · revalidation fail → rejection/supersession event, không phát sinh execution intent · revalidation pass → execution tiếp tục, phải tham chiếu revalidation thành công.

## [Unreleased] — Ch8 v4.2 · ADR-009 · ADR-010 (**1 Blocker · 2 Major · 1 Minor · 1 Suggestion**)

### Fixed — Blocker (Claude vi phạm ranh giới do chính mình đặt)
- **Chapter 8 định nghĩa lại SEMANTIC của `causation_refs`, trái Chapter 6 (Locked):** §6.7 quy định Chapter 6 sở hữu *ngữ nghĩa* causation, Chapter 8 chỉ sở hữu *representation + cardinality* — Claude tự viết ranh giới này rồi tự vi phạm, thu hẹp causation thành "chỉ payload/state prerequisite" và ép mọi `causation_ref` phải thuộc Input Contract universe. Hệ quả sai: `DECISION_CREATED → RISK_REJECTED` là nhân quả nghiệp vụ thật nhưng consumer không đọc payload → buộc phải chọn giữa "ép mọi Input Contract include stream đó" hoặc "hạ xuống `related_event_refs`, mất `P_causation`". Thêm nữa `causation_refs` là metadata **cấp event bất biến** còn Input Contract là scope **cấp run** — không tồn tại "Input Contract universe của event" để append-validator kiểm.
- **Sửa:** khôi phục `causation_refs` = *direct domain causal predecessor* (semantic theo §6.7 + Event Contract), `related_event_refs` = quan hệ **không mang causal meaning**. **Causal closure chuyển về tầng Input Contract/run validation** qua `causal_closure_policy`: nếu processor cần payload/state của A thì stream A bắt buộc trong scope; causal predecessor không phải state-input thì không bị ép vào scope. Vi phạm → **Input Contract invalid**, không phải event invalid. *(Phương án "mọi Input Contract phải causally closed hoàn toàn" bị loại: quá rộng — portfolio-view contract sẽ phải include mọi decision/risk stream dù không đọc payload nào.)*

### Fixed — Major
- **Stale wording tạo trạng thái kép:** §8.4.1 có heading "PO quyết" nhưng thân bài vẫn "chưa có policy / Cần Product Owner chọn"; ADR-009 vẫn ghi "chưa có quyết định của Product Owner; ADR-009 không được accept khi mục này còn mở". Automation/reviewer đọc đúng câu stale sẽ kết luận §8.4.1 vẫn Open. Viết lại §8.4.1 thành lịch sử ngắn (2 phương án đã xem xét → PO chọn → vì sao loại phương án kia); ADR-009 sửa thành cross-reference.
- **Guardrail revalidation chưa có evidence chain normative:** "phải có một success event" không đủ — implementation vẫn có thể dùng success của Decision khác, success dưới registry khác, hoặc tạo Execution Intent không truy được về revalidation. Nâng thành **relational invariant**: `OriginalDecision ← RevalidationSucceeded ← RiskApproved ← ExecutionIntentCreated`, kèm 4 ràng buộc (tham chiếu chính xác Decision gốc · ghi evidence registry/knowledge boundary đã dùng · Risk Approval causally depend vào revalidation · Execution Intent truy vết được cả hai). Đây là **platform-level invariant** (I-1 + I-4), không phải test fixture.

### Fixed — Minor
- **Hai cặp "Model A/B" khác nghĩa trong cùng ADR-010** (§2.2 time field vs §2.6 transition policy) làm cross-reference mơ hồ. Đổi tên mô tả: **Decision Effective-Time Model** và **Append-and-Revalidate Policy**; alternatives thành **Dual-field Effective Time** và **Reject-and-Recompute**.

### Added — Suggestion
- 4 fixture mới trong ADR-009: domain-causal predecessor không phải state input (vẫn giữ `P_causation`) · state dependency ngoài closure (Input Contract invalid) · revalidation success của Decision A không mở eligibility cho Decision B · revalidation dưới registry v4 không approve flow yêu cầu v5.

## [Unreleased] — Chapter 9 v2.9 (ChatGPT review round 8: **0 Blocker · 1 Major · 0 Minor · 0 Suggestion mới**)

### Fixed — Major: atomic promotion compatibility set chưa propagation exact Build Artifact
- §9.1 (v2.8) đã khóa Plugin Version một mình không đủ để xác định exact artifact đã chạy — nhưng `validated compatibility set` của atomic activation boundary ở §9.5 vẫn chỉ liệt kê `runtime implementation/deployment version`, không bắt buộc pin exact artifact/manifest. Hệ quả: activation boundary có thể mở đúng mọi version/contract/permission nhưng runtime lại đang chạy một rebuild khác (cùng Plugin Version, khác content hash) so với artifact đã parity-validate — evidence ghi lại sau khi chạy chỉ chứng minh artifact nào đã chạy, không chứng minh nó từng nằm trong tập được validate tại activation (cùng lớp lỗi với "published contract compliance ≠ decision-time visibility compliance").
- **Sửa:** thêm vào compatibility set — exact Package/Build Artifact content identity đã qua validation, hoặc immutable release manifest version/content identity + target platform/runtime discriminator resolve duy nhất tới artifact đó. Làm rõ: chỉ trùng Plugin Version không đủ eligibility. Mở rộng định nghĩa mixed-version activation để bao gồm **mixed-build activation** (runtime chạy artifact khác artifact đã validate dù cùng Plugin Version) → integrity violation, fail-safe. Làm rõ luôn: exact artifact hash trong Decision evidence phải khớp artifact đã có trong compatibility set được validate tại boundary, không chỉ khớp artifact đã chạy.

### Checklist
- Ch9 v2.9 · §9.1→§9.10 liên tục · **0 tham chiếu §9.x gãy** · atomic promotion compatibility set và §9.1 exact-artifact evidence giờ nhất quán hai chiều (evidence sau khi chạy ↔ eligibility tại activation).

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 9 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 9 v2.8 (ChatGPT review round 7: **0 Blocker · 2 Major · 0 Minor · 0 Suggestion mới**)

### Fixed — Major: Decision evidence pin Plugin Version chưa đủ để tái dựng exact implementation
- Một Plugin Version có thể có nhiều Package/Build Artifact (theo target platform, hoặc do rebuild), mỗi artifact content hash riêng. Pin chỉ Plugin Version không trả lời được artifact nào thực sự chạy, platform nào, build nào — Replay không verify được đúng binary lịch sử. **Sửa:** khóa Decision evidence phải pin Plugin Version **đồng thời** resolve bất biến tới exact Package/Build Artifact/immutable release manifest (content hash · target platform/runtime · build identity · dependency/runtime environment). Đưa ra 2 mô hình hợp lệ không hardcode schema: (A) Decision pin trực tiếp `plugin_definition_id · plugin_version · artifact_content_hash`; (B) `plugin_version` trỏ immutable release manifest exact-pin theo platform, Decision pin đủ discriminator để resolve qua manifest. Cũng làm rõ luôn 2 chỗ dùng lowercase "plugin implementation version" (§9.3) để trỏ về đúng tầng Plugin Version + yêu cầu exact-artifact mới.

### Fixed — Major: alias "Definition/Package" còn sót ở §9.1
- Dù §9.3 đã sửa ở v2.7, câu "Mỗi plugin (ở tầng Definition/Package)" ở §9.1 vẫn gộp ngược hai tầng vừa tách, ngay trong section đã khóa bốn tầng. Sửa thành "Mỗi Plugin Definition". Đã grep mở rộng toàn file theo đề xuất ChatGPT cho các alias khác (`Definition/Package` · `plugin implementation version` · `Strategy Plugin (Plugin Version)` · `runtime module type/definition`) — không còn alias sai; usage còn lại của "plugin implementation version" đã được làm rõ trỏ đúng tầng.

### Checklist
- Ch9 v2.8 · §9.1→§9.10 liên tục · **0 tham chiếu §9.x gãy** · grep xác nhận 0 alias `Definition/Package` · Decision evidence bắt buộc exact-artifact resolution, không chỉ Plugin Version.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 8 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 9 v2.7 (ChatGPT review round 6: **1 Blocker · 2 Major · 0 Minor · 0 Suggestion mới**)

### Note — checklist v2.6 "0 wording cũ còn sót" đã không chính xác
Checklist v2.6 tuyên bố "0 wording cũ còn sót" nhưng chỉ kiểm 3 cụm từ cụ thể (peer-authority OR · single-implementation · zero-impact) — không kiểm alias `Plugin Definition / Package` vẫn còn nguyên trong bảng §9.3 sau khi §9.1 đã tách 4 tầng. Đây là lỗi phạm vi kiểm tra (checklist hẹp hơn khẳng định), không phải sai fact về các mục đã kiểm. Ghi nhận để vòng sau kiểm rộng hơn: sau mỗi thay đổi thuật ngữ ở §9.1, phải grep toàn file cho alias cũ, không chỉ raw diff.

### Fixed — Blocker: `module-registry` và event log cùng có nguy cơ sở hữu Strategy Instance runtime identity
- v2.6 viết independently-operated Strategy Instance "có `module-registry` entry cho runtime component" — mâu thuẫn trực tiếp với §9.8 (runtime lifecycle facts: created/activated/retired → authoritative event log; registry không phải runtime truth) và với Chapter 7 Locked (registry sở hữu module identity/taxonomy, không sở hữu deployment/instance fact). Kịch bản vỡ: instance retire → không rõ registry entry bị xóa/đổi hay giữ nguyên trong khi event log đã nói retired; scale thêm instance → phải sửa architecture registry cho một operational action, phá §9.10.
- **Sửa:** registry chỉ sở hữu **registered module type/definition**, không bao giờ sở hữu instance fact — dù hosted hay independently operated. Instance không tự tạo `module-registry` entry chỉ vì có deployment/scale riêng. Chỉ khi kiến trúc tạo ra một **module type mới** với published responsibility riêng (không chỉ thêm instance của type đã có) mới cần entry mới, và đó là architecture change thuộc diện ADR Required. `strategy_instance_id` luôn khác `module_id`; identity/lifecycle của instance luôn authoritative trong event log, không phụ thuộc operational boundary.

### Fixed — Major
- **§9.3 vẫn gộp `Plugin Definition / Package` sau khi §9.1 đã tách 4 tầng:** xóa alias, bảng ba-identity giờ chỉ dùng **Plugin Definition** (trỏ về 4 tầng ở §9.1); ghi rõ Package/Build Artifact và Plugin Runtime không thuộc bảng ba-identity domain/runtime này. Sửa luôn câu "Một Strategy Plugin (Plugin Version) phục vụ nhiều Strategy Instance" → "Một Plugin Version của một Plugin Definition có thể phục vụ nhiều Strategy Instance" — không dùng "Strategy Plugin" như alias cho Plugin Version.
- **§9.3 mở đầu "Vì Strategy Instance nằm ngoài `module-registry`" mâu thuẫn với §9.1 mới:** đổi thành "Strategy Instance identity không được lấy từ `module-registry`" — khớp mô hình module-type-vs-instance vừa khóa ở Blocker trên, không còn nói instance "nằm trong/ngoài" registry một cách mơ hồ.

### Checklist (mở rộng phạm vi kiểm tra sau lỗi ở v2.6)
- Ch9 v2.7 · §9.1→§9.10 liên tục · **0 tham chiếu §9.x gãy** · grep toàn file xác nhận 0 alias `Plugin Definition / Package` · 0 câu "nằm ngoài `module-registry`" · 0 exception clause cũ về independently-operated instance tự tạo registry entry · registry ↔ event log không còn competing authority cho instance fact.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 7 và Product Owner Approve/Lock.

## [Unreleased] — Chapter 9 v2.6 (ChatGPT review round 5, actual: **2 Blocker · 4 Major · 1 Minor · 0 Suggestion mới**)

### Correction — entry v2.5 bên dưới ghi sai severity
Entry gốc cho v2.5 (giữ nguyên bên dưới, không xóa để tránh mất lịch sử) ghi **"0 Blocker · 0 Major · 1 Minor"** và note "ChatGPT khuyến nghị Approve". Đây là **sai lệch với review thật** của ChatGPT round 5, vốn là **Revision Requested** với đúng **2 Blocker · 4 Major · 1 Minor · 0 Suggestion mới**. Round 5 xác nhận 6 concern outstanding từ v2.4 vẫn chưa đóng; v2.5 chỉ xử lý phần precondition của promotion (đúng như entry gốc mô tả), KHÔNG xử lý 6 concern còn lại. Không tự kết luận "đã sạch" khi chưa đối chiếu đủ nguyên văn bảng severity.

### Fixed — Blocker
- **`decision-dependency contract` là peer authority của Input Contract (§9.5):** chữ "hoặc" giữa Input Contract và decision-dependency contract tạo hai authority ngang hàng — `decision_context_cursor` chỉ pin Input Contract, nên dependency contract nằm ngoài trở thành **hidden input** không có root path bắt buộc khi replay, bất kể có immutable hay không. **Sửa:** decision-dependency contract giờ là **subordinate immutable artifact** phải được Input Contract **exact-pin**; không tự mở rộng input scope; đổi reference bắt buộc bump Input Contract version; xóa hoàn toàn cấu trúc OR. Nếu cần nhiều peer input authority thật sự, phải qua ADR sửa canonical cursor — Chapter 9 không tự tạo bằng prose.
- **Promotion `decision-relevant` chưa có authoritative activation boundary:** v2.5 mới có precondition verify (4 điều kiện visibility) nhưng không định nghĩa promotion có hiệu lực từ đâu — có thể rơi vào half-promoted/mixed-version state theo cả hai chiều (Plugin Contract đã promote nhưng Input Contract/permission/runtime chưa theo kịp, hoặc ngược lại). **Sửa:** khóa invariant **atomic activation boundary** — một **validated compatibility set** (Plugin Contract version · Input Contract version · published contract refs · permission grant version · capability/compatibility result · runtime deployment version) phải đồng bộ tại boundary. Trước boundary: cấm dùng cho authoritative Decision. Sau boundary: mọi Decision phải pin đúng promoted snapshot. Partial/mixed-version activation → integrity violation, fail-safe I-6. Cơ chế fencing cụ thể defer Phase 1; atomic semantic khóa ngay ở Chapter 9.

### Fixed — Major
- **Strategy Instance bị loại tuyệt đối khỏi Module Taxonomy (§9.1):** chỉ đúng với hosted instance. Độc lập operated instance (process/pod riêng, deploy/restart/scale riêng, published contract riêng) thỏa định nghĩa module của Ch7 §7.0. **Sửa:** tách bảng thành Strategy Instance (hosted) = KHÔNG thuộc taxonomy · Strategy Instance (independently operated) = CÓ, có `module-registry` entry cho runtime component, `strategy_instance_id ≠ module_id`. Nguyên tắc: classification phụ thuộc operational boundary thật, không phụ thuộc domain identity class.
- **Plugin Definition / Package vẫn gộp logical + artifact identity (§9.1, §9.3):** không rõ registry đăng ký logical plugin hay binary; Decision evidence không rõ pin semantic version hay content hash; promote/rollback không rõ tác động layer nào. **Sửa:** tách 4 tầng — Plugin Definition (logical identity) ≠ Plugin Version (immutable release) ≠ Package/Build Artifact (immutable bytes + content hash) ≠ Plugin Runtime (deployment/replica). `module-registry.yaml` chỉ đăng ký Plugin Definition; Decision evidence pin Plugin Version.
- **Strategy Definition bị khóa vào một Strategy Plugin (§9.3):** yếu hơn Chapter 3 Locked, vốn cho phép authoritative/shadow/experimental/migration implementation song song. **Sửa:** một Strategy Definition có thể có nhiều implementation/Plugin Version; đúng một implementation authoritative trong mỗi execution/parity scope; shadow/experimental/migration không sinh authoritative Decision trước parity validation + promotion. "Canonical" = authority status trong scope, không phải cardinality.
- **Version independence bị hiểu thành zero downstream impact (§9.7):** "cập nhật một plugin không ảnh hưởng plugin khác" sai — plugin update có thể ảnh hưởng consumer qua contract/semantic/capability/permission/freshness/dependency/resource contention. **Sửa:** "independent versioning ≠ zero downstream impact"; impact đánh giá bằng compatibility/capability/dependency rules của Chapter 10.

### Fixed — Minor
- **§9.4 câu mở "chịu toàn bộ ràng buộc" vẫn đọc được thành bảng exhaustive** dù đã có câu "CẦN chưa ĐỦ" ở đoạn sau. Đổi câu mở thành: bảng tóm tắt các ràng buộc trực tiếp quan trọng nhất, không thay thế toàn bộ Chapter 8 và ADR-010.

### Checklist
- Ch9 v2.6 · §9.1→§9.10 liên tục · **0 tham chiếu §9.x gãy** · 0 wording cũ còn sót (peer-authority OR · single-implementation · zero-impact) · CHANGELOG v2.5 đã đính chính severity sai.

### Note
- Không tự tuyên bố Approve. Chờ ChatGPT review round 6 xác nhận, và chờ Product Owner Approve/Lock.

## [Unreleased] — Chapter 9 v2.5 (ChatGPT review round 5: **0 Blocker · 0 Major · 1 Minor** — ⚠️ **entry này ghi sai, xem đính chính ở entry v2.6 phía trên**)

### Fixed — Minor
- **"Verify lại toàn bộ §9.5" mơ hồ về điều kiện cụ thể của promote:** liệt kê rõ 4 điều kiện bắt buộc trước khi promote một plugin thành decision-relevant có hiệu lực — cursor/snapshot-bounded · không đọc ambient state · pin projection version/schema/config · evidence đủ cho Replay (I-5).

### Note
- ChatGPT khuyến nghị **Approve** Chapter 9 sau vòng này. *(⚠️ Sai lệch với review thật — xem đính chính ở entry v2.6.)*

## [Unreleased] — Chapter 9 v2.4 (ChatGPT review round 4: **1 Blocker · 2 Major**)

### Fixed — Blocker: lỗ hổng reclassification ngầm do chính câu Claude thêm ở v2.3
- v2.3 viết *"phân loại theo **đường dữ liệu thực tế**, không theo ý định ban đầu"* — nghe hợp lý nhưng biến decision-relevance thành thuộc tính **suy ra lúc runtime**. Hệ quả: cùng một plugin, cùng một version, cùng một output sẽ **đổi ràng buộc theo hành vi của consumer** — evidence requirement thay đổi hồi tố, không audit được, và một consumer có thể **lặng lẽ kéo plugin chưa đủ điều kiện vào Decision Pipeline** rồi tuyên bố "giờ nó decision-relevant".
- **Sửa:** decision-relevance là **thuộc tính CONTRACT được khai báo** (`Decision participation`, §9.6), không suy runtime. **CẤM** dùng output của plugin chưa khai báo decision-relevant làm Decision input → integrity violation, fail-safe I-6, **không tự động nâng cấp**. Muốn tái sử dụng phải **promote qua contract change** (versioned, verify lại §9.5, ADR Required nếu đổi pipeline topology). **CẤM silent reclassification**. Làm rõ cách hiểu đúng: "đường dữ liệu thực tế" dùng để **phát hiện vi phạm**, KHÔNG phải để **tự động hợp thức hóa**.
- Thêm dòng tương ứng vào Forbidden patterns.

### Fixed — Major
- **Một dòng trong Forbidden patterns không có runtime enforcement:** "Bắt mở ADR cho mọi activate/pause instance" là lỗi **quy trình/governance**, không phải hành vi runtime — không cơ chế kỹ thuật nào phát hiện được. Để chung bảng làm loãng chuẩn "mọi dòng phải thi hành được" mà chính v2.3 vừa thiết lập. Tách thành bảng riêng **"Anti-pattern thuộc phạm vi GOVERNANCE"** với cột phát hiện = governance/process review.
- **"Instance identity không được tái sử dụng" chưa thi hành được:** thiếu (a) **uniqueness scope** — Ch6 §6.1 (Locked) cấm mặc định global, phải khai báo tường minh (global/per-Account/per-Strategy-Definition); nếu hẹp hơn global thì reference qua boundary phải qualified; (b) **retention/resolvability horizon** — Ch8 §8.1.1 yêu cầu persistently resolvable trong horizon platform cam kết, hết horizon phải có explicit retention/archive policy. Không có hai thứ này thì "không tái dùng" không kiểm chứng được sau vài năm.

### Checklist (7 mục)
- Ch9 v2.4 · decision-relevance là contract property · cấm silent reclassification · bảng governance tách riêng · instance identity có scope + horizon · **0 tham chiếu §9.x gãy** · bảng runtime không còn dòng governance.

## [Unreleased] — Chapter 9 v2.3 (ChatGPT review round 3: **1 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker: §9.4 mất ràng buộc visibility sau khi tách §9.5
- Vòng trước Claude **nâng decision-time visibility thành §9.5 độc lập** nhưng **không để lại liên kết** trong §9.4. Kết quả: bảng §9.4 liệt kê 6 ràng buộc và tự xưng là "toàn bộ ràng buộc đã Locked ở Chapter 8 + ADR-010", trong khi thiếu đúng ràng buộc quyết định — implementation đọc riêng §9.4 sẽ kết luận Decision Advisor chỉ cần schema đúng. Sửa: thêm dòng **Decision-time visibility (§9.5, bắt buộc)** vào bảng + câu chốt **"bảng trên là điều kiện CẦN, chưa ĐỦ"** + đưa "không có ngoại lệ cho AI module" về đúng chỗ.
- *Lớp lỗi:* tách một mục ra khỏi mục khác mà không kiểm mục gốc còn tự đủ không — cùng họ với các lỗi propagation đã ghi nhận.

### Fixed — Major
- **Instance lifecycle transition chưa bảo vệ Decision evidence:** §9.3 nói state transition là authoritative event, §9.8 nói lifecycle facts thuộc event log — nhưng không nói pause/stop/retire **không được** hủy/vô hiệu hóa evidence của Decision đã tính. Thêm ràng buộc 5: Decision đã tính vẫn tái dựng đầy đủ với đúng instance + plugin version + config (I-1) · **instance identity không được tái sử dụng** sau retire ([Ch6 §6.1](constitution/06-identity-model.md)) · nếu retire/stop chặn một Decision in-flight thì áp **cùng nguyên tắc ADR-010 §2.6**: ghi immutable preservation/rejection fact đủ evidence, **không xóa/ghi đè** Decision gốc, **không** cấp execution eligibility.
- **Forbidden patterns thiếu enforcement/verification ownership:** bảng liệt kê pattern + invariant bị vi phạm nhưng không nói **ai phát hiện, ai chặn** → là checklist review, không phải rule thi hành được (đúng bài học I-7: bypass không nhất thiết xuất hiện dưới dạng import code). Thêm cột **"Phát hiện / chặn bởi"** cho cả 9 dòng, **không tạo authority mới** — mỗi dòng trỏ về cơ chế đã tồn tại (I-7 Verification · Risk Gateway · Grant layer `granted ⊆ declared` · I-11 access-control audit · self-contained replay test · registry review · event log). Ghi rõ: pattern không có cột này chỉ là *khuyến nghị*.

### Fixed — Minor
- **§9.5 heading và body lệch phạm vi:** heading nói "MỌI plugin sinh authoritative output", body nói "decision-relevant path" → không rõ reporting/notification plugin có phải cursor-bound không. Thống nhất: áp cho plugin **trong decision-relevant path**; ghi rõ **ngoài phạm vi** (reporting/notification thuần túy, observability projection) — **nhưng** nếu output về sau được dùng làm input cho Decision thì plugin đó **trở thành** decision-relevant và phải tuân đầy đủ; phân loại theo **đường dữ liệu thực tế**, không theo ý định ban đầu.

### Checklist (7 mục)
- Ch9 v2.3 · §9.4 có dòng visibility · §9.4 nói rõ "CẦN chưa ĐỦ" · lifecycle không hủy evidence · forbidden patterns có cột enforcement · §9.5 có mục "ngoài phạm vi" · **0 tham chiếu §9.x gãy**.

## [Unreleased] — Chapter 9 v2.2 (ChatGPT review round 2: **1 Blocker · 2 Major · 1 Minor · 1 Suggestion**)

### Fixed — Blocker: mâu thuẫn nội tại về phạm vi Module Taxonomy
- §9.1 khẳng định plugin là runtime application component → có taxonomy type + `module-registry` entry; §9.3 lại khẳng định Strategy Instance KHÔNG phải module. Nhưng theo [Ch7 §7.0](constitution/07-module-taxonomy.md) (Locked), Strategy Instance **cũng** có runtime responsibility và published boundary → hai câu không thể cùng đúng nếu đọc §7.0 theo nghĩa rộng.
- **Sửa bằng cách làm rõ, KHÔNG định nghĩa lại Ch7:** Ch7 §7.0 viết *"**deployable** service, process, hoặc in-process component **được vận hành độc lập**"*. Strategy Instance chạy bên trong Strategy Engine **không được vận hành độc lập** → nằm ngoài phạm vi taxonomy. Thêm bảng: **Plugin Definition/Package** (deployable/executable unit) = CÓ taxonomy type + registry entry · **Strategy Instance** (runtime configuration bound vào deployable unit) = KHÔNG. Ghi rõ điều kiện escalate: *nếu reviewer đánh giá đây là redefinition chứ không phải clarification thì bắt buộc mở ADR sửa Ch7 — Chapter 9 không được tự làm.*

### Fixed — Major
- **Strategy Instance nằm ngoài registry nhưng chưa có identity/state authority:** không có nó thì I-1 và ADR-010 không tái dựng được Decision. Thêm 4 ràng buộc: instance identity **ổn định qua restart/redeploy** · đổi plugin version/config phải tạo **binding hoặc instance version mới** (cấm mutate ngầm identity đang chạy) · Decision evidence phải resolve chính xác `strategy_instance` + `configuration version` + `plugin implementation version` (ba thứ ADR-010 đã tách riêng) · state transition (created/activated/paused/stopped/retired) là **authoritative event**, không suy từ registry hay config file.
- **Permission boundary chỉ là declaration, chưa có enforcement/verification authority:** khai báo mà không nói ai cấp, ai chặn, ai chứng minh thì đó là mô tả, không phải ranh giới an toàn. Thêm phân tầng 4 lớp: **Declaration** (Plugin Contract) · **Grant** (deployment/authorization config, versioned — plugin **không tự cấp quyền cho mình**) · **Enforcement runtime** (Risk Gateway với execution intent I-4 · Exchange Adapter/Signing Service với credential I-11 · contract/API authorization với query & command) · **Verification** (đúng bộ kiểm I-7 đã khóa). Ràng buộc: **`granted ⊆ declared`**; vượt quyền = integrity violation → fail-safe I-6. Khóa tuyệt đối: **plugin KHÔNG bao giờ được cấp quyền dùng exchange credential trực tiếp** (I-11, không ngoại lệ).

### Fixed — Minor
- **Decision-time visibility đặt sai chỗ:** nằm trong §9.4 "Decision Advisor" nhưng phải áp cho **mọi plugin sinh authoritative output** trong decision-relevant path (Strategy Plugin · Feature/Signal · Risk-context · plugin sinh input cho Decision) — vì I-3 chống look-ahead ở **mọi** compute path, không riêng bước cuối. Nâng thành **§9.5 độc lập**.

### Added — Suggestion
- **§9.9 Forbidden patterns** — bảng 9 anti-pattern đối chiếu trực tiếp với invariant bị vi phạm (gọi Exchange API → I-4 · đọc storage module khác → I-7 · đọc "current state" không cursor-bound → I-2/I-3/I-5 · cấp credential cho plugin → I-11 · registry entry cho mỗi instance → §9.1/§9.3 · mutate ngầm version đang chạy → §9.3 · suy runtime state từ registry → I-12 · ADR cho mọi activate/pause → §9.10 · nâng strategy philosophy thành invariant → Ch2).

### Checklist
- Ch9 v2.2 · §9.1→§9.10 liên tục · fence 2 (chẵn) · **0 tham chiếu §9.x gãy** · phạm vi taxonomy làm rõ kèm điều kiện escalate ADR · runtime identity 4 ràng buộc · permission 4 tầng + `granted ⊆ declared` · decision-time visibility là mục độc lập · forbidden patterns 9 dòng.

## [Unreleased] — Chapter 9 v2.1 (ChatGPT review round 1: **2 Blocker · 2 Major · 1 Suggestion**)

### Fixed — Blocker 1: "Strategy = Plugin" đồng nhất 3 identity khác nhau
- ADR-010 (Approved) đã khóa evidence của Decision gồm **strategy/model version** *và* **strategy instance** *và* **configuration version** như ba thứ riêng — nhưng Chapter 9 gộp tất cả thành "strategy là plugin". Hệ quả: `BTC-15m-conservative`, `BTC-1h-aggressive`, `ETH-15m-paper` cùng dùng `ride-strategy-negation v2.1` nhưng khác tham số sẽ thành **3 module riêng, 3 registry entry, 3 plugin version** — architecture registry phình theo runtime instance, mất khả năng trả lời *"hai instance có dùng cùng implementation không?"*. Tách §9.3: **Plugin Definition/Package** (architecture, `module-registry`) ≠ **Strategy Definition** (domain semantics, Domain Contract) ≠ **Strategy Instance** (runtime, có identity/params/Input Contract/config/lifecycle riêng). Khóa: một plugin phục vụ **nhiều** instance; **Strategy Instance KHÔNG tạo `module-registry` entry mới**.

### Fixed — Blocker 2: query/read contract chưa bị Decision-time visibility ràng buộc
- Công thức mấu chốt: **`Published contract compliance ≠ Decision-time visibility compliance`**. Plugin tuân I-7 hoàn hảo vẫn phá I-2/I-3/I-5 nếu query trả về "current state": cursor pin frontier 1000 → gọi `getCurrentExposure()` → projection đã ở 1010 → Decision attach cursor 1000 nhưng **đã đọc state từ tương lai**. Schema hợp lệ, invariant vỡ. Thêm §9.4: Decision Advisor **cấm đọc ambient/current mutable state**; mọi dependency phải (1) khai báo trong Input Contract/immutable decision-dependency contract · (2) resolve tại hoặc trước `decision_context_cursor` · (3) **pin projection version/schema/config** khi đọc derived state · (4) có evidence đủ để Replay tái tạo đúng snapshot (I-5). Query không chứng minh được knowledge boundary → **cấm dùng tạo authoritative Decision**; projection cho Decision phải trả về source frontier + version + freshness, **cấm lấy "latest" ngầm**.

### Fixed — Major
- **Lifecycle authority chưa tách khỏi architecture registry:** §9.6 cũ gộp "đăng ký, kích hoạt, gỡ bỏ" thành một, ngầm biến `module-registry.yaml` thành nguồn runtime truth — trái I-12 (runtime facts → event log). Tách 4 tầng authority: module identity/taxonomy → `module-registry.yaml` · installable version + content identity → artifact reference (thỏa Referenced Authoritative Artifact rules §8.1.1 nếu bị event/cursor tham chiếu) · **runtime lifecycle facts → authoritative event log** · Strategy Instance state → Strategy Domain Contract.
- **ADR gate quá rộng, chặn vận hành:** "thay đổi ảnh hưởng Decision Pipeline → ADR Required" + "Strategy Plugin mặc định tham gia Decision Pipeline" ⟹ **bật/tắt một strategy instance phải mở ADR** — không vận hành được. §9.8 tách: ADR Required cho architecture/contract change (plugin type/capability mới · published contract · dependency graph · pipeline topology · authority model · lifecycle semantics); **KHÔNG** cho operational action (tạo instance từ plugin đã approved · activate/pause/stop · promote/rollback theo policy đã approved · kill-switch disable · uninstall version không còn reference). Ghi rõ **không đóng ngầm OQ-002** (Strategy Lifecycle Gate vẫn Open, thuộc Quality Gates).

### Added — Suggestion
- **§9.5 Plugin Contract** — 6 nhóm khai báo tối thiểu (Identity · Contract surface · Permission boundary · Decision participation · Lifecycle class · Required capabilities). Không có chúng thì các kiểm tra I-7 Verification đã khóa (network ACL · authorization scope · event schema compatibility · command authorization · capability declaration) **không thực hiện được**. Chapter 9 sở hữu *sự tồn tại + ý nghĩa*; Chapter 10 sở hữu *thuật toán compatibility*.

### Checklist (8 mục)
- Ch9 v2.1 · fence 2 (chẵn) · §9.1→§9.8 liên tục · ba identity tách rõ · query cursor-bounded · runtime facts không lấy từ module-registry · ADR không áp runtime op · OQ-002 không bị đóng ngầm.

## [Unreleased] — Chapter 9 (Plugin Model) v2.0 — Claude tự review

### Fixed — mâu thuẫn trực tiếp với chapter đã Locked
- **"AI Module mặc định là consumer thuần túy của Event Bus" lặp lại wording I-7 ĐÃ BỊ SỬA:** I-7 được siết ở Chapter 7 review từ "mọi module mới mặc định là consumer của Event Bus" → "module mở rộng không được mặc định trở thành thành phần nội bộ của Decision Pipeline; plugin chỉ tương tác qua published contracts". Lý do siết: **không phải plugin nào cũng cần là event consumer** — một plugin chỉ cần query/read contract là hợp lệ. Chapter 9 vẫn mang model cũ. Sửa: phát biểu theo **published contract**, không theo consumer role.
- **Dùng "Event Bus" như authority, trái Chapter 8 §8.1 (Locked):** Chapter 8 khóa transport/broker KHÔNG phải source of truth (authority ở durable append-only event log). Mô tả plugin "consume Event Bus" là mô tả theo **transport** thay vì theo **contract**. Đã sửa.

### Fixed — khoảng trống thẩm quyền
- **Quan hệ Plugin ↔ Module Taxonomy chưa xác định:** Chapter 7 §7.0 định nghĩa taxonomy áp cho "runtime application component" — plugin đúng là loại đó, nhưng Chapter 9 không nói plugin có primary type hay đăng ký ở đâu. Chốt §9.1: plugin **thuộc phạm vi taxonomy**, có primary type (Strategy Plugin điển hình = Compute Engine), đăng ký trong **`module-registry.yaml`** cùng mọi module khác. **KHÔNG tạo plugin registry riêng** — sẽ có 2 nguồn cho cùng sự thật "component nào tồn tại và thuộc loại gì" (I-12).
- **`strategy.json` hardcode artifact vào Constitution:** lặp lại đúng lớp lỗi đã sửa ở I-2 (field list), I-13 (state machine), ADR-008 (ngôn ngữ). Sửa: Constitution giữ nguyên tắc (metadata gồm philosophy/tham số/version), **format và tên file thuộc Domain Contract/module-registry**; chọn format cụ thể là ADR Required nếu ảnh hưởng nhiều module.
- **Versioning chồng lấn Chapter 10:** Chapter 9 phát biểu quy tắc versioning trong khi Chapter 10 sở hữu SemVer/`schemaVersion`/capability/Capability Matrix. §9.5 chỉ tuyên bố *tính độc lập*, trỏ chi tiết sang Chapter 10. Kèm cảnh báo **tránh vòng dependency**: Chapter 10 khai `depends_on: [09-plugin-model]` nên Chapter 9 không được tham chiếu ngược vào chi tiết Ch10.

### Added
- **§9.4 Decision Advisor** — nối plugin với toàn bộ ràng buộc Chapter 8 + ADR-010 vừa Locked: `event_class: decision` · `decision_time` (effective) + `effective_time` prohibited · `decision_context_cursor` đủ 5 field · relational invariants · Append-and-Revalidate khi có registry transition · I-4 (mọi intent qua Risk Gateway). Khóa rõ: **không có ngoại lệ cho AI module** — dùng ML không đổi bất kỳ ràng buộc nào; I-1 vẫn đòi model/config version trong evidence.
- **§9.6 Plugin lifecycle** — thay đổi version/trạng thái plugin đang tham gia Decision Pipeline **không được làm mất evidence của Decision đã tính** (I-1). Protocol cụ thể (drain, activation boundary, in-flight handling) → Phase 1 design spec.
- Frontmatter: thêm dependency `08-event-model` (Chapter 9 giờ tham chiếu trực tiếp Decision event requirements).

## [Unreleased] — Sửa lỗi MANIFEST phát hiện khi re-orientation

### Fixed
- **OQ-005/OQ-006: chữ "RESOLVED" nằm SAI CỘT.** Lần cập nhật milestone trước dùng regex thay nội dung, khiến "RESOLVED" rơi vào cột **Chủ đề** trong khi cột **Trạng thái** vẫn là . Đọc bảng sẽ thấy hai OQ này vẫn Open dù ADR đã Approved. Phát hiện khi Product Owner yêu cầu re-orientation từ MANIFEST — đúng giá trị của việc đọc lại từ nguồn thay vì tin trí nhớ. Đã tách đúng cột.
- **Decision Log còn text stale:** ADR-009/ADR-010 status đã  nhưng phần tóm tắt vẫn ghi "ADR chờ review + accept". Đã sửa thành "Approved 2026-07-18, resolves OQ-00x".
- *Lớp lỗi lặp lại:* regex/replace hàng loạt trên bảng Markdown mà không verify theo cột — cùng họ với các lỗi verify đã ghi nhận trước đó.

## [Milestone] — 2026-07-18 — 🔒 Chapter 8 (Event Model) LOCKED · ADR-009 & ADR-010 APPROVED

Product Owner thực hiện **atomic transition** theo [Chapter 11 §metadata contract](constitution/11-adr-process.md), đúng thứ tự dependency gate:

**1. ADR-009 — Ordering Mechanism → `Approved`**
`status: Draft → Approved` · `addresses: [OQ-005] → []` · `resolves: [] → [OQ-005]` · `approved_by/at` set · **OQ-005 → `Resolved`**.

**2. ADR-010 — Decision Effective-Time Model + Append-and-Revalidate → `Approved`** (sau ADR-009, thỏa dependency gate §7)
`status: Draft → Approved` · `addresses: [OQ-006] → []` · `resolves: [] → [OQ-006]` · `approved_by/at` set · **OQ-006 → `Resolved`**.
*Xác minh gate:* hash ADR-009 không đổi từ vòng 31 (`03fe53cf`), nên ADR-010 ở vòng 32-33 đã được review đối chiếu **đúng snapshot đang được accept** — không cần re-review sau accept.

**3. Chapter 8 → `Locked`** — đủ cả 6 điều kiện lock gate:
1. ✅ ADR-009 Approved · 2. ✅ ADR-010 Approved theo dependency gate · 3. ✅ OQ-005/006 → Resolved · 4. ✅ §8.4.1 Append-and-Revalidate (PO quyết) · 5. ✅ Scoped Policy + canonical Audit Stream (PO quyết) · 6. ✅ Consolidation review hoàn tất.

### Quy mô công việc
Chapter 8 là chapter nặng nhất dự án: **33 vòng review** (so với 3-6 vòng của Chapter 0-7). Các model đã khóa: event log authority (không phải transport) · event envelope + cardinality + relational invariants · `P_global`/`P_run` · per-stream contiguous sequence · explicit causation (semantic thuộc Ch6) · Input Contract cross-mode (exact registry pin, `causal_closure_policy`, `frontier_policy`) · Stream Registry + Genesis Registry + protected Lifecycle/Audit streams · canonical Replay Cursor + `lifecycle_frontier` · Decision Effective-Time Model + `decision_context_cursor` · Append-and-Revalidate + Scoped Preservation Policy · revalidation evidence chain + 3 execution boundary.

### Deferred sang Phase 1 (ADR-009 per-capability gate)
watermark/committed frontier/barrier · multi-stream completeness · late-arrival protocol · buffer sizing/overflow · coordinator/checkpoint · topological merge + cycle-detection implementation · writer handoff/retirement/registry activation protocol · storage/archive/retention/recovery.

**Đã Locked tới nay:** Chapter 0, 1, 2, 3, 4, 5, 6, 7, **8** + ADR-005 → ADR-010.

**Next Milestone:** Chapter 9 — Plugin Model.

## [Unreleased] — Vòng 33: Ch8 v4.8 · ADR-010 (**0 Blocker · 1 Major hẹp**)

### Fixed — Major: preservation fact ép `risk_policy_version` trước khi Risk từng xảy ra
- Vòng trước Claude thêm `risk policy version` vào evidence **bắt buộc** của preservation fact. Nhưng nhánh preservation có thể **kết thúc trước bất kỳ Risk evaluation nào**: Decision tính xong → target stream retire/ineligible → ghi preservation fact → **không có execution eligibility** → không nhất thiết qua Risk Gateway. Ép field này tạo hai kết quả đều sai: (1) gán một risk policy **chưa từng được evaluate** → **evidence giả**; (2) không có policy nên **không ghi được** preservation fact → path thất bại đúng lúc cần bảo toàn evidence.
- **Sửa — tách 2 nhóm evidence với cardinality riêng:**

| Nhóm | Cardinality | Nội dung |
|---|---|---|
| Decision computation | **Required** | semantic Decision output · original cursor · strategy/model version + instance · configuration version · code/build version · mọi policy/reference **thực sự được Decision computation tiêu thụ** |
| Risk evaluation (`risk_policy_ref`) | **Conditional** | chỉ khi Risk evaluation **đã thực sự xảy ra** hoặc policy **thực sự là input** của Decision computation |

- Khóa thêm: **CẤM gán risk policy chưa từng evaluate chỉ để thỏa schema**; Risk Action về sau **tự sở hữu** policy/version nó áp dụng (I-4 — Risk Gateway nằm sau Decision, trước Execution). Đúng tinh thần I-1: trace phải chứa risk policy **đã áp dụng**, không đòi mọi event mang một policy chưa được áp dụng.
- Propagate đồng bộ Chapter 8 §8.4.1 + ADR-010 §2.6.

### Trạng thái sau vòng này
- **ADR-009: `technically ready for Product Owner decision`** (ChatGPT xác nhận, vẫn `Draft` — quyền quyết định thuộc Product Owner).
- ADR-010: Major hẹp duy nhất đã xử lý.
- ChatGPT ghi rõ vòng kế chỉ cần kiểm propagation của evidence ownership + regression liên quan; **không có lý do mở lại** ordering, cursor, lifecycle hay causation model.

### Checklist (5 mục)
- Ch8 v4.8 · fence 68 (chẵn) · `risk_policy_ref` = Conditional trong bảng Ch8 · "CẤM gán" hiện diện ở cả Ch8 và ADR-010 · ADR-010 tách rõ 2 nhóm evidence.

## [Unreleased] — Vòng 32: Ch8 v4.7 · ADR-010 (**1 Blocker · 2 Major · 1 Suggestion**)

### Fixed — Blocker: `dependency_authority` có hai schema shape trong cùng Chapter
- §8.2.3 vẫn hiển thị **object** `dependency_authority: {event_contract_ref: {...}}` trong khi prose kế tiếp và §8.3.4 + ADR-009 đều dùng **scalar enum** `per_effect_event_contract` → validator có thể hợp lệ hóa hai cấu trúc hoàn toàn khác nhau. Đúng lớp lỗi "một concept, nhiều schema shape" đã gặp nhiều lần. Xóa object shape, chuẩn hóa scalar + thêm **cardinality tường minh**: `mode: full` → `dependency_authority` **PROHIBITED**; `mode: declared-state-dependencies` → **REQUIRED**, giá trị duy nhất hiện hỗ trợ `per_effect_event_contract`.

### Fixed — Major
- **Merge target vẫn có thể bị hiểu là `P_global`:** câu "topological order trên **hợp của hai partial order này**" chính là cách vừa định nghĩa `P_global = P_stream ∪ P_causation` → implementation có thể quay lại sort toàn `P_global` gồm cả external vertex, trái model mới. Sửa dứt khoát: **merge order trên `P_run`**; `P_global` chỉ là authority để kiểm causal integrity, phát hiện cycle, và suy quan hệ bắc cầu phải bảo toàn trong `P_run`. Đồng thời **hợp nhất alias**: `P_authoritative` (tên cũ) ≡ `P_global` — giữ hai tên cho cùng concept là nguồn tái phát mơ hồ "merge target nào mới là authority".
- **Execution-boundary validity ở Chapter 8 YẾU HƠN ADR-010:** Chapter 8 chỉ yêu cầu Risk Approval còn valid tại thời điểm **emit intent**; ADR-010 yêu cầu tới **trước external side effect**. Kịch bản hỏng: Risk check pass ở frontier 900 → emit intent → registry transition ở 901 → Execution Engine gửi lệnh ra sàn ở 902 dưới authorization **đã stale**. Propagate rule mạnh vào Chapter 8: eligibility **KHÔNG được đóng băng tại intent creation**; authorization chain phải valid tại **cả 3 boundary** (Risk Approval · Execution Intent · **ngay trước external side effect**); transition ở bất kỳ khoảng nào → blocked lại. Cơ chế (atomic check/fencing token/transaction) → Phase 1; **boundary semantic** khóa tại Chapter 8.

### Added — Suggestion: preservation fact phải đủ evidence tái dựng Decision đã tính
- Scoped Preservation Policy trước đó chỉ bắt buộc cursor + lý do + boundary — nhưng mục tiêu là chứng minh *"một Decision đã được tính"*, trong khi **I-1** yêu cầu tái dựng được cả model/strategy version, configuration, risk policy version. Thêm conformance requirement cho dedicated Event Contract: preservation fact phải **chứa hoặc resolve được** immutable evidence đủ tái dựng semantic Decision output. Nếu không, preservation path thành **"audit stub" rỗng nội dung**. Propagate cả Chapter 8 và ADR-010.

### Note — trạng thái hai ADR
- Lần đầu ChatGPT đánh giá **cả ADR-009 và ADR-010 là "technically near-ready"** — không còn Blocker độc lập trong bản thân hai ADR; chỉ chờ Chapter 8 dùng **cùng schema + cùng merge target + cùng execution-boundary invariant**. Sau vòng này cả ba đã đồng bộ.
- ChatGPT xác nhận `Option A/Option B` còn lại (phần contiguous sequence) có subject ngay trong câu, không tạo cross-reference mơ hồ → không đạt stop rule, không tính finding.

### Checklist (7 mục)
- Ch8 v4.7 · fence 68 (chẵn) · **0 object shape `dependency_authority`** · merge target = `P_run` · `P_authoritative` chỉ còn dạng alias khai báo · 3 execution boundary hiện diện · preservation evidence I-1 ở cả Ch8 và ADR-010.

## [Unreleased] — Vòng 31: Ch8 v4.6 · ADR-009 · ADR-010 (**1 Blocker · 2 Major**)

### Fixed — Blocker: `P_global/P_run` chưa THAY THẾ mô hình cũ, chỉ mới thêm vào
- Chapter 8 thêm split ở §8.2.3 nhưng **§8.3.4 vẫn giữ nguyên** rule cũ "trước khi apply, processor phải xác nhận **mọi** `causation_ref` đã visible và resolved tại cursor". Hai rule không thể cùng áp cho external cause (không thuộc universe + không có `stream_position` + vẫn phải cursor-visible). Sửa: **thay thế hoàn toàn** bằng bảng tách theo scope — in-scope (cursor-visible + apply trước effect + buffer/defer + unresolved tại complete cursor = integrity violation) vs external non-state (chỉ cần committed/existence proof; không cursor-visibility, không `stream_position`, không frontier completeness, cấm đọc payload).
- **Bổ sung tính bắc cầu:** `P_run` bảo toàn quan hệ giữa vertex in-scope **kể cả khi đường nhân quả đi qua vertex external** — `A ≺ X ≺ B` trong `P_global` (X external) ⟹ `A ≺ B` giữ trong `P_run`.
- **ADR-009 §2.3 chưa có split** — vẫn chỉ một `P_authoritative` và tuyên bố merge topological order trên toàn hợp. Đã propagate: merge order trên **`P_run`**, không phải `P_global`; kèm định nghĩa external satisfied prerequisite.

### Fixed — Major
- **`dependency_authority` dạng một `event_contract_ref` singular không đủ:** mỗi event tự pin Event Contract của event type nó; một Input Contract apply nhiều event type/nhiều contract version → một reference đơn không trả lời được "của effect event nào", "có phân loại cho mọi event type không". Vì classification bị cấm nằm trong code, implementation không còn nơi hợp lệ để suy ra. Sửa thành **`dependency_authority: per_effect_event_contract`** — mỗi effect event dùng chính `event_contract_ref` đã pin của nó để phân loại. Machine-readable, không mơ hồ cardinality.
- **ADR-010 chưa ghi dedicated preservation Event Contract:** Chapter 8 đã khóa nhưng ADR-010 — tài liệu **sở hữu** Scoped Preservation Policy — chỉ ghi "ghi fact vào Audit Stream, mang cursor/lý do/boundary". Đây không phải chi tiết payload mà là **event-to-stream eligibility** và guardrail chống dùng Audit Stream để lách `allowed_streams`. Propagate: preservation fact là event type riêng, pin dedicated immutable Event Contract (`allowed_streams` = [canonical Audit Stream], prohibited execution eligibility); **cấm** ghi original Decision event hoặc tái dùng Decision Contract trên preservation path.

### Ghi nhận lỗi xác minh (Claude)
- Vòng trước Claude tuyên bố "**0 chỗ còn Model A/B**" dựa trên grep chuỗi `Model A|Model B` — **bỏ sót biến thể tiếng Việt** "Mô hình A/B", "phương án A". ChatGPT bắt đúng. Lại là lớp lỗi *"lệnh verify không phủ hết đối tượng cần kiểm"*. Đã dọn nốt 3 chỗ và verify lại bằng grep case-insensitive phủ cả 4 biến thể.

### Note — Convergence gate CHƯA binding
- ChatGPT chỉ ra chính xác: stop rule hiện chỉ là **thỏa thuận của vòng review**, ghi ở CHANGELOG — **không phải governance binding**. Muốn binding phải đưa vào **Chapter 11 hoặc 12** qua một vòng review riêng (cả hai đang `In Review`). Ghi **BL-007** thay vì tự đưa vào Constitution.

### Checklist (8 mục, grep phủ cả biến thể VN)
- Ch8 v4.6 · fence 64 (chẵn) · **0 rule cũ "mọi causation cursor-visible"** · bảng in-scope/external hiện diện · ADR-009 có `P_run` (4 chỗ) · `per_effect_event_contract` · ADR-010 có dedicated preservation contract · 0 "Model/Mô hình A|B" (kết quả duy nhất còn lại là "model artifact" — ML artifact, không liên quan).

## [Unreleased] — Vòng 30: Ch8 v4.5 · ADR-009 · ADR-010 (**2 Blocker · 2 Major · 1 Minor**)

### Fixed — Blocker 1: tách global causation graph khỏi run-local apply graph
- **Mâu thuẫn formal:** §8.2.3 cho phép external non-state cause nằm ngoài cursor universe (không `stream_position`, không thuộc apply set) NHƯNG §8.3.4 vẫn bắt **mọi** `causation_ref` phải cursor-visible và nằm trong topological apply order → không thể cùng thực thi. Sửa: tách **`P_global`** (= `P_stream ∪ P_causation` trên toàn bộ event graph, phải là DAG) khỏi **`P_run`** (induced order trên apply set của một Input Contract). External cause KHÔNG phải vertex của `P_run`, là **external satisfied prerequisite**: cần committed/existence proof, không cần `stream_position`, không ảnh hưởng frontier completeness, cấm đọc payload. Processor rule tách đôi: in-scope → cursor-visible + apply trước effect; external → chỉ cần committed proof.
- **`causal_closure_policy` bắt buộc nhưng vắng mặt trong canonical Input Contract YAML** — đã thêm vào schema và vào danh sách bắt buộc bump `contract_version`.

### Fixed — Blocker 2: ADR-009 chưa thiết lập hạ tầng mà ADR-010 phụ thuộc
- ADR-010 (Scoped Policy) phụ thuộc **canonical Audit Stream**, nhưng ADR-009 — tài liệu sở hữu stream lifecycle/topology — không hề quyết định nó. Do acceptance order bắt buộc accept ADR-009 trước, ADR-009 có thể được accept mà **không thiết lập hạ tầng bắt buộc** cho ADR-010. Thêm vào ADR-009: Genesis Registry định nghĩa đúng MỘT Lifecycle Stream + đúng MỘT Audit Stream, cả hai là **protected streams** (stable ID · active mọi registry version · KHÔNG được retire · writer handoff được nhưng identity không đổi). Ranh giới: ADR-009 sở hữu *sự tồn tại + lifecycle invariants*; ADR-010 sở hữu *Decision nào được dùng preservation path + guardrail*.

### Fixed — Major
- **ADR-010 thiếu validity interval của revalidation:** implementation có thể hiểu "chỉ cần một success event trong quá khứ là đủ". Propagate nguyên rule + bổ sung điểm quan trọng: **kiểm lúc tạo `ExecutionIntent` là CHƯA ĐỦ** nếu registry đổi giữa intent creation và lúc Execution Engine thực sự gửi lệnh — phải xác nhận authorization chain còn valid **tại execution boundary**, trước khi phát sinh external side effect.
- **Preservation fact chưa có Event Contract authority:** Chapter 8 khóa "Event Contract là nguồn duy nhất cho event-to-stream eligibility", nhưng ghi original Decision event vào Audit Stream sẽ vi phạm chính `allowed_streams` của nó. Khóa: preservation fact là **event type RIÊNG**, pin **dedicated Event Contract** (`allowed_streams` chỉ gồm canonical Audit Stream · mang full `decision_context_cursor` gốc · tham chiếu transition/retirement boundary · **prohibited execution eligibility**); cấm tái dùng contract của Decision gốc để lách eligibility.

### Fixed — Minor: dọn sạch tên "Model A/B" mơ hồ
- ChatGPT nêu cho ADR-010, nhưng rà ra Chapter 8 có **4 cặp Model A/B khác nghĩa nhau**. Đổi hết sang tên mô tả: **Direct Contract Pin** (vs Composite Identity) · **Retained-in-Universe** (vs Excluded-from-Universe) · **Single Lifecycle Stream** (vs Lifecycle Frontier Vector) · **Dedicated Lifecycle Frontier** (vs Control-Stream-In-Contract). Kết quả: **0 chỗ còn "Model A/B"** trong Ch8, ADR-009, ADR-010, MANIFEST.

### Note — Convergence gate (ChatGPT đề xuất, Claude đồng ý)
- ChatGPT **không đồng ý đóng băng v4.4** như Claude đề xuất trước đó, với lý do hợp lý: các Blocker gần đây là **mâu thuẫn bên trong chính model đã chọn**, không phải chi tiết protocol Phase 1. Nhưng sau khi sửa, áp **stop rule** — chỉ nhận finding mới nếu: (1) mâu thuẫn Chapter đã Locked · (2) tạo hai authority cạnh tranh · (3) làm một invariant đã chọn không implementable · (4) phá governance/acceptance order. KHÔNG mở rộng sang: cycle-detection algorithm · coordinator cụ thể · storage layout · watermark implementation · buffer sizing · recovery workflow — những thứ này giữ ở Phase 1 đúng như ADR-009 đã defer.

### Checklist (7 mục)
- **0 "Model A/B"** trong cả 4 tài liệu · `P_global`/`P_run` tách · `causal_closure_policy` trong YAML · ADR-009 có protected Audit Stream · ADR-010 có validity interval · preservation Event Contract khóa · fence 64 (chẵn).

## [Unreleased] — 2026-07-18 — PO quyết Scoped Policy (Ch8 v4.4 · ADR-009 · ADR-010) + vòng 30 fixes

### Product Owner decision — Blocker "Decision stream retire tại transition"
- Chọn **Hướng 1 (Scoped Policy)**: Append-and-Revalidate chỉ áp khi Decision target stream **vẫn active + event vẫn eligible** dưới post-transition registry. Nếu stream đã retire/không eligible → ghi **immutable computation/rejection fact vào canonical Audit Stream**. Alternative (lifecycle drain invariant — cấm retire tới khi mọi in-flight Decision đóng) bị loại vì retirement có thể chờ không giới hạn.
- **Artifact mới: canonical Audit Stream** — định nghĩa tại **Genesis Registry** cùng canonical Lifecycle Stream. Cả hai là **protected streams**: retirement invariant KHÔNG áp dụng, vì retire chúng sẽ tái tạo đúng vòng bootstrap mà Genesis Registry sinh ra để chặn.
- 4 ràng buộc với preservation fact: tham chiếu chính xác `decision_context_cursor` gốc (đầy đủ) · ghi lý do + `event_record_ref` của retirement/activation boundary · KHÔNG cấp execution eligibility · **cấm dùng preservation path để lách retirement** khi đường append bình thường còn khả dụng.
- **Lock gate điều kiện 5 hoàn thành** — còn 4: ADR-009 accept · ADR-010 accept · OQ-005/006 Resolved · consolidation hoàn tất.

### Fixed — Blocker 1 (propagation)
- **ADR-009 §2.4 vẫn giữ mô hình causation cũ đã bị Chapter 8 v4.2 bác** — hai authoritative document công bố hai semantic khác nhau. Sửa: `causation_refs` = direct domain causal predecessor (semantic thuộc Ch6 §6.7, ADR KHÔNG định nghĩa lại); closure là ràng buộc cấp Input Contract; closure violation làm **Input Contract invalid**, không đổi semantic bất biến của event. Fixture sửa theo.

### Fixed — Major
- **`causal_closure_policy` bắt buộc nhưng chưa có schema/authority:** formal hóa `{mode: full | declared-state-dependencies, dependency_authority.event_contract_ref}`. Với `declared-state-dependencies`, **Event Contract** (immutable, versioned) khai báo cause nào là state dependency — **cấm để classification trong code processor**, nếu không một Input Contract immutable sẽ đổi semantic sau mỗi lần deploy. Hòa giải mâu thuẫn "mọi causation phải visible tại cursor": yêu cầu đó chỉ áp cho cause **thuộc apply set**; external non-state cause chỉ cần chứng minh đã committed, KHÔNG thuộc merged apply set, **cấm giả lập `stream_position`**.
- **Revalidation success có thể stale trước Risk/Execution:** evidence chain không đứt ≠ evidence còn hiệu lực. Thêm **validity interval**: `revalidation.registry_version = active_registry_at(risk_approval_lifecycle_frontier)`; transition xảy ra sau revalidation nhưng trước Risk/Execution → eligibility **quay lại blocked**, bắt buộc revalidate lại; Execution Intent phải chứng minh Risk Approval còn valid dưới boundary hiện tại.

### Fixed — Minor
- **Authority của `related_event_refs` mô tả sai:** Chapter 6 §6.7 chỉ định nghĩa correlation + causation, **không** định nghĩa quan hệ non-causal này — tài liệu đang trỏ tới một semantic authority không tồn tại. Sửa: Chapter 8 sở hữu base representation + invariant "non-causal"; **Event Contract** sở hữu ý nghĩa cụ thể từng relation.

### Checklist (8 mục)
- Ch8 v4.4 · fence 60 (chẵn) · Audit Stream trong Genesis (4 chỗ) · protected streams · Scoped Policy chốt · lock gate ĐK5 xong · ADR-010 có Scoped Policy · ADR-009 có fixtures mới.

### Checklist (8 mục)
- Ch8 v4.2 · fence 58 (chẵn) · semantic Ch6 khôi phục · `causal_closure_policy` ở tầng Input Contract · evidence chain normative · **0 stale wording** · **0 "Model A/B" mơ hồ trong ADR-010** · fixtures mới hiện diện.

### Checklist (7 mục)
- Ch8 v4.1 · fence 58 (chẵn) · **0 chỗ còn "CHỜ PRODUCT OWNER QUYẾT"** · ADR-010 có §2.6 · ADR-009 wording đã chính xác boundary · fixtures cho A hiện diện · lock gate điều kiện 4 đánh dấu xong.

## [Unreleased] — Chapter 6 (Identity Model) v2.0 — Claude tự review

### Fixed — mâu thuẫn với chapter đã Locked (Backward Consistency Check)
- **"Một phiên bản mới = một ID mới" mâu thuẫn I-13 (Locked):** áp cho mọi entity thì Position sau mỗi state transition (OPEN→CLOSED) sẽ thành ID mới — phá vỡ khái niệm stateful entity của I-13 (cùng Position giữ cùng ID qua vòng đời). §6.2 tách rõ Event Identity (mỗi event 1 ID, invalidate = record mới) vs Entity Identity (giữ 1 ID xuyên suốt state machine).
- **ID sortable theo thời gian mâu thuẫn Ordering Authority (Chapter 5 §5.4 Locked):** dùng ID nhúng timestamp để sort = dựa gián tiếp physical clock, đúng lỗi cross-node ordering Chapter 5 cấm. §6.3 tách bạch: ID sortable chỉ để index/storage locality, KHÔNG phải nguồn business/causal ordering.

### Fixed — hardcode (bài học I-2/I-13)
- Danh sách ID cụ thể (SwingID/StructureID/RegimeID/DecisionID...) là domain-specific — Chapter 4 (Locked) đã quy định domain concept sống ở /docs/domain/. Bỏ liệt kê, chỉ giữ nguyên tắc ID (unique/immutable/distributed-safe).
- ULID chốt cứng công nghệ trong Constitution → chuyển thành ADR (nguyên tắc: sortable/unique/distributed-safe; ULID/UUIDv7/Snowflake là cơ chế).

### Changed
- Thêm dependency `04-domain-principles`, `05-time-model` vào frontmatter (chapter này tương tác trực tiếp với cả hai).
- §6.5 làm rõ vai trò Identity với I-1 Explainability (ID reuse phá correlation/causation chain).

## [Unreleased] — Chapter 6 v2.1 (ChatGPT review round 1: 3 Major + 2 Minor)

### Fixed — Major
- **"Distributed-safe, không cần khóa tập trung" cấm nhầm sequence-based ID:** yêu cầu này vô tình cấm loại ID cần nhất cho arbitrage đa sàn (broker/coordinator-assigned sequence cho total order). Sửa: tách Identity uniqueness (sinh phân tán OK) vs Ordering/sequence assignment (có thể cần single-writer/coordinator — hợp lệ, không cấm).
- **Ép mọi domain concept có ID:** value object (Price, Money, TimeRange — `kind: value_object` ở Chapter 4) không có identity riêng (equality by value). Thêm loại thứ 3 vào §6.2: Event / Entity / Value Object.
- **Thiếu Correlation/Causation Identity cho I-1:** entity ID một mình không đủ để reconstruct causation chain. Thêm §6.5: Correlation ID (nhóm event cùng luồng) + Causation ID (trỏ parent event) — hạ tầng bắt buộc cho Explainability, tách biệt entity ID.

### Fixed — Minor
- ID uniqueness scope phải khai báo tường minh trong Domain Contract (per-Account/per-Venue...), không mặc định global — venue-assigned order ID chỉ unique trong 1 venue.
- Thêm quy tắc thời điểm cấp ID: trước/tại thời điểm entity đầu tiên tồn tại, không cấp muộn — bắt buộc cho I-10 (execution intent cần client-assigned ID trước khi gửi venue để chống duplicate).

## [Unreleased] — Chapter 6 v2.2 (ChatGPT review round 2: 2 Minor)

### Fixed — Minor
- **§6.5 Internal Identity vs External Reference:** venue order ID / exchange trade ID không do Ride kiểm soát (có thể trùng giữa venue, format đổi) — không được dùng làm primary identity, chỉ lưu như attribute. Order có internal `OrderID` (cho I-10) + lưu kèm `venue_order_id`, reconcile theo cặp.
- **§6.7 ID là opaque:** không nhúng business meaning để logic suy diễn ngược từ ID — nếu logic phụ thuộc cấu trúc ID thì đổi format ID (ULID→UUIDv7) sẽ phá logic ở nơi không ngờ. Thông tin nghiệp vụ phải là field tường minh. (Timestamp trong ID cho sortable/index §6.3 là tối ưu storage, không phải business meaning.)
