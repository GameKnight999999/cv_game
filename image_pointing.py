import pygame, os, json

def save() -> None:
    json.dump(points, open(f"{os.path.splitext(filenames[cur])[0]}.json", 'wt'))


dir = input("Input images dir: ")
os.chdir(dir)
img = []
filenames = os.listdir(".")
for filename in filenames:
    img.append(pygame.image.load(filename))
pygame.init()
screen = pygame.display.set_mode(img[0].get_size())
clock = pygame.time.Clock()

cur = 0
points = []
mouse = pygame.mouse.get_pos()
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEMOTION:
            mouse = e.pos
        elif e.type == pygame.MOUSEBUTTONDOWN:
            points.append(e.pos)
    
    if len(points) >= 10:
        save()
        cur += 1
        points = []

    screen.fill(0)
    screen.blit(img[cur], (0, 0))
    for point in points:
        pygame.draw.circle(screen, (0, 255, 0), point, 5)
    pygame.draw.circle(screen, (0, 255, 0, 127), mouse, 5)

    pygame.display.flip()
    clock.tick(60)