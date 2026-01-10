import os
import sys

# Определяем папку с exe
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

os.environ['TCL_LIBRARY'] = os.path.join(base_dir, 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(base_dir, 'tk8.6')


import logging
from app.core.tools.const import LOG_FORM, LOG_FILEMOD, LOG_FILENAME
from main import App


def main():
    logging.basicConfig(
        format=LOG_FORM,
        filemode=LOG_FILEMOD,
        filename=LOG_FILENAME,
        level=logging.INFO,
    )

    app = App()
    app.run()


if __name__ == "__main__":
    main()