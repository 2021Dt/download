import os
import sys
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon, QColor, QPainter, QLinearGradient, QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QDialog, \
    QHBoxLayout, QCheckBox, QRadioButton, QSlider, QSpinBox
from API.weibo import Weibo

class TieBaWidget(QWidget):
    closed = Signal()

    def __init__(self, url, cookie):
        super().__init__()
        self.down_load = None
        self.model1_layout = None
        self.query1_layout = None
        self.init_ui()
        self.cookie = cookie
        self.url = url

    def init_ui(self):
        self.current_dir = os.path.dirname(__file__)
        file_path = os.path.join(self.current_dir, 'img\\icon.jpg')
        self.setWindowTitle('微博 1.0')
        self.setGeometry(400, 400, 400, 400)
        self.setMinimumHeight(300)
        self.setMinimumWidth(500)
        self.setMaximumHeight(400)
        self.setMaximumWidth(800)
        self.setWindowIcon(QIcon(file_path))

        self.main_layout = QVBoxLayout(self)  # 主体为垂直布局
        self.main_layout.setAlignment(Qt.AlignHCenter)

        layout = QHBoxLayout(self)  # 设置水平布局
        layout.setAlignment(Qt.AlignHCenter)  # 设置居中
        layout2 = QHBoxLayout(self)  # 设置水平布局
        layout2.setAlignment(Qt.AlignHCenter)  # 设置居中

        self.label = QLabel(self)
        self.label.setText('<font size="6" face="Arial">线程数： </font>')
        self.label2 = QLabel(self)
        self.label2.setText('<font size="6" face="Arial">页数： </font>')

        # 创建一个输入框
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, 20)  # 设置数值范围
        self.spinbox.setSingleStep(1)  # 设置步长
        self.spinbox.setValue(1)  # 设置初始值

        self.spinbox2 = QSpinBox()
        self.spinbox2.setRange(1, 9999)
        self.spinbox2.setSingleStep(1)  # 设置步长
        self.spinbox2.setValue(1)  # 设置初始值

        self.button = QPushButton('Go!')
        self.button.setObjectName('evilButton')
        self.button.setStyleSheet('''QPushButton#evilButton {
                                        background-color: white;
                                        border-style: outset;
                                        border-width: 2px;
                                        border-radius: 10px;
                                        border-color: beige;
                                        font: bold 14px;
                                        min-width: 10em;
                                        padding: 6px;
                                    }''')
        self.button.clicked.connect(self.model_select)


        layout.addWidget(self.label)
        layout.addWidget(self.spinbox)

        layout2.addWidget(self.label2)
        layout2.addWidget(self.spinbox2)

        self.main_layout.addLayout(layout)
        self.main_layout.addLayout(layout2)
        self.main_layout.addWidget(self.button)

    def model_select(self):
        QMessageBox.warning(self, '成功','正在为你爬取，请耐心等待！')
        weibo = Weibo(self.url,number=self.spinbox.value(),cookie=self.cookie)
        weibo.run(str(self.spinbox2.value()))
        QMessageBox.warning(self, '成功', '当前数据下载完成！')

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                elif child.layout():
                    self.clear_layout(child.layout())

    def paintEvent(self, event):
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(247, 149, 51, 25))
        gradient.setColorAt(0.15, QColor(243, 112, 85, 25))
        gradient.setColorAt(0.3, QColor(239, 78, 123, 25))
        gradient.setColorAt(0.44, QColor(161, 102, 171, 25))
        gradient.setColorAt(0.58, QColor(80, 115, 184, 25))
        gradient.setColorAt(0.72, QColor(16, 152, 173, 25))
        gradient.setColorAt(0.86, QColor(7, 179, 155, 25))
        gradient.setColorAt(1, QColor(109, 186, 130, 25))

        painter = QPainter(self)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)


