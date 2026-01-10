from direct.gui.DirectGui import DirectButton, DirectFrame, DGG
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import NodePath, Filename, BitMask32
import json
import tkinter as tk
from tkinter import filedialog
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
            scale=(0.33, 0, 0.12),
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
            relief=DGG.FLAT,
            command=self._on_load_scene
        )

    def _on_new_scene(self):
        config_scene = ConfigScene(self.base)
        self.scene_manager.switch_to(config_scene.get_root(), is_3d=True)

    def _on_load_scene(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Загрузить полетную область",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        root.destroy()
        if not file_path:
            return

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        config_scene = ConfigScene(self.base)

        # Настройка области
        area = data.get("area", {})
        shape = area.get("shape", "Куб")
        if shape == "Куб":
            size = float(area.get("size", 50))
            config_scene.current_shape = "Куб"
            config_scene.shape_btn["text"] = "Куб"
            config_scene.size_entry.enterText(str(size))
            config_scene.width_label.hide()
            config_scene.width_entry.hide()
            config_scene.length_label.hide()
            config_scene.length_entry.hide()
            config_scene.height_label.hide()
            config_scene.height_entry.hide()
        else:
            config_scene.current_shape = "Параллелепипед"
            config_scene.shape_btn["text"] = "Параллелепипед"
            w = float(area.get("width", 100))
            l = float(area.get("length", 150))
            h = float(area.get("height", 80))
            config_scene.width_entry.enterText(str(w))
            config_scene.length_entry.enterText(str(l))
            config_scene.height_entry.enterText(str(h))
            config_scene.size_label.hide()
            config_scene.size_entry.hide()

        config_scene.apply_size()

        if shape == "Куб":
            config_scene.size_label.show()
            config_scene.size_entry.show()
        else:
            config_scene.width_label.show()
            config_scene.width_entry.show()
            config_scene.length_label.show()
            config_scene.length_entry.show()
            config_scene.height_label.show()
            config_scene.height_entry.show()

        # Загрузка моделей
        for model_data in data.get("models", []):
            path = model_data["path"]
            pos = model_data["position"]
            rot = model_data["rotation"]
            filename = Filename.fromOsSpecific(path)
            panda_path = filename.getFullpath()
            try:
                model = self.base.loader.loadModel(panda_path)
                model.reparentTo(config_scene.root)
                model.setPos(pos["x"], pos["y"], pos["z"])
                model.setHpr(rot["x"], rot["y"], rot["z"])
                model.setTag('clickable', 'true')
                model.setPythonTag('path', path)
                model.setCollideMask(BitMask32.bit(1))
            except Exception as e:
                print("Ошибка загрузки модели:", path, e)

        self.scene_manager.switch_to(config_scene.get_root(), is_3d=True)