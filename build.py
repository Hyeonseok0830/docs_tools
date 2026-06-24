import sys
import os

def build():
    # Make sure we have PyInstaller installed
    try:
        import PyInstaller.__main__
    except ImportError:
        print("PyInstaller is not installed. Installing...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        import PyInstaller.__main__

    print("--- Docs Tool Standalone Packaging Start ---")
    
    # PyInstaller arguments (excluding 'pyinstaller' program name)
    sep = ";" if sys.platform.startswith("win") else ":"
    cmd_args = [
        "--onefile",                   # Build into a single executable file
        "--noconsole",                 # Hide console window
        f"--add-data=icon.png{sep}.",  # Bundle window icon
        "--name=DocsTool",             # Output executable name
    ]

    # Attach desktop icon if present
    if os.path.exists("icon.ico"):
        cmd_args.append("--icon=icon.ico")

    cmd_args.append("app.py")

    
    # Run PyInstaller via Python API directly
    try:
        PyInstaller.__main__.run(cmd_args)
        print("\n🎉 Build completed successfully!")
        print("Check the 'dist/' folder for the standalone executable.")
    except Exception as e:
        print(f"\n❌ Build failed: {e}")

if __name__ == "__main__":
    build()
