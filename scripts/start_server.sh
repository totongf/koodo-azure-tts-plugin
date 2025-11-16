#!/bin/bash
# Azure TTS 服务器启动脚本

# 注意：不再硬编码环境变量，请在系统或项目配置中设置
# 需要设置的环境变量：
# - SPEECH_KEY: Azure Speech 服务密钥
# - SPEECH_REGION: Azure Speech 服务区域
# - TTS_ACCESS_TOKEN: API 访问令牌
# - PORT: 服务器端口（默认 5003）

# 启动服务器
cd "$(dirname "$0")/.."
# 确保使用当前目录的虚拟环境
export UV_VENV_ENV=.venv
uv run python main/python/app.py