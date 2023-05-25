import sys
from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QLabel
from config_reader import load_config

class ProgressThread(QThread):
    update_progress = pyqtSignal(int)

    def run(self):
        for i in range(101):
            self.update_progress.emit(i)
            self.msleep(100)  # 模擬耗時操作

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("進度條示範")
        self.layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.label = QLabel()
        self.start_button = QPushButton("開始")
        self.pause_button = QPushButton("暫停")
        
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.pause_button)
        self.setLayout(self.layout)
        
        self.start_button.clicked.connect(self.start_progress)
        self.pause_button.clicked.connect(self.pause_progress)
        
        self.thread = ProgressThread()
        self.thread.update_progress.connect(self.update_progress_bar)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        
        self.paused = False

    def start_progress(self):
        if self.paused:
            self.timer.start()
            self.paused = False
        else:
            self.progress_bar.setValue(0)
            self.thread.start()
            self.timer.start(100)

    def pause_progress(self):
        self.timer.stop()
        self.paused = True

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
        else:
            self.timer.stop()

    def load_config(self, filename):
        config = load_config(filename)
        host = config['database']['host']
        self.label.setText(f"Database Host: {host}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.load_config('config.json')
    window.show()
    sys.exit(app.exec_())
