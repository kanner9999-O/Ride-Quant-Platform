---
id: 10-compatibility-capability-contract
title: Compatibility & Capability Contract
version: "1.0"
status: In Review
owner: Product Owner
reviewers: [ChatGPT, Claude]
approved_by: null
approved_at: null
created_at: "2026-07-16"
last_review: "2026-07-16"
next_review: null
depends_on: ["09-plugin-model"]
---

# 10. Compatibility & Capability Contract

Version đúng không đảm bảo dữ liệu đủ — cần kiểm tra thêm **capability**:

```json
{
  "requires": { "StructureEngine": "^2.0.0" },
  "supports": ["SWING_STRENGTH", "BOS", "CHOCH"]
}
```

**Quy tắc:**
- Mỗi Engine khi publish version mới phải khai báo `schemaVersion` và danh sách capability nó hỗ trợ.
- Thay đổi breaking schema = bắt buộc bump major version (SemVer nghiêm ngặt).
- **Plugin Loader** kiểm tra compatibility + capability lúc **khởi động (startup)**. Không khớp → **fail-fast lúc startup**.
- **Capability Matrix** cho từng engine (Supports Replay / Live / Backtest / Multi-Exchange: Yes/No) — dùng làm tiêu chí readiness cho production.
