#!/usr/bin/env node

/**
 * 测试 Azure TTS 插件脚本
 */

const path = require('path');
const fs = require('fs');

// 加载插件脚本
const pluginCode = fs.readFileSync('./main/js/koodo_azure_tts_plugin.js', 'utf8');
eval(pluginCode);

async function testPlugin() {
    try {
        console.log('开始测试 Azure TTS 插件...');
        
        // 测试参数
        const text = 'Hello Azure TTS';
        const rate = 1.0;
        const outputDir = '/tmp';
        const config = {
            url: 'http://127.0.0.1:5003/api/tts',
            voice: 'xiaoxiao',
            token: 'azure-tts-2024'
        };
        
        // 调用插件函数
        const audioPath = await getAudioPath(text, rate, outputDir, config);
        
        console.log('音频文件生成成功:', audioPath);
        
        // 验证文件
        if (fs.existsSync(audioPath)) {
            const stats = fs.statSync(audioPath);
            console.log('文件大小:', stats.size, '字节');
            
            // 验证文件格式
            const { execSync } = require('child_process');
            const fileType = execSync(`file "${audioPath}"`).toString().trim();
            console.log('文件类型:', fileType);
            
            console.log('测试成功！');
        } else {
            console.error('音频文件未生成');
        }
        
    } catch (error) {
        console.error('测试失败:', error.message);
    }
}

// 运行测试
testPlugin();