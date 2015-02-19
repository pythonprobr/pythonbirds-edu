# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import math

DESTROYED = 'Destroyed'
ACTIVE = 'Active'


class Actor():
    _active_character = 'A'
    _destroyed_character = ' '

    def __init__(self, x=0, y=0):
        self.y = y
        self.x = x
        self._collision_time = None

    def character(self, time):
        return self._active_character if self.status(time) == ACTIVE else self._destroyed_character

    def reset(self):
        self._collision_time = None

    def status(self, tempo):
        if self._collision_time is None or self._collision_time > tempo:
            return ACTIVE
        return DESTROYED

    def calculate_position(self, time):
        return self.round_position()

    def round_position(self):
        self.x, self.y = round(self.x), round(self.y)
        return self.x, self.y

    def clash(self, another_actor, time, interval=1):
        if self.status(time) == DESTROYED or another_actor.status(time) == DESTROYED:
            return
        x1, y1 = self.round_position()
        x2, y2 = another_actor.round_position()

        if x1 - interval <= x2 <= x1 + interval and y1 - interval <= y2 <= y1 + interval:
            self._collision_time = time
            another_actor._tempo_de_colisao = time


class Obstacle(Actor):
    _active_character = 'O'


class Pig(Actor):
    _active_character = '@'
    _destroyed_character = '+'


GRAVITY = 10  # m/s^2


class Bird(Actor):
    velocity = None

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self._x_initial = x
        self._y_initial = y
        self._launch_time = None
        self._launch_angle = None  # radians

    def reset(self):
        super().reset()
        self._launch_time = None
        self._launch_angle = None


    def was_launched(self):
        return self._launch_time is not None

    def ground_clash(self, time):
        if self.y <= 0:
            self._collision_time = time

    def _calculate_horizontal_position(self, delta_t):
        self.x = self._x_initial + self.velocity * delta_t * math.cos(self._launch_angle)

    def _calculate_vertical_position(self, delta_t):
        self.y = (self._y_initial +
                  self.velocity * delta_t * math.sin(self._launch_angle) -
                  (GRAVITY / 2) * delta_t ** 2)

    def _calculate_position(self, time):
        delta_t = time - self._launch_time
        self._calculate_vertical_position(delta_t)
        self._calculate_horizontal_position(delta_t)

    def calculate_position(self, time):
        if self._waiting_launch(time):
            self.x = self._x_initial
            self.y = self._y_initial
        elif self._has_collided(time):
            self._calculate_position(self._collision_time)
        else:
            self._calculate_position(time)
        return self.round_position()

    def launch(self, angulo, tempo):
        self._launch_time = tempo
        self._launch_angle = math.radians(angulo)

    def _waiting_launch(self, tempo):
        return not self.was_launched() or tempo < self._launch_time

    def _has_collided(self, tempo):
        return self.was_launched() and self.status(tempo) == DESTROYED


class YellowBird(Bird):
    velocity = 30  # m/s
    _active_character = 'A'
    _destroyed_character = 'a'


class RedBird(Bird):
    velocity = 20  # m/s
    _active_character = 'V'
    _destroyed_character = 'v'
