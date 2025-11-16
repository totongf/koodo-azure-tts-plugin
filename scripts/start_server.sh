#!/bin/bash
# Azure TTS 服务器启动脚本

# 设置环境变量
export SPEECH_KEY=***REMOVED***
export SPEECH_REGION=eastasia
export TTS_ACCESS_TOKEN=azure-tts-2024
export PORT=5003

# 启动服务器
cd "$(dirname "$0")/.."
# 确保使用当前目录的虚拟环境
export UV_VENV_ENV=.venv
uv run python main/python/app.py