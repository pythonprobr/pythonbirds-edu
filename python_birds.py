# -*- coding: utf-8 -*-
from actors import RedBird, YellowBird, Pig, Obstacle
from phase import Phase
import placa_grafica

fase_exemplo = Phase()
passaros = [RedBird(3, 3), YellowBird(3, 3), YellowBird(3, 3)]
porcos = [Pig(78, 1), Pig(70, 1)]
obstaculos = [Obstacle(31, 10)]

fase_exemplo.add_birds(*passaros)
fase_exemplo.add_pigs(*porcos)
fase_exemplo.add_obstacles(*obstaculos)

# Solução para ganhar
# fase_exemplo.lancar(45, 1)
# fase_exemplo.lancar(63, 3)
# fase_exemplo.lancar(23, 4)

if __name__ == '__main__':
    placa_grafica.animar(fase_exemplo)
