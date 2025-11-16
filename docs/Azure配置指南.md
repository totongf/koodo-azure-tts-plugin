# Azure TTS 服务配置指南

## 🔧 已修复的问题

### ✅ 访问令牌匹配问题
- **问题**：Flask 服务器默认令牌与 JavaScript 插件令牌不匹配
- **解决**：统一使用 `your-api-token` 作为访问令牌
- **位置**：`main/python/app.py:24`

### ✅ 日志路径规范化
- **问题**：日志文件存放在 `main/logs/` 而不是项目规范要求的 `/logs`
- **解决**：修正日志路径配置，统一存放至项目根目录 `/logs/`
- **位置**：`main/python/app.py:8-11`

### ✅ 服务启动脚本
- **新增**：`start_service.sh` 启动脚本
- **功能**：自动加载环境变量、激活虚拟环境、启动服务

## 📋 当前状态

### ✅ 已解决
- 访问令牌验证问题
- 服务启动流程优化

### ⚠️ 仍需配置
- Azure TTS 环境变量（`SPEECH_KEY` 和 `SPEECH_REGION`）

## 🚀 使用方法

### 1. 快速启动
```bash
# 使用提供的启动脚本
./start_service.sh
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
```

**Windows**：
```cmd
set SPEECH_KEY="your_actual_key"
set SPEECH_REGION="your_actual_region"
```

## 🧪 验证配置

配置完成后，重启服务并检查：
```bash
# 检查服务健康状态
curl http://localhost:5003/health

# 测试语音合成
curl "http://localhost:5003/api/tts?text=测试&voice=xiaoxiao&token=your-api-token"
```

### 4. 支持的语音

项目支持以下中文语音：
- **女声**: xiaoxiao, xiaoyi, yunxi, yunxia, xiaochen, xiaohan, xiaomeng, xiaomo, xiaoxuan, xiaoyan
- **男声**: yaoyao, yunyang, yunye
- **童声**: xiaoyi, xiaochen, xiaomeng

### 5. 速度参数映射说明

**⚠️ 重要：Koodo 速度参数与 Azure TTS 语速的映射关系**

Koodo 中的速度参数需要转换为 Azure TTS 的语速参数，映射公式如下：

```
Azure语速 = 1.0 + (Koodo速度参数 / 100)
```

**具体映射关系：**
- `Koodo=0` → `Azure=1.0` (基准语速，100%)
- `Koodo=25` → `Azure=1.25` (25%加快语速)
- `Koodo=-25` → `Azure=0.75` (25%减慢语速)
- `Koodo=50` → `Azure=1.5` (50%加快语速)
- `Koodo=-50` → `Azure=0.5` (50%减慢语速)

**参数范围：**
- Koodo 速度参数：-100 到 100
- Azure 语速参数：0.0 到 2.0
- 基准速度：Koodo=0 对应 Azure=1.0

**注意事项：**
- `Koodo=0` 表示基准语速，不是停止播放
- 正值表示比标准语速快，负值表示比标准语速慢
- Azure TTS 服务会自动处理超出范围的速度值

## 注意事项

- 确保 Azure 认知服务资源已正确创建并激活
- 密钥和区域信息必须在 Azure Portal 中获取
- 环境变量包含敏感信息，请勿提交到版本控制系统
- 确保服务启动前已正确设置所有必要的环境变量