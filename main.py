import logging
import tkinter as tk
from PIL import Image, ImageTk
from panda3d.core import loadPrcFileData, WindowProperties
from direct.showbase.ShowBase import ShowBase

from app.core.config.config import Config

from app.screenManager import SceneManager
from app.menuScene.menuScene import MenuScene

logger = logging.getLogger(__name__)

loadPrcFileData("", "window-title Fly Pro by AERO")
loadPrcFileData("", "win-size 1280 720")
loadPrcFileData("", "icon-filename media/ico/ico.ico")

def show_splash(duration=2):
    root = tk.Tk()
    root.overrideredirect(True)

    img = Image.open("media/logo/wgite.png")
    img_ratio = img.width / img.height

    target_width = 900
    target_height = int(target_width / img_ratio)
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(img)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (target_width // 2)
    y = (screen_height // 2) - (target_height // 2)
    root.geometry(f"{target_width}x{target_height}+{x}+{y}")

    label_logo = tk.Label(root, image=logo, borderwidth=0)
    label_logo.pack()

    root.after(int(duration * 1000), root.destroy)
    root.mainloop()

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(Config.APP_COLOR)

        props = WindowProperties()
        props.setForeground(True)
        props.setTitle("Config Pro by AERO")
        self.win.requestProperties(props)

        self.screen_manager = SceneManager(self)
        self.menu_scene = MenuScene(self, self.screen_manager)
        self.screen_manager.switch_to(self.menu_scene.root, is_3d=False)

show_splash(duration=2)
