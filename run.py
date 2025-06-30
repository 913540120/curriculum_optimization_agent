#!/usr/bin/env python3
"""
培养方案智能优化平台 V2.0 - 启动脚本
"""

import subprocess
import sys
import os

def check_dependencies():
    """检查依赖包是否安装"""
    try:
        import streamlit
        import openai
        print("✅ 依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def run_app():
    """运行Streamlit应用"""
    if not check_dependencies():
        return
    
    print("🚀 启动培养方案智能优化平台...")
    print("📱 应用将在浏览器中自动打开")
    print("🔗 如果没有自动打开，请访问: http://localhost:8501")
    print("⏹️  按 Ctrl+C 停止应用")
    print("-" * 50)
    
    try:
        # 设置环境变量，禁用遥测
        os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
        
        # 运行Streamlit应用
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    run_app() 