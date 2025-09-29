# test_pyqt5.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Test Window')
window.setGeometry(100, 100, 300, 200)
window.show()
sys.exit(app.exec_())
