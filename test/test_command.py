""" Tests for the command class. """
try:
    from unittest.mock import Mock, PropertyMock, patch
except ImportError:
    from mock import Mock, PropertyMock, patch

import sure

from .fixtures import *

from metapipe.parser import Parser
from metapipe.models import *


def test_eval_1():
    parser = Parser(overall)

    cmds = parser.consume()
    cmds[0].eval()[0].eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/python somescript.py -i '
        'somefile.1 somefile.2 somefile.3 -o mp.1.1.output '
        '-fgh somefile.txt')


def test_eval_2():
    parser = Parser(overall)
    cmds = parser.consume()

    cmds[0].eval()[1].eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/python somescript.py -i '
        'somefile.4 somefile.5 somefile.6 -o mp.1.2.output '
        '-fgh somefile.txt')


def test_eval_3():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:1]:
        old_commands.extend(cmd.eval())

    cmd = cmds[1].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/bash somescript.sh -i mp.1.1.output'
        ' -o mp.2.1.output -fgh somefile.txt')


def test_eval_4():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:1]:
        old_commands.extend(cmd.eval())

    cmd = cmds[1].eval()[1]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/bash somescript.sh -i mp.1.2.output'
        ' -o mp.2.2.output -fgh somefile.txt')


def test_eval_5():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:2]:
        old_commands.extend(cmd.eval())

    cmd = cmds[2].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/ruby somescript.rb -i mp.2.1.output'
        ' >> somefile')


def test_eval_6():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:2]:
        old_commands.extend(cmd.eval())

    cmd = cmds[2].eval()[1]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/ruby somescript.rb -i mp.2.2.output'
        ' >> somefile')


def test_eval_7():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:2]:
        old_commands.extend(cmd.eval())

    cmd = cmds[2].eval()[2]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n/usr/bin/ruby somescript.rb -i '
        'mp.1.1.output mp.1.2.output >> somefile')


def test_eval_8():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:3]:
        old_commands.extend(cmd.eval())

    cmd = cmds[3].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        'cut -f *.counts > something.file')


def test_eval_9():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:4]:
        old_commands.extend(cmd.eval())

    cmd = cmds[4].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        'paste *.counts > some.file # some.file')


def test_eval_10():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:5]:
        old_commands.extend(cmd.eval())

    cmd = cmds[5].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        './somescript somefile.1 somefile.2 '
        'somefile.3 somefile.4')


def test_eval_11():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:5]:
        old_commands.extend(cmd.eval())

    cmd = cmds[5].eval()[1]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        './somescript somefile.1.counts somefile.2.counts '
        'somefile.3.counts somefile.4.counts')


def test_eval_12():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:6]:
        old_commands.extend(cmd.eval())

    cmd = cmds[6].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/ruby somescript.rb -i somefile.1.counts')


def test_eval_13():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:6]:
        old_commands.extend(cmd.eval())

    cmd = cmds[6].eval()[1]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/ruby somescript.rb -i somefile.2.counts')


def test_eval_14():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:6]:
        old_commands.extend(cmd.eval())

    cmd = cmds[6].eval()[2]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/ruby somescript.rb -i somefile.3.counts')


def test_eval_14():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:6]:
        old_commands.extend(cmd.eval())

    cmd = cmds[6].eval()[3]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/ruby somescript.rb -i somefile.4.counts')


def test_eval_15():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:7]:
        old_commands.extend(cmd.eval())

    cmd = cmds[7].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        '/usr/bin/python somescript.py -i somefile.1.counts'
        ' somefile.2.counts somefile.3.counts somefile.4.counts # *.bam')


def test_eval_16():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:8]:
        old_commands.extend(cmd.eval())

    cmd = cmds[8].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('#PBS_O_WORKDIR=~/someuser\nset -e;'
        '\nmodule load python\n# do something\n'
        'cat somefile.1.bam somefile.2.bam somefile.bam')


def test_eval_16_deps():
    parser = Parser(overall)
    cmds = parser.consume()
    old_commands = []
    for cmd in cmds[0:8]:
        old_commands.extend(cmd.eval())

    cmd = cmds[8].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.depends_on.should.have.length_of(1)


def test_eval_multiple_inputs():
    parser = Parser(multiple_inputs)
    cmds = parser.consume()
    old_commands = []

    cmd = cmds[0].eval()[0]
    print(cmd)
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('bash somescript somefile.1 --conf somefile.4 > '
        'mp.1.1.output')


def test_multiple_outputs1():
    parser = Parser(multiple_outputs)
    cmds = parser.consume()
    old_commands = []

    cmd = cmds[0].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('bash somescript somefile.1 --log'
        ' mp.1.1-1.output -r mp.1.1-2.output')


