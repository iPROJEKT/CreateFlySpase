import logging
import time

from panda3d.core import (
    loadPrcFileData,
    WindowProperties,
    TransparencyAttrib,
)
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task

from app.core.config.config import Config
from app.screenManager import SceneManager
from app.menuScene.menuScene import MenuScene

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

loadPrcFileData("", "window-type none")
loadPrcFileData("", "icon-filename media/ico/ico.ico")
loadPrcFileData("", "show-frame-rate-meter 0")


class SplashScreen:
    def __init__(self, base: ShowBase, image_path: str, duration: float = 3.0, on_finish=None):
        self.base = base
        self.on_finish = on_finish

        # Создаём временное окно для сплеш-скрина
        props = WindowProperties()
        props.setSize(800, 300)  # Укажи нужный размер
        props.setUndecorated(True)  # Убирает рамку и заголовок
        props.setTitle("Fly Pro by AERO")
        self.base.openDefaultWindow(props=props)

        # Фон чёрный (или любой другой)
        self.base.setBackgroundColor(0, 0, 0, 1)

        # Изображение по центру
        self.image = OnscreenImage(
            image=image_path,
            pos=(0, 0, 0),
            scale=1,  # Подгони под размер окна или укажи явно, например (0.5, 1, 0.5)
            parent=self.base.render2d
        )
        self.image.setTransparency(TransparencyAttrib.MAlpha)

        # Рендерим пару кадров, чтобы изображение появилось
        self.base.graphicsEngine.renderFrame()
        self.base.graphicsEngine.renderFrame()

        # Запускаем таймер
        self.base.taskMgr.doMethodLater(duration, self.finish_splash, "finish_splash")

    def finish_splash(self, task: Task):
        self.image.destroy()
        self.image = None

        if self.on_finish:
            self.on_finish()

        return Task.done


class App(ShowBase):
    def __init__(self):
        super().__init__(windowType="none")
        logger.info("App created, no main window yet")

        SplashScreen(
            base=self,
            image_path="media/logo/wgite.png",
            duration=2.0,
            on_finish=self.start_app
        )

    def start_app(self):
        logger.info("Opening main window")
        loadPrcFileData("", "window-title Fly Pro by AERO")
        loadPrcFileData("", "win-size 1280 720")

        self.openDefaultWindow()
        self.setBackgroundColor(Config.APP_COLOR)

        self.screen_manager = SceneManager(self)
        self.menu_scene = MenuScene(self, self.screen_manager)
        self.screen_manager.switch_to(self.menu_scene.root, is_3d=False)