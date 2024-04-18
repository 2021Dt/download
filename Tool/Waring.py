import os
import sys
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, Qt, QLinearGradient, QColor, QPainter, QGradient
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout, \
    QLineEdit


class AgreementWidget(QWidget):
    agreement_accepted = Signal()

    def __init__(self):
        super().__init__()
        self.current_dir = os.path.dirname(__file__)
        file_path = os.path.join(self.current_dir, 'img\\icon.jpg')
        self.setWindowIcon(QIcon(file_path))
        self.setWindowTitle('软件使用条例和警告')
        self.setGeometry(700,400,200,200)
        layout = QVBoxLayout()

        agreement_text = (
            "请仔细阅读以下条例并确认同意：\n"
            "1. 此软件仅用于个人学习和研究，禁止用于任何商业用途。\n"
            "2. 禁止将程序用于非法用途。\n"
            "3. 作者不对因使用本程序造成的任何损失负责。\n"
            "5. 有一切程序上的问题都可以询问作者。\n"
            "4. 使用本软件即视为同意以上条例。"
        )

        agreement_label = QLabel(agreement_text)
        layout.addWidget(agreement_label)

        agree_button = QPushButton('同意')
        agree_button.clicked.connect(self.accept_agreement)
        layout.addWidget(agree_button)

        self.setLayout(layout)

    def accept_agreement(self):
        QMessageBox.information(self, '提示', '您已同意条例，可以开始使用软件。')
        self.agreement_accepted.emit()
        self.close()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_dir = os.path.dirname(__file__)
        file_path = os.path.join(self.current_dir, 'img\\icon.jpg')
        self.setObjectName('MainWindow')  # 为主窗口指定ID
        self.setWindowTitle('Welcome 1.0')

        self.setGeometry(400, 400, 800, 400)  # x,y,长，宽
        self.setMinimumHeight(300)  # 设置窗口最小高度
        self.setMinimumWidth(500)  # 设置窗口最小宽度
        self.setMaximumHeight(400)  # 设置窗口最大高度
        self.setMaximumWidth(800)  # 设置窗口最大宽度

        self.billbill_widget = None

        self.setWindowIcon(QIcon(file_path))  # 设置图标

        layout1 = QVBoxLayout(self)  # 设置垂直布局
        layout1.setAlignment(Qt.AlignCenter)  # 让布局中的组件在垂直方向上居中

        self.label = QLineEdit('')
        self.label.setPlaceholderText('请输入你要处理的网址')
        self.label.setToolTip('不要胡乱输入哦！')
        self.label.setClearButtonEnabled(True)
        self.label.setMinimumWidth(450)  # 设置输入框的最小宽度
        self.label.setMinimumHeight(35)  # 设置输入框的最小宽度
        self.label.setMaximumWidth(700)
        self.label.setStyleSheet('''
            QLineEdit {
                border: 2px solid gray;
                border-radius: 10px;
                padding: 0 8px;
                background: white;
                selection-background-color: darkgray;
            }
        ''')

        button1 = QPushButton('Go!')
        button1.setObjectName('evilButton')  # 设置按钮的ID为 'evilButton'
        button1.setStyleSheet('''QPushButton#evilButton {
                                background-color: white;
                                border-style: outset;
                                border-width: 2px;
                                border-radius: 10px;
                                border-color: beige;
                                font: bold 14px;
                                min-width: 10em;
                                padding: 6px;
                            }''')

        label1 = QLabel('<font size="6" face="Arial">当前支持B站，微博，百度贴吧的数据爬取</font>')


        label1.setAlignment(Qt.AlignCenter)

        button1.setToolTip('感受力量吧！')
        button1.clicked.connect(self.click_go)

        layout1.addWidget(label1)

        layout1.addWidget(self.label)
        layout1.addWidget(button1)

        # self.setLayout(layout1)  # 设置布局

    def click_go(self):
        url = self.label.text().strip()
        if not url:
            QMessageBox.warning(self, '警告', '输入为空，请输入网址。')
            self.label.setText('')
            return

        select_url = ['www.bilibili.com', 's.weibo.com', 'tieba.baidu.com', 'weibo.com']
        found_supported_url = False
        for i, supported_url in enumerate(select_url):
            if supported_url in url and supported_url != url:
                found_supported_url = True
                if i == 0:
                    print('此处写哔哩界面')
                    self.billbill()
                elif i == 1:
                    print('此次写微博热榜')
                elif i == 2:
                    print('此次写贴吧')
                elif i == 3:
                    print('此次写微博')
                break  # 结束循环，因为已经找到匹配的 URL
            elif supported_url in url and supported_url == url:
                found_supported_url = True
                if i == 0:
                    QMessageBox.warning(self, '警告', '我知道你输入的是B站,但是后面的呢? 巧妇难为无米之炊啊!')
                    self.label.setText('')
                elif i == 1:
                    QMessageBox.warning(self, '警告', '我知道你输入的是微博热榜,但是后面的呢? 巧妇难为无米之炊啊!')
                    self.label.setText('')
                elif i == 2:
                    QMessageBox.warning(self, '警告', '我知道你输入的是贴吧,但是后面的呢? 巧妇难为无米之炊啊!')
                    self.label.setText('')
                elif i == 3:
                    QMessageBox.warning(self, '警告', '我知道你输入的是微博,但是后面的呢? 巧妇难为无米之炊啊!')
                    self.label.setText('')
                break

        if not found_supported_url:
            QMessageBox.warning(self, '警告', '你莫不是在乱输? 请输入正确的网址。')
            self.label.setText('')

    def paintEvent(self, event):
        """死人系列"""
        # 创建渐变对象
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(247, 149, 51, 25))  # 起始颜色，设置透明度
        gradient.setColorAt(0.15, QColor(243, 112, 85, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(0.3, QColor(239, 78, 123, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(0.44, QColor(161, 102, 171, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(0.58, QColor(80, 115, 184, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(0.72, QColor(16, 152, 173, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(0.86, QColor(7, 179, 155, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(1, QColor(109, 186, 130, 25))  # 结束颜色，设置透明度

        # 创建绘制器对象
        painter = QPainter(self)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

    def billbill(self):
        self.hide()
        if not self.billbill_widget:
            self.billbill_widget = BillBillWidget()
            self.billbill_widget.closed.connect(self.show)  # 连接信号到槽
        self.billbill_widget.show()


class BillBillWidget(QWidget):
    closed = Signal()  # 定义一个信号

    def __init__(self):
        super().__init__()
        self.current_dir = os.path.dirname(__file__)
        file_path = os.path.join(self.current_dir, 'img\\icon.jpg')
        self.setObjectName('MainWindow')  # 为主窗口指定ID
        self.setWindowTitle('Welcome')
        self.setGeometry(400, 400, 800, 400)  # x,y,长，宽
        self.setMinimumHeight(300)  # 设置窗口最小高度
        self.setMinimumWidth(500)  # 设置窗口最小宽度
        self.setMaximumHeight(400)  # 设置窗口最大高度
        self.setMaximumWidth(800)  # 设置窗口最大宽度

        self.setWindowIcon(QIcon(file_path))  # 设置图标

        layout1 = QVBoxLayout(self)  # 设置垂直布局
        layout1.setAlignment(Qt.AlignCenter)  # 让布局中的组件在垂直方向上居中

        self.label = QLineEdit('')
        self.label.setPlaceholderText('请输入你要处理的网址')
        self.label.setToolTip('不要胡乱输入哦！')
        self.label.setClearButtonEnabled(True)
        self.label.setStyleSheet('''
            QLineEdit {
                border: 2px solid gray;
                border-radius: 10px;
                padding: 0 8px;
                background: white;
                selection-background-color: darkgray;
            }
        ''')

        button1 = QPushButton('Go!')
        button1.setObjectName('evilButton')  # 设置按钮的ID为 'evilButton'
        button1.setStyleSheet('''QPushButton#evilButton {
                                background-color: white;
                                border-style: outset;
                                border-width: 2px;
                                border-radius: 10px;
                                border-color: beige;
                                font: bold 14px;
                                min-width: 10em;
                                padding: 6px;
                            }''')

        label1 = QLabel('<font size="5" face="Arial">当前支持B站，微博，百度贴吧的数据爬取</font>')

        label1.setAlignment(Qt.AlignCenter)

        button1.setToolTip('感受力量吧！')

        layout1.addWidget(label1)

        layout1.addWidget(self.label)
        layout1.addWidget(button1)

    def paintEvent(self, event):
        """死人系列"""
        # 创建渐变对象
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(247, 149, 51, 25))  # 起始颜色，设置透明度
        gradient.setColorAt(0.15, QColor(243, 112, 85, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(0.3, QColor(239, 78, 123, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(0.44, QColor(161, 102, 171, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(0.58, QColor(80, 115, 184, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(0.72, QColor(16, 152, 173, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(0.86, QColor(7, 179, 155, 25))  # 中间颜色，设置透明度
        gradient.setColorAt(1, QColor(109, 186, 130, 25))  # 结束颜色，设置透明度

        # 创建绘制器对象
        painter = QPainter(self)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

    def closeEvent(self, event):
        self.closed.emit()  # 在窗口关闭时发射信号
        super().closeEvent(event)  # 调用父类的closeEvent以确保窗口正常关闭


def run():
    app = QApplication(sys.argv)
    agreement_widget = AgreementWidget()
    main_widget = MainWidget()

    agreement_widget.agreement_accepted.connect(main_widget.show)

    agreement_widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()
