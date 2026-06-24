from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QComboBox, QMessageBox, QFileDialog, QFrame
)
from PySide6.QtCore import Slot
from views.base_view import BaseFileView
from utils.pdf_worker import PdfWorker

class OrganizeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Title
        title = QLabel("PDF 구성 및 관리")
        title.setObjectName("category-title")
        layout.addWidget(title)

        # Base File view (accepts multiple PDFs)
        self.file_view = BaseFileView(file_filter="PDF Files (*.pdf)", accept_multiple=True)
        layout.addWidget(self.file_view)

        # Control Panel Box (Options)
        control_panel = QFrame()
        control_panel.setObjectName("panel-box")
        control_layout = QVBoxLayout(control_panel)
        control_layout.setSpacing(12)

        sec_title = QLabel("작업 선택 및 상세 옵션 설정")
        sec_title.setObjectName("panel-section-title")
        control_layout.addWidget(sec_title)

        # Selection of Action
        action_layout = QHBoxLayout()
        action_layout.addWidget(QLabel("수행할 작업:"))
        self.action_combo = QComboBox()
        self.action_combo.addItems(["PDF 합치기 (Merge)", "PDF 분할 (Split)", "페이지 추출 및 제거 (Extract / Remove)"])
        self.action_combo.currentIndexChanged.connect(self.on_action_changed)
        action_layout.addWidget(self.action_combo)
        control_layout.addLayout(action_layout)

        # Split options widget
        self.split_widget = QWidget()
        split_layout = QHBoxLayout(self.split_widget)
        split_layout.setContentsMargins(0, 0, 0, 0)
        split_layout.addWidget(QLabel("분할 범위 지정 (예: 1-3, 5, 6-8):"))
        self.split_edit = QLineEdit()
        self.split_edit.setPlaceholderText("범위 입력 (쉼표 및 하이픈 사용)...")
        split_layout.addWidget(self.split_edit)
        control_layout.addWidget(self.split_widget)
        self.split_widget.hide()

        # Extract/Remove options widget
        self.page_widget = QWidget()
        page_layout = QHBoxLayout(self.page_widget)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(QLabel("페이지 번호 (예: 1, 3, 5):"))
        self.page_edit = QLineEdit()
        self.page_edit.setPlaceholderText("페이지 번호 입력...")
        
        self.page_mode_combo = QComboBox()
        self.page_mode_combo.addItems(["선택한 페이지 추출하기 (Extract)", "선택한 페이지 제거하기 (Remove)"])
        
        page_layout.addWidget(self.page_edit)
        page_layout.addWidget(self.page_mode_combo)
        control_layout.addWidget(self.page_widget)
        self.page_widget.hide()

        # Action Button
        self.btn_run = QPushButton("작업 실행 ⚡")
        self.btn_run.setObjectName("btn-action")
        self.btn_run.clicked.connect(self.run_task)
        control_layout.addWidget(self.btn_run)

        layout.addWidget(control_panel)
        layout.addStretch()

        # Keep a reference to worker thread to prevent GC
        self.worker = None

    def on_action_changed(self, index):
        if index == 0:  # Merge
            self.split_widget.hide()
            self.page_widget.hide()
            self.file_view.accept_multiple = True
        elif index == 1:  # Split
            self.split_widget.show()
            self.page_widget.hide()
            self.file_view.accept_multiple = False
            self.file_view.update_ui_state()
        elif index == 2:  # Extract/Remove
            self.split_widget.hide()
            self.page_widget.show()
            self.file_view.accept_multiple = False
            self.file_view.update_ui_state()

    def run_task(self):
        files = self.file_view.get_files()
        if not files:
            QMessageBox.warning(self, "경고", "먼저 작업할 PDF 파일을 선택해주세요.")
            return

        action_idx = self.action_combo.currentIndex()

        if action_idx == 0:  # Merge
            if len(files) < 2:
                QMessageBox.warning(self, "경고", "PDF 병합을 하려면 2개 이상의 파일을 선택해야 합니다.")
                return
            
            output_path, _ = QFileDialog.getSaveFileName(self, "병합 파일 저장 경로 선택", "", "PDF Files (*.pdf)")
            if not output_path:
                return
                
            params = {
                "file_paths": files,
                "output_path": output_path
            }
            self.start_worker("merge", params)

        elif action_idx == 1:  # Split
            split_ranges = self.split_edit.text().strip()
            if not split_ranges:
                QMessageBox.warning(self, "경고", "분할 페이지 범위(예: 1-3, 5)를 입력해주세요.")
                return
                
            output_dir = QFileDialog.getExistingDirectory(self, "분할된 파일을 저장할 폴더 선택")
            if not output_dir:
                return
                
            params = {
                "file_path": files[0],
                "output_dir": output_dir,
                "split_ranges": split_ranges
            }
            self.start_worker("split", params)

        elif action_idx == 2:  # Page Extract / Remove
            page_str = self.page_edit.text().strip()
            if not page_str:
                QMessageBox.warning(self, "경고", "대상 페이지 번호(예: 1, 3, 5)를 입력해주세요.")
                return
                
            try:
                page_numbers = [int(p.strip()) for p in page_str.split(',') if p.strip()]
            except ValueError:
                QMessageBox.warning(self, "경고", "올바른 페이지 번호 형식으로 입력해주세요. (숫자와 쉼표만 가능)")
                return
                
            output_path, _ = QFileDialog.getSaveFileName(self, "가공된 PDF 저장 경로 선택", "", "PDF Files (*.pdf)")
            if not output_path:
                return
                
            action_type = "extract" if self.page_mode_combo.currentIndex() == 0 else "remove"
            
            params = {
                "file_path": files[0],
                "output_path": output_path,
                "page_numbers": page_numbers,
                "action": action_type
            }
            self.start_worker("manage_pages", params)

    def start_worker(self, op_type, params):
        self.btn_run.setEnabled(False)
        self.btn_run.setText("작업 진행 중...")
        
        self.worker = PdfWorker(op_type, params)
        self.worker.finished_signal.connect(self.on_task_finished)
        self.worker.start()

    @Slot(bool, str)
    def on_task_finished(self, success, message):
        self.btn_run.setEnabled(True)
        self.btn_run.setText("작업 실행 ⚡")
        
        if success:
            QMessageBox.information(self, "성공", message)
        else:
            QMessageBox.critical(self, "오류", f"작업 실패:\n{message}")
        self.worker = None
