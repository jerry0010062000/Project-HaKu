import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Example")
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel("Hello, PyQt!", self)
        self.label.setGeometry(100, 50, 150, 30)

        self.button = QPushButton("Click Me", self)
        self.button.setGeometry(100, 100, 100, 30)
        self.button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        self.label.setText("Button Clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
