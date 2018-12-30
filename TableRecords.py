import pygame


class Record:
    line = ""
    score = 0

    def __init__(self, l, s):
        self.score = s
        self.line = l


class TableRecords:
    Records = None

    def __init__(self):
        self.Records = []
        f = open('records.txt')
        res = []
        for line in f:
            try:
                s = line.split(" ")
                name = s[0]
                score = int(s[1])
                res.append(Record(name, score))
            except Exception:
                continue
        res.sort(key=lambda x: -x.score)
        self.Records = res[:10]

    def draw(self, screen):
        im = pygame.image.load("Materials/fonn.jpg")
        im = pygame.transform.scale(im, (602, 400))
        screen.blit(im, (0, 0))
        font = pygame.font.SysFont('arial', 40)  # name caption
        loading_caption = font.render("Records", False, (0, 0, 0))
        screen.blit(loading_caption, (230, 10))
        pygame.display.update()
        font = pygame.font.SysFont('arial', 25)  # name caption
        i = 40
        for r in self.Records:
            record = font.render(r.line, False, (0, 0, 0))
            screen.blit(record, (50, i))
            record = font.render(str(r.score), False, (0, 0, 0))
            screen.blit(record, (500, i))
            i += 28
        plate = pygame.image.load("Materials/plate.png")
        plate = pygame.transform.scale(plate, (130, 40))
        screen.blit(plate, (235, 340))
        font = pygame.font.SysFont('arial', 25)  # name caption
        loading_caption = font.render("Back", False, (0, 0, 0))
        screen.blit(loading_caption, (270, 347))
        pygame.display.update()

    def start(self, screen):
        self.draw(screen)
        while True:
            for event in pygame.event.get():
                if event is pygame.QUIT:
                    raise SystemExit
                if event.type is pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 235 < x < 365:
                        if 340 < y < 380:
                            return
