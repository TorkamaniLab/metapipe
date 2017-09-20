""" Tests for the runtime using a mock job. """

from __future__ import print_function

import sure

from metapipe.parser import Parser
from metapipe.runtime import Runtime
from metapipe.models import *

from .mocks import MockJob
from .fixtures import *


JOB_TYPES = {
    'mock': MockJob,
    'local': LocalJob,
}


# New Command Tests


def test_get_new_commands_1():
    parser = Parser(overall)
    cmds = parser.consume()[:1]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock')
    new = pipeline.queue.queue
    new.should.have.length_of(1)


def test_get_new_commands_2():
    parser = Parser(overall)
    cmds = parser.consume()[:2]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock')
    new = pipeline.queue.queue
    new.should.have.length_of(2)


def test_get_new_commands_3():
    parser = Parser(overall)
    cmds = parser.consume()[:3]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock')
    new = pipeline.queue.queue
    new.should.have.length_of(3)


def test_get_new_commands_4():
    parser = Parser(overall)
    cmds = parser.consume()[:4]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock')
    new = pipeline.queue.queue
    new.should.have.length_of(4)


def test_get_new_commands_5():
    parser = Parser(overall)
    cmds = parser.consume()[:5]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock')
    new = pipeline.queue.queue
    new.should.have.length_of(5)


def test_get_new_commands_6():
    parser = Parser(overall)
    cmds = parser.consume()[:6]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock')
    new = pipeline.queue.queue
    new.should.have.length_of(6)


def test_get_new_commands_7():
    parser = Parser(overall)
    cmds = parser.consume()[:7]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock')
    new = pipeline.queue.queue
    new.should.have.length_of(7)


def test_get_new_commands_8():
    parser = Parser(overall)
    cmds = parser.consume()[:8]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock')
    new = pipeline.queue.queue
    new.should.have.length_of(8)


def test_get_new_commands_9():
    parser = Parser(overall)
    cmds = parser.consume()[:9]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock')
    new = pipeline.queue.queue
    new.should.have.length_of(9)


# Run Tests


def test_run_1():
    parser = Parser(overall)
    cmds = parser.consume()[:1]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(8)


def test_run_2():
    parser = Parser(overall)
    cmds = parser.consume()[:2]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(15)


def test_run_3():
    parser = Parser(overall)
    cmds = parser.consume()[:3]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(23)


def test_run_4():
    parser = Parser(overall)
    cmds = parser.consume()[:4]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(23)


def test_run_5():
    parser = Parser(overall)
    cmds = parser.consume()[:5]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(23)


def test_run_6():
    parser = Parser(overall)
    cmds = parser.consume()[:6]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(23)


def test_run_7():
    parser = Parser(overall)
    cmds = parser.consume()[:7]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(24)


def test_run_8():
    parser = Parser(overall)
    cmds = parser.consume()[:8]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(24)


def test_run_9():
    parser = Parser(overall)
    cmds = parser.consume()[:9]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(25)


def test_run_10():
    parser = Parser(overall)
    cmds = parser.consume()[:10]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(25)


def test_run_11():
    parser = Parser(overall)
    cmds = parser.consume()[:11]

    pipeline = Runtime(cmds, ReportingJobQueue, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.be.greater_than(15)


def test_max_concurrent_jobs():
    parser = Parser(concurrent)
    cmds = parser.consume()

    pipeline = Runtime(cmds, ReportingJobQueue, { 'local': MockJob }, 'local', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.be.greater_than(30)
