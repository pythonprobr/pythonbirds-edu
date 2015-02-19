# -*- coding: utf-8 -*-
from itertools import chain

import os
from os import path
from unittest.case import TestCase
import math
import sys

project_dir = path.dirname(__file__)
project_dir = path.join('..')
sys.path.append(project_dir)
from graphics_tk import rodar_fase

project_dir = os.path.join(os.path.dirname(__file__), '..')
project_dir = os.path.normpath(project_dir)
sys.path.append(project_dir)

from actors import Obstacle, Pig, RedBird, YellowBird, DESTROYED, ACTIVE
from phase import Fase, Ponto, EM_ANDAMENTO, VITORIA, DERROTA


class FaseTestes(TestCase):
    def teste_adicionar_obstaculo(self):
        fase = Fase()
        self.assertListEqual([], fase._obstaculos)
        obstaculo = Obstacle()
        fase.adicionar_obstaculo(obstaculo)
        self.assertListEqual([obstaculo], fase._obstaculos)

        obstaculo1, obstaculo2 = Obstacle(), Obstacle()
        fase.adicionar_obstaculo(obstaculo1, obstaculo2)
        self.assertListEqual([obstaculo, obstaculo1, obstaculo2], fase._obstaculos)

    def teste_adicionar_porco(self):
        fase = Fase()
        self.assertListEqual([], fase._porcos)
        porco = Pig()
        fase.adicionar_porco(porco)
        self.assertListEqual([porco], fase._porcos)

        porco1, porco2 = Pig(), Pig()
        fase.adicionar_porco(porco1, porco2)
        self.assertListEqual([porco, porco1, porco2], fase._porcos)

    def teste_adicionar_passaro(self):
        fase = Fase()
        self.assertListEqual([], fase._passaros)
        passaro = RedBird()
        fase.adicionar_passaro(passaro)
        self.assertListEqual([passaro], fase._passaros)

        passaro1, passaro2 = RedBird(), YellowBird()
        fase.adicionar_passaro(passaro1, passaro2)
        self.assertListEqual([passaro, passaro1, passaro2], fase._passaros)


    def teste_acabou_sem_porcos(self):
        fase = Fase()
        self.assertEqual(VITORIA, fase.status())

    def teste_acabou_com_porcos_e_passaros(self):
        fase = Fase()
        porcos = [Pig(1, 1) for i in range(2)]  # criando 2 porcos
        passaros = [YellowBird(1, 1) for i in range(2)]  # criando 2 pássaros
        fase.adicionar_porco(*porcos)
        fase.adicionar_passaro(*passaros)

        self.assertEqual(EM_ANDAMENTO, fase.status())

        # colidindo cada passaro com um porco no tempo 3
        for passaro, porco in zip(passaros, porcos):
            passaro.clash(porco, 3)

        self.assertEqual(VITORIA, fase.status())

        fase.adicionar_obstaculo(Obstacle())
        self.assertEqual(VITORIA, fase.status(), 'Obstáculo não interfere no fim do jogo')

        fase.adicionar_porco(Pig())
        self.assertEqual(DERROTA, fase.status(), 'Com Pig ativo e sem pássaro para lançar, o jogo deveria acabar')

        fase.adicionar_passaro(YellowBird())
        self.assertEqual(EM_ANDAMENTO, fase.status(),
                         'Com Pig ativo e com pássaro para lançar, o jogo não deveria acabar')

    def teste_status(self):
        fase = Fase()
        porcos = [Pig(1, 1) for i in range(2)]
        passaros = [YellowBird(1, 1) for i in range(2)]
        fase.adicionar_porco(*porcos)
        fase.adicionar_passaro(*passaros)
        self.assertEqual(EM_ANDAMENTO, fase.status())

        for passaro, porco in zip(passaros, porcos):
            passaro.clash(porco, 3)

        self.assertEqual(VITORIA, fase.status(),
                         'Sem porcos ativos o jogo deveria terminar com vitória')

        fase.adicionar_obstaculo(Obstacle())
        self.assertEqual(VITORIA, fase.status(),
                         'Obstáculo não interfere para definir vitória')

        porco = Pig()
        fase.adicionar_porco(porco)
        self.assertEqual(DERROTA, fase.status(),
                         'Com Pig ativo e sem pássaro para lançar, o jogo deveria acabar em derrota')

        fase.adicionar_passaro(YellowBird())
        self.assertEqual(EM_ANDAMENTO, fase.status(),
                         'Com Pig ativo e com pássaro para lançar, o jogo não deveria acabar')

        porco.clash(porco, 3)
        self.assertEqual(VITORIA, fase.status(),
                         'Sem porco ativo, o jogo deveria acabar com vitória')

    def teste_lancar_passaro_sem_erro_quando_nao_existe_passaro(self):
        passaro_vermelho, passaro_amarelo = RedBird(1, 1), YellowBird(1, 1)
        fase = Fase()
        fase.adicionar_passaro(passaro_vermelho, passaro_amarelo)
        self.assertFalse(passaro_vermelho.launched())
        self.assertFalse(passaro_amarelo.launched())
        fase.launch(90, 1)
        fase.launch(45, 3)
        fase.launch(31, 5)  # testando que lançar passaros depios de todos lançados não causa erro

        self.assertTrue(passaro_vermelho.launched())
        self.assertEqual(math.radians(90), passaro_vermelho._launch_angle)
        self.assertEqual(1, passaro_vermelho._launch_time)

        self.assertTrue(passaro_amarelo.launched())
        self.assertEqual(math.radians(45), passaro_amarelo._launch_angle)
        self.assertEqual(3, passaro_amarelo._launch_time)

    def teste_intervalo_de_colisao_padrão(self):
        '''
        Método que testa se o intervalo de colisão da Fase é repassado aos atores. Padrão de intervalo é 1
        '''
        fase = Fase()
        passaro = YellowBird(1, 1)
        fase.adicionar_passaro(passaro)
        porco = Pig(2, 2)
        fase.adicionar_porco(porco)
        fase.calcular_pontos(0)
        self.assertEqual(DESTROYED, passaro.status)
        self.assertEqual(DESTROYED, porco.status)

    def teste_intervalo_de_colisao_nao_padrao(self):
        '''
        Método que testa se o intervalo de colisão da Fase é repassado aos atores. valor testado: 31
        '''
        fase = Fase(30)
        passaro = YellowBird(1, 1)
        fase.adicionar_passaro(passaro)
        porco = Pig(31, 31)
        fase.adicionar_porco(porco)
        fase.calcular_pontos(0)
        self.assertEqual(DESTROYED, passaro.status)
        self.assertEqual(DESTROYED, porco.status)

    def teste_calcular_pontos(self):
        fase_exemplo = criar_fase_exemplo()
        expected = set([Ponto(3, 3, 'Y'), Ponto(3, 3, 'Y'), Ponto(31, 10, 'O'), Ponto(78, 1, '@'),
                        Ponto(70, 1, '@'), Ponto(3, 3, 'R')])
        self.assertSetEqual(expected, set(fase_exemplo.calcular_pontos(0)))

        fase_exemplo.launch(45, 1)

        # i variando de 1 até 2.9
        for i in range(100, 300, 1):
            fase_exemplo.calcular_pontos(i / 100)

        fase_exemplo.launch(63, 3)

        # i variando de 3 até 3.9
        for i in range(300, 400, 1):
            fase_exemplo.calcular_pontos(i / 100)

        fase_exemplo.launch(23, 4)

        expected = set([Ponto(32, 11, 'r'), Ponto(17, 25, 'Y'), Ponto(3, 3, 'Y'), Ponto(31, 10, ' '), Ponto(78, 1, '@'),
                        Ponto(70, 1, '@')])

        self.assertSetEqual(expected, set(fase_exemplo.calcular_pontos(4)))

        # i variando de 4 até 6.9
        for i in range(400, 700, 1):
            fase_exemplo.calcular_pontos(i / 100)

        expected = set(
            [Ponto(32, 11, 'r'), Ponto(57, 30, 'Y'), Ponto(70, 2, 'y'), Ponto(31, 10, ' '), Ponto(78, 1, '@'),
             Ponto(70, 1, '+')])

        self.assertSetEqual(expected, set(fase_exemplo.calcular_pontos(7)))

        # i variando de 7 até 8.49
        for i in range(700, 849, 1):
            fase_exemplo.calcular_pontos(i / 100)
        print(fase_exemplo.calcular_pontos(8.5))

        expected = set([Ponto(32, 11, 'r'), Ponto(77, 0, 'y'), Ponto(70, 2, 'y'), Ponto(31, 10, ' '), Ponto(78, 1, '+'),
                        Ponto(70, 1, '+')])

        self.assertSetEqual(expected, set(fase_exemplo.calcular_pontos(8.5)))

        self.assertEqual(VITORIA, fase_exemplo.status())


def criar_fase_exemplo(multiplicador=1):
    fase_exemplo = Fase(1 if multiplicador == 1 else 32)
    passaros = [RedBird(3 * multiplicador, 3 * multiplicador),
                YellowBird(3 * multiplicador, 3 * multiplicador),
                YellowBird(3 * multiplicador, 3 * multiplicador)]
    porcos = [Pig(78 * multiplicador, multiplicador), Pig(70 * multiplicador, multiplicador)]
    obstaculos = [Obstacle(31 * multiplicador, 10 * multiplicador)]

    fase_exemplo.adicionar_passaro(*passaros)
    fase_exemplo.adicionar_porco(*porcos)
    fase_exemplo.adicionar_obstaculo(*obstaculos)

    return fase_exemplo


if __name__ == '__main__':
    rodar_fase(criar_fase_exemplo(10))
