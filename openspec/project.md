# Project Context

## Purpose
Azure TTS 测试项目，专注于为 Koodo 创建 Azure TTS 版本的语音插件。项目旨在开发一个兼容 Koodo 语音 API 的 Azure TTS 插件，替代现有的 Coqui TTS 插件。

## Tech Stack
- Python - 主要编程语言，使用 uv 作为包管理工具
- Azure TTS - 微软语音合成服务
- JavaScript - Koodo 插件脚本开发
- HTTP API - RESTful 接口通信

## Project Conventions

### Code Style
- Python 遵循 PEP 8 规范
- JavaScript 使用现代 ES6+ 语法
- 文件命名使用小写字母和下划线
- 注释优先使用中文
- 使用 uv 创建和管理 .venv 虚拟环境
- 使用 uv pip 安装和管理项目依赖
- 所有 Python 开发必须在 .venv 虚拟环境中进行

### Architecture Patterns
- 微服务架构，TTS 服务独立部署
- RESTful API 接口设计
- 异步音频处理和流式传输
- 虚拟环境管理：使用 uv 创建和管理 .venv 虚拟环境，使用 uv pip 进行包管理
- 目录结构分离：
  - main/ - 主要代码目录
    - python/ - Azure TTS Python 集成代码
    - js/ - Koodo 插件 JavaScript 代码
  - test/ - 测试代码目录
    - unit/ - 单元测试
    - integration/ - 集成测试
  - docs/ - 项目文档目录
  - logs/ - 日志文件目录
  - config/ - 配置文件目录
  - plugins/ - 插件相关文件和构建输出
  - audio/ - 音频文件临时存储
  - scripts/ - 构建和部署脚本
  - examples/ - 示例配置和使用案例

### Testing Strategy
- 单元测试覆盖核心功能
- 集成测试验证 API 接口
- 性能测试关注音频生成速度和质量

### Git Workflow
- 主分支：main
- 功能分支：feature/功能名称
- 修复分支：hotfix/问题描述
- 提交信息使用中文，格式：类型: 简短描述

## Domain Context
- Koodo 语音插件系统架构
- TTS（Text-to-Speech）文本转语音技术
- Azure TTS 服务集成和配置
- 音频格式处理（WAV、MP3 等）
- 多语言语音支持（重点关注中文）
- 插件配置格式和脚本 SHA256 校验
- uv Python 包管理器和虚拟环境管理

## Koodo 插件参数规范
- t (string): 文本内容（要转换为语音的文字）
- e (number): 语速因子（倍速，如 1.0、1.2）
- o (string): 输出目录（保存语音文件的根路径）
- i (object): TTS 配置对象（包含 host、url、voice、pitch、volume 等配置）

## Important Constraints
- 音频质量优先，确保语音自然度
- 响应时间控制在可接受范围内
- 支持并发请求处理
- 资源使用优化，避免内存泄漏
- Python环境管理：项目使用 uv 进行 Python 包管理和虚拟环境创建
- 虚拟环境目录：项目使用 .venv 作为 Python 虚拟环境目录

## External Dependencies
- Azure TTS 云服务
- Koodo 语音插件系统
- HTTP 客户端库（axios）
- 本地文件系统存储

## Environment Configuration
- SPEECH_KEY: Azure TTS 订阅密钥（已配置）
- SPEECH_REGION: Azure TTS 服务区域（eastasia，已配置）
- ENDPOINT: Azure TTS 服务终结点（可选，可通过区域自动生成）

## Azure TTS 技术细节
- 支持语音格式：WAV、MP3 等
- 神经网络语音：多语言支持，如 zh-CN-XiaoxiaoNeural
- SSML 支持：语音合成标记语言，用于控制语音样式、音调等
- 异步处理：支持流式音频生成
- 错误处理：网络超时、认证失败、配额限制等
