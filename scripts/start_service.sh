#!/bin/bash

# Azure TTS 服务启动脚本

echo "启动 Azure TTS 服务..."

# 检查并设置必要的环境变量
if [ -z "$SPEECH_KEY" ]; then
    echo "⚠️  警告: SPEECH_KEY 环境变量未设置"
    echo "请设置 SPEECH_KEY 环境变量"
fi

if [ -z "$SPEECH_REGION" ]; then
    echo "⚠️  警告: SPEECH_REGION 环境变量未设置"
    echo "请设置 SPEECH_REGION 环境变量"
fi

# 检查 Python 环境
if [ -d ".venv" ]; then
    echo "🐍 激活虚拟环境..."
    source .venv/bin/activate
fi

# 启动服务
echo "🚀 启动服务..."
cd main/python
python app.py