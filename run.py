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