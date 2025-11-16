# azure-tts-plugin Specification

## Purpose
TBD - created by archiving change add-azure-tts-plugin. Update Purpose after archive.
## Requirements
### Requirement: Azure TTS 服务器
系统 SHALL 提供基于 Python Flask 的 Azure TTS HTTP 服务器。

#### Scenario: 服务器启动
- **WHEN** 启动 Azure TTS 服务器
- **THEN** 服务器监听指定端口（默认 5003）
- **AND** 加载 Azure TTS 配置和环境变量
- **AND** 初始化语音合成器

#### Scenario: 文本转语音请求
- **WHEN** 接收到 GET /api/tts 请求
- **THEN** 验证请求参数（text、voice、token 等）
- **AND** 映射语速因子 e 到 Azure TTS rate 参数
- **AND** 调用 Azure TTS 服务生成音频
- **AND** 直接返回 WAV 格式音频数据（不保存文件）

### Requirement: Koodo 插件配置
系统 SHALL 提供兼容 Koodo 的插件配置文件。

#### Scenario: 插件元数据配置
- **WHEN** 生成插件配置
- **THEN** 包含插件标识符、类型、版本信息
- **AND** 定义多种中文语音列表（xiaoxiao、yaoyao、yunyang）
- **AND** 配置 Azure TTS 服务器 URL 和访问令牌

#### Scenario: JavaScript 插件脚本
- **WHEN** 生成插件脚本
- **THEN** 实现 getAudioPath 函数（按 Coqui TTS 方式处理）
- **AND** 支持文本、语速、输出目录参数
- **AND** 接收音频数据并保存为 WAV 文件
- **AND** 处理 Azure TTS API 调用和错误

### Requirement: 音频数据处理
系统 SHALL 处理音频数据的生成和传输。

#### Scenario: 音频数据生成
- **WHEN** 文本转语音请求成功
- **THEN** 生成 WAV 格式音频数据（16kHz，256kbps）
- **AND** 直接在内存中处理
- **AND** 通过 HTTP 响应返回音频数据

### Requirement: 服务器管理和错误处理
系统 SHALL 提供服务器状态检查和错误处理机制。

#### Scenario: 健康检查
- **WHEN** 接收到 GET /health 请求
- **THEN** 返回服务器状态信息
- **AND** 验证 Azure TTS 连接状态

#### Scenario: API 调用失败
- **WHEN** Azure TTS API 调用失败
- **THEN** 记录错误日志（不包含令牌）
- **AND** 返回 HTTP 错误响应

#### Scenario: 参数验证失败
- **WHEN** 请求参数无效或令牌错误
- **THEN** 返回相应的 HTTP 错误码

