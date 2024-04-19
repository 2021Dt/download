import os
import sys
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon, QColor, QPainter, QLinearGradient, QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, \
    QInputDialog, QDialog, QHBoxLayout, QCheckBox, QRadioButton

from API.CommentAPI import CommentAPI
from Tool.Cookie import out_cookie, set_cookie
from Tool.DowbLoad import DownLoad
from API.DanMuAPI import DanMu
from API.BaiNianJi import BaiNianJi


class AgreementWidget(QWidget):
    agreement_accepted = Signal()

    def __init__(self):
        super().__init__()
        self.current_dir = os.path.dirname(__file__)
        file_path = os.path.join(self.current_dir, 'img\\icon.jpg')
        self.setWindowIcon(QIcon(file_path))
        self.setWindowTitle('软件使用条例和警告')
        self.setGeometry(700, 400, 200, 200)
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
        self.cookie = None
        self.init_ui()

    def init_ui(self):
        self.current_dir = os.path.dirname(__file__)
        file_path = os.path.join(self.current_dir, 'img\\icon.jpg')
        self.setObjectName('MainWindow')
        self.setWindowTitle('Welcome 1.0')
        self.setGeometry(400, 400, 800, 400)
        self.setMinimumHeight(300)
        self.setMinimumWidth(500)
        self.setMaximumHeight(400)
        self.setMaximumWidth(800)
        self.billbill_widget = None
        self.setWindowIcon(QIcon(file_path))
        layout1 = QVBoxLayout(self)
        layout1.setAlignment(Qt.AlignCenter)
        self.label = QLineEdit('')
        self.label.setPlaceholderText('请输入你要处理的网址')
        self.label.setToolTip('不要胡乱输入哦！')
        self.label.setClearButtonEnabled(True)
        self.label.setMinimumWidth(450)
        self.label.setMinimumHeight(35)
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
        button1.setObjectName('evilButton')
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
                    if out_cookie('bilibili.txt') is None:
                        self.cookie_win = Cookie('bilibili.txt')
                        self.cookie_win.show()
                        self.cookie_win.cookie_set.connect(self.update_cookie)
                    else:
                        self.billbill()
                        self.label.setText('')
                elif i == 1:
                    if out_cookie('weibo.txt') is None:
                        self.cookie_win = Cookie('weibo')
                        self.cookie_win.show()
                        self.cookie_win.cookie_set.connect(self.update_cookie)
                    else:
                        self.weiborebang()
                        self.label.setText('')
                elif i == 2:
                    if out_cookie('tieba.txt') is None:
                        self.cookie_win = Cookie('tieba.txt')
                        self.cookie_win.show()
                        self.cookie_win.cookie_set.connect(self.update_cookie)
                    else:
                        self.tieba()
                        self.label.setText('')
                elif i == 3:
                    if out_cookie('weibo.txt') is None:
                        self.cookie_win = Cookie('weibo')
                        self.cookie_win.show()
                        self.cookie_win.cookie_set.connect(self.update_cookie)
                    else:
                        self.weibo()
                        self.label.setText('')
                break
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

    def update_cookie(self, value):
        self.cookie = value

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

    def billbill(self):
        self.hide()
        url = self.label.text()
        if not self.billbill_widget:
            self.billbill_widget = BillBillWidget(url, self.cookie)
            self.billbill_widget.closed.connect(self.show)
        self.billbill_widget.show()
        self.setWindowTitle('欢迎回来')

    def weibo(self):
        pass

    def tieba(self):
        pass

    def weiborebang(self):
        pass


