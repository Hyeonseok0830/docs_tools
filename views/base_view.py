import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QFileDialog, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal

class BaseFileView(QWidget):
    files_changed = Signal()

    def __init__(self, file_filter="PDF Files (*.pdf)", accept_multiple=True, parent=None):
        super().__init__(parent)
        self.file_filter = file_filter
        self.accept_multiple = accept_multiple
        self.selected_files = []
        self.setup_base_ui()

    def setup_base_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # File List panel
        self.list_panel = QWidget()
        self.list_panel.setObjectName("panel-box")
        list_layout = QVBoxLayout(self.list_panel)
        list_layout.setSpacing(10)

        section_title = QLabel("파일 선택 및 관리")
        section_title.setObjectName("panel-section-title")
        list_layout.addWidget(section_title)

        # Drag & Drop Zone
        self.drop_zone = QLabel("이곳에 PDF 또는 작업 파일을 드래그 앤 드롭 하거나\n아래의 '파일 추가' 버튼을 눌러 선택하세요.")
        self.drop_zone.setObjectName("drop-zone")
        self.drop_zone.setAlignment(Qt.AlignCenter)
        self.drop_zone.setAcceptDrops(True)
        # Custom property to style drag event
        self.drop_zone.setProperty("dragged", False)
        list_layout.addWidget(self.drop_zone)

        # File list box
        self.file_list = QListWidget()
        self.file_list.setObjectName("file-list")
        if not self.accept_multiple:
            self.file_list.setMaximumHeight(80)
        list_layout.addWidget(self.file_list)

        # Add/Remove buttons
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("파일 추가 ➕")
        self.btn_add.clicked.connect(self.add_files_dialog)
        self.btn_remove = QPushButton("선택 파일 제거 ❌")
        self.btn_remove.clicked.connect(self.remove_selected_file)
        self.btn_clear = QPushButton("전체 비우기 🧹")
        self.btn_clear.clicked.connect(self.clear_files)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        btn_layout.addWidget(self.btn_clear)
        list_layout.addLayout(btn_layout)

        layout.addWidget(self.list_panel)

        # Setup Drag and Drop events on drop_zone
        self.drop_zone.dragEnterEvent = self.dz_dragEnterEvent
        self.drop_zone.dragLeaveEvent = self.dz_dragLeaveEvent
        self.drop_zone.dropEvent = self.dz_dropEvent

    def add_files_dialog(self):
        if self.accept_multiple:
            paths, _ = QFileDialog.getOpenFileNames(self, "파일 선택", "", self.file_filter)
            if paths:
                self.add_files(paths)
        else:
            path, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", self.file_filter)
            if path:
                self.add_files([path])

    def add_files(self, paths):
        if not self.accept_multiple:
            self.clear_files()
            
        for path in paths:
            if path not in self.selected_files:
                self.selected_files.append(path)
                item = QListWidgetItem(os.path.basename(path))
                item.setToolTip(path)
                self.file_list.addItem(item)
                
        self.files_changed.emit()
        self.update_ui_state()

    def remove_selected_file(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            # Find the match using tooltip path
            path_to_remove = item.toolTip()
            if path_to_remove in self.selected_files:
                self.selected_files.remove(path_to_remove)
            self.file_list.takeItem(self.file_list.row(item))
            
        self.files_changed.emit()
        self.update_ui_state()

    def clear_files(self):
        self.selected_files.clear()
        self.file_list.clear()
        self.files_changed.emit()
        self.update_ui_state()

    def update_ui_state(self):
        if self.selected_files:
            self.drop_zone.hide()
            self.file_list.show()
        else:
            self.drop_zone.show()
            self.file_list.hide()

    def get_files(self):
        return self.selected_files

    # Drag and Drop handlers
    def dz_dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drop_zone.setProperty("dragged", True)
            self.drop_zone.style().unpolish(self.drop_zone)
            self.drop_zone.style().polish(self.drop_zone)

    def dz_dragLeaveEvent(self, event):
        self.drop_zone.setProperty("dragged", False)
        self.drop_zone.style().unpolish(self.drop_zone)
        self.drop_zone.style().polish(self.drop_zone)

    def dz_dropEvent(self, event):
        self.drop_zone.setProperty("dragged", False)
        self.drop_zone.style().unpolish(self.drop_zone)
        self.drop_zone.style().polish(self.drop_zone)
        
        urls = event.mimeData().urls()
        if urls:
            dropped_paths = []
            for url in urls:
                path = url.toLocalFile()
                if os.path.exists(path):
                    # Basic extension check based on filters (e.g. .pdf)
                    ext = os.path.splitext(path)[1].lower()
                    if "pdf" in self.file_filter.lower() and ext == ".pdf":
                        dropped_paths.append(path)
                    elif "image" in self.file_filter.lower() or "jpg" in self.file_filter.lower():
                        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
                            dropped_paths.append(path)
                    else:
                        # Fallback to allow any file if no specific check matches
                        dropped_paths.append(path)
                        
            if dropped_paths:
                self.add_files(dropped_paths)
