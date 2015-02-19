# -*- coding: utf-8 -*-
from itertools import chain
from actors import ACTIVE

# Status possíveis do jogo

VICTORY = 'VICTORY'
DEFEAT = 'DEFEAT'
ON_GOING = 'ON_GOING'


class Point():
    def __init__(self, x, y, character):
        self.character = character
        self.x = round(x)
        self.y = round(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.character == other.character

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self, *args, **kwargs):
        return "Point(%s,%s,'%s')" % (self.x, self.y, self.character)


class Phase():
    def __init__(self, clash_interval=1):
        """
        Method that initializes a phase.

        :param clash_interval:
        """
        self.clash_interval = clash_interval
        self._birds = []
        self._pigs = []
        self._obstacles = []

    def _add_actors(self, lst, *actors):
        lst.extend(actors)

    def add_obstacles(self, *obstacles):
        """
        Add obstacles to a phase

        :param obstacles:
        """
        self._add_actors(self._obstacles, *obstacles)

    def add_pigs(self, *pigs):
        """
        Add pigs to a phase

        :param pigs:
        """
        self._add_actors(self._pigs, *pigs)

    def add_birds(self, *birds):
        """
        Add birds to a phase

        :param birds:
        """
        self._add_actors(self._birds, *birds)


    def status(self):
        """
        Method that indicates the game's status:

        ON_GOING if game is still running (there is one bird active at least).

        DEFEAT if game is over with defeat (there is one pig active at least and no bird active)

        VICTORY if game is over with victory (there is no active pig)

        :return:
        """
        if not self._is_there_active_pig():
            return VICTORY
        if self._is_there_active_bird():
            return ON_GOING
        return DEFEAT

    def launch(self, angle, time):
        """
        Method that executes launch logic.

        It must pick the first not launched bird from list

        If there is no bird of this kind, nothing must happen

        :param angle: launch angle
        :param time: launch time
        """
        for bird in self._birds:
            if not bird.launched():
                bird.launch(angle, time)
                return


    def calculate_points(self, time):
        """
        Method that convert Actors to Points.

        :param time: game's time
        :return: Point object
        """
        points = [self._calculate_bird_points(p, time) for p in self._birds]
        obstacles_and_pigs = chain(self._obstacles, self._pigs)
        points.extend([self._to_point(actor) for actor in obstacles_and_pigs])
        return points

    def _to_point(self, actor):
        return Point(actor.x, actor.y, actor.character())

    def _calculate_bird_points(self, bird, time):
        bird.calculate_position(time)
        for actor in chain(self._obstacles, self._pigs):
            if ACTIVE == bird.status:
                bird.clash(actor, self.clash_interval)
                bird.ground_clash()
            else:
                break
        return self._to_point(bird)

    def _is_there_active_pig(self):
        return self._check_active_actor(self._pigs)

    def _check_active_actor(self, actors):
        for a in actors:
            if a.status == ACTIVE:
                return True
        return False

    def _is_there_active_bird(self):
        return self._check_active_actor(self._birds)
