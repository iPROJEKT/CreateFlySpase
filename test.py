import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, loadPrcFileData

# Отключаем автоматическое окно Panda
loadPrcFileData("", "window-type none")


class PandaWidget(ShowBase):
    def __init__(self, parent_win_id, width, height):
        super().__init__()

        # Настройки окна Panda для Qt
        props = WindowProperties()
        props.setOrigin(0, 0)
        props.setSize(width, height)
        props.setParentWindow(int(parent_win_id))

        self.openDefaultWindow(props=props)
        self.setBackgroundColor(0.1, 0.1, 0.15, 1)
        self.disableMouse()

        # Пример модели
        cube = self.loader.loadModel("models/box")
        cube.reparentTo(self.render)
        cube.setPos(0, 10, 0)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fly Pro by AERO")
        self.resize(1280, 720)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Верхняя панель с логотипом и кнопками
        top_panel = QtWidgets.QWidget()
        top_panel.setFixedHeight(120)
        top_layout = QtWidgets.QHBoxLayout(top_panel)
        top_layout.setContentsMargins(10, 10, 10, 10)

        logo_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("media/logo/wgite.png")
        pixmap = pixmap.scaledToHeight(100, QtCore.Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        top_layout.addWidget(logo_label)

        buttons_layout = QtWidgets.QVBoxLayout()
        btn_new = QtWidgets.QPushButton("Создать новую сцену")
        btn_load = QtWidgets.QPushButton("Загрузить существующую")
        buttons_layout.addWidget(btn_new)
        buttons_layout.addWidget(btn_load)
        top_layout.addLayout(buttons_layout)

        layout.addWidget(top_panel)

        # Frame для Panda3D
        self.panda_frame = QtWidgets.QFrame()
        self.panda_frame.setStyleSheet("background-color: black;")
        layout.addWidget(self.panda_frame, stretch=1)

        # Получаем WinID для Panda
        self.panda_frame.winId()  # убедимся, что Qt подготовил окно
        self.panda_app = PandaWidget(self.panda_frame.winId(),
                                     self.panda_frame.width(),
                                     self.panda_frame.height())

        # Поддержка ресайза
        self.panda_frame.resizeEvent = self.on_resize

    def on_resize(self, event):
        w = event.size().width()
        h = event.size().height()
        wp = WindowProperties()
        wp.setSize(w, h)
        self.panda_app.win.requestProperties(wp)
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())