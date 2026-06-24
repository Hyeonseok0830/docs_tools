# Docs Tool - PDF Suite

Docs Tool은 리눅스, macOS, Windows 환경에서 원클릭으로 가볍고 빠르게 동작하는 PySide6(Qt6) 기반의 네이티브 데스크톱 PDF 종합 가공 도구입니다. 개인정보 보호를 위해 모든 가공 처리는 로컬 환경에서 완전히 오프라인으로 안전하게 수행됩니다.

---

## 🎨 주요 기능 및 카테고리

### 1. PDF 구성 (Organize)
* **PDF 합치기**: 여러 개의 PDF 파일을 단일 문서로 병합합니다.
* **PDF 분할**: 특정 페이지 범위(예: `1-3, 5, 8-10`)를 기준으로 개별 PDF로 분할합니다.
* **페이지 제어**: 문서의 특정 페이지만 지정해 추출하거나 삭제하여 새로운 PDF를 만듭니다.

### 2. PDF 최적화 (Optimize)
* **압축**: PDF 내의 리소스를 다운샘플링하여 화질 손상을 최소화하면서 용량을 대폭 줄입니다.
* **복구**: 깨지거나 열리지 않는 손상된 PDF의 인덱스를 재구조화하여 복원합니다.
* **OCR 텍스트 인식**: 스캔된 이미지 기반 PDF의 문자를 판독하여 검색 및 선택 가능한 텍스트 레이어로 추가합니다.

### 3. PDF로 변환 (➔ PDF)
* **이미지 변환**: 다중 JPG/PNG 이미지를 원본 화질 무손실로 단일 PDF로 합칩니다.
* **오피스 변환**: Word, Excel, PPT 등의 오피스 문서를 PDF 파일로 깔끔하게 변환합니다.

### 4. PDF에서 변환 (PDF ➔)
* **이미지 추출**: PDF의 각 페이지를 고해상도 PNG/JPG 이미지 시퀀스로 출력합니다.
* **Word 변환**: PDF 문서를 편집 가능한 `.docx` 문서 파일로 레이아웃을 보존하여 복원합니다.

### 5. PDF 편집 및 보완 (Edit)
* **페이지 회전**: 90도, 180도, 270도 단위로 페이지 각도를 변경합니다.
* **자르기 (Crop)**: 상하좌우 마진 여백을 퍼센트 단위로 입력하여 정밀하게 잘라냅니다.
* **워터마크 추가**: 텍스트 문구, 투명도, 크기, 회전 각도를 설정하여 워터마크를 각 페이지 중앙에 오버레이합니다.
* **페이지 번호 삽입**: 페이지 하단/상단, 중앙/우측 등 원하는 포맷(예: `Page {num} of {total}`)으로 번호를 일괄 삽입합니다.

### 6. PDF 보안 관리 (Security)
* **PDF 보호**: 강력한 128-bit 보안 암호를 설정하여 열람을 차단합니다.
* **보호 해제**: 기존 비밀번호를 제거하여 암호 없이 열 수 있는 일반 PDF로 저장합니다.
* **영구 검열 (Redaction)**: 입력한 특정 기밀 키워드(예: 이름, 주민번호) 영역을 검은색 박스로 영구 마스킹 처리하여 안전하게 유출을 차단합니다.
* **두 PDF 문서 비교**: 두 PDF 간의 텍스트 상이점을 탐색하고 불일치 페이지를 이미지 및 텍스트 리포트로 자동 추출합니다.

---

## 🛠️ 기술 스택 및 라이브러리
* **GUI Framework**: PySide6 (Qt6 Python bindings)
* **Core PDF Engine**: PyMuPDF (fitz), pypdf
* **Image Processing**: Pillow (PIL), img2pdf
* **Document Reflow**: pdf2docx, reportlab
* **OCR Engine**: pytesseract (Tesseract OCR wrapper)

---

## 🚀 시작하기 & 의존성 설치

### 1. 전제 시스템 필수 소프트웨어 (필요시)
* **OCR 기능**: 사용 국가 언어팩이 포함된 `tesseract-ocr` 엔진이 로컬 OS에 설치되어 있어야 합니다.
  * *우분투*: `sudo apt install tesseract-ocr tesseract-ocr-kor tesseract-ocr-eng`
  * *Windows/Mac*: 공식 Tesseract 설치 파일을 통해 셋업이 필요합니다.
* **오피스 변환**: 시스템에 `libreoffice` 가 설치되어 있어야 동작합니다.

### 2. 가상환경 구축 및 실행 (OS별 원클릭 헬퍼)

#### 🐧 Linux / 🍎 macOS
```bash
# 1. 프로젝트 폴더로 이동
cd docs_tool

# 2. 의존성 자동 원클릭 설치 (가상환경 venv 생성 및 pip 패키지 자동 셋업)
./install.sh

# 3. 프로그램 실행
./run.sh
```

#### 🪟 Windows
1. 폴더 내에 있는 **`install.bat`** 파일을 더블 클릭하여 가상환경 및 패키지 설치를 진행합니다.
2. 설치가 끝나면 **`run.bat`** 파일을 더블 클릭하여 프로그램을 구동합니다.

---

## 📦 독립 배포판 빌드 방법 (Standalone Packaging)

`PyInstaller` 라이브러리를 사용해 타겟 PC에 파이썬이 안 깔려 있어도 더블클릭만으로 구동되는 **무설치 단독 실행 파일**을 생성할 수 있습니다.

* **Linux/macOS**: `./build_binary.sh` 실행
* **Windows**: `build_binary.bat` 더블 클릭

빌드 완료 시 프로젝트 내 `dist/` 디렉토리에 **`DocsTool` (또는 `DocsTool.exe`)** 완성본이 패키징됩니다.

---

## 🤖 GitHub Actions를 통한 CI/CD 배포 자동화
프로젝트에 내장된 `.github/workflows/build.yml` 설정으로 인하여, 코드 버전을 담아 깃 태그를 업로드하면 GitHub 서버가 클라우드 상에서 **Windows, macOS, Linux용 바이너리 3종을 병렬 자동 빌드하여 GitHub Release의 Assets 탭에 직접 첨부**합니다.

```bash
# 최신 코드 커밋 및 버전 릴리즈 태그 push 예시
git add .
git commit -m "docs: add README.md documentation"
git push origin main

# 배포 트리거 생성
git tag v1.0.0
git push origin v1.0.0 -f
```
