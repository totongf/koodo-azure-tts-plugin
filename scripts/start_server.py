#!/usr/bin/env python3
"""
Azure TTS 服务器启动脚本
"""
import os
import sys
import subprocess
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "main" / "python"))

def main():
    """启动服务器"""
    print("启动 Azure TTS 服务器...")
    
    # 检查环境变量
    required_vars = ['SPEECH_KEY', 'SPEECH_REGION', 'TTS_ACCESS_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"错误: 缺少环境变量: {', '.join(missing_vars)}")
        print("请设置以下环境变量:")
        for var in missing_vars:
            print(f"  export {var}=your_value")
        sys.exit(1)
    
    # 启动 Flask 应用
    app_path = project_root / "main" / "python" / "app.py"
    cmd = ['uv', 'run', 'python', str(app_path)]
    
    print(f"执行命令: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except subprocess.CalledProcessError as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
