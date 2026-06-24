from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QMessageBox, QFileDialog, QFrame, QTabWidget
)
from PySide6.QtCore import Slot
from views.base_view import BaseFileView
from utils.pdf_worker import PdfWorker

class ConvertView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Title
        title = QLabel("PDF 상호 변환 도구")
        title.setObjectName("category-title")
        layout.addWidget(title)

        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: External File -> PDF
        self.tab_to_pdf = QWidget()
        self.setup_to_pdf_tab()
        self.tabs.addTab(self.tab_to_pdf, "PDF로 변환 (➔ PDF)")

        # Tab 2: PDF -> External File
        self.tab_from_pdf = QWidget()
        self.setup_from_pdf_tab()
        self.tabs.addTab(self.tab_from_pdf, "PDF에서 변환 (PDF ➔)")

        layout.addWidget(self.tabs)
        self.worker = None

    def setup_to_pdf_tab(self):
        layout = QVBoxLayout(self.tab_to_pdf)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(12)

        # Base File View for images or office files
        self.to_pdf_file_view = BaseFileView(
            file_filter="Images/Documents (*.jpg *.jpeg *.png *.docx *.xlsx *.pptx)", 
            accept_multiple=True
        )
        layout.addWidget(self.to_pdf_file_view)

        # Panel Box
        panel = QFrame()
        panel.setObjectName("panel-box")
        p_layout = QVBoxLayout(panel)
        p_layout.setSpacing(10)

        p_layout.addWidget(QLabel("변환 설정"))
        
        to_mode_layout = QHBoxLayout()
        to_mode_layout.addWidget(QLabel("변환 소스 유형:"))
        self.to_mode_combo = QComboBox()
        self.to_mode_combo.addItems(["이미지 파일 (JPG, PNG) ➔ PDF", "오피스 문서 (Word, Excel, PPT) ➔ PDF"])
        to_mode_layout.addWidget(self.to_mode_combo)
        p_layout.addLayout(to_mode_layout)

        self.btn_run_to = QPushButton("PDF로 변환 실행 ⚡")
        self.btn_run_to.setObjectName("btn-action")
        self.btn_run_to.clicked.connect(self.run_to_pdf)
        p_layout.addWidget(self.btn_run_to)

        layout.addWidget(panel)
        layout.addStretch()

    def setup_from_pdf_tab(self):
        layout = QVBoxLayout(self.tab_from_pdf)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(12)

        # Base File view for target PDF
        self.from_pdf_file_view = BaseFileView(file_filter="PDF Files (*.pdf)", accept_multiple=False)
        layout.addWidget(self.from_pdf_file_view)

        # Panel Box
        panel = QFrame()
        panel.setObjectName("panel-box")
        p_layout = QVBoxLayout(panel)
        p_layout.setSpacing(10)

        p_layout.addWidget(QLabel("변환 설정"))
        
        from_mode_layout = QHBoxLayout()
        from_mode_layout.addWidget(QLabel("변환 타겟 유형:"))
        self.from_mode_combo = QComboBox()
        self.from_mode_combo.addItems(["PDF ➔ 이미지 시퀀스 (PNG)", "PDF ➔ 이미지 시퀀스 (JPG)", "PDF ➔ Word 문서 (DOCX)"])
        from_mode_layout.addWidget(self.from_mode_combo)
        p_layout.addLayout(from_mode_layout)

        self.btn_run_from = QPushButton("파일로 변환 실행 ⚡")
        self.btn_run_from.setObjectName("btn-action")
        self.btn_run_from.clicked.connect(self.run_from_pdf)
        p_layout.addWidget(self.btn_run_from)

        layout.addWidget(panel)
        layout.addStretch()

    def run_to_pdf(self):
        files = self.to_pdf_file_view.get_files()
        if not files:
            QMessageBox.warning(self, "경고", "먼저 변환할 소스 파일을 선택해주세요.")
            return

        mode_idx = self.to_mode_combo.currentIndex()

        if mode_idx == 0:  # Image to PDF
            output_path, _ = QFileDialog.getSaveFileName(self, "변환 PDF 파일 저장 경로 선택", "", "PDF Files (*.pdf)")
            if not output_path:
                return
            params = {
                "image_paths": files,
                "output_path": output_path
            }
            self.start_worker("convert_images_to_pdf", params, self.btn_run_to)
            
        elif mode_idx == 1:  # Office to PDF
            # Currently accepts only single or folder outputs
            output_dir = QFileDialog.getExistingDirectory(self, "변환된 PDF를 저장할 폴더 선택")
            if not output_dir:
                return
            
            # Run office conversion in background sequentially
            # For simplicity in prototype, convert the first selected file
            params = {
                "file_path": files[0],
                "output_dir": output_dir
            }
            self.start_worker("convert_office_to_pdf", params, self.btn_run_to)

    def run_from_pdf(self):
        files = self.from_pdf_file_view.get_files()
        if not files:
            QMessageBox.warning(self, "경고", "먼저 변환할 대상 PDF 파일을 선택해주세요.")
            return

        mode_idx = self.from_mode_combo.currentIndex()

        if mode_idx == 0 or mode_idx == 1:  # PDF to PNG or JPG
            output_dir = QFileDialog.getExistingDirectory(self, "이미지를 저장할 폴더 선택")
            if not output_dir:
                return
            img_format = "png" if mode_idx == 0 else "jpg"
            params = {
                "file_path": files[0],
                "output_dir": output_dir,
                "img_format": img_format
            }
            self.start_worker("convert_pdf_to_images", params, self.btn_run_from)
            
        elif mode_idx == 2:  # PDF to DOCX
            output_path, _ = QFileDialog.getSaveFileName(self, "변환 Word 문서 저장 경로 선택", "", "Word Documents (*.docx)")
            if not output_path:
                return
            params = {
                "file_path": files[0],
                "output_path": output_path
            }
            self.start_worker("convert_pdf_to_word", params, self.btn_run_from)

    def start_worker(self, op_type, params, button_ref):
        button_ref.setEnabled(False)
        button_ref.setText("변환 작업 진행 중...")
        
        self.worker = PdfWorker(op_type, params)
        # Connect to finish slot, passing button_ref to restore state
        self.worker.finished_signal.connect(lambda s, m: self.on_task_finished(s, m, button_ref))
        self.worker.start()

    @Slot(bool, str, QPushButton)
    def on_task_finished(self, success, message, button_ref):
        button_ref.setEnabled(True)
        button_ref.setText("변환 실행 ⚡")
        
        if success:
            QMessageBox.information(self, "성공", message)
        else:
            QMessageBox.critical(self, "오류", f"변환 실패:\n{message}")
        self.worker = None
