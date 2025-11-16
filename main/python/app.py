"""
Azure TTS Flask 服务器
为 Koodo 提供文本转语音 API 服务
"""
import os
import logging
import math
from flask import Flask, request, jsonify, Response
from azure_tts_service import AzureTTSService


def isNaN(value):
    """检查值是否为NaN"""
    try:
        return math.isnan(float(value))
    except (ValueError, TypeError):
        return True


# 配置日志 - 按照项目规范存放在根目录 /logs
# 获取项目根目录路径
project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
log_dir = os.path.join(project_root, 'logs')
log_file = os.path.join(log_dir, 'server.log')
os.makedirs(log_dir, exist_ok=True)

# 尝试设置日志文件权限
try:
    os.chmod(log_file, 0o666)
except Exception as e:
    print(f"警告: 无法设置日志文件权限: {e}")

# 创建根日志记录器 - 简化配置避免重复
root_logger = logging.getLogger()
root_logger.setLevel(logging.WARNING)

# 只使用文件handler，避免重复
root_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
root_handler.setFormatter(formatter)

# 清除现有处理器并添加新的
root_logger.handlers = []
root_logger.addHandler(root_handler)

# 创建 Flask 应用
app = Flask(__name__)

# Flask应用设置最简配置
app.logger.setLevel(logging.INFO)

# 固定访问令牌（从环境变量获取）
ACCESS_TOKEN = os.getenv('TTS_ACCESS_TOKEN', 'azure-tts-2024')

# 初始化 Azure TTS 服务
try:
    tts_service = AzureTTSService()
    app.logger.info("Azure TTS 服务初始化成功")
except Exception as e:
    app.logger.error(f"Azure TTS 服务初始化失败: {str(e)}")
    tts_service = None


def validate_token():
    """验证访问令牌"""
    token = request.args.get('token')
    if not token or token != ACCESS_TOKEN:
        app.logger.warning(f"无效的访问令牌: {token}")
        return False
    return True


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    try:
        if tts_service is None:
            return jsonify({
                'status': 'error',
                'message': 'TTS 服务未初始化'
            }), 500
        
        # 检查 Azure TTS 连接
        connection_ok = tts_service.check_connection()
        
        return jsonify({
            'status': 'healthy' if connection_ok else 'unhealthy',
            'azure_tts_connection': 'ok' if connection_ok else 'failed',
            'supported_voices': list(tts_service.supported_voices.keys())
        })
    except Exception as e:
        app.logger.error(f"健康检查失败: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def map_speed_to_rate(koodo_speed):
    """
    将Koodo速度参数映射为Azure TTS语速参数
    映射公式: Azure语速 = 1.0 + (Koodo速度参数 / 100)
    """
    try:
        if koodo_speed is None or koodo_speed == '':
            koodo_speed = 0
        
        koodo_speed = float(koodo_speed)
        
        if isNaN(koodo_speed):
            app.logger.warning("Koodo 速度参数无效，使用默认值 0")
            return 1.0
        
        mapped_rate = 1.0 + (koodo_speed / 100)
        final_rate = max(0.5, min(2.0, mapped_rate))
        
        if final_rate != mapped_rate:
            app.logger.info(f"速度参数调整: Koodo={koodo_speed} -> Azure={mapped_rate:.2f} -> 最终={final_rate:.2f}")
        else:
            app.logger.info(f"速度参数映射: Koodo={koodo_speed} -> Azure={final_rate:.2f}")
            
        return final_rate
    except (ValueError, TypeError):
        app.logger.warning(f"速度参数格式错误: {koodo_speed}，使用默认值 0")
        return 1.0


@app.route('/api/tts', methods=['GET'])
def text_to_speech():
    """文本转语音 API"""
    try:
        # 验证访问令牌
        if not validate_token():
            return jsonify({'error': '无效的访问令牌'}), 401
        
        if tts_service is None:
            return jsonify({'error': 'TTS 服务不可用'}), 503
        
        # 获取请求参数
        text = request.args.get('text')
        voice = request.args.get('voice', 'xiaoxiao')
        koodo_speed = request.args.get('e', 0)  # Koodo速度参数
        
        # 验证必要参数
        if not text:
            return jsonify({'error': '缺少必要参数: text'}), 400
        
        # 验证语音类型
        if voice not in tts_service.supported_voices:
            app.logger.warning(f"不支持的语音类型: {voice}")
            voice = 'xiaoxiao'  # 使用默认语音
        
        # 将Koodo速度参数映射为Azure语速
        azure_rate = map_speed_to_rate(koodo_speed)
        
        app.logger.info(f"处理 TTS 请求: text={text[:50]}..., voice={voice}, Koodo速度={koodo_speed}, Azure语速={azure_rate:.2f}")
        
        # 生成语音
        audio_data = tts_service.synthesize_speech(text, voice, azure_rate)
        
        # 返回音频数据
        return Response(
            audio_data,
            mimetype='audio/wav',
            headers={
                'Content-Disposition': 'attachment; filename=speech.wav',
                'Content-Length': str(len(audio_data))
            }
        )
        
    except ValueError as e:
        app.logger.error(f"参数错误: {str(e)}")
        return jsonify({'error': f'参数错误: {str(e)}'}), 400
    except Exception as e:
        app.logger.error(f"TTS 处理失败: {str(e)}")
        return jsonify({'error': '语音合成失败'}), 500


@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({'error': '端点不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    app.logger.error(f"内部服务器错误: {str(error)}")
    return jsonify({'error': '内部服务器错误'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5003))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    app.logger.info(f"启动 Azure TTS 服务器，端口: {port}")
    app.logger.info(f"调试模式: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)