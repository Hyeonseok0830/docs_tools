#!/bin/bash
# Docs Tool 실행 헬퍼 스크립트
set -e

# 가상환경 venv 및 python3 바이너리가 없는 경우 자동으로 install.sh 실행
if [ ! -d "venv" ] || [ ! -f "venv/bin/python3" ]; then
    echo "⚠️ 가상환경(venv)이 손상되었거나 설치되지 않았습니다."
    echo "자동으로 의존성 설치 스크립트(install.sh)를 시작합니다..."
    chmod +x install.sh
    ./install.sh
fi

venv/bin/python3 app.py
