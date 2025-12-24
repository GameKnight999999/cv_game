"""
    UI Facade based on pygame. Gives some basic instruments like Button
"""
import pygame
import cv2
import event_handler as ev
from cachetools import cached
from typing import Callable
import settings


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

def darken(surface: pygame.Surface, factor: float = 0.5) -> pygame.Surface:

    surf = surface.copy()
    value = int(255 * factor)
    surf.fill((value, value, value), special_flags=pygame.BLEND_RGB_MULT)
    return surf

CURSOR_NORMAL = load_image("cursor.png")
CURSOR_CLICK = load_image("cursor_click.png")

class UIElement:
    def __init__(self) -> None:
        self.listeners = []
        ui_elements.append(self)

    def destroy(self):
        for l in self.listeners:
            ev.remove_event_listener(l)

    def render(self):
        pass


class Font:
    """
    A font class, which can print out a text and start a timer
    """

    def __init__(self) -> None:
        self.available_symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                  'R',
                                  'S', 'T',
                                  'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.',
                                  ':', ' ', '<', '>']
        self.version = 'font version: 0.1'
        self.not_available = set()

        self.timer_running = False
        self.seconds = []
        self.timer_start_time = None

    def print_at(self, text: str, size: float, x: int, y: int, hovered: bool=False) -> tuple:
        """
        Prints the text with left top corner at (x, y)

        :param text: Text to print
        :param size: Font size
        :param x: Left-top corner x coord
        :param y: Left-top corner y coord
        :param hovered: if the text should be darkened
        """
        """
        Prints the given text on the screen and writes not available symbols in a file
        Args:
            text: the text that will be printed out
            symbol_size: the size of each symbol in pixels, a set with two variables: width and height
        Returns:
            A string containing the greeting message.
        """
        # basic stuff -- getting symbol size, the max amount of symbols the screen can fit, turning text into capitals, setting symbol index to 0
        text = text.upper()

        start_text_pos_x = x
        start_text_pos_y = y

        # getting the storting position
        start_pos = (start_text_pos_x, start_text_pos_y)

        # processing the text ig
        for symbol in text:
            if symbol in self.available_symbols:
                # the system didn't let me save files named like :.png, etc., so i added this
                # please don't delete, or it's gonna crash :(
                if symbol == '.':
                    symbol = 'dot'
                elif symbol == ':':
                    symbol = 'colon'
                elif symbol == ' ':
                    symbol = 'space'
                elif symbol == '<':
                    symbol = 'arrow_left'
                elif symbol == '>':
                    symbol = 'arrow_right'

                image = load_image(f'{symbol}.png')
                # scale the symbol to a new size
                image = pygame.transform.scale(image, (image.get_width() * size, image.get_height() * size))
                if hovered:
                    image = darken(image)
                screen.blit(image, start_pos)
                # change the x
                start_text_pos_x += image.get_width() * size + 10

            else:
                self.not_available.add(symbol)
            # change the position and increase the symbol's index by one
            start_pos = (start_text_pos_x, start_text_pos_y)
        return start_pos

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
    Class for rendering some images on the screen
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
        super().__init__(pygame.Surface((video.get(cv2.CAP_PROP_FRAME_WIDTH), video.get(cv2.CAP_PROP_FRAME_HEIGHT))), x,
                         y)

    @classmethod
    def load(cls, filename: str, x: int, y: int) -> "Image":
        """
        Loads and creates a video

        :param filename: Video file path
        :param x: x coord of video on-screen
        :param y: y coord of video on-screen
        :return: New Video object
        """
        return cls(cv2.VideoCapture(filename), x, y)

    def read(self) -> pygame.SurfaceType:
        success, frame = self.video.read()
        if not success:
            return load_image(settings.VIDEO_PLACEHOLDER)
        else:
            return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")

    def render(self) -> None:
        self.image = self.read()
        return super().render()

class Button(UIElement):
    """
    Creates a button
    Attributes:
        text: The text of the button
        action: callback function to call on click
        x: x coord of left-top corner of the button
        y: y coord of left-top corner of the button
        sound: true if the sound is played on click
    """

    def __init__(self, text: str, action: Callable, x: int, y: int, sound: bool) -> None:
        super().__init__()
        self.text = text
        self.action = action
        self.x, self.y = x, y
        self.width, self.height = len(text) * 100 * settings.FONT_SIZE, 100
        self.font = Font()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sound = sound
        self.end_pos = (0, 0)
        def callback(e: pygame.event.Event):
            if self.rect.collidepoint(e.pos) and self.action != 'none':
                self.action()
                if self.sound:
                    play_sound('click')

        self.listener = ev.add_event_listener(pygame.MOUSEBUTTONDOWN, callback)
        self.listeners.append(self.listener)

    def render(self) -> None:
        """
        Render the button to the screen
        """
        #pygame.draw.rect(screen, "green", self.rect, border_radius=5)
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)
        self.end_pos = self.font.print_at(self.text, settings.FONT_SIZE, self.x, self.y, hovered)

