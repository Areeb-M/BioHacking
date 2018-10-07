import pygame
import os
import teensy

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# System Variables
PATH = os.getcwd()

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Fonts
pygame.font.init()
size = 24
small_size = 12
large_size = 50
giant_size = 100
font_cache = {}
NORMAL = 0
SMALL = 1
BOLD = 2
LARGE = 3
GIANT = 4


def load_sys_font(name):
    global size, small_size
    return [pygame.font.SysFont(name, size),
            pygame.font.SysFont(name, small_size),
            pygame.font.SysFont(name, size, bold=True),
            pygame.font.SysFont(name, large_size),
            pygame.font.SysFont(name, giant_size)
            ]

font_list = ["agencyfb", "arcenamedium", "aressencemedium"]
font = [load_sys_font(f) for f in font_list]


def font_render(font_id, font_type, color, text):
    global font_cache, font
    cache_id = str(font_id) + str(font_type) + str(color) + text
    if cache_id not in font_cache:
        font_cache[cache_id] = font[font_id][font_type].render(text, True, color)
    return font_cache[cache_id]

# Sound
pygame.mixer.init()
SOUND_PATH = PATH + "\\assets\\sound\\"
sound_cache = {}


def load_audio_file(path):
    global SOUND_PATH
    path = SOUND_PATH + path
    return pygame.mixer.Sound(path)


def get_audio(name):
    global sound_cache
    cache_id = name
    if cache_id not in sound_cache:
        sound_cache[cache_id] = load_audio_file(name + ".wav")
    return sound_cache[cache_id]

command_queue = []

# Teensy Controller Interface Functions
# setup_motor
# activate_motor
# deactivate_motor
# flush_commands


def setup_motor(pin):
    global command_queue
    command_queue += [255, 2, pin, 1]


def activate_motor(pin):
    global command_queue
    command_queue += [255, 1, pin, 1]


def deactivate_motor(pin):
    global command_queue
    command_queue += [255, 1, pin, 0]


def delay_teensy(time):
    global command_queue
    first = (time & 0xFF00) >> 8
    second = time & 0x00FF
    command_queue += [255, 3, first, second]


def flush_commands():
    global command_queue
    teensy.write(bytes(command_queue))
    command_queue = []


def setup_controller():
    teensy.connect('COM3', 10000)
    for i in range(1, 8):
        setup_motor(i)
    flush_commands()


def clear():
    for i in range(1, 8):
        deactivate_motor(i)
    flush_commands()


def transmit_letter(letter):
    clear()
    binary = ord(letter)
    for i in range(1, 8):
        motor = i - 1
        if binary >> motor & 1:
            activate_motor(i)
    flush_commands()
