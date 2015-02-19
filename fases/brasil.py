# -*- coding: utf-8 -*-
from os import path
import sys

project_dir = path.dirname(__file__)
project_dir = path.join('..')
sys.path.append(project_dir)

from actors import YellowBird, RedBird, Obstacle, Pig
from phase import Phase
from graphics_tk import rodar_fase

if __name__ == '__main__':
    fase = Phase(intervalo_de_colisao=10)


    deltax_gambi=80
    # Adicionar Pássaros Amarelos
    for i in range(100):
        fase.add_birds(YellowBird(30, 30))

    # linhas verticais
    for i in range(30, 300, 32):
        fase.add_pigs(Pig(700-deltax_gambi, i))
        fase.add_pigs(Pig(200-deltax_gambi, i))

    # linhas horizontais
    for i in range(240, 680, 32):
        fase.add_pigs(Pig(i-deltax_gambi, 30))
        fase.add_pigs(Pig(i-deltax_gambi, 286))

    x0 = 210-deltax_gambi
    # losango
    meio = 160
    n = 9
    delta_x = 28
    delta_y = 12
    for i in range(1, n):
        fase.add_pigs(Pig(x0 + delta_x * i, meio + delta_y * i))
        fase.add_pigs(Pig(x0 + delta_x * i, meio - delta_y * i))
        fase.add_pigs(Pig(x0 + (n + i - 1) * delta_x, meio + (n - i) * delta_y))
        fase.add_pigs(Pig(x0 + (n + i - 1) * delta_x, meio + (i - n) * delta_y))

    rodar_fase(fase)