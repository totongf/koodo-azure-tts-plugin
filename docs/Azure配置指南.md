# Azure TTS 服务配置指南

## 🔧 已修复的问题

### ✅ 访问令牌匹配问题
- **问题**：Flask 服务器默认令牌与 JavaScript 插件令牌不匹配
- **解决**：改为必须通过环境变量 `TTS_ACCESS_TOKEN` 注入访问令牌
- **位置**：`main/python/app.py`

### ✅ 日志路径规范化
- **问题**：日志文件存放在 `main/logs/` 而不是项目规范要求的 `/logs`
- **解决**：修正日志路径配置，统一存放至项目根目录 `/logs/`
- **位置**：`main/python/app.py:8-11`

### ✅ 服务启动脚本
- **新增**：`scripts/start_service.sh` 启动脚本
- **功能**：自动加载环境变量、激活虚拟环境、启动服务

## 📋 当前状态

### ✅ 已解决
- 访问令牌验证问题
- 服务启动流程优化

### ⚠️ 仍需配置
- Azure TTS 环境变量（`SPEECH_KEY` 和 `SPEECH_REGION`）
- API 访问令牌（`TTS_ACCESS_TOKEN`）

## 🚀 使用方法

### 1. 快速启动
```bash
# 使用提供的启动脚本
./scripts/start_service.sh
```

### 2. 手动启动
```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动服务
cd main/python
python app.py
```

## 🔑 Azure TTS 配置

### 获取 Azure 认知服务配置

1. **创建 Azure 认知服务资源**：
   - 访问 [Azure Portal](https://portal.azure.com)
   - 创建"认知服务"资源
   - 选择"语音服务"

2. **获取配置信息**：
   - 在资源页面找到"密钥和终结点"
   - 复制"密钥 1"作为 `SPEECH_KEY`
   - 复制"位置/区域"作为 `SPEECH_REGION`

### 配置方法

**设置系统环境变量**

项目直接使用系统环境变量进行配置，无需创建 .env 文件。设置方法如下：

**Linux/macOS**：
```bash
export SPEECH_KEY="your_actual_key"
export SPEECH_REGION="your_actual_region"
export TTS_ACCESS_TOKEN="your_secure_token"
```

**Windows**：
```cmd
set SPEECH_KEY="your_actual_key"
set SPEECH_REGION="your_actual_region"
set TTS_ACCESS_TOKEN="your_secure_token"
```

## 🧪 验证配置

配置完成后，重启服务并检查：
```bash
# 检查服务健康状态
curl http://localhost:5003/health

# 测试语音合成
curl "http://localhost:5003/api/tts?text=测试&voice=xiaoxiao&token=your-secure-token"
```

### 4. 支持的语音

项目支持以下中文语音：
- **女声**: xiaoxiao, xiaoyi, yunxi, yunxia, xiaochen, xiaohan, xiaomeng, xiaomo, xiaoxuan, xiaoyan, yaoyao
- **男声**: yunyang, yunye
- **童声**: yundeng

### 5. 速度参数映射说明

**⚠️ 重要：Koodo 速度参数与 Azure TTS 语速的映射关系**

插件目前支持两组速度输入：
1. `-50、-25、0、25、50、75、100`（Koodo 传统枚举），按照 `Azure = 1.0 + (Koodo / 100)` 转换，并在 0.5~2.0 之间截断。
2. `0.5、0.75、1、1.25、1.5、1.75、2`（Koodo 新枚举），直接作为 Azure 语速使用，同样限制在 0.5~2.0 范围。

**注意事项：**
- 任何未在枚举中的值都会回退到 1.0 倍速。
- Azure TTS 最低支持 0.5 倍速、最高支持 2.0 倍速；更低或更高的值会被截断。
- 请求日志仅输出语速信息和文本长度，避免泄露具体文本内容。

## 注意事项

- 确保 Azure 认知服务资源已正确创建并激活
- 密钥和区域信息必须在 Azure Portal 中获取
- 环境变量包含敏感信息，请勿提交到版本控制系统
- 确保服务启动前已正确设置所有必要的环境变量
