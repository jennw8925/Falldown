
import gamebox
import pygame
from random import randint

screen_width = 800
screen_height = 600
camera = gamebox.Camera(screen_width, screen_height)

cat = gamebox.from_image(40, 100, 'hello kitty.jpg')
cat.scale_by(0.045)
cat.speedy = 0

game_over = gamebox.from_text(screen_width/2, screen_height/2, 'Game Over', 60, 'black', bold=True)
background = gamebox.from_image(screen_width / 2, screen_height / 2, 'clouds.webp')
background.scale_by(1.2)
score = 0


# different floors

floors = [[gamebox.from_color(-300, 150, 'light blue', 900, 30), gamebox.from_color(620, 150, 'light blue', 800, 30)],
          [gamebox.from_color(10, 350, 'light blue', 900, 30), gamebox.from_color(930, 350, 'light blue', 800, 30)],
          [gamebox.from_color(-200, 250, 'beige', 900, 30), gamebox.from_color(720, 250, 'beige', 800, 30)],
          [gamebox.from_color(-15, 450, 'beige', 900, 30), gamebox.from_color(905, 450, 'beige', 800, 30)],
          [gamebox.from_color(100, 550, 'light blue', 900, 30), gamebox.from_color(1020, 550, 'light blue', 800, 30)],
          [gamebox.from_color(0, 650, 'beige', 900, 30), gamebox.from_color(920, 650, 'beige', 800, 30)],
          [gamebox.from_color(-70, 750, 'light blue', 900, 30), gamebox.from_color(850, 750, 'light blue', 800, 30)]
          ]


def floor_funct():
    global floors
    """
    This function codes for the cat to stand on the floor, makes the floors move up at a constant speed, and
    repeats the floors list when each floor goes out of frame.
    :return: nothing
    """
    for each in floors:  # get the cat to stand on the floor
        random_num = randint(-90, 70)
        for floor in each:
            cat.move_to_stop_overlapping(floor)
            floor.speedy = -1  # makes the floors move up
            floor.move_speed()
            if floor.y < -15:  # once the floor moves out of the camera, reset it to the bottom
                floor.y = 685
                floor.x += random_num


def sides():
    """
    This function prevents the cat from going off to the left, right, or bottom of the screen.
    :return: nothing
    """
    if cat.x < 0:  # if cat goes off to left
        cat.x = 0
    if cat.x > 800:  # if cat goes off to right
        cat.x = 800
    if cat.y > 600:  # if cat goes off bottom of screen
        cat.y = 600

def lose():
    """
    This function codes for ending the game if the cat reaches the top of the screen.
    :return: nothing
    """
    if cat.y < 0:  # if cat reaches top of screen
        gamebox.pause()
        camera.draw(game_over)  # drawing game over


def scoring():
    """
    This function calculates the time passed.
    :return: nothing
    """
    global score
    score += 0.05
    camera.draw(str(int(score)), 36, "black", 30, 590)

def tick(keys):
    """
    This function codes for movement (the cat to move left and right using user input and give it downward acceleration),
    draws different aspects of the game, and displays score.
    :param keys: set of keys on keyboard
    :return: nothing
    """
    global floors

    camera.clear('black')  # allows cat to not leave tracks
    if pygame.K_RIGHT in keys:
        cat.x += 5
    if pygame.K_LEFT in keys:
        cat.x -= 5
    cat.speedy += 5  # allows the cat to fall between cracks at an acceleration
    cat.move_speed()

    sides()
    floor_funct()
    for each in floors:
        for floor in each:
            cat.move_to_stop_overlapping(floor)

# Drawing everything
    camera.draw(background)
    camera.draw(cat)
    for each in floors:
        for floor in each:
            camera.draw(floor)
    lose()
    scoring()
    camera.display()

ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)
