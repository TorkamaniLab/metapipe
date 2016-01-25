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
}


# New Command Tests


def test_get_new_commands_1():
    parser = Parser(overall)
    cmds = parser.consume()[:1]
    
    pipeline = Runtime(cmds, JOB_TYPES, 'mock')
    new = pipeline._get_new_commands()
    print(new)
    new.should.have.length_of(2)    


def test_get_new_commands_2():
    parser = Parser(overall)
    cmds = parser.consume()[:2]
    
    pipeline = Runtime(cmds, JOB_TYPES, 'mock')
    new = pipeline._get_new_commands()
    print(new)
    new.should.have.length_of(2)    


def test_get_new_commands_3():
    parser = Parser(overall)
    cmds = parser.consume()[:3]
    
    pipeline = Runtime(cmds, JOB_TYPES, 'mock')
    new = pipeline._get_new_commands()
    print(new)
    new.should.have.length_of(2)    


def test_get_new_commands_4():
    parser = Parser(overall)
    cmds = parser.consume()[:4]

    pipeline = Runtime(cmds, JOB_TYPES, 'mock')
    new = pipeline._get_new_commands()
    print(new)
    new.should.have.length_of(3)    


def test_get_new_commands_5():
    parser = Parser(overall)
    cmds = parser.consume()[:5]

    pipeline = Runtime(cmds, JOB_TYPES, 'mock')
    new = pipeline._get_new_commands()
    print(new)
    new.should.have.length_of(4)    


def test_get_new_commands_6():
    parser = Parser(overall)
    cmds = parser.consume()[:6]

    pipeline = Runtime(cmds, JOB_TYPES, 'mock')
    new = pipeline._get_new_commands()
    print(new)
    new.should.have.length_of(6)    


def test_get_new_commands_7():
    parser = Parser(overall)
    cmds = parser.consume()[:7]

    pipeline = Runtime(cmds, JOB_TYPES, 'mock')
    new = pipeline._get_new_commands()
    print(new)
    new.should.have.length_of(10)    


def test_get_new_commands_8():
    parser = Parser(overall)
    cmds = parser.consume()[:8]

    pipeline = Runtime(cmds, JOB_TYPES, 'mock')
    new = pipeline._get_new_commands()
    print(new)
    new.should.have.length_of(11)    


def test_get_new_commands_9():
    parser = Parser(overall)
    cmds = parser.consume()[:9]

    pipeline = Runtime(cmds, JOB_TYPES, 'mock')
    new = pipeline._get_new_commands()
    print(new)
    new.should.have.length_of(11)    


# Run Tests


def test_run_1():
    parser = Parser(overall)
    cmds = parser.consume()[:1]
    
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(1)


def test_run_2():
    parser = Parser(overall)
    cmds = parser.consume()[:2]
    
    print(cmds)
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(2)


def test_run_3():
    parser = Parser(overall)
    cmds = parser.consume()[:3]
    
    print(cmds)
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(3)


def test_run_4():
    parser = Parser(overall)
    cmds = parser.consume()[:4]
    
    print(cmds)
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(3)


def test_run_5():
    parser = Parser(overall)
    cmds = parser.consume()[:5]
    
    print(cmds)
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(3)


def test_run_6():
    parser = Parser(overall)
    cmds = parser.consume()[:6]
    
    print(cmds)
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(3)


def test_run_7():
    parser = Parser(overall)
    cmds = parser.consume()[:7]
    
    print(cmds)
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(3)


def test_run_8():
    parser = Parser(overall)
    cmds = parser.consume()[:8]
    
    print(cmds)
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(3)


def test_run_9():
    parser = Parser(overall)
    cmds = parser.consume()[:9]
    
    print(cmds)
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(3)


def test_run_10():
    parser = Parser(overall)
    cmds = parser.consume()[:10]
    
    print(cmds)
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(3)


def test_run_11():
    parser = Parser(overall)
    cmds = parser.consume()[:11]
    
    print(cmds[-1].parts)
    pipeline = Runtime(cmds, JOB_TYPES, 'mock', sleep_time=0.01)
    iters = pipeline.run()
    iters.should.equal(4)


