import pygame

from FieldClass import Field
from BallClass import Ball
import time
import os

Stars = 3
pygame.init()
white = (255, 255, 255)
screen = pygame.display.set_mode((602, 400))
pygame.display.set_caption("Lines")
pygame.mixer.init()


def main():
    field = Field("record.txt")
    done = True
    pygame.mixer.music.load(os.path.join('Materials', "main_theme.mp3"))
    pygame.mixer.music.play(loops=0, start=0.0)
    menu()
    pygame.display.update()
    move_list = []
    while done:
        if len(field.Balls) >= 78:
            if field.Score > field.BestScore:
                win_sound = pygame.mixer.Sound(os.path.join('Materials', "record.wav"))
                win_sound.play()
                f = open("record.txt", 'w')
                f.write(str(field.Score))
                f.close()
            time.sleep(2)
            from TableAdd import AddRecord
            S = AddRecord(screen, field.Score)
            pygame.mixer.music.rewind()
            menu()
            field = Field("record.txt")
        is_success = False
        draw_field(field)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = False
                if event.key == pygame.K_s:
                    make_preservation(field)
                if event.key == pygame.K_l:
                    load_preservation(field)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if 15 < x < 45:
                        if 365 < y < 400:
                            print("star")
                    if len(move_list) == 0:
                        win_sound = pygame.mixer.Sound(os.path.join('Materials', "chose.wav"))
                        win_sound.play()
                    move_list.append(event.pos)
        if len(move_list) == 2:
            is_success = try_move(move_list, field)
            move_list.clear()
            find_lines(field)
        if is_success:
            win_sound = pygame.mixer.Sound(os.path.join('Materials', "win.wav"))
            win_sound.play()
            for ball in field.Next:
                field.Balls.append(ball)
            field.Next = field.set_balls(field.Balls)
            find_lines(field)
        pygame.display.update()


def draw_field(field):
    screen.blit(field.Image, (0, 0))
    font = pygame.font.Font(None, 25)
    text1 = font.render("Best score " + str(field.BestScore), True, white)
    text = font.render("Score " + str(field.Score), True, white)
    screen.blit(text, [15, 10])
    screen.blit(text1, [15, 30])
    draw_balls(field)
    star = pygame.image.load("Materials/star.png")
    star = pygame.transform.scale(star, (20, 20))
    screen.blit(star, (65, 365))
    font = pygame.font.Font(None, 30)
    text = font.render(str(Stars), True, (255, 255, 0))
    screen.blit(text, [90, 368])
    text = font.render("Next: ", True, (255, 255, 255))
    screen.blit(text, [40, 200])
    j = 35
    for i in field.Next:
        screen.blit(i.Image, (j, 230))
        j += 40
    pygame.display.flip()


def draw_animation(field, start_ball, end_ball):
    a = 35
    s_image = pygame.image.load("Materials/" + start_ball.Color + ".png")
    e_image = pygame.image.load("Materials/" + start_ball.Color + ".png")
    defa = pygame.image.load("Materials/default.jpg")
    defa = pygame.transform.scale(defa, (37, 37))
    while a >= 7:
        a -= 7
        draw_field(field)
        if a <= 0:
            draw_field(field)
            pygame.display.update()
            break
        e_image = pygame.image.load("Materials/" + start_ball.Color + ".png")
        e_image = pygame.transform.scale(e_image, (a, a))
        screen.blit(defa, (197 + end_ball.X * 44, 19 + end_ball.Y * 41))
        screen.blit(e_image, (197 + start_ball.X * 44 - int(a/2) + 20, 19 + start_ball.Y * 41 - int(a/2) + 20))
        s_image = pygame.transform.scale(s_image, (37 - a, 37 - a))
        screen.blit(s_image, (195 + end_ball.X * 44 + int(a/2), 19 + end_ball.Y * 41 + int(a / 2)))
        pygame.display.update()
        #time.sleep(0.05)


