import os
import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame,
    QPushButton, QLabel, QStackedWidget, QButtonGroup
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from styles import QSS_STYLESHEET

from views.organize_view import OrganizeView
from views.optimize_view import OptimizeView
from views.convert_view import ConvertView
from views.edit_view import EditView
from views.security_view import SecurityView

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Docs Tool - PDF Suite")
        self.resize(1100, 750)
        self.setWindowIcon(QIcon(get_resource_path("icon.png")))
        self.setup_ui()
        self.setStyleSheet(QSS_STYLESHEET)


    def setup_ui(self):
        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main Layout (Split into Sidebar and Content Area)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Sidebar Panel
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        # Logo/Title Section
        logo_label = QLabel("Docs Tool 📑")
        logo_label.setObjectName("logo-label")
        logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo_label)

        # Navigation Button Group
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        nav_items = [
            ("PDF 구성 (Organize)", 0),
            ("PDF 최적화 (Optimize)", 1),
            ("PDF 상호 변환 (Convert)", 2),
            ("PDF 페이지 편집 (Edit)", 3),
            ("PDF 보안 관리 (Security)", 4),
        ]

        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setObjectName("sidebar-btn")
            btn.setCheckable(True)
            if index == 0:
                btn.setChecked(True)
            
            # Connect clicked signal via lambda
            btn.clicked.connect(lambda checked, idx=index: self.change_view(idx))
            
            self.btn_group.addButton(btn, index)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Sidebar Footer
        footer_label = QLabel("v1.0.0 (Local Standalone)")
        footer_label.setStyleSheet("color: rgba(255,255,255,0.25); font-size: 10px;")
        footer_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(footer_label)

        main_layout.addWidget(sidebar)

        # 2. Right Content Panel
        content_widget = QWidget()
        content_widget.setObjectName("content-area")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)

        # Header Section
        self.lbl_view_title = QLabel("PDF 구성 (Organize)")
        self.lbl_view_title.setObjectName("category-title")
        content_layout.addWidget(self.lbl_view_title)

        # Stacked Widget containing all sub-views
        self.stacked_widget = QStackedWidget()
        
        self.view_organize = OrganizeView()
        self.view_optimize = OptimizeView()
        self.view_convert = ConvertView()
        self.view_edit = EditView()
        self.view_security = SecurityView()

        self.stacked_widget.addWidget(self.view_organize)
        self.stacked_widget.addWidget(self.view_optimize)
        self.stacked_widget.addWidget(self.view_convert)
        self.stacked_widget.addWidget(self.view_edit)
        self.stacked_widget.addWidget(self.view_security)

        content_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(content_widget)

    def change_view(self, index):
        self.stacked_widget.setCurrentIndex(index)
        
        titles = {
            0: "PDF 구성 및 페이지 제어",
            1: "PDF 압축 최적화 및 OCR 인식",
            2: "PDF 상호 파일 변환",
            3: "PDF 회전, 자르기 및 워터마크 추가",
            4: "PDF 보안 암호 관리 및 문서 검열"
        }
        self.lbl_view_title.setText(titles.get(index, "PDF Suite Tool"))
