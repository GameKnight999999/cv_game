import pygame

#setup
pygame.init()
screen = pygame.display.set_mode((1580, 820))
pygame.display.set_caption("ui test")
clock = pygame.time.Clock()

#constants
version = 'font version: 0.1'
line = 0
timer = False
white = (255, 255, 255)
default_position = (0, 0)
screen_width, screen_height = screen.get_size()
symbol_size = (100, 180)
start_text_pos_y = 0
available_symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '.', ':', ' ']
running = True

#image loading function
def load_image(name, colorkey=None):
    fullname = 'images/' + name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image

#print text on the screen
def print_text(text, symbol_size):
    global line
    symbol_width, symbol_height = symbol_size
    line_max_symbols = screen_width // symbol_width
    text = text.upper()
    if len(text) >= line_max_symbols:
        start_text_pos_x = (screen_width - line_max_symbols * symbol_width) // 2
    else:
        start_text_pos_x = (screen_width - len(text) * symbol_width) // 2
    start_pos = (start_text_pos_x, start_text_pos_y + symbol_height * line)
    index = 0
    for symbol in text:
        if symbol in available_symbols:
            #the system didn't let me save files named like :.png, etc :(
            if symbol == '.':
                symbol = 'dot'
            elif symbol == ':':
                symbol = 'colon'
            elif symbol == ' ':
                symbol = 'space'

            #print the symbol, change the x
            screen.blit(load_image(f'{symbol}.png'), start_pos)
            start_text_pos_x += symbol_width

            #move to the next line
            if index == line_max_symbols:
                line += 1
                start_text_pos_x = (screen_width - index * symbol_width) // 2
                index -= line_max_symbols

        start_pos = (start_text_pos_x, start_text_pos_y + symbol_height * line)
        index += 1

#main cycle
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                line += 1
    pygame.display.flip()
    screen.fill(white)
    print("Write the text you want to be printed out:")
    keyboard_input = input()
    if keyboard_input == 'version':
        keyboard_input = version
    print_text(keyboard_input, symbol_size)
    get_text = False
    clock.tick(60)

pygame.quit()