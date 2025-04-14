from settings import *
import pygame
import sys

class Timer:
    def __init__(self, duration, call_back = None):
        self.duration = duration
        self.call_back = call_back
        self.remaining = 0

        print("test1")


    @property
    def active(self):
        return self.remaining > 0


    def activate(self):

        self.remaining = self.duration

    def deactivate(self):

        self.remaining = 0

    def update(self, dt):
        if self.active:
            self.remaining -= dt
            if self.remaining <= 0:
                self.deactivate()
                print("deactivated")


