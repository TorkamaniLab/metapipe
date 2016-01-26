from __future__ import print_function

import sure

from metapipe.models import *

from .fixtures import *


def test_cmd():
    alias = 'test'
    cmd = Command('testcmd', ['test', 'command'])
    job = LocalJob(alias, cmd)
    job.cmd.should.equal(['bash', 'metapipe.test.job'])
