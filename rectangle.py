import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QFont


class Overlay(QWidget):
    def __init__(self, width=200, height=100, parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.initUI()
        self.dragging = False
        self.offset = QPoint()
        self.handle_height = 30  # 드래그 핸들 영역의 높이

    def initUI(self):
        # 창 설정: 항상 위, 프레임 없음, 배경 투명
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)  # 창 전체 불투명

        # 창 크기 설정 (300x500)
        self.resize(self.width, self.height)

        # 초기 위치를 화면 중앙으로 설정
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.move(x, y)

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 사각형 그리기: 빨간색 3px 테두리
        pen = QPen(Qt.red, 5, Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)  # 내부 채우기 없음

        rect = QRect(0, 0, self.width, self.height)
        painter.drawRect(rect)

        # 드래그 핸들 표시 (상단 30px)
        handle_rect = QRect(0, 0, self.width, self.handle_height)
        handle_color = QColor(255, 0, 0, 100)  # 약간 투명한 빨간색
        painter.fillRect(handle_rect, handle_color)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 클릭한 위치가 드래그 핸들 영역 내에 있는지 확인
            if QRect(0, 0, self.width, self.handle_height).contains(event.pos()):
                self.dragging = True
                self.offset = event.globalPos() - self.frameGeometry().topLeft()
                # print(f"Overlay: 드래그 시작 위치 {self.pos()}, 마우스 클릭 위치 {event.pos()}")

    def mouseMoveEvent(self, event):
        if self.dragging:
            # 창 위치 업데이트
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)
            # print(f"Overlay: 창 이동 중... 새로운 위치 {self.pos()}")

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            # print(f"Overlay: 창 이동 종료, 최종 위치 {self.pos()}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            # print("Overlay: ESC 키 눌림. 창을 닫습니다.")
            self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.overlay = None  # Overlay 창 인스턴스

    def initUI(self):
        # 창 설정: 항상 위
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("사각형 이동기")
        self.setGeometry(100, 100, 200, 120)

        # "화면 위에 사각형 띄우고 이동하기" 버튼
        self.show_rect_button = QPushButton("사각형 이동하기", self)
        self.show_rect_button.setGeometry(30, 20, 100, 20)
        self.show_rect_button.setFont(QFont("Arial", 10))
        self.show_rect_button.clicked.connect(self.show_overlay)

        self.show()

    def show_overlay(self):
        if self.overlay is None or not self.overlay.isVisible():
            # 빨간 사각형
            self.overlay = Overlay(width=65, height=50)
        #     print("MainWindow: Overlay 창을 표시했습니다.")
        # else:
        #     print("MainWindow: Overlay 창이 이미 표시되고 있습니다.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
