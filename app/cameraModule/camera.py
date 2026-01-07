import math
from panda3d.core import Point3, Vec3
from direct.task import Task

class CameraControl:
    def __init__(self, base, center=Point3(0, 0, 0), distance=600.0):
        self.base = base
        self.center = Point3(center)
        self.distance = distance
        self.base.disableMouse()

        self.current_h = 60.0
        self.current_p = 15.0

        self.left_mouse_pressed = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.rotation_speed = 0.3

        self.task_name = "CameraOrbitTask"

        self.update_camera_position()

        self.base.accept("mouse1", self.on_mouse_press)
        self.base.accept("mouse1-up", self.on_mouse_release)
        self.base.taskMgr.add(self.mouse_task, self.task_name)

    def update_camera_position(self):
        h_rad = math.radians(self.current_h)
        p_rad = math.radians(self.current_p)

        x = self.distance * math.cos(p_rad) * math.sin(h_rad)
        y = self.distance * math.cos(p_rad) * math.cos(h_rad)
        z = self.distance * math.sin(p_rad)

        cam_pos = self.center + Vec3(x, y, z)
        self.base.camera.setPos(cam_pos)
        self.base.camera.lookAt(self.center)

    def set_distance(self, distance):
        self.distance = max(1.0, distance)  # не позволяем distance быть <=0
        self.update_camera_position()

    def move_center(self, new_center):
        self.center = Point3(new_center)
        self.update_camera_position()

    def on_mouse_press(self):
        if self.base.mouseWatcherNode.hasMouse():
            self.left_mouse_pressed = True
            m = self.base.mouseWatcherNode.getMouse()
            self.last_mouse_x = m.getX()
            self.last_mouse_y = m.getY()

    def on_mouse_release(self):
        self.left_mouse_pressed = False

    def mouse_task(self, task):
        if not self.left_mouse_pressed or not self.base.mouseWatcherNode.hasMouse():
            return Task.cont

        mouse = self.base.mouseWatcherNode.getMouse()
        dx = mouse.getX() - self.last_mouse_x
        dy = mouse.getY() - self.last_mouse_y

        self.current_h += dx * 100 * self.rotation_speed
        self.current_p -= dy * 100 * self.rotation_speed

        self.current_p = max(-89.9, min(89.9, self.current_p))
        self.current_h = self.current_h % 360

        self.update_camera_position()
        self.last_mouse_x = mouse.getX()
        self.last_mouse_y = mouse.getY()
        return Task.cont

    def enable(self):
        self.base.accept("mouse1", self.on_mouse_press)
        self.base.accept("mouse1-up", self.on_mouse_release)
        self.base.taskMgr.add(self.mouse_task, self.task_name)

    def disable(self):
        self.base.ignore("mouse1")
        self.base.ignore("mouse1-up")
        self.base.taskMgr.remove(self.task_name)