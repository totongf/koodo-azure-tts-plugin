/**
 * Azure TTS Koodo 插件脚本
 * 兼容 Koodo 语音插件系统，调用 Azure TTS 服务
 */

const getAudioPath = async (text, rate, outputDir, config) => {
    const path = require("path");
    const fs = require("fs");
    
    // 生成唯一文件名
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
};

// 将对象转换为查询字符串
const objectToQueryString = (obj) => {
    const params = [];
    for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
            const value = obj[key];
            const encodedKey = encodeURIComponent(key);
            const encodedValue = encodeURIComponent(value);
            params.push(`${encodedKey}=${encodedValue}`);
        }
    }
    return params.join("&");
};

// 调用 Azure TTS API 获取音频数据
const getTTSAudio = async (text, rate, config) => {
    const axios = require("axios");
    
    // 获取配置参数
    const url = config.url || "http://127.0.0.1:5003/api/tts";
    const voice = config.voice || "xiaoxiao";
    const token = config.token;

    if (!token) {
        throw new Error("未配置 token，无法调用 Azure TTS 服务。请在插件 JSON 中填写与服务器一致的 token。");
    }
    
    // 构建请求参数
    const params = {
        text: text,
        voice: voice,
        e: rate.toString(), // 语速因子
        token: token
    };
    
    const queryString = objectToQueryString(params);
    const fullUrl = `${url}?${queryString}`;
    
    return new Promise((resolve, reject) => {
        axios.get(fullUrl, { 
            responseType: "arraybuffer",
            timeout: 30000 // 30秒超时
        })
        .then(response => {
            console.log("Azure TTS 请求成功");
            resolve(response.data);
        })
        .catch(error => {
            console.error("Azure TTS 请求失败:", error.message);
            
            // 提供更详细的错误信息
            let errorMessage = "音频生成失败";
            if (error.response) {
                // 服务器响应错误
                errorMessage = `服务器错误: ${error.response.status}`;
                if (error.response.data) {
                    try {
                        const errorText = Buffer.from(error.response.data).toString('utf8');
                        errorMessage += ` - ${errorText}`;
                    } catch (e) {
                        // 忽略解码错误
                    }
                }
            } else if (error.request) {
                // 网络错误
                errorMessage = "网络连接失败";
            } else {
                // 其他错误
                errorMessage = error.message;
            }
            
            console.error(errorMessage);
            reject(new Error(errorMessage));
        });
    });
};

// 导出函数供 Koodo 调用
global.getAudioPath = getAudioPath;
