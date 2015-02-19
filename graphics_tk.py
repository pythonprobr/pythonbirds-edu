# coding: utf-8
import time
from tkinter import PhotoImage, NW, Tk, Canvas
from tkinter.constants import ALL
import math
from os import path
import actors

from phase import Phase
from actors import RedBird, YellowBird, Pig, Obstacle

SCREEN_HEIGHT = 600  # px

root = Tk()

IMAGES_PATH = path.dirname(__file__)
IMAGES_PATH = path.join(IMAGES_PATH, 'images')
RED_BIRD = PhotoImage(file=path.join(IMAGES_PATH, "red_bird.gif"))
YELLOW_BIRD = PhotoImage(file=path.join(IMAGES_PATH, "yellow_bird.gif"))
PIG = PhotoImage(file=path.join(IMAGES_PATH, "pig.gif"))
DEAD_PIG = PhotoImage(file=path.join(IMAGES_PATH, "dead_pig.gif"))
OBSTACLE = PhotoImage(file=path.join(IMAGES_PATH, "obstacle.gif"))
TRANSPARENT = PhotoImage(file=path.join(IMAGES_PATH, "transparent.gif"))
BACKGROUND = PhotoImage(file=path.join(IMAGES_PATH, "background.gif"))
PYTHONBIRDS_LOGO = PhotoImage(file=path.join(IMAGES_PATH, "python-birds-logo.gif"))
MENU = PhotoImage(file=path.join(IMAGES_PATH, "menu.gif"))
YOU_WIN = PhotoImage(file=path.join(IMAGES_PATH, "python-birds-you-win-popup.gif"))
YOU_LOSE = PhotoImage(file=path.join(IMAGES_PATH, "python-birds-you-lose-popup.gif"))

CHARACTER_DCT = {'V': RED_BIRD,
                 'A': YELLOW_BIRD,
                 '@': PIG,
                 'O': OBSTACLE,
                 '+': DEAD_PIG,
                 ' ': TRANSPARENT}


def plotar(actors_layer, point):
    if point.character != ' ':
        x = point.x
        y = SCREEN_HEIGHT - point.y - 120  # adjust to put ground same as background
        image = CHARACTER_DCT.get(point.character, TRANSPARENT)
        actors_layer.create_image((x, y), image=image, anchor=NW)


def animate(screen, actors_layer, phase, step=0.01, delta_t=0.01):
    time = 0
    step = int(1000 * step)
    angle = 0
    rewind_multiplier = 20

    def _animate():
        nonlocal time
        nonlocal delta_t
        nonlocal angle
        time += delta_t
        if time <= 0:
            time = 0
            delta_t /= -rewind_multiplier
        if phase.is_over(time):
            actors_layer.create_image(162, 55, image=PYTHONBIRDS_LOGO, anchor=NW)
            actors_layer.create_image(54, 540, image=MENU, anchor=NW)
            if 'Win' in phase.status(time):
                img = YOU_WIN
            else:
                img = YOU_LOSE
            actors_layer.create_image(192, 211, image=img, anchor=NW)
        else:
            actors_layer.delete(ALL)
            actors_layer.create_image((0, 0), image=BACKGROUND, anchor=NW)
            arrow_size = 60
            angle_rad = math.radians(-angle)

            actors_layer.create_line(52, 493, 52 + arrow_size * math.cos(angle_rad),
                                     493 + arrow_size * math.sin(angle_rad), width=1.5)
            actors_layer.create_text(35, 493, text=u"%d°" % angle)
            for point in phase.calculate_points(time):
                plotar(actors_layer, point)
            screen.after(step, _animate)

    def _listen_launch_command(event):
        nonlocal angle
        if event.keysym == 'Up':
            angle += 1
        elif event.keysym == 'Down':
            angle -= 1
        elif event.keysym == 'Return' or event.keysym == 'space':
            phase.launch(angle, time)

    def _replay(event):
        nonlocal time
        nonlocal delta_t
        if phase.is_over(time):
            delta_t *= -rewind_multiplier
            _animate()


    def _play_again(event):
        nonlocal time
        nonlocal delta_t
        if phase.is_over(time):
            time = delta_t
            phase.reset()
            _animate()

    def _finalize(event):
        root.destroy()

    actors_layer.pack()
    _animate()
    screen.bind_all('<KeyPress>', _listen_launch_command)
    screen.bind_all('1', _replay)
    screen.bind_all('2', _play_again)
    screen.bind_all('3', _finalize)
    screen.bind_all('<Escape>', _finalize)

    screen.mainloop()
    screen.after(step, _animate)


def play(phase):
    root.title("Python Birds")
    root.geometry("800x600")
    root.resizable(0, 0)
    stage = Canvas(root, width=800, height=SCREEN_HEIGHT)

    multiplier = 10
    YellowBird.velocity *= multiplier
    RedBird.velocity *= multiplier
    actors.GRAVITY = 100
    animate(root, stage, phase)


if __name__ == '__main__':
    fase = Phase(collision_interval=32)
    birds = [RedBird(30, 30), YellowBird(30, 30), YellowBird(30, 30)]
    pigs = [Pig(750, 1), Pig(700, 1)]
    obstacles = [Obstacle(310, 100)]

    fase.add_obstacle(*obstacles)
    fase.add_bird(*birds)
    fase.add_pig(*pigs)
    play(fase)
