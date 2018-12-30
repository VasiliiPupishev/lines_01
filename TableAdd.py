import pygame


class Record:
    line = ""
    score = 0

    def __init__(self, l, s):
        self.score = s
        self.line = l


class AddRecord:
    write = False
    score = 0
    Records = None
    Name = ""
    full_list = None

    def __init__(self, screen, scr):
        self.Records = []
        f = open('records.txt')
        self.full_list = []
        for line in f:
            try:
                s = line.split(" ")
                name = s[0]
                score = int(s[1])
                self.full_list.append(Record(name, score))
            except Exception:
                continue
        self.full_list.sort(key=lambda x: -x.score)
        self.Records = self.full_list[:5]
        self.start(screen, scr)

    def start(self, screen, scr):
        self.draw(screen, scr)
        while True:
            for event in pygame.event.get():
                if event is pygame.QUIT:
                    raise SystemExit
                if event.type is pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 340 < y < 380:
                        if 160 < x < 290:
                            return
                        if 310 < x < 440:
                            f = open("records.txt", 'a')
                            if len(self.Name) == 0:
                                self.Name = "unknown_player"
                            f.write("\n" + self.Name + " " + str(scr))
                            f.close()
                            self.full_list.append(Record(self.Name, scr))
                            self.full_list.sort(key=lambda x: -x.score)
                            self.Records = self.full_list[:5]
                            self.draw(screen, scr)
                            import time
                            time.sleep(2)
                            return
                    if 150 < x < 450:
                        if 270 < y < 330:
                            self.write = True
                if event.type == pygame.KEYDOWN and self.write:
                    if event.key == pygame.K_BACKSPACE and len(self.Name) > 0:
                        self.Name = self.Name[:len(self.Name) - 1]
                    else:
                        self.Name += chr(event.key)
                    self.draw(screen, scr)

    def draw(self, screen, scr):
        im = pygame.image.load("Materials/fonn.jpg")
        im = pygame.transform.scale(im, (602, 400))
        screen.blit(im, (0, 0))
        font = pygame.font.SysFont('arial', 40)  # name caption
        loading_caption = font.render("Records", False, (0, 0, 0))
        screen.blit(loading_caption, (230, 10))
        pygame.display.update()
        font = pygame.font.SysFont('arial', 25)  # name caption
        i = 50
        for r in self.Records:
            record = font.render(r.line, False, (0, 0, 0))
            screen.blit(record, (50, i))
            record = font.render(str(r.score), False, (0, 0, 0))
            screen.blit(record, (500, i))
            i += 28
        plate = pygame.image.load("Materials/plate.png")
        plate = pygame.transform.scale(plate, (130, 40))
        screen.blit(plate, (160, 340))
        screen.blit(plate, (310, 340))
        font = pygame.font.SysFont('arial', 25)  # name caption
        loading_caption = font.render("Back", False, (0, 0, 0))
        screen.blit(loading_caption, (195, 347))
        loading_caption = font.render("Write", False, (0, 0, 0))
        screen.blit(loading_caption, (345, 347))
        text = pygame.image.load("Materials/text.jpg")
        text = pygame.transform.scale(text, (300, 60))
        screen.blit(text, (150, 270))
        font = pygame.font.SysFont('arial', 25)  # name caption
        loading_caption = font.render(self.Name, False, (255, 0, 0))
        screen.blit(loading_caption, (180, 280))
        font = pygame.font.SysFont('arial', 35)  # name caption
        loading_caption = font.render("Your Score: " + str(scr), False, (255, 0, 0))
        screen.blit(loading_caption, (180, 220))
        pygame.display.update()
