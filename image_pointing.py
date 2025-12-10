import pygame, os, json, math

def save() -> None:
    out = []
    for i in (1, 2, 3, 4, 6, 7, 8, 9):
        out.append(math.atan2(-(points[i][1] - points[i - 1][1]), points[i][0] - points[i - 1][0]))
    json.dump(out, open(f"{os.path.splitext(filenames[cur])[0]}.json", 'wt'))


dir = "poses"
os.chdir(dir)
img = []
filenames = os.listdir(".")
for filename in filenames:
    try:
        img.append(pygame.image.load(filename))
    except:
        continue
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
    if cur >= len(img):
        break

    screen.fill(0)
    screen.blit(img[cur], (0, 0))
    for point in points:
        pygame.draw.circle(screen, (0, 255, 0), point, 5)
    pygame.draw.circle(screen, (0, 255, 0, 127), mouse, 5)

    pygame.display.flip()
    clock.tick(60)