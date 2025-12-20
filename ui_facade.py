"""
    UI Facade based on pygame. Gives some basic instruments like Button
"""


import pygame
import cv2
import event_handler as ev
from settings import *
from cachetools import cached
from typing import Callable


@cached(None)
def load_image(name: str) -> pygame.SurfaceType:
    """
    loads an image
    Args:
        name: the name of an image in the 'images' folder
    """
    fullname = 'images/' + name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise FileNotFoundError(message)
    return image


class UIElement:
    def __init__(self) -> None:
        ui_elements.append(self)
    

    def render(self) -> None:
        pass


    def __del__(self) -> None:
        ui_elements.remove(self)


class Font:
    """
    A font class, which can print out a text and start a timer
    """
    def __init__(self) -> None:
        self.available_symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                             'S', 'T',
                             'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ':', ' ']
        self.version = 'font version: 0.1'

        self.symbol_size = (100, 180)
        self.line = 0
        self.not_available = set()

        self.timer_running = False
        self.seconds = []
        self.timer_start_time = None

    def print_at(self, text: str, size: float, x: int, y: int) -> None:
        """
        Prints the text with left top corner at (x, y)
        
        :param text: Text to print
        :param size: Font size
        :param x: Left-top corner x coord
        :param y: Left-top corner y coord
        """
        """
        Prints the given text on the screen and writes not available symbols in a file
        Args:
            text: the text that will be printed out
            symbol_size: the size of each symbol in pixels, a set with two variables: width and height
        Returns:
            A string containing the greeting message.
        """
        #basic stuff -- getting symbol size, the max amount of symbols the screen can fit, turning text into capitals, setting symbol index to 0
        text = text.upper()
        message = False

        start_text_pos_x = x
        start_text_pos_y = y

        #getting the storting position
        start_pos = (start_text_pos_x, start_text_pos_y)

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

                image = load_image(f'{symbol}.png')
                # scale the symbol to a new size
                image = pygame.transform.scale(image, (image.get_width() * size, image.get_height() * size))

                screen.blit(image, start_pos)
                #change the x
                start_text_pos_x += image.get_width() * size

            else:
                message = True
                self.not_available.add(symbol)
            # change the position and increase the symbol's index by one
            start_pos = (start_text_pos_x, start_text_pos_y)

        self.line = 0
        if message:
            print('Some of symbols in your text are not available yet, check out the file')


    def start_timer(self, start_time) -> None:
        """
        Starts a decreasing timer
        Args:
            start_time: Timer's starting time in seconds.
        """
        self.seconds = [str(sec) for sec in range(0, start_time + 1)]
        self.timer_running = True


    def end_timer(self) -> None:
        """
        Ends the timer
        """
        self.timer_running = False
        self.seconds = []
        self.timer_start_time = None


class Image(UIElement):
    """
    Class for rendering some imges on the screen
    """
    def __init__(self, image: pygame.SurfaceType, x: int, y: int) -> None:
        """
        Creates Image from pygame.Surface
        
        :param image: Surface to use as image
        :param x: x coord of image on screen
        :param y: y coord of image on screen
        """
        self.image = image
        self.pos = x, y
        super().__init__()
    

    @classmethod
    def load(cls, filename: str, x: int, y: int) -> "Image":
        """
        Loads and creates an image
        
        :param filename: Image file path
        :param x: x coord of image on screen
        :param y: y coord of image on screen
        :return: New Image object
        """
        return cls(load_image(filename), x, y)


    def render(self) -> None:
        screen.blit(self.image, self.pos)