class BillBillWidget(QWidget):
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
        self.setWindowTitle('B站 1.0')
        self.setGeometry(400, 400, 800, 400)
        self.setMinimumHeight(300)
        self.setMinimumWidth(500)
        self.setMaximumHeight(400)
        self.setMaximumWidth(800)
        self.setWindowIcon(QIcon(file_path))

        self.main_layout = QVBoxLayout(self)  # 主体为垂直布局

        layout = QHBoxLayout(self)  # 设置水平布局
        layout.setAlignment(Qt.AlignHCenter)  # 设置居中

        # Qt.AlignTop：顶部对齐。
        # Qt.AlignBottom：底部对齐。
        # Qt.AlignLeft：左对齐。
        # Qt.AlignRight：右对齐。
        # Qt.AlignHCenter：水平居中对齐。
        # Qt.AlignVCenter：垂直居中对齐。
        # Qt.AlignCenter：水平和垂直居中对齐（默认）。

        self.label = QLabel(self)
        self.label.setText('<font size="6" face="Arial">选择模式： </font>')

        self.checkbox1 = QRadioButton(self)
        self.checkbox2 = QRadioButton(self)

        self.checkbox1.setText('下载视频')
        self.checkbox2.setText('获取弹幕或评论区')

        # 设置标签和单选框的字体大小
        font = QFont('Arial', 16)  # 设置标签的字体
        self.checkbox1.setFont(font)  # 设置单选框1的字体
        self.checkbox2.setFont(font)  # 设置单选框2的字体

        layout.addWidget(self.label)
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)

        self.main_layout.addLayout(layout)

        self.checkbox1.clicked.connect(self.select_model1)
        self.checkbox2.clicked.connect(self.select_model2)

    def select_model1(self):
        # 清除之前的选择项布局（如果存在）
        self.clear_layout(self.model1_layout)

        if 'video' in self.url:
            # 创建新的选择项布局
            self.model1_layout = QHBoxLayout(self)
            self.model1_layout.setAlignment(Qt.AlignHCenter)

            label2 = QLabel('<font size="6" face="Arial">下载方式： </font>')
            self.checkbox3 = QRadioButton('仅下载音频')
            self.checkbox4 = QRadioButton('仅下载视频（无声音）')
            self.checkbox5 = QRadioButton('下载视频')

            self.checkbox8 = QRadioButton('返回上一级')

            # 设置标签和单选框的字体大小
            font = QFont('Arial', 16)
            self.checkbox3.setFont(font)
            self.checkbox4.setFont(font)
            self.checkbox5.setFont(font)
            self.checkbox8.setFont(font)

            self.checkbox3.clicked.connect(lambda: self.download('1'))
            self.checkbox4.clicked.connect(lambda: self.download('2'))
            self.checkbox5.clicked.connect(lambda: self.download('3'))
            self.checkbox8.clicked.connect(lambda: self.download('4'))

            # 添加标签和单选框到布局中
            self.model1_layout.addWidget(label2)
            self.model1_layout.addWidget(self.checkbox3)
            self.model1_layout.addWidget(self.checkbox4)
            self.model1_layout.addWidget(self.checkbox5)
            self.model1_layout.addWidget(self.checkbox8)

            # 将模式1的布局添加到主布局中
            self.main_layout.addLayout(self.model1_layout)

        else:
            # 创建新的选择项布局
            self.model1_layout = QHBoxLayout(self)
            self.model1_layout.setAlignment(Qt.AlignHCenter)

            label2 = QLabel('<font size="6" face="Arial">下载方式： </font>')
            self.checkbox5 = QRadioButton('下载视频')
            self.checkbox8 = QRadioButton('返回上一级')

            # 设置标签和单选框的字体大小
            font = QFont('Arial', 16)
            self.checkbox5.setFont(font)
            self.checkbox8.setFont(font)

            self.checkbox5.clicked.connect(lambda: self.download('3'))
            self.checkbox8.clicked.connect(lambda: self.download('4'))

            # 添加标签和单选框到布局中
            self.model1_layout.addWidget(label2)
            self.model1_layout.addWidget(self.checkbox5)
            self.model1_layout.addWidget(self.checkbox8)

            # 将模式1的布局添加到主布局中
            self.main_layout.addLayout(self.model1_layout)

    def download(self, sel):
        self.checkbox1.setEnabled(False)
        self.checkbox2.setEnabled(False)
        if sel == '4':
            # 清除之前的选择项布局
            if self.query1_layout is not None:
                self.clear_layout(self.query1_layout)
                self.clear_layout(self.model1_layout)
            else:
                self.clear_layout(self.model1_layout)
            # 使所有复选框可用
            self.checkbox1.setEnabled(True)
            self.checkbox2.setEnabled(True)
            return
        '''防止乱点多下载'''
        if 'video' in self.url:
            self.down_load = DownLoad(self.url, self.cookie)  # 初始化数据
            quality = self.down_load.quality
            if sel == '1':
                self.checkbox3.setEnabled(False)
                QMessageBox.information(self, '提示', '开始下载...')
                self.down_load.run_view('1', 0)
                QMessageBox.warning(self, '成功', '下载完成！')
                self.checkbox3.setEnabled(True)
            elif sel == '2':
                self.checkbox4.setEnabled(False)
                self.create_quality_radiobuttons(quality, sel)
                self.checkbox4.setEnabled(True)
            elif sel == '3':
                self.checkbox5.setEnabled(False)
                QMessageBox.warning(self, '提示', '视频合成可能要很长时间，请耐心等候。')
                self.create_quality_radiobuttons(quality, sel)
                self.checkbox5.setEnabled(True)

        elif 'festival' in self.url:
            QMessageBox.warning(self, '提示', '拜年祭可能要很长时间，挂着就行，不要关闭窗口。')
            self.down_load = BaiNianJi(self.url, self.cookie)
            quality = self.down_load.quality
            self.checkbox5.setEnabled(False)
            self.create_quality_radiobuttons(quality, '4')
            self.checkbox5.setEnabled(True)

        # print(quality)

    def create_quality_radiobuttons(self, quality_dict, sel):
        self.query1_layout = QHBoxLayout(self)
        self.query1_layout.setAlignment(Qt.AlignHCenter)
        font = QFont('Arial', 16)
        for description, quality_id in quality_dict.items():
            radio_button = QRadioButton(description)
            radio_button.setFont(font)
            radio_button.clicked.connect(lambda _, id=quality_id: self.quality_selected(sel, id))
            self.query1_layout.addWidget(radio_button)
        self.main_layout.addLayout(self.query1_layout)

    def quality_selected(self, sel, quality_id):

        QMessageBox.information(self, '提示', '开始下载...')
        if sel == '4':
            a = self.down_load.run_view(quality_id)
        else:
            a = self.down_load.run_view(sel, quality_id)
        if a != -1:
            QMessageBox.warning(self, '成功', '下载完成！')
        else:
            QMessageBox.warning(self, '失败', '当前账号不支持该清晰度')
        # print(quality_id)
        return quality_id

    def select_model2(self):
        # 清除之前的选择项布局（如果存在）
        self.clear_layout(self.model1_layout)

        # 创建新的选择项布局
        self.model1_layout = QHBoxLayout(self)
        self.model1_layout.setAlignment(Qt.AlignHCenter)

        label2 = QLabel('<font size="6" face="Arial">下载方式： </font>')
        self.checkbox6 = QRadioButton('下载弹幕数据')
        self.checkbox7 = QRadioButton('下载评论区数据')
        self.checkbox9 = QRadioButton('返回上一级')

        # 设置标签和单选框的字体大小
        font = QFont('Arial', 16)
        self.checkbox6.setFont(font)
        self.checkbox7.setFont(font)
        self.checkbox9.setFont(font)

        self.checkbox6.clicked.connect(lambda: self.comment_danmu('3'))
        self.checkbox7.clicked.connect(lambda: self.comment_danmu('2'))
        self.checkbox9.clicked.connect(lambda: self.comment_danmu('1'))

        # 添加标签和单选框到布局中
        self.model1_layout.addWidget(label2)
        self.model1_layout.addWidget(self.checkbox6)
        self.model1_layout.addWidget(self.checkbox7)
        self.model1_layout.addWidget(self.checkbox9)

        # 将模式1的布局添加到主布局中
        self.main_layout.addLayout(self.model1_layout)

    def comment_danmu(self, sel):
        if sel == '1':
            self.clear_layout(self.model1_layout)
        elif sel == '2':
            CommentAPI(self.url, cookie=self.cookie).run()
            QMessageBox.warning(self, '成功', '下载完成！')
        elif sel == '3':
            danmu_text = '<a href="{0}">Click here for DanMu API</a>'.format(DanMu(self.url, self.cookie).api())
            QMessageBox.information(self, '弹幕api', danmu_text)

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


