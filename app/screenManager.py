from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath

class SceneManager:
    def __init__(self, base: ShowBase):
        self.base = base
        self.current_scene: NodePath | None = None

    def switch_to(self, new_scene_node: NodePath, is_3d: bool = False):
        if self.current_scene:
            self.current_scene.detach_node()

        self.current_scene = new_scene_node
        parent = self.base.render if is_3d else self.base.aspect2d
        self.current_scene.reparent_to(parent)

    def hide_current(self):
        if self.current_scene:
            self.current_scene.detach_node()