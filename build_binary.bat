@echo off
:: Windows용 PyInstaller 단독 파일 패키징 스크립트
chcp 65001 >nul
if not exist venv\Scripts\python.exe (
    echo ⚠️ 가상환경이 생성되지 않았거나 손상되었습니다.
    echo 자동으로 install.bat 스크립트를 구동하여 의존성을 설치합니다...
    call install.bat
)
venv\Scripts\python build.py
pause
