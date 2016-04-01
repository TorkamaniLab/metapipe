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
    q = BaseQueue()
    str(q).should.equal('<Queue: jobs=0>')

def test_on_end():
    """ Ticks the queue when it's empty. """
    q = BaseQueue()
    tick = q.tick()

def test_progress_1():
    q = ReportingJobQueue()
    q.push(MockJob('', None))
    q.progress.should.equal(0)

def test_progress_2():
    q = ReportingJobQueue()
    q.push(MockJob('1.1', None))
    tick = q.tick()
    for _ in range(10):
        next(tick)

    q.push(MockJob('2.2', None))
    for _ in range(6):
        next(tick)

    q.push(MockJob('3.3', None))
    q.push(MockJob('4.4', None))
    for _ in range(4):
        next(tick)
    q.progress.should.equal(50)
