@echo off
:: Windows용 Docs Tool 의존성 원클릭 설치 스크립트
chcp 65001 >nul
echo =============================================
echo  Docs Tool - PDF Suite 의존성 설치 (Windows)
echo =============================================

:: 1. 파이썬 설치 확인
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ [오류] 시스템에 Python이 설치되어 있지 않습니다.
    echo 파이썬 공식 홈페이지에서 설치 후 다시 시도해 주세요.
    pause
    exit /b 1
)

:: 2. 가상환경 생성
echo 1️⃣ 프로젝트 전용 가상환경(venv) 생성 중...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ [오류] 가상환경 생성에 실패했습니다.
    pause
    exit /b 1
)

:: 3. 패키지 설치
echo 2️⃣ requirements.txt 패키지 의존성 설치 진행 중...
venv\Scripts\pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ [오류] 패키지 의존성 설치에 실패했습니다.
    pause
    exit /b 1
)

echo =============================================
echo 🎉 의존성 설치 및 가상환경 구축 완료!
echo ---------------------------------------------
echo 실행 방법: run.bat
echo 단독 실행 파일 빌드 방법: build_binary.bat
echo =============================================
pause
