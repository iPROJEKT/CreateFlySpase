from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectGui import DGG
from panda3d.core import (
    NodePath, Point3, TransparencyAttrib,
    TextNode, BitMask32, CollisionTraverser, CollisionNode,
    CollisionHandlerQueue, CollisionRay, Filename
)
from scene_utils import create_grid_floor, create_box, create_rect_box
from app.cameraModule.camera import CameraControl
from app.core.config.config import Config

class ConfigScene:
    def __init__(self, base):
        self.base = base
        self.root = NodePath("ConfigSceneRoot")
        self.font = self.base.loader.loadFont("app/core/font/Ubuntu-Regular.ttf")

        self.grid = create_grid_floor(size=300, step=10)
        self.grid.reparentTo(self.root)

        self.box = create_box(size=50)
        self.box.reparentTo(self.root)

        self.camera_control = CameraControl(base=self.base, center=Point3(0, 0, 25))

        self.toggle_btn = DirectButton(
            image='media/button/m.png',
            image_scale=0.12,
            relief=None,
            command=self.open_sidebar,
            pos=(1.7, 0, 0)
        )
        self.toggle_btn.setTransparency(TransparencyAttrib.MAlpha)
        self.toggle_btn.reparentTo(self.base.aspect2d)

        self.sidebar = DirectFrame(
            frameColor=(0.1, 0.1, 0.1, 1),
            frameSize=(-0.4, 0.4, -1.6, 1.6),
            pos=(1.5, 0, 0)
        )
        self.sidebar.reparentTo(self.base.aspect2d)
        self.sidebar.hide()

        self.close_btn = DirectButton(
            parent=self.sidebar,
            text="Закрыть",
            text_font=self.font,
            text_scale=0.05,
            command=self.close_sidebar,
            pos=(0, 0, -0.8),
            frameSize=(-0.3, 0.3, -0.07, 0.07),
            text_pos=(0, -0.01),
            relief=DGG.FLAT,
            frameColor=Config.OPTION_ITEM_FRAME_COLOR,
        )
        self.close_btn.setTransparency(TransparencyAttrib.MAlpha)

        DirectLabel(
            parent=self.sidebar,
            text="Настройки полетной области",
            text_font=self.font,
            text_scale=0.05,
            pos=(0, 0, 0.8),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1)
        )

        self.current_shape = "Куб"
        self.shape_btn = DirectButton(
            parent=self.sidebar,
            text="Куб",
            text_font=self.font,
            text_pos=(0, -0.02),
            text_scale=0.06,
            pos=(0, 0, 0.5),
            frameSize=(-0.35, 0.35, -0.08, 0.08),
            relief=DGG.FLAT,
            frameColor=Config.OPTION_ITEM_FRAME_COLOR,
            command=self.toggle_shape
        )

        self.add_model_btn = DirectButton(
            parent=self.sidebar,
            text="Добавить модель",
            text_font=self.font,
            text_scale=0.05,
            command=self.add_model,
            pos=(0, 0, -0.4),
            frameSize=(-0.3, 0.3, -0.07, 0.07),
            text_pos=(0, -0.01),
            relief=DGG.FLAT,
            frameColor=Config.OPTION_ITEM_FRAME_COLOR,
        )

        self.size_label = DirectLabel(
            parent=self.sidebar,
            text="Размер:",
            text_font=self.font,
            text_scale=0.05,
            pos=(-0.15, 0, 0.3),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ARight
        )
        self.size_entry = DirectEntry(
            parent=self.sidebar,
            scale=0.05,
            pos=(0.1, 0, 0.3),
            text_pos=(-0.5, 0, 0),
            frameSize=(-3, 3, -0.8, 1.2),
            initialText="50",
            numLines=1,
            command=self.apply_size,
            focusOutCommand=self.apply_size
        )

        self.width_label = DirectLabel(
            parent=self.sidebar,
            text="Ширина",
            text_font=self.font,
            text_scale=0.05,
            pos=(-0.17, 0, 0.3),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ARight
        )
        self.width_entry = DirectEntry(
            parent=self.sidebar,
            scale=0.05,
            pos=(0.14, 0, 0.3),
            text_pos=(-0.8, 0, 0),
            frameSize=(-3, 3, -0.8, 1.2),
            initialText="100",
            numLines=1,
            command=self.apply_size,
            focusOutCommand=self.apply_size
        )

        self.length_label = DirectLabel(
            parent=self.sidebar,
            text="Длина",
            text_font=self.font,
            text_scale=0.05,
            pos=(-0.19, 0, 0.1),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ARight
        )
        self.length_entry = DirectEntry(
            parent=self.sidebar,
            scale=0.05,
            pos=(0.14, 0, 0.1),
            text_pos=(-0.8, 0, 0),
            frameSize=(-3, 3, -0.8, 1.2),
            initialText="150",
            numLines=1,
            command=self.apply_size,
            focusOutCommand=self.apply_size
        )

        self.height_label = DirectLabel(
            parent=self.sidebar,
            text="Высота",
            text_font=self.font,
            text_scale=0.05,
            pos=(-0.17, 0, -0.1),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ARight
        )
        self.height_entry = DirectEntry(
            parent=self.sidebar,
            scale=0.05,
            pos=(0.14, 0, -0.1),
            text_pos=(-0.8, 0, 0),
            frameSize=(-3, 3, -0.8, 1.2),
            initialText="80",
            numLines=1,
            command=self.apply_size,
            focusOutCommand=self.apply_size
        )

        self.save_btn = DirectButton(
            parent=self.sidebar,
            text="Сохранить",
            text_font=self.font,
            text_scale=0.05,
            command=self.save_flight_area,
            pos=(0, 0, -0.6),
            frameSize=(-0.3, 0.3, -0.07, 0.07),
            text_pos=(0, -0.01),
            relief=DGG.FLAT,
            frameColor=Config.OPTION_ITEM_FRAME_COLOR,
        )

        self.width_label.hide()
        self.width_entry.hide()
        self.length_label.hide()
        self.length_entry.hide()
        self.height_label.hide()
        self.height_entry.hide()

        self.model_panel = DirectFrame(
            frameColor=(0.1, 0.1, 0.1, 1),
            frameSize=(-0.4, 0.4, -1.6, 1.6),
            pos=(-1.5, 0, 0)
        )
        self.model_panel.reparentTo(self.base.aspect2d)
        self.model_panel.hide()

        DirectLabel(
            parent=self.model_panel,
            text="Свойства модели",
            text_font=self.font,
            text_scale=0.05,
            pos=(0, 0, 0.8),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1)
        )

        DirectLabel(
            parent=self.model_panel,
            text="Позиция X:",
            text_font=self.font,
            text_scale=0.05,
            pos=(-0.1, 0, 0.5),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ARight
        )
        self.pos_x = DirectEntry(
            parent=self.model_panel,
            scale=0.05,
            pos=(0.15, 0, 0.5),
            text_pos=(-0.8, 0, 0),
            frameSize=(-3, 3, -0.8, 1.2),
            initialText="0",
            numLines=1,
            command=self.update_model_transform,
            focusOutCommand=self.update_model_transform
        )

        DirectLabel(
            parent=self.model_panel,
            text="Позиция Y:",
            text_font=self.font,
            text_scale=0.05,
            pos=(-0.1, 0, 0.3),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ARight
        )
        self.pos_y = DirectEntry(
            parent=self.model_panel,
            scale=0.05,
            pos=(0.15, 0, 0.3),
            text_pos=(-0.8, 0, 0),
            frameSize=(-3, 3, -0.8, 1.2),
            initialText="0",
            numLines=1,
            command=self.update_model_transform,
            focusOutCommand=self.update_model_transform
        )

        DirectLabel(
            parent=self.model_panel,
            text="Позиция Z:",
            text_font=self.font,
            text_scale=0.05,
            pos=(-0.1, 0, 0.1),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ARight
        )
        self.pos_z = DirectEntry(
            parent=self.model_panel,
            scale=0.05,
            pos=(0.15, 0, 0.1),
            text_pos=(-0.8, 0, 0),
            frameSize=(-3, 3, -0.8, 1.2),
            initialText="0",
            numLines=1,
            command=self.update_model_transform,
            focusOutCommand=self.update_model_transform
        )

        DirectLabel(
            parent=self.model_panel,
            text="Поворот X:",
            text_font=self.font,
            text_scale=0.05,
            pos=(-0.1, 0, -0.2),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ARight
        )
        self.rot_x = DirectEntry(
            parent=self.model_panel,
            scale=0.05,
            pos=(0.15, 0, -0.2),
            text_pos=(-0.8, 0, 0),
            frameSize=(-3, 3, -0.8, 1.2),
            initialText="0",
            numLines=1,
            command=self.update_model_transform,
            focusOutCommand=self.update_model_transform
        )

        DirectLabel(
            parent=self.model_panel,
            text="Поворот Y:",
            text_font=self.font,
            text_scale=0.05,
            pos=(-0.1, 0, -0.4),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ARight
        )
        self.rot_y = DirectEntry(
            parent=self.model_panel,
            scale=0.05,
            pos=(0.15, 0, -0.4),
            text_pos=(-0.8, 0, 0),
            frameSize=(-3, 3, -0.8, 1.2),
            initialText="0",
            numLines=1,
            command=self.update_model_transform,
            focusOutCommand=self.update_model_transform
        )

        DirectLabel(
            parent=self.model_panel,
            text="Поворот Z:",
            text_font=self.font,
            text_scale=0.05,
            pos=(-0.1, 0, -0.6),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ARight
        )
        self.rot_z = DirectEntry(
            parent=self.model_panel,
            scale=0.05,
            pos=(0.15, 0, -0.6),
            text_pos=(-0.8, 0, 0),
            frameSize=(-3, 3, -0.8, 1.2),
            initialText="0",
            numLines=1,
            command=self.update_model_transform,
            focusOutCommand=self.update_model_transform
        )

        self.delete_model_btn = DirectButton(
            parent=self.model_panel,
            text="Удалить модель",
            text_font=self.font,
            text_scale=0.05,
            command=self.delete_selected_model,
            pos=(0, 0, -0.8),
            frameSize=(-0.3, 0.3, -0.07, 0.07),
            text_pos=(0, -0.01),
            relief=DGG.FLAT,
            frameColor=(0.8, 0.2, 0.2, 1)
        )

        self.clicked_model = None
        self.base.accept("mouse1", self.on_mouse1_down, extraArgs=[False])
        self.base.accept("mouse1-up", self.on_mouse1_down, extraArgs=[True])

    def toggle_shape(self):
        if self.current_shape == "Куб":
            self.current_shape = "Параллелепипед"
            self.shape_btn["text"] = "Параллелепипед"
            self.size_label.hide()
            self.size_entry.hide()
            self.width_label.show()
            self.width_entry.show()
            self.length_label.show()
            self.length_entry.show()
            self.height_label.show()
            self.height_entry.show()
        else:
            self.current_shape = "Куб"
            self.shape_btn["text"] = "Куб"
            self.width_label.hide()
            self.width_entry.hide()
            self.length_label.hide()
            self.length_entry.hide()
            self.height_label.hide()
            self.height_entry.hide()
            self.size_label.show()
            self.size_entry.show()
        self.apply_size()

    def apply_size(self, text=None):
        self.box.removeNode()
        if self.current_shape == "Куб":
            try:
                size = float(self.size_entry.get())
            except ValueError:
                size = 50
            self.box = create_box(size=size)
            center_z = size / 2
            max_dim = size
        else:
            try:
                w = float(self.width_entry.get())
                l = float(self.length_entry.get())
                h = float(self.height_entry.get())
            except ValueError:
                w, l, h = 100, 150, 80
            self.box = create_rect_box(width=w, length=l, height=h)
            center_z = h / 2
            max_dim = max(w, l, h)
        self.box.reparentTo(self.root)
        self.camera_control.center = Point3(0, 0, center_z)
        self.camera_control.set_distance(max_dim * 2.0)

    def open_sidebar(self):
        self.toggle_btn.hide()
        self.sidebar.show()

    def close_sidebar(self):
        self.sidebar.hide()
        self.toggle_btn.show()

    def on_enter(self):
        self.root.reparentTo(self.base.render)
        self.base.disableMouse()
        self.camera_control.enable()

    def on_exit(self):
        self.camera_control.disable()
        self.root.detachNode()

    def get_root(self):
        return self.root

    def save_flight_area(self):
        import json
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            title="Сохранить полетную область",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        data = {}

        # Основная область
        if self.current_shape == "Куб":
            try:
                size = float(self.size_entry.get())
            except ValueError:
                size = 50
            data["area"] = {"shape": "Куб", "size": size}
        else:
            try:
                w = float(self.width_entry.get())
                l = float(self.length_entry.get())
                h = float(self.height_entry.get())
            except ValueError:
                w, l, h = 100, 150, 80
            data["area"] = {"shape": "Параллелепипед", "width": w, "length": l, "height": h}

        # Добавленные модели
        data["models"] = []
        for child in self.root.getChildren():
            if child.hasTag("clickable"):
                pos = child.getPos()
                hpr = child.getHpr()
                path = child.getPythonTag("path")
                model_data = {
                    "path": path,
                    "position": {"x": pos.x, "y": pos.y, "z": pos.z},
                    "rotation": {"x": hpr.x, "y": hpr.y, "z": hpr.z}
                }
                data["models"].append(model_data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_model(self):
        import tkinter as tk
        from tkinter import filedialog
        from panda3d.core import Filename
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.askopenfilename(
            title="Выберите 3D модель",
            filetypes=[
                ("Все поддерживаемые", "*.bam *.egg *.obj *.gltf *.glb *.stl *.fbx *.dae"),
                ("Panda3D", "*.bam *.egg"),
                ("glTF", "*.gltf *.glb"),
                ("OBJ", "*.obj"),
                ("Другие", "*.stl *.fbx *.dae"),
                ("Все файлы", "*.*")
            ]
        )
        root.destroy()
        if not file_path:
            return
        filename = Filename.fromOsSpecific(file_path)
        panda_path = filename.getFullpath()
        try:
            model = self.base.loader.loadModel(panda_path)
            model.reparentTo(self.root)
            model.setPos(0, 0, 0)
            model.setTag('clickable', 'true')
            model.setPythonTag('path', file_path)
            model.setCollideMask(BitMask32.bit(1))
            print("Модель загружена:", file_path)
        except Exception as e:
            print("Ошибка загрузки:", e)

    def on_mouse1_down(self, released):
        if not self.base.mouseWatcherNode.hasMouse():
            return
        if self.base.mouseWatcherNode.isOverRegion():
            return
        if released:
            self.camera_control.on_mouse_release()
            return
        self.camera_control.on_mouse_press()
        self.on_scene_click()

    def on_scene_click(self):
        if not self.base.mouseWatcherNode.hasMouse():
            return
        mpos = self.base.mouseWatcherNode.getMouse()
        picker_ray = CollisionRay()
        picker_ray.setFromLens(self.base.camNode, mpos.getX(), mpos.getY())
        traverser = CollisionTraverser()
        handler = CollisionHandlerQueue()
        picker_node = CollisionNode('picker_ray')
        picker_node.setFromCollideMask(BitMask32.bit(1))
        picker_node.addSolid(picker_ray)
        picker_np = self.base.camera.attachNewNode(picker_node)
        traverser.addCollider(picker_np, handler)
        traverser.traverse(self.root)
        if handler.getNumEntries() > 0:
            handler.sortEntries()
            entry = handler.getEntry(0)
            node = entry.getIntoNodePath()
            clickable = node.findNetTag('clickable')
            if not clickable.isEmpty():
                if self.clicked_model:
                    self.clicked_model.clearColor()
                self.clicked_model = clickable
                clickable.setColor(1, 0.5, 0.5, 1)
                self.model_panel.show()
                pos = clickable.getPos()
                hpr = clickable.getHpr()
                self.pos_x.set(str(pos.x))
                self.pos_y.set(str(pos.y))
                self.pos_z.set(str(pos.z))
                self.rot_x.set(str(hpr.x))
                self.rot_y.set(str(hpr.y))
                self.rot_z.set(str(hpr.z))
                picker_np.removeNode()
                return
        self.model_panel.hide()
        self.clear_selection()
        picker_np.removeNode()

    def clear_selection(self):
        if self.clicked_model:
            self.clicked_model.clearColor()
            self.clicked_model = None

    def update_model_transform(self, text=None):
        if not self.clicked_model:
            return
        try:
            x = float(self.pos_x.get())
            y = float(self.pos_y.get())
            z = float(self.pos_z.get())
            rx = float(self.rot_x.get())
            ry = float(self.rot_y.get())
            rz = float(self.rot_z.get())
        except ValueError:
            return
        self.clicked_model.setPos(x, y, z)
        self.clicked_model.setHpr(rx, ry, rz)

    def delete_selected_model(self):
        if self.clicked_model:
            self.clicked_model.removeNode()
            self.clear_selection()
            self.model_panel.hide()