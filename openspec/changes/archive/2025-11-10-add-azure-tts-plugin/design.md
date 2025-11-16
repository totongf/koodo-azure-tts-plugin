## Context
项目需要为 Koodo 创建一个 Azure TTS 插件，替代现有的 Coqui TTS 插件。需要实现 Python 服务器和 JavaScript 插件脚本，确保与 Koodo 插件系统完全兼容。

## Goals / Non-Goals
- Goals: 
  - 提供稳定的 Azure TTS 语音合成服务
  - 完全兼容 Koodo 插件参数规范
  - 支持多种中文语音（xiaoxiao、yaoyao、yunyang 等）
  - 输出 WAV 格式，16kHz 采样率，适合听书
  - 使用固定令牌进行访问控制
- Non-Goals:
  - 不支持 Docker 容器化部署
  - 不实现音频缓存机制
  - 不考虑高并发场景（个人使用）
  - 不支持实时流式音频（当前版本）

## Decisions
- Decision: 使用 Python Flask 创建轻量级 HTTP 服务器
  - Rationale: 简单易部署，快速开发，与 Azure SDK 兼容性好
- Decision: 使用 Azure Cognitive Services Speech SDK
  - Rationale: 官方支持，功能完整，文档丰富
- Decision: 保持与 Coqui TTS 插件相同的 API 接口
  - Rationale: 确保向后兼容，减少迁移成本

## Risks / Trade-offs
- Azure TTS API 调用频率限制 → 实现请求限流和错误重试
- 网络延迟影响响应时间 → 异步处理和超时机制
- 个人使用场景 → 简化架构，专注核心功能

## Migration Plan
1. 部署 Python Azure TTS 服务器（端口 5003）
2. 生成插件配置文件和语音列表
3. 配置固定令牌访问控制
4. 在 Koodo 中安装新插件
5. 测试多种中文语音合成功能
6. 逐步替换 Coqui TTS 插件

## Technical Specifications
- 音频格式：WAV，16kHz 采样率，256kbps 比特率
- 支持语音：zh-CN-XiaoxiaoNeural、zh-CN-YaoyaoNeural、zh-CN-YunyangNeural
- 服务器端口：5003（避免与现有服务冲突）
- API 接口：GET /api/tts（所有参数通过 Query 传递）
- 访问控制：固定令牌（通过 Query 参数 token 传递）
- 参数映射：语速因子 e 映射到 Azure TTS rate 参数
- 音频处理：内存中处理，不持久化存储
- 健康检查：GET /health 端点
- 日志记录：简单日志输出，不记录令牌，不考虑轮转