# utilidades de sonido sencillas para el juego.

import pygame

from core.utils.paths import asset

_golpe = None
_ambiente = None
_festejo = None


def load_sounds():
    global _golpe, _ambiente, _festejo
    if _golpe is None:
        try:
            _golpe = pygame.mixer.Sound(asset("sfx", "golpe.wav"))
            _golpe.set_volume(0.85)
        except pygame.error:
            _golpe = None

    if _ambiente is None:
        try:
            _ambiente = pygame.mixer.Sound(asset("sfx", "ambiente.mp3"))
            _ambiente.set_volume(0.25)
        except pygame.error:
            _ambiente = None

    if _festejo is None:
        try:
            _festejo = pygame.mixer.Sound(asset("sfx", "festejo.mp3"))
            _festejo.set_volume(0.65)
        except pygame.error:
            _festejo = None


def play_golpe():
    if _golpe is None:
        load_sounds()
    if _golpe:
        _golpe.play()


def play_ambiente(loop=True, restart=True):
    if _ambiente is None:
        load_sounds()
    if _ambiente:
        if restart:
            _ambiente.stop()
        _ambiente.play(loops=-1 if loop else 0)


def stop_ambiente():
    if _ambiente:
        _ambiente.stop()


def play_festejo():
    if _festejo is None:
        load_sounds()
    if _festejo:
        _festejo.play()


def stop_festejo():
    if _festejo:
        _festejo.stop()
