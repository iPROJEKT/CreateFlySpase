def rgb(r, g, b, a=255):
    return (r / 255, g / 255, b / 255, a / 255)

class Config:
    WINDOW_TITLE = "WAAMMER"
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 8005
    RECONNECT_INTERVAL = 5.0
    LIGHT_POSITIONS = [
        (0, 100000, 0), (0, -100000, 0),
        (-100000, 0, 0), (100000, 0, 0),
        (0, 0, -100000), (0, 0, 100000)
    ]
    DEFAULT_CAMERA_POS = (1.2 * 4362.32, 1.2 * 3821.91, 1.2 * 155.31)
    DEFAULT_TARGET = (0, 700, 0)

    AXIS_COLOR = rgb(154, 154, 154)
    GRID_COLOR = rgb(77, 77, 77)
    BUTTON_BG_COLOR = rgb(64, 64, 64)
    PRINT_LINE_COLOR = rgb(0, 0, 255)
    IDLE_LINE_COLOR = rgb(255, 0, 255)
    TEXT_COLOR = rgb(255, 255, 255)
    PANEL_BG_COLOR = rgb(0, 0, 0)
    VALUE_FRAME_COLOR = rgb(33, 33, 33)
    OPTION_ITEM_FRAME_COLOR = rgb(77, 77, 77)
    SEGMENT_LABEL_COLOR = rgb(154, 154, 154)
    APP_COLOR = rgb(35, 38, 34)
    FLY_LINES_COLOR = rgb(192, 192, 192)

    MAX_POINTS_FOR_GRAF = 1000
    NUMBER_OF_SELECTABLE_POINTS = 1
    ADD_TIME_GRAF = NUMBER_OF_SELECTABLE_POINTS * 0.016
    MAX_POINT_IN_FLY = 15

    DOD_FIRST_POINT_SCALE = 20
    DOD_OTHER_POINT_SCALE = 8
    DOD_COLOR_POINT = (1, 0, 0, 1)


    DRONE_MODEL_PATH = "moled/Material/drone_costum.obj" # Путь до модели дрона
    BOX_SIZE = 200                                       # Размер коробки
    DRON_SCALE = 3                                       # Множитель увеличения моедли дрона

    PATH_FONT="app/core/font/Ubuntu-Regular.ttf"