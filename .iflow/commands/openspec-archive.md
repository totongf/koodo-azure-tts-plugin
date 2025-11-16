---
name: /openspec-archive
id: openspec-archive
category: OpenSpec
description: 归档已部署的 OpenSpec 变更并更新规范。
---
<!-- OPENSPEC:START -->
**安全护栏**
- 优先选择直接、最简化的实现，只有在明确要求或确实需要时才会添加复杂性。
- 保持变更严格聚焦于所请求的结果。
- 如果需要额外的 OpenSpec 规范或澄清，请参考 `openspec/AGENTS.md`（位于 `openspec/` 目录内—如果看不到请运行 `ls openspec` 或 `openspec update`）。

**步骤**
1. 确定要归档的变更 ID：
   - 如果此提示已经包含特定的变更 ID（例如在由斜杠命令参数填充的 `<ChangeId>` 块内），请在使用前去除空白字符。
   - 如果对话中松散地引用了变更（例如按标题或摘要），请运行 `openspec list` 来显示可能的 ID，分享相关候选，并确认用户意图的是哪个。
   - 否则，请检查对话，运行 `openspec list`，并询问用户要归档哪个变更；在继续之前等待确认的变更 ID。
   - 如果仍然无法识别单个变更 ID，请停止并告诉用户暂时无法归档任何内容。
2. 通过运行 `openspec list`（或 `openspec show <id>`）验证变更 ID，如果变更缺失、已归档或在其他方面不准备归档，请停止。
3. 运行 `openspec archive <id> --yes`，以便 CLI 移动变更并应用规范更新而不显示提示（仅对纯工具工作使用 `--skip-specs`）。
4. 检查命令输出以确认目标规范已更新且变更已放置在 `changes/archive/` 中。
5. 使用 `openspec validate --strict` 进行验证，如果有任何异常，使用 `openspec show <id>` 进行检查。

**参考**
- 在归档之前使用 `openspec list` 确认变更 ID。
- 使用 `openspec list --specs` 检查刷新的规范，并在移交之前解决任何验证问题。
<!-- OPENSPEC:END -->
