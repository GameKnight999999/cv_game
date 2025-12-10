import pygame

# setup
pygame.init()
screen = pygame.display.set_mode((1580, 820))
pygame.display.set_caption("ui test")
clock = pygame.time.Clock()

class Font:
    def __init__(self):
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

    def print_text(self, text, symbol_size):
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
            print('Hey! Some of symbols in your text are not available yet, check out the file')

    def start_timer(self, start_time, symbol_size):
        self.seconds = [str(sec) for sec in range(0, start_time + 1)]
        self.timer_running = True

    def end_timer(self):
        self.timer_running = False
        self.seconds = []
        self.timer_start_time = None


# constants
white = (255, 255, 255)
default_position = (0, 0)
screen_width, screen_height = screen.get_size()
running = True
timer_running = False

#class font, functions -- print_text(Text, symbol_size), prints out the given text, timer(start_time, symbol_size) -- create a timer (still in progress)
font = Font()

# image loading function
def load_image(name, colorkey=None):
    fullname = 'images/' + name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image

async def inp(prompt: str) -> str:
    return input(prompt)

# main cycle
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                font.line += 1

    pygame.display.flip()
    screen.fill(white)
    if font.timer_running:
        current_second = pygame.time.get_ticks() // 1000
        font.print_text(font.seconds[-(current_second - font.timer_start_time)], font.symbol_size)
        if font.seconds[-(current_second - font.timer_start_time)] == '0':
            font.end_timer()
            print('end.')

    else:
        print("Write the text you want to be printed out:")
        keyboard_input = input()
        if keyboard_input == 'version':
            keyboard_input = font.version
        elif keyboard_input == 'quit.':
            running = False
        elif keyboard_input == 'timer':
            font.start_timer(60, font.symbol_size)
            font.timer_start_time = pygame.time.get_ticks() // 1000 - 1
            keyboard_input = ''
        font.print_text(keyboard_input, font.symbol_size)
    clock.tick(60)

pygame.quit()

with open("not_available_symbols.txt", "a") as f:
    for symbol in font.not_available:
        f.write(f'{symbol} is not available')
        f.write('\n')

#open and read the file after the appending:
with open("not_available_symbols.txt") as f:
  print(f.read())
#to save the changes and exit the editor press Esc, type :wq and press Enter