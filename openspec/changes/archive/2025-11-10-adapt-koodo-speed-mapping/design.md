# 设计文档 - Koodo 速度参数映射适配

## 技术架构

### 当前架构
```
Koodo → 插件(直接传递) → Azure TTS 服务
        rate 参数          e 参数
```

### 目标架构
```
Koodo → 插件(映射转换) → Azure TTS 服务
        rate 参数  →  azure_rate → e 参数
        映射公式: azure_rate = 1.0 + (rate / 100)
```

## 核心设计决策

### 1. 映射位置
选择在 JavaScript 插件中实现映射转换，原因：
- **性能考虑**: 在客户端进行转换，避免服务端开销
- **兼容性**: 保持服务端 API 格式不变
- **隔离性**: 将映射逻辑与业务逻辑分离

### 2. 映射函数设计
```javascript
function mapKoodoSpeedToAzureRate(koodoSpeed) {
    // 公式: Azure语速 = 1.0 + (Koodo速度参数 / 100)
    const azureRate = 1.0 + (koodoSpeed / 100.0);
    
    // 边界值处理
    return Math.max(0.0, Math.min(2.0, azureRate));
}
```

### 3. 参数验证策略
- **类型检查**: 确保输入为数字类型
- **范围限制**: Koodo 速度参数 -100 到 100
- **边界处理**: Azure 语速限制在 0.0 到 2.0
- **默认值**: 异常情况下使用 1.0 (基准语速)

## 实现细节

### JavaScript 插件修改
**文件**: `plugins/azure_tts_plugin.json`

**当前代码结构**:
```javascript
const getTTSAudio = async(text, rate, config) => {
    // ...
    const params = {
        text: text,
        voice: voice,
        e: rate.toString(),  // 直接传递
        token: token
    };
    // ...
}
```

**修改后结构**:
```javascript
const mapKoodoSpeedToAzureRate = (koodoSpeed) => {
    if (typeof koodoSpeed !== 'number' || isNaN(koodoSpeed)) {
        console.warn('无效的 Koodo 速度参数:', koodoSpeed);
        return 1.0; // 默认基准语速
    }
    
    const azureRate = 1.0 + (koodoSpeed / 100.0);
    const clampedRate = Math.max(0.0, Math.min(2.0, azureRate));
    
    if (clampedRate !== azureRate) {
        console.log(`Koodo速度 ${koodoSpeed} 映射为 Azure语速 ${clampedRate} (原始: ${azureRate})`);
    }
    
    return clampedRate;
};

const getTTSAudio = async(text, rate, config) => {
    // ...
    const azureRate = mapKoodoSpeedToAzureRate(rate);
    console.log(`映射: Koodo速度 ${rate} → Azure语速 ${azureRate}`);
    
    const params = {
        text: text,
        voice: voice,
        e: azureRate.toString(),  // 使用映射后的值
        token: token
    };
    // ...
}
```

### 错误处理策略
1. **类型错误**: 记录警告，使用默认值
2. **范围错误**: 记录日志，应用边界值
3. **异常处理**: 捕获所有可能的错误，确保功能不中断

### 性能考虑
- **函数内联**: 映射函数简单，内联优化友好
- **最小化计算**: 只有在速度参数非零时才进行日志记录
- **缓存**: 相同速度参数的结果可以缓存（可选）

## 测试策略

### 单元测试
1. **映射公式验证**
   - Koodo=0 → Azure=1.0
   - Koodo=25 → Azure=1.25
   - Koodo=-25 → Azure=0.75

2. **边界值测试**
   - Koodo=-100 → Azure=0.0
   - Koodo=100 → Azure=2.0
   - 超范围值自动裁剪

3. **错误处理测试**
   - 非数字输入
   - NaN 值
   - null/undefined

### 集成测试
1. **完整流程测试**: Koodo 设置 → 插件映射 → Azure 服务
2. **实际语音验证**: 不同速度参数的实际语音效果
3. **性能测试**: 映射功能的性能影响

## 向后兼容性

### API 兼容性
- ✅ 服务端 API 格式保持不变
- ✅ JSON 配置结构不变
- ✅ 现有使用方式不受影响

### 功能兼容性
- ✅ 现有语速设置仍然有效
- ✅ 零速度参数映射为基准语速
- ✅ 负速度参数正确处理

## 监控和日志

### 关键指标
- 映射函数调用次数
- 边界值裁剪频率
- 错误率统计

### 日志级别
- **INFO**: 映射参数记录
- **WARNING**: 边界值裁剪
- **ERROR**: 类型错误或异常

## 部署策略

### 灰度发布
1. 先部署到测试环境验证
2. 小范围用户试点
3. 监控指标正常后全量发布

### 回滚方案
- 保留当前插件版本作为回滚选项
- 可通过配置开关快速禁用映射功能
- 完整的错误处理确保服务稳定性

## 未来扩展

### 可配置性
- 支持自定义映射公式
- 可配置的边界值限制
- 不同语音的映射调整

### 优化方向
- 性能监控和优化
- 缓存机制实现
- 更多速度范围支持