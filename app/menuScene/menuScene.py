from direct.gui.DirectGui import DirectButton, DirectFrame, DGG
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import NodePath
from app.configScene.configScene import ConfigScene

class MenuScene:
    def __init__(self, base, scene_manager):
        self.base = base
        self.scene_manager = scene_manager
        self.root = NodePath("MenuSceneRoot")

        self.font = self.base.loader.loadFont("app/core/font/Ubuntu-Regular.ttf")

        self.top_panel = DirectFrame(
            frameSize=(-1.9, 1.9, -0.12, 0.12),
            frameColor=(0, 0, 0, 0.4),
            parent=self.root,
            pos=(0, 0, 0.88)
        )
        self.logo = OnscreenImage(
            image="media/logo/wgite.png",
            scale=(0.3, 0, 0.12),
            parent=self.top_panel,
            pos=(-1.6, 0, 0)
        )

        self.buttons_frame = DirectFrame(
            frameColor=(0, 0, 0, 0),
            parent=self.root
        )
        self.new_btn = DirectButton(
            text="Создать новую сцену",
            scale=0.07,
            frameSize=(-7, 7, -7, 7),
            frameColor=(0.2, 0.4, 0.8, 1),
            text_fg=(1, 1, 1, 1),
            text_font=self.font,
            parent=self.buttons_frame,
            pos=(-0.6, 0, 0),
            relief=DGG.FLAT,
            command=self._on_new_scene
        )
        self.load_btn = DirectButton(
            text="Загрузить существующую",
            scale=0.07,
            frameSize=(-7, 7, -7, 7),
            frameColor=(0.25, 0.25, 0.25, 1),
            text_fg=(1, 1, 1, 1),
            text_font=self.font,
            parent=self.buttons_frame,
            pos=(0.6, 0, 0),
            relief=DGG.FLAT
        )

    def _on_new_scene(self):
        config_scene = ConfigScene(self.base)
        self.scene_manager.switch_to(config_scene.get_root(), is_3d=True)