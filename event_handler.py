import pygame
import time
from typing import Callable

__any__ = ["tick", "add_event_listener", "remove_event_listener"]

last_call = None
listeners = []


class Listener:
    def __init__(self, eventtype: pygame.event._EventTypes, callback: Callable) -> None:
        self.eventtype = eventtype
        self.callback = callback
    

    def call(self, *args, **kwargs) -> None:
        self.callback(*args, **kwargs)


def tick(fps: float = -1) -> float:
    global last_call
    """
    Tick function, has to be called every game cycle.
    
    :param fps: Prefeered FPS value. If unset or not positive, do not limit it at all.
    :type fps: float
    :return: Returns time left from last call (in milliseconds).
    :rtype: float
    """
    for e in pygame.event.get():
        for l in listeners:
            if e.type == l.eventtype or e.type in l.eventtype:
                l.call(e)
    if fps > 0:
        time.sleep(1 / fps)
    now = time.time() * 1e3
    if last_call is None:
        last_call = now
    dt = now - last_call
    last_call = now
    return dt


def add_event_listener(eventtype: pygame.event._EventTypes, callback: Callable) -> Listener:
    """
    Add listener for any pygame events
    
    :param eventtype: Type of events listen to
    :type eventtype: pygame.event._EventTypes
    :param callback: Callback funtion for this listener
    :type callback: Callable
    :return: A Listener object which is used to delete listener
    :rtype: Listener
    """
    listeners.append(Listener(eventtype, callback))
    return listeners[-1]


def remove_event_listener(listener: Listener) -> None:
    """
    Remove listener so it won't get events anymore
    
    :param listener: Type of events listen to
    :type listener: Listener
    """
    listeners.remove(listener)