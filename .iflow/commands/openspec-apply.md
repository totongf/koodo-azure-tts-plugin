---
name: /openspec-apply
id: openspec-apply
category: OpenSpec
description: 实现已批准的 OpenSpec 变更并保持任务同步。
---
<!-- OPENSPEC:START -->
**安全护栏**
- 优先选择直接、最简化的实现，只有在明确要求或确实需要时才会添加复杂性。
- 保持变更严格聚焦于所请求的结果。
- 如果需要额外的 OpenSpec 规范或澄清，请参考 `openspec/AGENTS.md`（位于 `openspec/` 目录内—如果看不到请运行 `ls openspec` 或 `openspec update`）。

**步骤**
将这些步骤跟踪为 TODO，并逐一完成。
1. 阅读 `changes/<id>/proposal.md`、`design.md`（如果存在）和 `tasks.md` 以确认范围和验收标准。
2. 按顺序处理任务，保持编辑最小化且专注于所请求的变更。
3. 在更新状态之前确认完成度—确保 `tasks.md` 中的每个项目都已完成。
4. 所有工作完成后更新检查清单，使每个任务标记为 `- [x]` 并反映实际情况。
5. 需要额外上下文时，参考 `openspec list` 或 `openspec show <item>`。

**参考**
- 在实现过程中如果需要从提案中获取额外上下文，请使用 `openspec show <id> --json --deltas-only`。
<!-- OPENSPEC:END -->
