#!/usr/bin/env node

/**
 * 压缩 Azure TTS 插件脚本
 * 将 JavaScript 代码压缩为单行，并计算 SHA256
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function compressScript(filePath) {
    try {
        // 读取原始脚本
        const scriptContent = fs.readFileSync(filePath, 'utf8');
        
        // 简单压缩：移除注释和多余空白
        let compressed = scriptContent
            .replace(/\/\*[\s\S]*?\*\//g, '') // 移除块注释
            .replace(/\/\/.*$/gm, '') // 移除行注释
            .replace(/\s+/g, ' ') // 合并空白
            .replace(/;\s*}/g, '}') // 移除分号前的空白
            .replace(/\s*([{}();,])\s*/g, '$1') // 移除运算符周围的空白
            .trim();
        
        // 计算 SHA256
        const hash = crypto.createHash('sha256').update(compressed).digest('hex');
        
        console.log('脚本压缩完成');
        console.log('原始大小:', scriptContent.length, '字符');
        console.log('压缩后大小:', compressed.length, '字符');
        console.log('SHA256:', hash);
        
        return {
            compressed: compressed,
            sha256: hash
        };
        
    } catch (error) {
        console.error('压缩脚本失败:', error.message);
        process.exit(1);
    }
}

// 主程序
function main() {
    const scriptPath = path.join(__dirname, '..', 'main', 'js', 'koodo_azure_tts_plugin.js');
    
    if (!fs.existsSync(scriptPath)) {
        console.error('插件脚本文件不存在:', scriptPath);
        process.exit(1);
    }
    
    const result = compressScript(scriptPath);
    
    // 保存压缩后的脚本
    const outputPath = path.join(__dirname, '..', 'plugins', 'azure_tts_plugin_compressed.js');
    fs.writeFileSync(outputPath, result.compressed);
    
    console.log('压缩脚本已保存到:', outputPath);
    console.log('SHA256 值:', result.sha256);
    
    // 输出可复制的 SHA256
    console.log('\n复制以下 SHA256 值到插件配置:');
    console.log(result.sha256);
}

if (require.main === module) {
    main();
}

module.exports = { compressScript };