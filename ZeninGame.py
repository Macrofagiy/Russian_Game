import pygame
import random

pygame.init()

display_width = 500
display_height = 500

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Russian Game.')

pygame.mixer_music.load('GST_8bit.mp3')
pygame.mixer_music.set_volume(0.3)

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

prep_img = [pygame.image.load('prep0.png'), pygame.image.load('prep1.png'), pygame.image.load('prep2.png')]

snow1_img = pygame.image.load('snow1.png')
snow2_img = pygame.image.load('snow2.png')

cloud1_img = pygame.image.load('cloud1.png')
cloud2_img = pygame.image.load('cloud2.png')

zen_img = [pygame.image.load('Zenin0.png'), pygame.image.load('Zenin1.png'), pygame.image.load('Zenin2.png'), pygame.image.load('Zenin3.png')]

img_counter = 0

class Prep:
    def __init__(self, x, y, width, height, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            # pygame.draw.rect(display, (225, 0, 0), (self.x, self.y, self.width, self.height))
            self.x -= self.speed
            return  True
        else:
            # self.x = display_width + 100 + random.randrange(-80, +50)
            return False

    def return_self(self, radius, image):
         self.x = radius
         self.image = image
         display.blit(self.image, (self.x, self.y))

class Button:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.ic = (0, 113, 225)
        self.ac = (0, 225, 225)

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x <= mouse[0] <= x + self.w and y <= mouse[1] <= y + self.h:
                pygame.draw.rect(display, self.ac, (x, y, self.w, self.h))
                if click[0] == 1 and action is not None:
                    action()
        else:
            pygame.draw.rect(display, self.ic, (x, y, self.w, self.h))

        print_text(message, x + 25, y + 10)




zen_width = 50
zen_height = 100
zen_x = display_width // 3
zen_y = display_height - zen_height - 100

prep_w = 100
prep_h = 100
prep_x = display_width - 100
prep_y = display_height - prep_h - 50

clock = pygame.time.Clock()

make_jump = False
jump_counter = 35

def sm():
    mb = pygame.image.load('menu.png')

    p_b = Button(100, 50)

    show = True
    while show:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(mb, (0, 0))
        p_b.draw(300, 425, 'PLAY', start_game)

        pygame.display.update()

def start_game():
    while game_c():
        pass


def game_c() :
    global make_jump
    pygame.mixer.music.play(-1)
    game = True
    prep_arr = []
    create_prep_arr(prep_arr)
    land = pygame.image.load('Land.png')

    snow1, snow2, cloud1, cloud2 = oro()

    while game:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True

        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        display.blit(land, (0, 0))

        draw_array(prep_arr)
        movob(snow1, snow2, cloud1, cloud2)

        # pygame.draw.rect(display, (225, 225, 0), (zen_x, zen_y, zen_width, zen_height))
        draw_zen()

        if cc(prep_arr):
            pygame.mixer_music.stop()
            game = False

        pygame.display.update()
        clock.tick(100)
    return game_over()




def jump():
    global zen_y, jump_counter, make_jump
    if jump_counter >= -35:
        zen_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 35
        make_jump = False



def create_prep_arr(array):
    choice = random.randrange(0, 3)
    img = prep_img[choice]
    array.append(Prep(display_width + 50, display_height - 175, 75, 75, img, 3))

    choice = random.randrange(0, 3)
    img = prep_img[choice]
    array.append(Prep(display_width + 300, display_height - 175, 75, 75, img,  3))

    choice = random.randrange(0, 3)
    img = prep_img[choice]
    array.append(Prep(display_width + 550, display_height - 175, 75, 75, img, 3))

def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 100:
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0 :
        radius += random.randrange (200, 350)
    else :
        radius += random.randrange (200, 350)

    return  radius

def draw_array(array):
    for prep in array:
        check = prep.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = prep_img[choice]

            prep.return_self(radius, img)

def oro():

    snow1 = Prep(0, display_height - 100, 500, 100, snow1_img, 3)
    snow2 = Prep(display_width, display_height - 100, 500, 100, snow2_img, 3)
    cloud1 = Prep(0, 0, 500, 200, cloud1_img, 1)
    cloud2 = Prep(display_width, 0, 500, 200, cloud2_img, 1)

    return snow1, snow2, cloud1, cloud2

def movob(snow1, snow2, cloud1, cloud2):
    check = snow1.move()
    if not check:
        snow1.return_self(display_width, snow1_img)

    check = snow2.move()
    if not check:
        snow2.return_self(display_width, snow2_img)

    check = cloud1.move()
    if not check:
        cloud1.return_self(display_width, cloud1_img)

    check = cloud2.move()
    if not check:
        cloud2.return_self(display_width, cloud2_img)

def draw_zen():
    global img_counter
    if img_counter == 32:
        img_counter = 0

    display.blit(zen_img[img_counter // 8], (zen_x, zen_y))
    img_counter += 1

def print_text(message, x, y, font_colour = (0, 0, 0), font_type = 'Px.ttf', font_size = 17 ):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_colour)
    display.blit(text, (x, y))

def print_textb(message, x, y, font_colour = (225, 0, 0), font_type = 'Px.ttf', font_size = 50 ):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_colour)
    display.blit(text, (x, y))

def print_texts(message, x, y, font_colour = (0, 0, 0), font_type = 'Px.ttf', font_size = 15 ):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_colour)
    display.blit(text, (x, y))

def pause():
    paused = True
    pygame.mixer_music.pause()
    while paused:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Пауза. Нажмите ENTER, чтобы продолжить', 30, 50)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()
    pygame.mixer_music.unpause()

def cc(barriers):
    for barrier in barriers:
        if zen_y + zen_height >= barrier.y:
            if barrier.x <= zen_x <= barrier.x + barrier.width:
                return True;
            elif barrier.x <= zen_x + zen_width <= barrier.x + barrier.width:
                return True
    return False

def game_over():
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_textb('Зенинъ умеръ.', 40, 50)
        print_text('Но если нажмете ENTERЪ,', 125, 150)
        print_texts('то онъ приметъ немного на грудь и воскреснетъ ', 20, 175)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False


        pygame.display.update()

sm()


pygame.quit()
quit()