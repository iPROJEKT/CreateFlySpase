import os

# Указываем пути к Tcl/Tk библиотекам
os.environ['TCL_LIBRARY'] = r"C:\CreateFlySpase\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\CreateFlySpase\tcl\tk8.6"

# Теперь можно импортировать _tkinter
import _tkinter

print("Tcl version:", _tkinter.TCL_VERSION)
print("Tk version:", _tkinter.TK_VERSION)