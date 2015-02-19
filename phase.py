# -*- coding: utf-8 -*-
from itertools import chain
from actors import ACTIVE


class Ponto():
    def __init__(self, x, y, character):
        self.character = character
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.character == other.character

    def __repr__(self, *args, **kwargs):
        return "Ponto(%s, %s,'%s')" % (self.x, self.y, self.character)


class Phase():
    def __init__(self, collision_interval=1):
        self.collision_interval = collision_interval
        self._birds = []
        self._pigs = []
        self._obstacles = []

    def _add_actor(self, lst, *actors):
        lst.extend(actors)

    def add_obstacle(self, *obstacles):
        self._add_actor(self._obstacles, *obstacles)

    def add_pig(self, *pigs):
        self._add_actor(self._pigs, *pigs)

    def add_bird(self, *birds):
        self._add_actor(self._birds, *birds)

    def is_over(self, time):
        return not self._is_there_active_pig(time) or not self._is_there_active_birds(time)

    def status(self, time):
        if not self._is_there_active_pig(time):
            return 'Game Over. You Win!'
        if self._is_there_active_birds(time):
            return 'Game on going.'
        return 'Game Over. You lost!'

    def launch(self, angle, time):
        for passaro in self._birds:
            if not passaro.was_launched():
                passaro.launch(angle, time)
                return

    def resetar(self):
        for ator in chain(self._birds, self._obstacles, self._pigs):
            ator.reset()

    def calculate_points(self, time):
        points = [self._calculate_bird_point(p, time) for p in self._birds]
        obstacles_and_pigs = chain(self._obstacles, self._pigs)
        points.extend([self._to_point(actor, time) for actor in obstacles_and_pigs])
        return points

    def _to_point(self, actor, time):
        return Ponto(actor.x, actor.y, actor.character(time))

    def _calculate_bird_point(self, bird, time):
        bird.calculate_position(time)
        for actor in chain(self._obstacles, self._pigs):
            if ACTIVE == bird.status(time):
                bird.clash(actor, time, self.collision_interval)
                bird.ground_clash(time)
            else:
                break
        return self._to_point(bird, time)

    def _is_there_active_pig(self, time):
        return self._is_there_active_actor(self._pigs, time)

    def _is_there_active_actor(self, actors, time):
        for a in actors:
            if a.status(time) == ACTIVE:
                return True
        return False

    def _is_there_active_birds(self, time):
        return self._is_there_active_actor(self._birds, time)
