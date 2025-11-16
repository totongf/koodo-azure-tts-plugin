# Koodo 听书连接问题诊断

## 🔧 当前状态检查

### ✅ 服务器状态
- **服务运行**：正常（PID: 16459）
- **端口监听**：5003 端口正常监听
- **API响应**：HTTP 200 状态码
- **语音合成**：Azure TTS 连接正常
- **访问令牌**：azure-tts-2024（匹配）

### ✅ 插件配置
- **插件文件**：`plugins/azure_tts_plugin.json` 
- **服务器URL**：`http://127.0.0.1:5003/api/tts`
- **访问令牌**：azure-tts-2024
- **语音列表**：xiaoxiao, xiaoyi, yunxi 等 14 个中文语音

## 🔍 可能的问题

### 1. Koodo 缓存问题
- **症状**：Koodo 使用旧版本的插件配置
- **解决**：重启 Koodo 或清除插件缓存

### 2. 插件重新加载
- **症状**：Koodo 未识别到新的插件文件
- **解决**：在 Koodo 设置中重新加载语音插件

### 3. 网络权限问题
- **症状**：Koodo 无法连接到本地服务器
- **解决**：检查 Koodo 的网络权限设置

### 4. 项目文件路径变更
- **症状**：Koodo 找不到插件文件
- **解决**：确保 `plugins/` 目录可访问

## 🛠️ 解决步骤

### 步骤 1：重启服务器
```bash
# 确保服务器正在运行
curl http://localhost:5003/health
# 应该返回 {"status":"healthy",...}
```

### 步骤 2：重启 Koodo
1. 完全关闭 Koodo 应用
2. 重新启动 Koodo
3. 检查是否加载了新的 Azure TTS 插件

### 步骤 3：清除缓存
1. 在 Koodo 设置中找到"语音插件"或"插件管理"
2. 重新扫描或刷新插件列表
3. 确保选择 Azure TTS 作为语音引擎

### 步骤 4：验证配置
1. 在 Koodo 中检查语音列表
2. 确认能看到晓晓、云希等 Azure 语音
3. 测试一个简单的听书文本

## 📊 测试命令

```bash
# 1. 测试服务器连接
curl http://localhost:5003/health

# 2. 测试完整TTS API
curl -s -o /dev/null -w "状态码: %{http_code}, 响应时间: %{time_total}s\n" \
  "http://127.0.0.1:5003/api/tts?text=测试&voice=xiaoxiao&e=1.0&token=azure-tts-2024"

# 3. 检查日志
tail -f logs/server.log
```

## 🎯 期望结果

正常情况下，你应该能看到：
- **健康检查**：返回 `{"status":"healthy",...}`
- **TTS API**：返回 HTTP 200 状态码
- **日志记录**：在 `logs/server.log` 中看到请求日志
- **Koodo**：能看到 Azure TTS 语音列表并能成功生成语音

## 🆘 如果仍有问题

1. **检查 Koodo 版本**：确保支持语音插件功能
2. **检查插件文件**：`plugins/azure_tts_plugin.json` 是否存在且格式正确
3. **检查网络连接**：Koodo 是否允许访问本地服务器
4. **检查日志**：查看 `logs/server.log` 中是否有错误信息

请尝试以上步骤，然后告诉我结果如何！