from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QMessageBox, QFileDialog, QFrame, QLineEdit
)
from PySide6.QtCore import Slot
from views.base_view import BaseFileView
from utils.pdf_worker import PdfWorker

class SecurityView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Title
        title = QLabel("PDF 보안 및 관리")
        title.setObjectName("category-title")
        layout.addWidget(title)

        # 1. Standard File View (used for protect, unlock, redact)
        self.file_view = BaseFileView(file_filter="PDF Files (*.pdf)", accept_multiple=False)
        layout.addWidget(self.file_view)

        # 2. Compare Files Widget (used only for compare)
        self.compare_widget = QFrame()
        self.compare_widget.setObjectName("panel-box")
        comp_layout = QVBoxLayout(self.compare_widget)
        comp_layout.setSpacing(10)
        
        comp_layout.addWidget(QLabel("비교 대상 PDF 파일 선택"))
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("원본 PDF (1):"))
        self.le_file1 = QLineEdit()
        self.le_file1.setReadOnly(True)
        btn_file1 = QPushButton("찾기")
        btn_file1.clicked.connect(lambda: self.browse_compare_file(1))
        row1.addWidget(self.le_file1)
        row1.addWidget(btn_file1)
        comp_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("비교 PDF (2):"))
        self.le_file2 = QLineEdit()
        self.le_file2.setReadOnly(True)
        btn_file2 = QPushButton("찾기")
        btn_file2.clicked.connect(lambda: self.browse_compare_file(2))
        row2.addWidget(self.le_file2)
        row2.addWidget(btn_file2)
        comp_layout.addLayout(row2)

        layout.addWidget(self.compare_widget)
        self.compare_widget.hide()

        # Panel Box for Action configuration
        control_panel = QFrame()
        control_panel.setObjectName("panel-box")
        control_layout = QVBoxLayout(control_panel)
        control_layout.setSpacing(12)

        sec_title = QLabel("보안 옵션 설정")
        sec_title.setObjectName("panel-section-title")
        control_layout.addWidget(sec_title)

        # Action Selector
        action_layout = QHBoxLayout()
        action_layout.addWidget(QLabel("수행할 보안 작업:"))
        self.action_combo = QComboBox()
        self.action_combo.addItems(["PDF 보호 (암호 설정)", "PDF 보호 해제 (암호 제거)", "영구 텍스트 검열 (Redaction)", "두 PDF 문서 비교 (Compare)"])
        self.action_combo.currentIndexChanged.connect(self.on_action_changed)
        action_layout.addWidget(self.action_combo)
        control_layout.addLayout(action_layout)

        # A. Password Entry Widget
        self.pw_widget = QWidget()
        pw_layout = QHBoxLayout(self.pw_widget)
        pw_layout.setContentsMargins(0, 0, 0, 0)
        pw_layout.addWidget(QLabel("비밀번호 입력:"))
        self.pw_edit = QLineEdit()
        self.pw_edit.setEchoMode(QLineEdit.Password)
        pw_layout.addWidget(self.pw_edit)
        control_layout.addWidget(self.pw_widget)

        # B. Redact Keyword Entry Widget
        self.redact_widget = QWidget()
        red_layout = QHBoxLayout(self.redact_widget)
        red_layout.setContentsMargins(0, 0, 0, 0)
        red_layout.addWidget(QLabel("삭제할 키워드 (쉼표 구분):"))
        self.redact_edit = QLineEdit()
        self.redact_edit.setPlaceholderText("검열할 문구(예: SSN, 주민번호, 성명) 입력...")
        red_layout.addWidget(self.redact_edit)
        control_layout.addWidget(self.redact_widget)
        self.redact_widget.hide()

        # Run Button
        self.btn_run = QPushButton("보안 작업 실행 ⚡")
        self.btn_run.setObjectName("btn-action")
        self.btn_run.clicked.connect(self.run_task)
        control_layout.addWidget(self.btn_run)

        layout.addWidget(control_panel)
        layout.addStretch()

        self.worker = None

    def on_action_changed(self, index):
        self.file_view.show()
        self.compare_widget.hide()
        self.pw_widget.hide()
        self.redact_widget.hide()

        if index == 0 or index == 1:  # Protect / Unlock
            self.pw_widget.show()
        elif index == 2:  # Redact
            self.redact_widget.show()
        elif index == 3:  # Compare
            self.file_view.hide()
            self.compare_widget.show()

    def browse_compare_file(self, num):
        file_path, _ = QFileDialog.getOpenFileName(self, f"PDF 파일 {num} 선택", "", "PDF Files (*.pdf)")
        if file_path:
            if num == 1:
                self.le_file1.setText(file_path)
            else:
                self.le_file2.setText(file_path)

    def run_task(self):
        action_idx = self.action_combo.currentIndex()

        if action_idx == 3:  # Compare
            file1 = self.le_file1.text().strip()
            file2 = self.le_file2.text().strip()
            if not file1 or not file2:
                QMessageBox.warning(self, "경고", "비교할 두 개의 PDF 파일을 모두 선택해주세요.")
                return
            
            output_dir = QFileDialog.getExistingDirectory(self, "비교 보고서 및 분석 이미지를 저장할 폴더 선택")
            if not output_dir:
                return
                
            params = {
                "file1": file1,
                "file2": file2,
                "output_dir": output_dir
            }
            self.start_worker("compare", params)
            return

        # Standard file actions (0, 1, 2)
        files = self.file_view.get_files()
        if not files:
            QMessageBox.warning(self, "경고", "먼저 처리할 PDF 파일을 선택해주세요.")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "보안 처리된 PDF 저장 경로 선택", "", "PDF Files (*.pdf)")
        if not output_path:
            return

        if action_idx == 0:  # Protect
            pw = self.pw_edit.text().strip()
            if not pw:
                QMessageBox.warning(self, "경고", "설정할 비밀번호를 입력해주세요.")
                return
            params = {
                "file_path": files[0],
                "output_path": output_path,
                "password": pw
            }
            self.start_worker("protect", params)

        elif action_idx == 1:  # Unlock
            pw = self.pw_edit.text().strip()
            if not pw:
                QMessageBox.warning(self, "경고", "PDF 암호를 해제하기 위해 기존 비밀번호를 입력해주세요.")
                return
            params = {
                "file_path": files[0],
                "output_path": output_path,
                "password": pw
            }
            self.start_worker("unlock", params)

        elif action_idx == 2:  # Redact
            terms_str = self.redact_edit.text().strip()
            if not terms_str:
                QMessageBox.warning(self, "경고", "검열할 키워드 목록을 입력해주세요.")
                return
            terms = [t.strip() for t in terms_str.split(',') if t.strip()]
            params = {
                "file_path": files[0],
                "output_path": output_path,
                "search_terms": terms
            }
            self.start_worker("redact", params)

    def start_worker(self, op_type, params):
        self.btn_run.setEnabled(False)
        self.btn_run.setText("보안 작업 진행 중...")
        
        self.worker = PdfWorker(op_type, params)
        self.worker.finished_signal.connect(self.on_task_finished)
        self.worker.start()

    @Slot(bool, str)
    def on_task_finished(self, success, message):
        self.btn_run.setEnabled(True)
        self.btn_run.setText("보안 작업 실행 ⚡")
        
        if success:
            QMessageBox.information(self, "성공", message)
        else:
            QMessageBox.critical(self, "오류", f"보안 작업 실패:\n{message}")
        self.worker = None
        self.pw_edit.clear()
