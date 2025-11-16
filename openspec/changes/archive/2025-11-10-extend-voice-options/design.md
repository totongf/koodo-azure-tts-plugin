# 设计文档：扩展 Azure TTS 语音选项和语速控制

## 架构设计

### 1. 语音扩展策略
- 添加更多 Azure TTS 支持的中文语音
- 按照语音特征进行分类（女声、男声、童声等）
- 提供语音描述信息（音色特点、适用场景）

### 2. 语速控制优化
- 保持语速范围：0.5 - 2.0
- 验证所有语音选项在 0.5-2.0 范围内的语速控制正常工作
- 添加语速测试标准，确保音频质量

### 3. 语音扩展策略
- 添加更多 Azure TTS 支持的中文语音
- 按照语音特征进行分类（女声、男声等）
- 提供语音描述信息（音色特点、适用场景）
- 验证新语音的可用性和语速控制功能

## 技术实现

### 1. Azure TTS 服务更新
```python
# 扩展的语音列表
self.supported_voices = {
    # 女声
    'xiaoxiao': 'zh-CN-XiaoxiaoNeural',
    'xiaoyi': 'zh-CN-XiaoyiNeural',
    'yunxi': 'zh-CN-YunxiNeural',
    'yunxia': 'zh-CN-YunxiaNeural',
    'xiaochen': 'zh-CN-XiaochenNeural',
    'xiaohan': 'zh-CN-XiaohanNeural',
    'xiaomeng': 'zh-CN-XiaomengNeural',
    'xiaomo': 'zh-CN-XiaomoNeural',
    'xiaoxuan': 'zh-CN-XiaoxuanNeural',
    'xiaoyan': 'zh-CN-XiaoyanNeural',
    # 男声
    'yaoyao': 'zh-CN-YaoyaoNeural',
    'yunyang': 'zh-CN-YunyangNeural',
    'yunye': 'zh-CN-YunyeNeural',
    # 童声
    'yundeng': 'zh-CN-YundengNeural'
}

# 语音描述
self.voice_descriptions = {
    'xiaoxiao': '女声，自然温柔，适合日常对话',
    'xiaoyi': '女声，年轻活泼，适合轻松内容',
    'yunxi': '女声，成熟稳重，适合正式场合',
    # ... 更多描述
}
```

### 2. 语速控制实现
```python
def synthesize_speech(self, text, voice='xiaoxiao', rate=1.0):
    """语音合成方法"""
    # 验证语速范围
    if rate < 0.5 or rate > 2.0:
        logger.warning(f"语速超出范围: {rate}，使用默认值 1.0")
        rate = 1.0
    
    # 构建 SSML
    ssml = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
        <voice name="{voice_name}">
            <prosody rate="{rate}">
                {text}
            </prosody>
        </voice>
    </speak>
    """
```

### 3. 插件配置更新
```json
{
  "voiceList": [
    {
      "displayName": "晓晓 (Azure)",
      "id": "xiaoxiao",
      "description": "女声，自然温柔",
      "category": "female"
    },
    {
      "displayName": "云希 (Azure)",
      "id": "yunxi", 
      "description": "女声，成熟稳重",
      "category": "female"
    }
    // ... 更多语音选项
  ]
}
```

## 语音可用性验证
- 测试每个新增语音在 Azure TTS 服务中的可用性
- 验证每个语音的语速控制功能（0.5-2.0 范围）
- 记录测试结果和任何发现的问题

## 测试策略
- 单元测试：验证所有语音选项
- 集成测试：测试语速控制效果
- 性能测试：确保扩展后性能稳定