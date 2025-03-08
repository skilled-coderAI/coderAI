"""
CoderAI Launcher Script
This script activates the virtual environment and launches the CoderAI application
with Helpmate-AI integration.
"""
import os
import sys
import subprocess
import threading
import time
import webbrowser

def check_helpmate_build():
    """Check if Helpmate-AI is built"""
    helpmate_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Helpmate-AI")
    dist_dir = os.path.join(helpmate_dir, "dist")
    
    if not os.path.exists(dist_dir):
        print("⚠️ Helpmate-AI build not found. Building now...")
        try:
            subprocess.run(
                ["npm", "run", "build"], 
                cwd=helpmate_dir,
                check=True
            )
            print("✅ Helpmate-AI build completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build Helpmate-AI: {str(e)}")
            return False
    return True

def launch_streamlit():
    """Launch the Streamlit application"""
    print("🚀 Launching CoderAI Streamlit application...")
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true"],
        env=os.environ.copy()
    )
    return streamlit_process

def open_browser_tabs():
    """Open browser tabs for both applications"""
    time.sleep(3)  # Give the servers time to start
    print("🌐 Opening applications in browser...")
    webbrowser.open("http://localhost:8501")  # Streamlit
    #webbrowser.open("http://localhost:5173")  # Helpmate-AI

def main():
    """Main launcher function"""
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Activate virtual environment
    venv_dir = os.path.join(script_dir, ".venv")
    if sys.platform == "win32":
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")
    
    if not os.path.exists(activate_script):
        print("❌ Virtual environment not found. Please create it first.")
        sys.exit(1)
    
    # Set environment variables
    os.environ["VIRTUAL_ENV"] = venv_dir
    os.environ["PATH"] = os.path.join(venv_dir, "Scripts" if sys.platform == "win32" else "bin") + os.pathsep + os.environ["PATH"]
    
    # Check Helpmate-AI build
    if not check_helpmate_build():
        print("⚠️ Continuing without Helpmate-AI build...")
    
    # Launch Streamlit
    streamlit_process = launch_streamlit()
    
    # Open browser tabs
    browser_thread = threading.Thread(target=open_browser_tabs)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Wait for Streamlit to exit
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping CoderAI...")
        streamlit_process.terminate()
    
    print("👋 CoderAI has been shut down.")

if __name__ == "__main__":
    main()
