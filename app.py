import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    # Explicitly set AppUserModelID to display the custom icon in the Windows taskbar
    if sys.platform.startswith("win"):
        try:
            import ctypes
            myappid = "Hyeonseok.DocsTool.PDFSuite.v1"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

