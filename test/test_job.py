""" Tests for the Job ABC

author: Brian Schrader
since: 2016-01-27
"""

from __future__ import print_function

import sure

from metapipe.models import *

from .fixtures import *


def test_new_job():
    alias, command, depends_on = 'test', Command([], []), []
    job = Job(alias, command, depends_on)
    job.alias.should.equal(alias)
    job.command.should.equal(command)
    job.depends_on.should.equal(depends_on)


