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

