""" Tests for the lexer and parser. """

import sys, sure

from metapipe import parser, lexer


def test_split_params():
    cmd = 'cut -hf --someflag {1,2,3||1,2||2,3,4}'
    res = parser._split_params(cmd)

    res[0].should.equal(('cut -hf --someflag {in}', ['1','2','3'], []))
    res[1].should.equal(('cut -hf --someflag {in}', ['1','2'], []))
    res[2].should.equal(('cut -hf --someflag {in}', ['2','3','4'], []))


def test_parse_job():
    cmd = 'cut -hf --someflag {1,2,3||1,2||2,3,4}'
    jobs = []
    files = [parser.File('file1', '1', '1'),
            parser.File('file2', '2', '2'),
            parser.File('file3', '3', '3'),
            parser.File('file4', '4', '4')]
    paths=[]

    jobs = parser.parse_job(cmd, jobs, files, paths)

    len(jobs).should.equal(3)
    jobs[0].raw_cmd.should.equal('cut -hf --someflag {in}')

    jobs[1].depends_on.should.contain(jobs[0])
    jobs[2].depends_on.should.contain(jobs[0])
    jobs[2].depends_on.should.contain(jobs[0])
    jobs[2].depends_on.should.contain(jobs[1])


def test_complex_job():
    cmd = 'cut -hf --someflag {1,2,3||1,2}'
    jobs = []
    files = [parser.File('file1', '1', '1'),
            parser.File('file2', '2', '2'),
            parser.File('file3', '3', '3'),
            parser.File('file4', '4', '4'),
            parser.File('file5', '5', '5')]
    paths=[]

    jobs = parser.parse_job(cmd, jobs, files, paths)

    cmd = 'python somescript -f {o:*.counts} {2,4||5}'
    jobs = parser.parse_job(cmd, jobs, files, paths)


    len(jobs).should.equal(4)
    jobs[0].raw_cmd.should.equal('cut -hf --someflag {in}')
    jobs[3].raw_cmd.should.equal('python somescript -f {out} {in}')

    jobs[1].depends_on.should.contain(jobs[0])
    jobs[2].depends_on.should.contain(jobs[0])
    jobs[2].depends_on.should.contain(jobs[1])
    len(jobs[3].depends_on).should.equal(0)


class ParserTest(object):

    def test_lexer(self):
        os.chdir('..')
        test_file_path = os.path.join(os.getcwd(),'docs','syntax.md') 
        test_file_text = open(test_file_path).read()

        return lexer(test_file_text)


if __name__ == '__main__':
    
    pt = ParserTest()
    lt = pt.test_lexer()
    print 'magic',lt.magic
    print 'cmds',lt.cmds
    print 'files',lt.files
    print 'paths',lt.paths
