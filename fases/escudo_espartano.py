# -*- coding: utf-8 -*-
from os import path
import sys
import math

project_dir = path.dirname(__file__)
project_dir = path.join('..')
sys.path.append(project_dir)

from actors import YellowBird, RedBird, Obstacle, Pig
from phase import Phase
from graphics_tk import rodar_fase
from random import randint

if __name__ == '__main__':
    fase = Phase(intervalo_de_colisao=32)


    # Adicionar Pássaros Amarelos
    for i in range(80):
        fase.add_birds(YellowBird(30, 30))


    # Obstaculos
    theta = 270
    h = 12
    k = 7
    step = 32
    r = 50

    while theta < 480:
        x = 600 + (h + r * math.cos(theta))
        y = (k + r * math.sin(theta))
        fase.add_obstacles(Obstacle(x, y))
        theta += 32

    # Porcos
    for i in range(30, 300, 32):
        x = randint(590, 631)
        y = randint(0, 21)
        fase.add_pigs(Pig(x, y))

    rodar_fase(fase)