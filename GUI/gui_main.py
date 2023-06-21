import sys
from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar, QLabel, QFileDialog

class ProgressThread(QThread):
    update_progress = pyqtSignal(int)

    def run(self):
        for i in range(101):
            self.update_progress.emit(i)
            self.msleep(100)  # 模擬耗時操作

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project HaKu Demo")

        #self.layout為主要布局
        self.layout = QVBoxLayout()
        self.processBar_layout = QVBoxLayout()
        self.filePath_layout = QHBoxLayout()
        self.filePath_layout2 = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.label = QLabel()
        self.start_button = QPushButton("開始")
        self.pause_button = QPushButton("暫停")
        self.label2 = QLabel("未選擇音檔路徑")
        self.select_button = QPushButton('選擇文件')
        self.label3 = QLabel("未選擇金鑰路徑")
        self.select_button2 = QPushButton('選擇金鑰')
              
        self.processBar_layout.addWidget(self.progress_bar)
        self.processBar_layout.addWidget(self.start_button)
        self.processBar_layout.addWidget(self.pause_button)
        self.filePath_layout.addWidget(self.select_button)
        self.filePath_layout.addWidget(self.label2)
        self.filePath_layout2.addWidget(self.select_button2)
        self.filePath_layout2.addWidget(self.label3)

        #加入模組layout
        #self.layout.addLayout(self.processBar_layout)
        self.layout.addLayout(self.filePath_layout)
        self.layout.addLayout(self.filePath_layout2)
        
        self.setLayout(self.layout)
        
        self.start_button.clicked.connect(self.start_progress)
        self.pause_button.clicked.connect(self.pause_progress)
        self.select_button.clicked.connect(lambda: self.get_file_path(self.label2))
        self.select_button2.clicked.connect(lambda: self.get_file_path(self.label3))
        
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

    def get_file_path(self, label):
        file_path, _= QFileDialog.getOpenFileName(self, '選擇檔案')
        if file_path:
            label.setText(file_path)
        else:
            label.setText("未選擇任何檔案")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setFixedSize(800,600)
    window.show()
    sys.exit(app.exec_())