def menu():
    print_menu()
    while True:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                raise SystemExit
            if event.type is pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if 150 < x < 450:
                        if 70 < y < 170:
                            print("play")
                            return
                        if 180 < y < 280:
                            table_records()
                            print("table records")
                            print_menu()
                    if 200 < x < 400:
                        if 290 < y < 340:
                            print("exit")
                            raise SystemExit


def table_records():
    from TableRecords import TableRecords
    tr = TableRecords()
    tr.start(screen)


def print_menu():
    font = pygame.font.Font(None, 80)
    image = pygame.image.load("Materials/fonn.jpg")
    image = pygame.transform.scale(image, (602, 400))
    screen.blit(image, (0, 0))
    text = font.render("LINES", True, (0, 0, 0))
    screen.blit(text, [225, 5])
    font = pygame.font.Font(None, 60)
    pygame.draw.rect(screen, (255, 20, 0), ((150, 70), (300, 100)))
    text = font.render("Start", True, (0, 0, 0))
    screen.blit(text, [255, 100])
    pygame.draw.rect(screen, (255, 70, 0), ((150, 180), (300, 100)))
    text = font.render("Records", True, (0, 0, 0))
    screen.blit(text, [220, 210])
    pygame.draw.rect(screen, (255, 70, 0), ((200, 290), (200, 50)))
    text = font.render("Exit", True, (0, 0, 0))
    screen.blit(text, [260, 297])
    pygame.display.update()


def load_preservation(field):
    try:
        new_balls = []
        file = open(os.path.join('Saves', "save_001.txt"), "r")
        all_information = file.read()
        strings = all_information.split('\n')
        for i in range(9):
            for j in range(9):
                color = ""
                if strings[i][j] == "#":
                    continue
                if strings[i][j] == "R":
                    color = "red"
                if strings[i][j] == "G":
                    color = "green"
                if strings[i][j] == "W":
                    color = "brown"
                if strings[i][j] == "Y":
                    color = "yellow"
                if strings[i][j] == "L":
                    color = "bluelite"
                if strings[i][j] == "P":
                    color = "pink"
                if strings[i][j] == "B":
                    color = "blue"
                if color != "":
                    new_balls.append(Ball(j, i, color))
        field.Score = int(strings[9])
        field.Balls = new_balls
    except Exception:
        return


def make_preservation(field):  #saving game
    full_field = []
    for i in range(9):
        full_field.append([])
        for j in range(9):
            full_field[i].append(Ball(i, j, "default"))
    for ball in field.Balls:
        full_field[ball.Y][ball.X] = ball
    open(os.path.join('Saves', "save_001.txt"), 'w').close()
    file = open(os.path.join('Saves', "save_001.txt"), "a")
    for i in range(9):
        for j in range(9):
            if full_field[i][j].Color == "default":
                file.write("#")
            if full_field[i][j].Color == "red":
                file.write("R")
            if full_field[i][j].Color == "green":
                file.write("G")
            if full_field[i][j].Color == "blue":
                file.write("B")
            if full_field[i][j].Color == "pink":
                file.write("P")
            if full_field[i][j].Color == "yellow":
                file.write("Y")
            if full_field[i][j].Color == "brown":
                file.write("W")
            if full_field[i][j].Color == "bluelite":
                file.write("L")
        file.write('\n')
    file.write(str(field.Score))
    file.close()


