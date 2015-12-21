""" Grammars for various parts of the input file. """

from pyparsing import *


approved_printables = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`|~'

lbrack = Literal('[').suppress()
rbrack = Literal(']').suppress()


class classproperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class Grammar(object):
    """ A container class for the various grammars in the input files. """

    _section = lbrack + Word(alphas) + rbrack
    _line = ~lbrack + Word(printables) + restOfLine

    __command_in = (
        Suppress('{') +
        OneOrMore(
        Group(OneOrMore(
                Combine(
                    Word(nums) +
                    Optional('.' + Word(nums))
                    ) +
                Suppress(Optional(','))
                )) +
            Suppress(Optional('||'))
            ) +
        Suppress('}')
        )

    __command_out = (
        Suppress('{') + 'o' + Suppress('}')
        )

    @classproperty
    @staticmethod
    def overall():
        """ The overall grammer for pulling apart the main input files. """
        return Optional(Grammar.comment) + Dict(ZeroOrMore(Group(
            Grammar._section + ZeroOrMore(Group(Grammar._line)))
            ))

    @classproperty
    @staticmethod
    def comment():
        return '#' + Optional(restOfLine)

    @classproperty
    @staticmethod
    def file():
        """ Grammar for files found in the overall input files.	"""
        return (
                Optional(Word(alphanums).setResultsName('alias') +
                    Suppress(Literal('.'))) + Suppress(White()) +
                Word(approved_printables).setResultsName('filename')
                )

    @classproperty
    @staticmethod
    def path():
        """ Grammar for paths found in the overall input files. """
        return (
                Word(alphanums).setResultsName('alias') +
                Suppress(White()) +
                Word(approved_printables).setResultsName('path')
                )

    @classproperty
    @staticmethod
    def command():
        """ Grammar for commands found in the overall input files. """
        return OneOrMore(
                Word(approved_printables+' ').setResultsName('command',
                    listAllMatches=True) ^
                Grammar.__command_in.setResultsName('_in') ^
                Grammar.__command_out.setResultsName('_out')
                )
