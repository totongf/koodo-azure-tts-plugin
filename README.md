# koodo-azure-tts-plugin

koodo-azure-tts-plugin 是一个兼容 Koodo 语音插件系统的 Azure 语音合成插件，提供高质量的语音合成服务。

## 功能特性

- 🎙️ **多语言支持**：支持多种语言和语音风格
- ⚡ **实时合成**：快速生成语音文件
- 📝 **文本处理**：支持复杂文本格式
- 🎵 **音频质量**：提供高保真音频输出
- 📁 **多格式输出**：支持 WAV/MP3 等格式
- 🔌 **Koodo 兼容**：无缝集成 Koodo 语音插件系统

## 技术栈

- **JavaScript 版本**：用于 Koodo 插件系统集成
- **Python 版本**：用于独立服务部署
- **Azure Speech Service**：语音合成核心引擎

## 安装

### 环境要求

- Node.js 14+（JavaScript 插件）
- Python 3.7+（Python 服务）

### 安装依赖

```bash
# JavaScript 依赖
npm install

# Python 依赖
pip install -r requirements.txt
```

## 配置

### 1. 获取 Azure 认知服务密钥

前往 [Azure 门户](https://portal.azure.com/) 创建认知服务资源，获取以下信息：
- `SPEECH_KEY`：语音服务密钥
- `SPEECH_REGION`：服务区域（如：`eastasia`）

### 2. 配置文件

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# Azure 认知服务语音密钥
SPEECH_KEY=your_azure_speech_key_here

# Azure 认知服务区域
SPEECH_REGION=your_azure_region_here

# 服务器配置（仅 Python 服务）
PORT=5003
DEBUG=False

# API 访问令牌（用于身份验证）
API_TOKEN=azure-tts-2024
```

## 使用方法

### JavaScript 插件（Koodo 集成）

```javascript
const azureTTSPLugin = require('./main/js/azure_tts_plugin');

// 调用语音合成
const audioPath = await azureTTSPLugin.getAudioPath(
  "你好，这是 Azure TTS 语音合成示例", // 文本内容
  1.0, // 语速（0.5-2.0）
  "./output", // 输出目录
  { /* 配置选项 */ }
);

console.log("生成的音频文件路径：", audioPath);
```

### Python 服务

```bash
# 启动服务
python main/python/app.py

# 或使用脚本
./scripts/start_server.sh
```

服务启动后，可通过 API 调用：

```bash
curl -X POST http://localhost:5003/tts \
  -H "Authorization: Bearer azure-tts-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，这是 Azure TTS 语音合成示例",
    "rate": 1.0
  }'
```

## 项目结构

```
├── audio/               # 音频文件输出目录
├── config/              # 配置文件目录
├── docs/                # 文档目录
├── examples/            # 示例配置
├── logs/                # 日志文件
├── main/                # 核心代码
│   ├── js/             # JavaScript 插件实现
│   └── python/         # Python 服务实现
├── openspec/            # 开放规范文档
├── plugins/             # 插件分发目录
├── scripts/             # 辅助脚本
├── test/                # 测试代码
├── .env                 # 配置文件
├── .env.example         # 配置示例
├── .gitignore           # Git 忽略规则
├── package.json         # JavaScript 项目配置
└── requirements.txt     # Python 依赖
```

## 开发

### 测试

```bash
# JavaScript 测试
npm test

# Python 测试
pytest test/
```

### 插件打包

```bash
node scripts/compress_plugin.js
```

生成的压缩插件将保存在 `plugins/` 目录下。

## 许可证

ISC

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系

如有问题或建议，请通过以下方式联系：
- GitHub Issues：在项目仓库提交问题
- Email：your-email@example.com
