""" Grammars for various parts of the input file. """

from pyparsing import *


approved_printables = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`|~'

lbrack = Literal('[').suppress()
rbrack = Literal(']').suppress()

OR_TOKEN = '<<OR>>'
AND_TOKEN = '<<AND>>'

class classproperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class Grammar(object):
    """ A container class for the various grammars in the input files. """

    _section = lbrack + Word(alphas) + rbrack
    _line = ~lbrack + Word(printables) + restOfLine

    __command = (
        Suppress('{') +
        OneOrMore(
        Group(OneOrMore(
            Combine(
                Word(alphanums+'.*:/_-') +
                Optional('.' + Word(nums))
            ) +
            Optional((
                Suppress(',' + FollowedBy('}')) ^
                Suppress(',')
            ).addParseAction(replaceWith(AND_TOKEN)).setResultsName('_and')) +
            Optional(
                ('||' + FollowedBy('}')).addParseAction(
                    replaceWith(OR_TOKEN)).setResultsName('magic_or') ^                    
                Suppress('||').addParseAction(
                    replaceWith(OR_TOKEN)).setResultsName('_or')
            )
        ))) + 
        Suppress('}')
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
                Word(approved_printables).setResultsName('alias') +
                Suppress(White()) +
                Word(approved_printables).setResultsName('path')
                )

    @classproperty
    @staticmethod
    def command():
        """ Grammar for commands found in the overall input files. """
        return (
            OneOrMore(
                Word(approved_printables+' ').setResultsName('command',
                    listAllMatches=True) ^
                Grammar.__command.setResultsName('_in', 
                    listAllMatches=True)
                )
            )