class Video(Image):
    def __init__(self, video: cv2.VideoCapture, x: int, y: int) -> None:
        """
        Create a Video object to show a video on screen
        
        :param video: cv2 VideoCapture object to read frames from
        :param x: x coord of video on screen
        :param y: y coord of video on screen
        """
        self.video = video
        super().__init__(pygame.Surface((video.get(cv2.CAP_PROP_FRAME_WIDTH), video.get(cv2.CAP_PROP_FRAME_HEIGHT))), x, y)
    

    @classmethod
    def load(cls, filename: str, x: int, y: int) -> "Image":
        """
        Loads and creates a video
        
        :param filename: Video file path
        :param x: x coord of video on screen
        :param y: y coord of video on screen
        :return: New Video object
        """
        return cls(cv2.VideoCapture(filename), x, y)
    

    def read(self) -> pygame.SurfaceType:
        success, frame = self.video.read()
        if not success:
            return load_image(VIDEO_PLACEHOLDER)
        else:
            return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")
    

    def render(self) -> None:
        self.image = self.read()
        return super().render()


class Text(UIElement):
    def __init__(self, text: str, size: int, x: int, y: int) -> None:
        self.text = text
        self.size = size
        self.pos = x, y
        super().__init__()
    

    def render(self) -> None:
        pass


class Button(UIElement):
    """
    Creates a button
    Attributes:
        text: The text of the button
        action: callback funtion to call on click
        x: x coord of left-top corner of the button
        y: y coord of left-top corner of the button
        width: width of the button
        height: height of the button
    """
    def __init__(self, text: str, action: Callable, x: int, y: int, width: int, height: int) -> None:
        self.text = text
        self.action = action
        self.x, self.y = x, y
        self.width, self.height = len(text) * 100 * FONT_SIZE, 100
        self.font = Font()
        def callback(e: pygame.event.Event):
            if 0 < e.pos[0] - x < self.width and 0 < e.pos[1] - x < self.height:
                self.action()
        self.listener = ev.add_event_listener(pygame.MOUSEBUTTONDOWN, callback)

        self.rect = (self.x, self.y, self.width, self.height)

        super().__init__()


    def render(self) -> None:
        """
        Render the button to the screen
        """
        pygame.draw.rect(screen, "green", self.rect, border_radius=5)
        self.font.print_at(self.text, FONT_SIZE, self.x, self.y)


    def __del__(self) -> None:
        ev.remove_event_listener(self.listener)
        super().__del__()


def tick(fps: float = -1) -> float:
    screen.fill("black")
    for el in ui_elements:
        el.render()
    pygame.display.flip()
    return ev.tick(fps)

def play_music(name: str):
    """
    Plays looped music

    :param name: Name of the music file without .mp3
    :type name: str
    """
    full_name = f'music/{name}.mp3'
    try:
        pygame.mixer.music.load(full_name)
    except pygame.error as e:
        print(f"Cannot load music file: {e}")
    pygame.mixer.music.play(-1)

def mute_and_unmute_music():
    """
    Mutes and unmutes the music
    """
    if pygame.mixer.music.get_volume() == 1:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(1)

def bind(key: str, callback: Callable) -> None:
    """
    Binds a function to a key
    
    :param key: Key to bind for
    :type key: str
    :param callback: function to bind
    :type callback: Callable
    """
    if key[0] not in keybinds:
        keybinds[key[0]] = []
    keybinds[key[0]].append(ev.add_event_listener(
        pygame.KEYDOWN,
        lambda e: callback if e.key == pygame.key.key_code(key[0]) else 0
    ))


def unbind(key: str) -> None:
    """
    Unbinds any functions from a key
    
    :param key: Key to unbind
    :type key: str
    """
    for l in keybinds[key[0]]:
        ev.remove_event_listener(l)


def clearscreen() -> None:
    global ui_elements
    ui_elements = []


# setup
__any__ = ["Button", "Font", "tick"]
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("ui test")
clock = pygame.time.Clock()
screen_width, screen_height = screen.get_size()
ui_elements: list[UIElement] = []
keybinds: dict[str, list[ev.Listener]] = {}

ev.add_event_listener(pygame.QUIT, lambda _: exit())
ev.add_event_listener(pygame.KEYDOWN, lambda x: mute_and_unmute_music() if x.key == pygame.K_m else None)
ev.add_event_listener(pygame.KEYDOWN, lambda x: exit() if x.key == pygame.K_ESCAPE else None)