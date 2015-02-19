# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import math

DESTROYED = 'Destroyed'
ACTIVE = 'Active'
GRAVITY = 10  # m/s^2


class Actor():
    """
    Class representing an actor. He represents a point on screen.
    """
    _active_char = 'A'
    _destroyed_char = ' '

    def __init__(self, x=0, y=0):
        """
        Method used to initialize class. It must initialize x, y and status attributes

        :param x: Initial actor's horizontal position
        :param y: Initial actor's vertical position
        """
        self.y = y
        self.x = x
        self.status = ACTIVE

    def character(self):
        return self._active_char if self.status == ACTIVE else self._destroyed_char

    def calculate_position(self, time):
        """
        Method to calculate position in a given time.
        Time starts in 0 s and advances in 0,01 s

        :param time: game's time
        :return: actor's position x, y
        """
        return self.x, self.y

    def clash(self, another_actor, interval=1):
        """
        Method tha execute clash logic for two actors.
        Clash must happen only if both actor's status are ACTIVE.
        For clash the actor must be considered as a square surrounding the point with "interval" been its side.
        If squares touch themselves, the clash occur and both actor's statuses must be changed do DESTROYED

        :param another_actor: Actor to be considered on clash
        :param interval: clash interval
        :return:
        """
        if self.status == DESTROYED or another_actor.status == DESTROYED:
            return

        if self.x - interval <= another_actor.x <= self.x + interval and self.y - interval <= another_actor.y <= self.y + interval:
            self.status = DESTROYED
            another_actor.status = DESTROYED


class Obstacle(Actor):
    _active_char = 'O'


class Pig(Actor):
    _active_char = '@'
    _destroyed_char = '+'


class Bird(Actor):
    velocity = None

    def __init__(self, x=0, y=0):
        """
        Method to initialize bird.

        It must initialize Actor. Besides that, it must store initial bird position (x_initial and y initial)
        launch_time and angle_time

        :param x:
        :param y:
        """
        super().__init__(x, y)
        self._x_initial = x
        self._y_initial = y
        self._launch_time = None
        self._launch_angle = None  # radians

    def launched(self):
        """
        Must return true if bird is already launched and false other else

        :return: boolean
        """
        return self._launch_time is not None

    def ground_clash(self):
        """
        Execute ground clash logic. Every time y is less or equals than0,
        Bird's status must be changed to destroyed

        """
        if self.y <= 0:
            self.status = DESTROYED

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
        """
        Method that calculates bird position in a given time.

        Before launch, it must return bird initial position

        After launch it must calculate bird's position according to its initial position, velocity, launch_angle,
        GRAVITY, and time of the game.

        After clash, it must retorn the clash position.

        :param time: game's time
        :return: position (tuple) x, y
        """
        if self._launch_time is None:
            return self._x_initial, self._y_initial
        if self.status == ACTIVE:
            self._calculate_position(time)
        return self.x, self.y


    def launch(self, angle, launch_time):
        """
        Bird launch logic. Must store angle and launch time for position calculations.
        Angle is given in degree and must be converted to radians.

        :param angle:
        :param launch_time:
        :return:
        """
        self._launch_time = launch_time
        self._launch_angle = math.radians(angle)

    def _waiting_launch(self, tempo):
        return not self.launched() or tempo < self._launch_time

    def _clashed(self):
        return self.launched() and self.status() == DESTROYED


class YellowBird(Bird):
    velocity = 30  # m/s
    _active_char = 'Y'
    _destroyed_char = 'y'


class RedBird(Bird):
    velocity = 20  # m/s
    _active_char = 'R'
    _destroyed_char = 'r'