class ButtonArrows(Button):
    """
    Creates an adjustment button with arrows
    Attributes:
        text: The text of the button
        name: the name of a variable, which will be changed by pressing the arrows
        value: current value of the variable
        max_value: max value of the variable
        x: x coord of left-top corner of the button
        y: y coord of left-top corner of the button
    """
    def __init__(self, text: str, name: str, value: (int, str), max_value: int, x: int, y: int, values: tuple=tuple(), add_to_value:int=1, min_value:int=1) -> None:
        self.max_value = max_value
        self.min_value = min_value
        self.name = name
        self.value = value
        self.values = values
        self.add_to_value = add_to_value
        super().__init__(text, self.apply_value, x, y, False)
        # note: change the variables to the actual ones
        self.arrow_left = pygame.Rect(int(self.x + self.width), self.y, self.width, self.height)
        self.arrow_right = pygame.Rect(int(self.x + self.width + 300), self.y, self.width, self.height)

        def callback(e: pygame.event.Event):
            if self.arrow_left.collidepoint(e.pos):
                if isinstance(self.value, int):
                    if self.value != self.min_value:
                        self.value -= self.add_to_value
                        self.action()
                else:
                    if self.values.index(self.value) != 0:
                        self.value = self.values[self.values.index(self.value) - 1]
                        self.action()
            elif self.arrow_right.collidepoint(e.pos):
                if isinstance(self.value, int):
                    if self.value != self.max_value:
                        self.value += self.add_to_value
                        self.action()
                else:
                    if self.values.index(self.value) != self.values.index(self.values[-1]):
                        self.value = self.values[self.values.index(self.value) - 1]
                        self.action()

        if self.name == 'USER_VOLUME':
            set_volume(self.value)
        self.arrow_listener = ev.add_event_listener(pygame.MOUSEBUTTONDOWN, callback)
        self.listeners.append(self.arrow_listener)

    def apply_value(self):
        setattr(settings, self.name, self.value)

    def render(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.end_pos = self.font.print_at(self.text, settings.FONT_SIZE, self.x, self.y)
        # note: change the variables to the actual ones
        self.arrow_left = pygame.Rect(self.end_pos[0], self.end_pos[1], 70, self.height)
        hovered = self.arrow_left.collidepoint(mouse_pos)
        self.end_pos = self.font.print_at('<', settings.FONT_SIZE, self.end_pos[0], self.end_pos[1], hovered)

        self.end_pos = self.font.print_at(str(self.value), settings.FONT_SIZE, self.end_pos[0], self.end_pos[1])

        self.arrow_right = pygame.Rect(self.end_pos[0], self.end_pos[1], 70, self.height)
        hovered = self.arrow_right.collidepoint(mouse_pos)
        self.end_pos = self.font.print_at('>', settings.FONT_SIZE, self.end_pos[0], self.end_pos[1], hovered)

class Label(UIElement):
    """
    Creates a text
    Attributes:
        text: The text
        size: Font size
        x: x coord of left-top corner of the text
        y: y coord of left-top corner of the text
    """
    def __init__(self, text, size, x, y):
        self.text = text
        self.size = size
        self.x = x
        self.y = y
        self.font = Font()
        super().__init__()

    def render(self):
        self.font.print_at(self.text, self.size, self.x, self.y)


def tick(fps: float = -1) -> float:
    if settings.THEME == 'dark':
        screen.fill('black')
    else:
        screen.fill('white')
    for el in ui_elements:
        el.render()
    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:  # left mouse button
        screen.blit(CURSOR_CLICK, mouse_pos)
    else:
        screen.blit(CURSOR_NORMAL, mouse_pos)
    pygame.display.flip()
    return ev.tick(fps)

def set_volume(vol: int):
    vol = max(0, min(100, vol))
    settings.USER_VOLUME = vol
    settings.VOLUME = vol / 100
    pygame.mixer.music.set_volume(settings.VOLUME)

def play_music(name: str) -> None:
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


def play_sound(name: str) -> None:
    """
    Plays a sound once

    :param name: Name of the sound file without .mp3
    :type name: str
    """
    full_name = f'sounds/{name}.mp3'
    try:
        sound = pygame.mixer.Sound(full_name)
        sound.set_volume(settings.VOLUME)
        sound.play()
    except pygame.error as e:
        print(f"Cannot load sound file: {e}")


def mute_and_unmute_music() -> None:
    """
    Mutes and unmutes the music
    """
    if pygame.mixer.music.get_volume() == 0:
        set_volume(getattr(settings, "_PREV_VOLUME", settings.USER_VOLUME))
    else:
        settings._PREV_VOLUME = settings.USER_VOLUME
        set_volume(0)


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
    """
    Clears the screen from all the elements
    :return:
    """
    global ui_elements
    for el in ui_elements:
        el.destroy()
    ui_elements = []
    if settings.THEME == 'dark':
        screen.fill('black')
    else:
        screen.fill('white')


# setup
__any__ = ["Button", "Font", "tick"]
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("ui test")
clock = pygame.time.Clock()
screen_width, screen_height = screen.get_size()
ui_elements: list[UIElement] = []
keybinds: dict[str, list[ev.Listener]] = {}
pygame.mouse.set_visible(False)


ev.add_event_listener(pygame.QUIT, lambda _: exit())
ev.add_event_listener(pygame.KEYDOWN, lambda x: mute_and_unmute_music() if x.key == pygame.K_m else None)
ev.add_event_listener(pygame.KEYDOWN, lambda x: exit() if x.key == pygame.K_ESCAPE else None)