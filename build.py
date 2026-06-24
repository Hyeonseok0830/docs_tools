import sys
import os

def build():
    # Make sure we have PyInstaller installed
    try:
        import PyInstaller.__main__
    except ImportError:
        print("PyInstaller가 설치되어 있지 않습니다. 설치를 시작합니다...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        import PyInstaller.__main__

    print("--- Docs Tool 단독 실행 파일 패키징 시작 ---")
    
    # PyInstaller arguments (excluding 'pyinstaller' program name)
    cmd_args = [
        "--onefile",         # 단일 파일로 빌드
        "--noconsole",       # 콘솔창 숨김 (GUI 환경 전용)
        "--name=DocsTool",   # 실행 파일명 지정
        "app.py"
    ]
    
    # Run PyInstaller via Python API directly
    try:
        PyInstaller.__main__.run(cmd_args)
        print("\n🎉 빌드가 성공적으로 완료되었습니다!")
        print("생성된 단독 실행 파일은 'dist/' 폴더 안에서 확인하실 수 있습니다.")
    except Exception as e:
        print(f"\n❌ 빌드 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    build()