def find_lines(field):
    field_by_string = []
    field_by_colon = []
    for i in range(9):
        field_by_string.append([])
        field_by_colon.append([])
        for j in range(9):
            field_by_string[i].append(Ball(i, j, "default"))
            field_by_colon[i].append(Ball(i, j, "default"))
    for ball in field.Balls:
        field_by_string[ball.Y][ball.X] = ball
        field_by_colon[ball.X][ball.Y] = ball
    lines = []
    count = 5
    colors = ["red", "blue", "green", "pink", "bluelite", "yellow", "brown"]
    for color in colors:
        for i in range(9):
            for item in field_by_string[i]:
                if item.Color == color:
                    lines.append(item)
                else:
                    if len(lines) >= count:
                        win_sound = pygame.mixer.Sound(os.path.join('Materials', "succes.wav"))
                        win_sound.play()
                        for ball in lines:
                            field.Balls.remove(ball)
                        field.Score = field.Score + 2 ** len(lines)
                    lines.clear()
            if len(lines) >= count:
                for ball in lines:
                    field.Balls.remove(ball)
                field.Score = field.Score + 2 ** len(lines)
            lines.clear()
        for i in range(9):
            for item in field_by_colon[i]:
                if item.Color == color:
                    lines.append(item)
                else:
                    if len(lines) >= count:
                        for ball in lines:
                            field.Balls.remove(ball)
                        field.Score = field.Score + 2 ** len(lines)
                    lines.clear()
            if len(lines) >= count:
                for ball in lines:
                    field.Balls.remove(ball)
            lines.clear()


def try_move(moves, field11):
    balls = field11.Balls
    (start_x, start_y) = moves[0]
    (end_x, end_y) = moves[1]
    if start_x < 195 or start_y < 18 or start_x > 585 or start_y > 385:
        return False
    if end_x < 195 or end_y < 18 or end_x > 585 or end_y > 385:
        return False
    (x, y) = get_position(start_x, start_y)
    (x1, y1) = get_position(end_x, end_y)
    if x == x1 and y == y1:
        return False
    flag = True
    start_ball = None
    end_ball = Ball(x1, y1, "default")
    for ball in balls:
        if ball.X == x and ball.Y == y:
            start_ball = ball
            flag = False
        if ball.X == x1 and ball.Y == y1:
            end_ball == ball
    if flag and end_ball.Color == "default":
        return False
    field = []
    for i in range(9):
        field.append([])
        for j in range(9):
            field[i].append(Ball(i, j, "default"))
    for ball in balls:
        field[ball.X][ball.Y] = ball
    visited = bfs(field, start_ball)
    for ball in visited:
        if ball.X == x1 and ball.Y == y1:
            new_ball = Ball(x1, y1, start_ball.Color)
            balls.append(new_ball)
            balls.remove(start_ball)
            draw_animation(field11, start_ball, new_ball)
            return True
    win_sound = pygame.mixer.Sound(os.path.join('Materials', "lose.wav"))
    win_sound.play()
    return False


def bfs(field, start):
    visited = []
    start = Ball(start.X, start.Y, "default")
    queue = [start]
    while queue:
        point = queue.pop(0)
        if point.Color == "default":
            visited.append(point)
        if point.X + 1 < 9:
            next_point = field[point.X + 1][point.Y]
            if next_point.Color == "default":
                if not visited.__contains__(next_point):
                    queue.append(next_point)
        if point.X - 1 >= 0:
            next_point = field[point.X - 1][point.Y]
            if next_point.Color == "default":
                if not visited.__contains__(next_point):
                    queue.append(next_point)
        if point.Y + 1 < 9:
            next_point = field[point.X][point.Y + 1]
            if next_point.Color == "default":
                if not visited.__contains__(next_point):
                    queue.append(next_point)
        if point.Y - 1 >= 0:
            next_point = field[point.X][point.Y - 1]
            if next_point.Color == "default":
                if not visited.__contains__(next_point):
                    queue.append(next_point)
    result = ""
    for point in visited:
        result += point.Color + " "
    return visited


def move_animation(ball, end_x, end_y):
    while ball.X != end_x or ball.Y != end_y:
        pass


def get_position(x, y):
    return int((x - 195)/44), int((y - 18)/41)


def draw_balls(field):
    for ball in field.Balls:
        screen.blit(ball.Image, (197 + ball.X * 44, 19 + ball.Y * 41))


main()
