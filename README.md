# koodo-azure-tts-plugin

koodo-azure-tts-plugin 是一个兼容 [Koodo Reader](https://github.com/troyeguo/koodo-reader) 语音插件系统的 Azure 语音合成插件，提供高质量的语音合成服务。

## 功能特性

- 🎙️ **多语言支持**：支持多种语言和语音风格
- ⚡ **实时合成**：快速生成语音文件
- 📝 **文本处理**：支持复杂文本格式
- 🎵 **音频质量**：提供高保真 WAV 输出
- 📁 **单格式输出**：当前版本输出 `wav` 文件（16kHz/16bit/Mono）
- 🔌 **Koodo 兼容**：无缝集成 Koodo 语音插件系统
  - 测试版本：2.2.1

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

# Python 依赖 - 使用 uv 包管理器
uv install

# 或者使用 uv pip 命令
uv pip install -r requirements.txt
```

## 配置

### 获取 Azure 认知服务密钥

前往 [Azure 门户](https://portal.azure.com/) 创建认知服务资源，获取以下信息：

### 环境变量配置

项目使用环境变量直接管理配置参数，无需创建 `.env` 文件。设置以下环境变量：

#### 核心配置（必须）
- `SPEECH_KEY`：Azure 认知服务语音密钥
- `SPEECH_REGION`：Azure 认知服务区域（如：`eastasia`）

#### 服务器配置（仅 Python 服务，可选）
- `PORT`：服务器监听端口，默认：`5003`
- `DEBUG`：是否开启调试模式，默认：`False`

#### 安全配置（必须）
- `TTS_ACCESS_TOKEN`：API 访问令牌（启动服务前必须配置）

### 环境变量设置方法

**Linux/macOS**：
```bash
export SPEECH_KEY=your_azure_speech_key_here
export SPEECH_REGION=eastasia
export TTS_ACCESS_TOKEN=your-secure-token
```

**Windows**：
```cmd
set SPEECH_KEY=your_azure_speech_key_here
set SPEECH_REGION=eastasia
set TTS_ACCESS_TOKEN=your-secure-token
```

## 使用方法

### Koodo 插件安装

在 Koodo 中安装本插件，只需以下简单步骤：

1. 打开 Koodo 应用
2. 进入「设置」→「插件」页面
3. 点击「添加插件」按钮
4. 在弹出的对话框中，粘贴 `plugins/koodo_azure_tts_plugin.json` 文件中的 JSON 配置代码
5. 点击「保存」按钮，完成插件安装

> ⚠️  将 JSON 中的 `token` 字段替换为你在服务器上配置的 `TTS_ACCESS_TOKEN`，否则请求会被拒绝。

JSON 配置文件路径：[plugins/koodo_azure_tts_plugin.json](plugins/koodo_azure_tts_plugin.json)

### JavaScript 插件（Koodo 集成）

```javascript
const azureTTSPlugin = require('./main/js/koodo_azure_tts_plugin');

// 调用语音合成
const audioPath = await azureTTSPlugin.getAudioPath(
  "你好，这是 Azure TTS 语音合成示例", // 文本内容
  1.0, // 语速（0.5-2.0）
  "./output", // 输出目录
  { /* 配置选项 */ }
);

console.log("生成的音频文件路径：", audioPath);
```

### Python 服务

```bash
# 使用脚本（自动检测环境变量和虚拟环境）
./scripts/start_service.sh

# 或直接启动（需手动激活虚拟环境并配置变量）
uv run python main/python/app.py
```

服务启动后，可通过 API 调用：

```bash
curl "http://localhost:5003/api/tts?text=你好，这是 Azure TTS 语音合成示例&voice=xiaoxiao&e=0&token=your-secure-token" \
  --output speech.wav
```

> 接口仅支持 `GET /api/tts`，`token` 通过查询参数传入并必须与服务器的 `TTS_ACCESS_TOKEN` 匹配。

## 项目结构

```
├── audio/               # 音频文件输出目录
├── config/              # 配置文件目录
├── docs/                # 文档目录
├── logs/                # 日志文件
├── main/                # 核心代码
│   ├── js/             # JavaScript 插件实现
│   └── python/         # Python 服务实现
├── openspec/            # 开放规范文档
├── plugins/             # 插件分发目录
├── scripts/             # 辅助脚本
├── test/                # 测试代码
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

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系

如有问题或建议，请通过以下方式联系：
- GitHub Issues：在项目仓库提交问题
- Email：your-email@example.com
