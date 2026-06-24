#!/usr/bin/env python
"""
run.py - AdalatMitra Application Runner
"""

import os
import sys
import subprocess
import webbrowser
import time

def main():
    """Run Streamlit app."""
    print("⚖️ Starting AdalatMitra...")
    print("=" * 50)
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("⚠️ .env file not found. Please create one with your API keys.")
        sys.exit(1)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__} found")
    except ImportError:
        print("❌ Streamlit not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Get the directory of this script
    project_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(project_dir, "frontend", "streamlit_app.py")
    
    # Check if app file exists
    if not os.path.exists(app_path):
        print(f"❌ App file not found: {app_path}")
        print("Please make sure frontend/streamlit_app.py exists")
        sys.exit(1)
    
    print(f"📁 Project Directory: {project_dir}")
    print(f"📄 App Path: {app_path}")
    print("=" * 50)
    print("🚀 Launching Streamlit App...")
    print("🌐 Opening browser at http://localhost:8501")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(project_dir)
    
    # Clear old CAPTCHA files
    captcha_files = ["captcha_temp.png", "captcha_enhanced.png"]
    for f in captcha_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"🧹 Removed old: {f}")
    
    # Run Streamlit with proper arguments
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        app_path,
        "--server.port", "8501",
        "--server.address", "localhost",
        "--browser.gatherUsageStats", "false",
        "--server.headless", "true"
    ]
    
    try:
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open("http://localhost:8501")
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Run Streamlit
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Stopping AdalatMitra...")
    except Exception as e:
        print(f"❌ Error running app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()