class Cookie(QDialog):
    cookie_set = Signal(str)

    def __init__(self, filename):
        super().__init__()
        self.init_ui()
        self.filename = filename

    def init_ui(self):
        self.current_dir = os.path.dirname(__file__)
        file_path = os.path.join(self.current_dir, 'img/icon.jpg')
        self.setWindowIcon(QIcon(file_path))
        self.setWindowTitle('设置Cookie')
        self.setGeometry(700, 400, 200, 200)
        layout = QVBoxLayout(self)

        self.label = QLineEdit()
        self.label.setPlaceholderText('输入cookie')
        button1 = QPushButton('OK!')
        button1.setObjectName('evilButton')
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

        layout.addWidget(self.label)
        layout.addWidget(button1)

        button1.clicked.connect(self.set_cookie)
        self.setLayout(layout)

    def set_cookie(self):
        cookie = self.label.text()
        set_cookie(cookie, filename=self.filename)
        self.cookie_set.emit(cookie)
        QMessageBox.information(self, '成功', '成功设置cookie，欢迎使用！')
        self.close()


def run():
    app = QApplication(sys.argv)
    agreement_widget = AgreementWidget()
    main_widget = MainWidget()

    agreement_widget.agreement_accepted.connect(main_widget.show)

    agreement_widget.show()
    sys.exit(app.exec())


# if __name__ == '__main__':
#     # run()
#     app = QApplication(sys.argv)
#     a = BillBillWidget(1, 1)
#     a.show()
#     app.exec()
