# Change: 添加 Azure TTS 插件支持

## Why
为 Koodo 创建基于 Azure TTS 的语音插件，替代现有的 Coqui TTS 插件，提供更稳定、高质量的云语音合成服务。

## What Changes
- 创建 Python Azure TTS 服务器，提供 RESTful API 接口
- 开发 Koodo 兼容的 JavaScript 插件脚本
- 配置 Azure TTS 插件元数据和语音列表
- 实现内存音频数据处理和传输
- 添加错误处理和日志记录

## Impact
- Affected specs: 新增 azure-tts-plugin 规范
- Affected code: 新增 Python 服务器代码和 JavaScript 插件脚本
- External dependencies: Azure TTS 服务