def test_multiple_outputs2():
    parser = Parser(multiple_outputs)
    cmds = parser.consume()
    old_commands = []

    cmd = cmds[1].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('python somescript.py somefile.4 somefile.5 '
        'somefile.6 --log mp.2.1-1.output -r mp.2.1-2.output '
        '--output mp.2.1-3.output')


def test_another_sample_pipeline():
    parser = Parser(another_sample)

    cmds = parser.consume()

    old_commands = []

    cmd = cmds[0].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('# Trimmomatic\n'
        'java -jar Trimmomatic-0.35/trimmomatic-0.35.jar '
        'PE somefile.1 somefile.2 mp.1.1-1.output mp.1.1-2.output '
        'mp.1.1-3.output mp.1.1-4.output '
        'ILLUMINACLIP:Trimmomatic-0.35/adapters/TruSeq3-PE.fa:2:30:10:2:true '
        'LEADING:3 TRAILING:3')


def test_another_sample_pipeline_1():
    parser = Parser(another_sample)

    cmds = parser.consume()

    old_commands = []
    for cmd in cmds[0:1]:
        old_commands.extend(cmd.eval())

    cmd = cmds[1].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('# Unzip the outputs from trimmomatic\n'
        'gzip --stdout -d mp.1.1-1.output > '
        'mp.2.1.output')


def test_another_sample_pipeline_1_deps():
    parser = Parser(another_sample)

    cmds = parser.consume()

    old_commands = []
    for cmd in cmds[0:1]:
        old_commands.extend(cmd.eval())

    cmd = cmds[1].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.depends_on.should.have.length_of(1)
    cmd.depends_on[0].should.equal('1.1')


def test_another_sample_pipeline_2():
    parser = Parser(another_sample)

    cmds = parser.consume()

    old_commands = []
    for cmd in cmds[0:2]:
        old_commands.extend(cmd.eval())

    cmd = cmds[2].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('# Cutadapt\n# cutadapt needs unzipped fastq '
        'files\n~/.local/bin/cutadapt --cut 7 -o '
        'mp.3.1.output mp.2.1.output')


def test_another_sample_pipeline_2():
    parser = Parser(another_sample)

    cmds = parser.consume()

    old_commands = []
    for cmd in cmds[0:2]:
        old_commands.extend(cmd.eval())

    cmd = cmds[2].eval()[1]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('# Cutadapt\n# cutadapt needs unzipped fastq '
        'files\n~/.local/bin/cutadapt --cut 7 -o '
        'mp.3.2.output mp.2.2.output')


def test_long_running_1():
    parser = Parser(long_running)

    old_commands = []

    templates = parser.consume()

    cmd = templates[0].eval()[0]
    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('cat somefile.1 > mp.1.1.output && sleep 1')


def test_long_running_2():
    parser = Parser(long_running)

    templates = parser.consume()

    old_commands = []

    for cmd in templates[0:1]:
        old_commands.extend(cmd.eval())
    cmd = templates[1].eval()[0]

    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('cat mp.1.1.output && '
        'sleep 1')


def test_full_output_file_name():
    parser = Parser(full_output_file_name)

    templates = parser.consume()

    old_commands = []

    cmd = templates[0].eval()[0]

    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('gzip --stdout somefile.1 > mp.1.1.output.gz')


def test_full_output_file_name_2():
    parser = Parser(full_output_file_name)

    templates = parser.consume()

    old_commands = []

    for cmd in templates[0:1]:
        old_commands.extend(cmd.eval())
    cmd = templates[1].eval()[0]

    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('cat mp.1.1.output.gz > mp.2.1.output.gz')


def test_magical_glob():
    parser = Parser(magical_glob)
    templates = parser.consume()
    old_commands = []

    for cmd in templates[0:1]:
        old_commands.extend(cmd.eval())

    with patch('metapipe.models.Input.files', new_callable=PropertyMock) as mock_files:
        mock_files.return_value = ['mp.1.1.output', 'mp.1.2.output']
        cmd = templates[1].eval()[0]

        cmd.update_dependent_files(old_commands)
        cmd.eval().should.equal('cat mp.1.1.output mp.1.2.output > mp.2.1.output')


def test_magical_glob2():
    parser = Parser(magical_glob2)
    templates = parser.consume()
    old_commands = []

    for cmd in templates[0:1]:
        old_commands.extend(cmd.eval())

    with patch('metapipe.models.Input.files', new_callable=PropertyMock) as mock_files:
        mock_files.return_value = ['mp.1.1.output', 'mp.1.2.output']
        cmd = templates[1].eval()[0]

    cmd.update_dependent_files(old_commands)
    cmd.eval().should.equal('cat mp.1.1.output > mp.2.1.output')
