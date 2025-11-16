#!/usr/bin/env node

/**
 * 简单测试 Azure TTS API
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

function getTTSAudio(text, rate, config) {
    return new Promise((resolve, reject) => {
        const url = config.url || "http://127.0.0.1:5003/api/tts";
        const voice = config.voice || "xiaoxiao";
        const token = config.token || "azure-tts-2024";
        
        // 构建查询参数
        const params = new URLSearchParams({
            text: text,
            voice: voice,
            e: rate.toString(),
            token: token
        });
        
        const fullUrl = `${url}?${params}`;
        const urlObj = new URL(fullUrl);
        
        const options = {
            hostname: urlObj.hostname,
            port: urlObj.port,
            path: urlObj.pathname + urlObj.search,
            method: 'GET',
            timeout: 30000
        };
        
        const client = urlObj.protocol === 'https:' ? https : http;
        
        const req = client.request(options, (res) => {
            let data = [];
            
            res.on('data', (chunk) => {
                data.push(chunk);
            });
            
            res.on('end', () => {
                if (res.statusCode === 200) {
                    console.log("Azure TTS 请求成功");
                    resolve(Buffer.concat(data));
                } else {
                    reject(new Error(`HTTP ${res.statusCode}: ${res.statusMessage}`));
                }
            });
        });
        
        req.on('error', (error) => {
            console.error("网络请求失败:", error.message);
            reject(error);
        });
        
        req.on('timeout', () => {
            req.destroy();
            reject(new Error("请求超时"));
        });
        
        req.end();
    });
}

async function getAudioPath(text, rate, outputDir, config) {
    const filename = new Date().getTime() + ".wav";
    const outputPath = path.join(outputDir, "tts");
    
    // 确保 tts 目录存在
    if (!fs.existsSync(outputPath)) {
        fs.mkdirSync(outputPath, { recursive: true });
    }
    
    try {
        // 获取音频数据
        const audioData = await getTTSAudio(text, rate, config);
        
        // 保存音频文件
        const filePath = path.join(outputPath, filename);
        fs.writeFileSync(filePath, audioData);
        
        return filePath;
    } catch (error) {
        console.error("生成音频失败:", error);
        throw error;
    }
}

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