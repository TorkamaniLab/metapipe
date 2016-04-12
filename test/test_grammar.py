""" A test of PyParsing. """

import sure

from metapipe.models.grammar import Grammar

from .fixtures import *


def test_cmd():
    res = Grammar.command.parseString(basic_cmd['text'])
    val = ['python somescript.py -i ', '-o ', '-fgh  somefile.txt']

    for i, c in enumerate(res.command):
        c.should.equal(val[i])

    res._in[0][0][0].should.equal('1')
    res._in[0][0][2].should.equal('2')
    res._in[0][0][4].should.equal('3')
    res._in[0][0][6].should.equal('4')
    res._in[0][0][8].should.equal('5')
    res._in[0][0][10].should.equal('6')
    res._in[1][0][0].should.equal('o')


def test_cmd_output_name():
    res = Grammar.command.parseString(cmd_suggest_output)
    val = ['bash somescript ', '> ']

    for i, c in enumerate(res.command):
        c.should.equal(val[i])

    res._in[1][0][0].should.equal('o.gz')


def test_cmd_magic1():
    res = Grammar.command.parseString(cmd_magic1)
    val = ['python somescript.py ', '> someout']

    for i, c in enumerate(res.command):
        c.should.equal(val[i])

    res._in[0][0][0].should.equal('*.counts')


def test_cmd_magic2():
    res = Grammar.command.parseString(cmd_magic2)
    val = ['python somescript.py ', '> someout']

    for i, c in enumerate(res.command):
        c.should.equal(val[i])
    res._in[0][0][0].should.equal('*.counts')


def test_cmd_compund1():
    res = Grammar.command.parseString(cmd_compound1)
    val = ['./somescript ', ['1', '2', '3', '4'], ['test/files/*.counts'], '<<OR>>']

    for i, c in enumerate(res.command):
        c.should.equal(val[i])
    res._in[0][0][0].should.equal('1')
    res._in[0][0][2].should.equal('2')
    res._in[0][0][4].should.equal('3')
    res._in[0][0][6].should.equal('4')
    res._in[0][0][8].should.equal('test/files/*.counts')


def test_cmd_compund2():
    res = Grammar.command.parseString(cmd_compound2)
    val = ['./somescript ', ['1', '<<AND>>', '2', '<<AND>>', '3', '<<AND>>', '4', '<<OR>>', 'test/files/*.counts', '<<AND>>']]

    for i, c in enumerate(res.command):
        c.should.equal(val[i])
    res._in[0][0][0].should.equal('1')
    res._in[0][0][2].should.equal('2')
    res._in[0][0][4].should.equal('3')
    res._in[0][0][6].should.equal('4')
    res._in[0][0][8].should.equal('test/files/*.counts')


def test_file():
	res = Grammar.file.parseString(file)
	res.alias.should.equal('1')
	res.filename.should.equal('somedir/somefile.ext')


def test_path():
	res = Grammar.path.parseString(path)
	res.alias.should.equal('python')
	res.path.should.equal('/usr/bin/python')


def test_overall():
	res = Grammar.overall.parseString(overall)

	res['COMMANDS'][0][0].should.equal('python')
	res['COMMANDS'][0][1].should.equal(' somescript.py -i {1,2,3||4,5,6} -o {o} -fgh somefile.txt')


def test_full_sample_pipeline():
	res = Grammar.overall.parseString(full_sample_pipeline)

	res['COMMANDS'][0][0].should.equal('#')
	res['COMMANDS'][0][1].should.equal(' Trimmomatic')
	res['COMMANDS'][1][0].should.equal('java')


def test_multiple_inputs():
	res = Grammar.command.parseString(cmd_multiple_inputs)
	res._in.should.have.length_of(3)


def test_multiple_close_inputs():
	res = Grammar.command.parseString(cmd_multiple_close_inputs)
	res._in.should.have.length_of(6)


def test_full_pipeline_1():
	res = Grammar.command.parseString(cmd_using_multiple_out)
	res._in.should.have.length_of(2)


def test_multiple_word_paths():
    res = Grammar.overall.parseString(overall)
    path = Grammar.path.parseString(''.join(res['PATHS'][4]))
    path.path.should.equal('module load cat2; cat2')
