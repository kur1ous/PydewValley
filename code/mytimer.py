from settings import *
import pygame
import sys

class Timer:
    def __init__(self, duration, callback = None):
        self.duration = duration
        self.callback = callback
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
                if self.callback: #if call back exists, run it
                    self.callback()
                self.deactivate()

            # print("deactivated")


