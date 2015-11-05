""" Tests the lexer. """

import os, sys

sys.path.insert(0, '../metapipe')
from parser import lexer


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


