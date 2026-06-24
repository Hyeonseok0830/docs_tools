# styles.py

QSS_STYLESHEET = """
QMainWindow {
    background-color: #0c0e17;
}

/* Sidebar Styling */
QFrame#sidebar {
    background-color: #121522;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

QLabel#logo-label {
    color: #ffffff;
    font-size: 16px;
    font-weight: bold;
    padding: 10px;
    margin-bottom: 10px;
}

QPushButton#sidebar-btn {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    color: #a0aec0;
    text-align: left;
    padding: 12px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton#sidebar-btn:hover {
    background-color: rgba(255, 255, 255, 0.04);
    color: #ffffff;
}

QPushButton#sidebar-btn:checked {
    background-color: rgba(99, 102, 241, 0.15);
    color: #818cf8;
    font-weight: bold;
    border-left: 3px solid #6366f1;
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
}

/* Content Area Styling */
QWidget#content-area {
    background-color: #0c0e17;
}

QLabel#category-title {
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 15px;
}

/* Panel Box (Card style) */
QFrame#panel-box {
    background-color: rgba(22, 28, 45, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 16px;
}

QLabel#panel-section-title {
    font-size: 12px;
    text-transform: uppercase;
    color: #a78bfa;
    font-weight: bold;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

/* Standard Inputs & Controls */
QLineEdit, QComboBox, QSpinBox {
    background-color: #07080d;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    color: #f3f4f6;
    padding: 8px 12px;
    font-size: 13px;
}

QLineEdit:focus, QSpinBox:focus {
    border: 1px solid #6366f1;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #121522;
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #f3f4f6;
    selection-background-color: #4f46e5;
}

/* List Widget */
QListWidget {
    background-color: #07080d;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    color: #f3f4f6;
    padding: 8px;
    font-size: 12px;
}

QListWidget::item {
    background-color: rgba(255, 255, 255, 0.02);
    border-radius: 6px;
    padding: 8px;
    margin-bottom: 4px;
}

QListWidget::item:selected {
    background-color: rgba(99, 102, 241, 0.2);
    color: #818cf8;
    border: 1px solid rgba(99, 102, 241, 0.4);
}

/* Drag and Drop Zone */
QLabel#drop-zone {
    border: 2px dashed rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    color: #9ca3af;
    font-size: 12px;
    background-color: rgba(22, 28, 45, 0.35);
    padding: 24px;
}

QLabel#drop-zone[dragged="true"] {
    border-color: #6366f1;
    background-color: rgba(99, 102, 241, 0.15);
    color: #ffffff;
}

/* Buttons */
QPushButton {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    color: #e5e7eb;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.15);
}

QPushButton:pressed {
    background-color: rgba(255, 255, 255, 0.15);
}

QPushButton#btn-action {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366f1, stop:1 #4f46e5);
    border: none;
    color: #ffffff;
    font-weight: bold;
    padding: 10px 20px;
    font-size: 14px;
}

QPushButton#btn-action:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #818cf8, stop:1 #6366f1);
}

QPushButton#btn-danger {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ef4444, stop:1 #dc2626);
    border: none;
    color: #ffffff;
    font-weight: bold;
}

QPushButton#btn-danger:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f87171, stop:1 #ef4444);
}

QCheckBox {
    color: #9ca3af;
    font-size: 12px;
}

QCheckBox:hover {
    color: #ffffff;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background-color: #07080d;
}

QCheckBox::indicator:checked {
    background-color: #6366f1;
    border-color: #6366f1;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #0c0e17;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.15);
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 0.25);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}
"""
