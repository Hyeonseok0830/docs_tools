from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QComboBox, QMessageBox, QFileDialog, QFrame, QSpinBox, QDoubleSpinBox, QLineEdit
)
from PySide6.QtCore import Slot
from views.base_view import BaseFileView
from utils.pdf_worker import PdfWorker

class EditView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Title
        title = QLabel("PDF 페이지 편집 및 추가")
        title.setObjectName("category-title")
        layout.addWidget(title)

        # Base File View
        self.file_view = BaseFileView(file_filter="PDF Files (*.pdf)", accept_multiple=False)
        layout.addWidget(self.file_view)

        # Panel Box
        control_panel = QFrame()
        control_panel.setObjectName("panel-box")
        control_layout = QVBoxLayout(control_panel)
        control_layout.setSpacing(12)

        sec_title = QLabel("편집 도구 선택 및 설정")
        sec_title.setObjectName("panel-section-title")
        control_layout.addWidget(sec_title)

        # Action Mode Selection
        action_layout = QHBoxLayout()
        action_layout.addWidget(QLabel("수행할 편집:"))
        self.action_combo = QComboBox()
        self.action_combo.addItems(["페이지 회전 (Rotate)", "페이지 자르기 (Crop)", "워터마크 추가 (Watermark)", "페이지 번호 추가 (Page Numbers)"])
        self.action_combo.currentIndexChanged.connect(self.on_action_changed)
        action_layout.addWidget(self.action_combo)
        control_layout.addLayout(action_layout)

        # 1. Rotate Options Widget
        self.rotate_widget = QWidget()
        rot_layout = QHBoxLayout(self.rotate_widget)
        rot_layout.setContentsMargins(0, 0, 0, 0)
        rot_layout.addWidget(QLabel("회전 각도:"))
        self.rot_combo = QComboBox()
        self.rot_combo.addItems(["시계방향 90도", "180도 회전", "반시계방향 90도 (270도)"])
        rot_layout.addWidget(self.rot_combo)
        control_layout.addWidget(self.rotate_widget)

        # 2. Crop Options Widget
        self.crop_widget = QWidget()
        crop_layout = QHBoxLayout(self.crop_widget)
        crop_layout.setContentsMargins(0, 0, 0, 0)
        crop_layout.addWidget(QLabel("여백 자르기 크기 (L / R / T / B) %:"))
        self.sb_left = QSpinBox()
        self.sb_left.setRange(0, 49)
        self.sb_right = QSpinBox()
        self.sb_right.setRange(0, 49)
        self.sb_top = QSpinBox()
        self.sb_top.setRange(0, 49)
        self.sb_bottom = QSpinBox()
        self.sb_bottom.setRange(0, 49)
        crop_layout.addWidget(self.sb_left)
        crop_layout.addWidget(self.sb_right)
        crop_layout.addWidget(self.sb_top)
        crop_layout.addWidget(self.sb_bottom)
        control_layout.addWidget(self.crop_widget)
        self.crop_widget.hide()

        # 3. Watermark Options Widget
        self.watermark_widget = QWidget()
        wm_layout = QVBoxLayout(self.watermark_widget)
        wm_layout.setContentsMargins(0, 0, 0, 0)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("워터마크 텍스트:"))
        self.wm_edit = QLineEdit()
        self.wm_edit.setPlaceholderText("워터마크 내용 입력...")
        row1.addWidget(self.wm_edit)
        wm_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("불투명도 (0.0-1.0):"))
        self.wm_opacity = QDoubleSpinBox()
        self.wm_opacity.setRange(0.05, 1.0)
        self.wm_opacity.setValue(0.3)
        self.wm_opacity.setSingleStep(0.05)
        
        row2.addWidget(QLabel("글씨 크기 (pt):"))
        self.wm_size = QSpinBox()
        self.wm_size.setRange(12, 120)
        self.wm_size.setValue(36)
        
        row2.addWidget(QLabel("회전 각도 (도):"))
        self.wm_angle = QSpinBox()
        self.wm_angle.setRange(-180, 180)
        self.wm_angle.setValue(45)
        
        row2.addWidget(self.wm_opacity)
        row2.addWidget(self.wm_size)
        row2.addWidget(self.wm_angle)
        wm_layout.addLayout(row2)
        control_layout.addWidget(self.watermark_widget)
        self.watermark_widget.hide()

        # 4. Page Numbers Options Widget
        self.pagenum_widget = QWidget()
        pn_layout = QHBoxLayout(self.pagenum_widget)
        pn_layout.setContentsMargins(0, 0, 0, 0)
        pn_layout.addWidget(QLabel("형식:"))
        self.pn_format = QLineEdit("Page {num} of {total}")
        
        pn_layout.addWidget(QLabel("표시 위치:"))
        self.pn_pos = QComboBox()
        self.pn_pos.addItem("하단 중앙", "bottom_center")
        self.pn_pos.addItem("하단 우측", "bottom_right")
        self.pn_pos.addItem("상단 중앙", "top_center")
        self.pn_pos.addItem("상단 우측", "top_right")
        
        pn_layout.addWidget(self.pn_format)
        pn_layout.addWidget(self.pn_pos)
        control_layout.addWidget(self.pagenum_widget)
        self.pagenum_widget.hide()

        # Run Button
        self.btn_run = QPushButton("편집 실행 ⚡")
        self.btn_run.setObjectName("btn-action")
        self.btn_run.clicked.connect(self.run_task)
        control_layout.addWidget(self.btn_run)

        layout.addWidget(control_panel)
        layout.addStretch()

        self.worker = None

    def on_action_changed(self, index):
        self.rotate_widget.hide()
        self.crop_widget.hide()
        self.watermark_widget.hide()
        self.pagenum_widget.hide()

        if index == 0:
            self.rotate_widget.show()
        elif index == 1:
            self.crop_widget.show()
        elif index == 2:
            self.watermark_widget.show()
        elif index == 3:
            self.pagenum_widget.show()

    def run_task(self):
        files = self.file_view.get_files()
        if not files:
            QMessageBox.warning(self, "경고", "먼저 편집할 PDF 파일을 선택해주세요.")
            return

        action_idx = self.action_combo.currentIndex()
        output_path, _ = QFileDialog.getSaveFileName(self, "편집된 PDF 파일 저장 경로 선택", "", "PDF Files (*.pdf)")
        if not output_path:
            return

        if action_idx == 0:  # Rotate
            rot_idx = self.rot_combo.currentIndex()
            angle = 90 if rot_idx == 0 else (180 if rot_idx == 1 else 270)
            params = {
                "file_path": files[0],
                "output_path": output_path,
                "angle": angle
            }
            self.start_worker("rotate", params)

        elif action_idx == 1:  # Crop
            params = {
                "file_path": files[0],
                "output_path": output_path,
                "left": self.sb_left.value(),
                "right": self.sb_right.value(),
                "top": self.sb_top.value(),
                "bottom": self.sb_bottom.value()
            }
            self.start_worker("crop", params)

        elif action_idx == 2:  # Watermark
            text = self.wm_edit.text().strip()
            if not text:
                QMessageBox.warning(self, "경고", "워터마크 문구를 입력해주세요.")
                return
            params = {
                "file_path": files[0],
                "output_path": output_path,
                "text": text,
                "opacity": self.wm_opacity.value(),
                "font_size": self.wm_size.value(),
                "angle": self.wm_angle.value()
            }
            self.start_worker("watermark", params)

        elif action_idx == 3:  # Page numbers
            params = {
                "file_path": files[0],
                "output_path": output_path,
                "format_str": self.pn_format.text(),
                "position": self.pn_pos.currentData()
            }
            self.start_worker("page_numbers", params)

    def start_worker(self, op_type, params):
        self.btn_run.setEnabled(False)
        self.btn_run.setText("편집 작업 진행 중...")
        
        self.worker = PdfWorker(op_type, params)
        self.worker.finished_signal.connect(self.on_task_finished)
        self.worker.start()

    @Slot(bool, str)
    def on_task_finished(self, success, message):
        self.btn_run.setEnabled(True)
        self.btn_run.setText("편집 실행 ⚡")
        
        if success:
            QMessageBox.information(self, "성공", message)
        else:
            QMessageBox.critical(self, "오류", f"편집 실패:\n{message}")
        self.worker = None
