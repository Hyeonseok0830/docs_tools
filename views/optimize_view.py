from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QMessageBox, QFileDialog, QFrame
)
from PySide6.QtCore import Slot
from views.base_view import BaseFileView
from utils.pdf_worker import PdfWorker

class OptimizeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Title
        title = QLabel("PDF 최적화 및 텍스트 인식")
        title.setObjectName("category-title")
        layout.addWidget(title)

        # Base File view (accepts single PDF)
        self.file_view = BaseFileView(file_filter="PDF Files (*.pdf)", accept_multiple=False)
        layout.addWidget(self.file_view)

        # Control Panel Box
        control_panel = QFrame()
        control_panel.setObjectName("panel-box")
        control_layout = QVBoxLayout(control_panel)
        control_layout.setSpacing(12)

        sec_title = QLabel("최적화 작업 선택")
        sec_title.setObjectName("panel-section-title")
        control_layout.addWidget(sec_title)

        # Operation Selection
        action_layout = QHBoxLayout()
        action_layout.addWidget(QLabel("수행할 작업:"))
        self.action_combo = QComboBox()
        self.action_combo.addItems(["PDF 용량 압축 (Compress)", "손상된 PDF 복구 (Repair)", "텍스트 인식 (OCR PDF)"])
        self.action_combo.currentIndexChanged.connect(self.on_action_changed)
        action_layout.addWidget(self.action_combo)
        control_layout.addLayout(action_layout)

        # Language selection for OCR
        self.ocr_lang_widget = QWidget()
        ocr_lang_layout = QHBoxLayout(self.ocr_lang_widget)
        ocr_lang_layout.setContentsMargins(0, 0, 0, 0)
        ocr_lang_layout.addWidget(QLabel("인식할 문자 언어:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("한국어 + 영어 (Default)", "kor+eng")
        self.lang_combo.addItem("한국어 (Korean)", "kor")
        self.lang_combo.addItem("영어 (English)", "eng")
        ocr_lang_layout.addWidget(self.lang_combo)
        control_layout.addWidget(self.ocr_lang_widget)
        self.ocr_lang_widget.hide()

        # Run Button
        self.btn_run = QPushButton("최적화 실행 ⚡")
        self.btn_run.setObjectName("btn-action")
        self.btn_run.clicked.connect(self.run_task)
        control_layout.addWidget(self.btn_run)

        layout.addWidget(control_panel)
        layout.addStretch()

        self.worker = None

    def on_action_changed(self, index):
        if index == 2:  # OCR
            self.ocr_lang_widget.show()
        else:
            self.ocr_lang_widget.hide()

    def run_task(self):
        files = self.file_view.get_files()
        if not files:
            QMessageBox.warning(self, "경고", "먼저 최적화할 PDF 파일을 선택해주세요.")
            return

        action_idx = self.action_combo.currentIndex()
        output_path, _ = QFileDialog.getSaveFileName(self, "최적화 파일 저장 경로 선택", "", "PDF Files (*.pdf)")
        if not output_path:
            return

        if action_idx == 0:  # Compress
            params = {
                "file_path": files[0],
                "output_path": output_path
            }
            self.start_worker("compress", params)

        elif action_idx == 1:  # Repair
            params = {
                "file_path": files[0],
                "output_path": output_path
            }
            self.start_worker("repair", params)

        elif action_idx == 2:  # OCR
            lang = self.lang_combo.currentData()
            params = {
                "file_path": files[0],
                "output_path": output_path,
                "lang": lang
            }
            self.start_worker("ocr", params)

    def start_worker(self, op_type, params):
        self.btn_run.setEnabled(False)
        self.btn_run.setText("최적화 작업 중...")
        
        self.worker = PdfWorker(op_type, params)
        self.worker.finished_signal.connect(self.on_task_finished)
        self.worker.start()

    @Slot(bool, str)
    def on_task_finished(self, success, message):
        self.btn_run.setEnabled(True)
        self.btn_run.setText("최적화 실행 ⚡")
        
        if success:
            QMessageBox.information(self, "성공", message)
        else:
            # Check for tesseract dependency error on OCR
            if "tesseract" in message.lower() or "pytesseract" in message.lower():
                QMessageBox.critical(
                    self, "오류", 
                    f"OCR 기능을 사용하려면 시스템에 Tesseract OCR 엔진이 설치되어 있어야 합니다.\n\n"
                    f"에러 세부 정보:\n{message}"
                )
            else:
                QMessageBox.critical(self, "오류", f"최적화 작업 실패:\n{message}")
        self.worker = None
