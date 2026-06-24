#!/bin/bash
# Docs Tool 의존성 원클릭 설치 스크립트 (Linux / macOS용)
set -e

echo "============================================="
echo " Docs Tool - PDF Suite 의존성 설치를 시작합니다."
echo "============================================="

# 1. 파이썬 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ 오류: 시스템에 python3가 설치되어 있지 않습니다."
    exit 1
fi

# 2. 가상환경(venv) 구축 및 pip 설치 (우분투/데비안 호환용 트릭 반영)
echo "1️⃣ 프로젝트 전용 가상환경(venv) 생성 중..."
python3 -m venv venv --without-pip

echo "2️⃣ 가상환경 내 pip 다운로드 및 자체 설치 중..."
curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
venv/bin/python3 get-pip.py
rm get-pip.py

# 3. 패키지 설치
echo "3️⃣ requirements.txt 패키지 의존성 빌드 및 설치 진행 중..."
venv/bin/pip install -r requirements.txt

# 4. 실행 및 빌드 헬퍼 스크립트 권한 부여
chmod +x run.sh build_binary.sh 2>/dev/null || true

echo "============================================="
echo "🎉 의존성 설치 및 가상환경 구축 완료!"
echo "---------------------------------------------"
echo "실행 방법: ./run.sh"
echo "단독 실행 파일 빌드 방법: ./build_binary.sh"
echo "============================================="
