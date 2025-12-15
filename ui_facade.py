import pygame
from event_handler import *
from typing import Callable
# setup
pygame.init()
screen = pygame.display.set_mode((1580, 820))
pygame.display.set_caption("ui test")
clock = pygame.time.Clock()
screen_width, screen_height = screen.get_size()
round_index = 0
status_num = 0

# image loading function
def load_image(name, colorkey=None):
    fullname = 'images/' + name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image


class Font:
    "class font, functions -- print_text(Text, symbol_size), prints out the given text, timer(start_time, symbol_size) -- create a timer (still in progress)"
    def __init__(self) -> None:
        self.available_symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                             'S', 'T',
                             'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ':', ' ']
        self.version = 'font version: 0.1'

        self.symbol_size = (100, 180)
        self.start_text_pos_y = 0
        self.line = 0
        self.not_available = set()

        self.timer_running = False
        self.seconds = []
        self.timer_start_time = None

    def print_text(self, text: str, symbol_size: set) -> None:
        #basic stuff -- getting symbol size, the max amount of symbols the screen can fit, turning text into capitals, setting symbol index to 0
        symbol_width, symbol_height = symbol_size
        line_max_symbols = screen_width // symbol_width - 1
        text = text.upper()
        index = 0
        message = False

        #if the text won't fit in the screen
        if len(text) >= line_max_symbols:
            start_text_pos_x = (screen_width - line_max_symbols * symbol_width) // 2
        else:
            start_text_pos_x = (screen_width - len(text) * symbol_width) // 2

        #getting the storting position
        start_pos = (start_text_pos_x, self.start_text_pos_y + symbol_height * self.line)

        #processing the text ig
        for symbol in text:
            if symbol in self.available_symbols:
                # the system didn't let me save files named like :.png, etc, so i added this
                # please don't delete or it's gonna crash :(
                if symbol == '.':
                    symbol = 'dot'
                elif symbol == ':':
                    symbol = 'colon'
                elif symbol == ' ':
                    symbol = 'space'
                # print the symbol, change the x
                screen.blit(load_image(f'{symbol}.png'), start_pos)
                start_text_pos_x += symbol_width
                # move to the next line
                if index == line_max_symbols:
                    self.line += 1
                    start_text_pos_x = (screen_width - index * symbol_width) // 2
                    index -= line_max_symbols
            else:
                message = True
                self.not_available.add(symbol)
            # change the position and increase the symbol's index by one
            start_pos = (start_text_pos_x, self.start_text_pos_y + symbol_height * self.line)
            index += 1

        self.line = 0
        if message:
            print('Some of symbols in your text are not available yet, check out the file')

    def start_timer(self, start_time, symbol_size) -> None:
        self.seconds = [str(sec) for sec in range(0, start_time + 1)]
        self.timer_running = True

    def end_timer(self) -> None:
        self.timer_running = False
        self.seconds = []
        self.timer_start_time = None

class Button:
    def __init__(self, text: str, action: Callable, x: int, y: int, width: int, height: int) -> None:
        self.text = text
        self.action = action
        self.x, self.y = x, y
        self.width, self.height = width, height
        def callback(e: pygame.event.Event):
            if 0 < e.pos[0] - x < self.width and 0 < e.pos[1] - x < self.height:
                self.action()
        self.listener = add_event_listener(pygame.MOUSEBUTTONDOWN, callback)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                pass

def Main_Menu():
    #draw main menu here
    pass

def Settings():
    #draw settings here
    pass

def Instructions():
    #draw the instruction menu here
    pass