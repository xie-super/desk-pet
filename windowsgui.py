import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QScrollArea, QSizePolicy
)
from PyQt5.Qt import QThread, pyqtSignal

from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont

from zhenghe import getAIAnswerWithoutTTS

class Thread_do(QThread):  # 定义线程类
    _signal = pyqtSignal(str)  # 定义带参数的信号

    def __init__(self, voiceText):
        super().__init__()
        self.voiceText = voiceText  # 接收主线程传递的参数

    def run(self):  # 线程的执行方法
        answer_text = getAIAnswerWithoutTTS(self.voiceText)
        self._signal.emit(answer_text)  # 通过信号传递AI回复

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AI聊天框")
        self.setGeometry(300, 100, 600, 500)

        # 主窗口小部件和布局
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        # 顶部面板
        self.topPanel = QLabel("聊天中")
        self.topPanel.setStyleSheet("background-color: #2E86C1; color: white; font: 18px '微软雅黑'; padding: 10px;")
        self.topPanel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.topPanel)

        # 聊天显示框（带滚动条）
        self.chatScrollArea = QScrollArea()
        self.chatScrollArea.setWidgetResizable(True)
        self.chatContentWidget = QWidget()
        self.chatContentLayout = QVBoxLayout(self.chatContentWidget)
        self.chatContentWidget.setStyleSheet("background-color: #F2F3F4;")
        self.chatScrollArea.setWidget(self.chatContentWidget)
        mainLayout.addWidget(self.chatScrollArea)

        # 底部面板
        self.bottomPanel = QWidget()
        self.bottomPanel.setStyleSheet("background-color: #D6EAF8;")
        self.bottomLayout = QHBoxLayout(self.bottomPanel)
        self.inputField = QLineEdit()
        self.inputField.setStyleSheet("padding: 8px; font-size: 14px;")
        self.sendButton = QPushButton("发送")
        self.sendButton.setStyleSheet(
            "background-color: #2E86C1; color: white; font-size: 14px; padding: 8px; border-radius: 5px;")
        self.bottomLayout.addWidget(self.inputField)
        self.bottomLayout.addWidget(self.sendButton)
        mainLayout.addWidget(self.bottomPanel)

        # 绑定发送按钮事件
        self.sendButton.clicked.connect(self.sendMessage)

    def sendMessage(self):
        message = self.inputField.text().strip()
        if message:
            self.addMessage(message, "我", isSelf=True)
            self.inputField.clear()
            # 创建线程实例并启动
            self.thread_do = Thread_do(message)
            self.thread_do._signal.connect(self.addAIMessage)
            self.thread_do.start()


    def addAIMessage(self, message):
        # 显示AI回复
        self.addMessage(message, '小布', isSelf=False)

    def addMessage(self, message, nickname, isSelf):
        # 创建消息条目
        messageWidget = QWidget()
        messageLayout = QVBoxLayout(messageWidget)

        # 昵称
        nicknameLabel = QLabel(nickname)
        nicknameLabel.setStyleSheet(f"""
            font-size: 12px; font-weight: bold; 
            color: {'royalblue' if isSelf else 'green'};
        """)

        # 时间戳
        timestamp = QLabel(QDateTime.currentDateTime().toString("hh:mm:ss"))
        timestamp.setStyleSheet("font-size: 10px; color: gray;")

        # 消息内容
        messageLabel = QLabel(message)
        messageLabel.setWordWrap(True)  # 启用自动换行
        messageLabel.setFont(QFont("微软雅黑", 12))  # 设置字体
        messageLabel.setStyleSheet("""
            border: 1px solid gray;
            border-radius: 5px;
            padding: 8px;
            font-size: 14px;
        """)
        messageLabel.setMaximumWidth(400)  # 限制消息气泡最大宽度
        messageLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # 自动调整高度
        messageLabel.setMinimumSize(messageLabel.sizeHint())  # 确保高度自适应

        # 根据发送者调整布局
        if isSelf:
            messageLabel.setStyleSheet(messageLabel.styleSheet() + "background-color: #D1F2EB; color: black;")
            messageLayout.addWidget(nicknameLabel, alignment=Qt.AlignRight)
            messageLayout.addWidget(messageLabel, alignment=Qt.AlignRight)
            messageLayout.addWidget(timestamp, alignment=Qt.AlignRight)
        else:
            messageLabel.setStyleSheet(messageLabel.styleSheet() + "background-color: #FADBD8; color: black;")
            messageLayout.addWidget(nicknameLabel, alignment=Qt.AlignLeft)
            messageLayout.addWidget(messageLabel, alignment=Qt.AlignLeft)
            messageLayout.addWidget(timestamp, alignment=Qt.AlignLeft)

        messageLayout.setSpacing(2)  # 缩小时间与昵称的距离
        self.chatContentLayout.addWidget(messageWidget)
        self.chatContentLayout.addSpacing(5)

        # 滚动到最新消息
        self.chatScrollArea.verticalScrollBar().setValue(self.chatScrollArea.verticalScrollBar().maximum())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())
