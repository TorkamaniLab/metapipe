""" Tests for the runtime using a mock job. """

from __future__ import print_function
import collections

import sure

from metapipe.parser import Parser
from metapipe.runtime import Runtime
from metapipe.models import *

from .mocks import MockJob
from .fixtures import *


def test_repr():
    q = Queue()
    str(q).should.equal('<Queue: jobs=0>')

def test_on_end():
    """ Ticks the queue when it's empty. """
    q = Queue()
    tick = q.tick()

def test_progress_1():
    q = JobQueue()
    q.push(MockJob('', None))
    q.progress.should.equal(0)

def test_progress_2():
    q = JobQueue()
    q.push(MockJob('', None))
    tick = q.tick()
    for _ in range(10):
        next(tick)

    q.push(MockJob('', None))
    for _ in range(6):
        next(tick)

    q.push(MockJob('', None))
    q.push(MockJob('', None))
    for _ in range(4):
        next(tick)


    q.progress.should.equal(50)
