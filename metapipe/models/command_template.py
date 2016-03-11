""" A template for creating commands.

author: Brian Schrader
since: 2016-01-13
"""

import copy, collections

from .tokens import Input, Output, FileToken, PathToken, CommentToken
from .command import Command


class Ticker(object):

    def __init__(self, maxlen, value=0):
        self.maxlen = maxlen
        self.value = value

    def tick(self, n=1):
        self.value += n
        if self.value >= self.maxlen:
            self.value -= self.maxlen


class CommandTemplate(Command):

    def __init__(self, alias, parts=[], dependencies=[]):
        self.alias = alias
        self.parts = parts
        self._dependencies = dependencies

    def __repr__(self):
        return '<CommandTemplate: {}, {} part(s), {} dep(s)>'.format(self.alias,
            len(self.parts), len(self._dependencies))

    @property
    def depends_on(self):
        """ Returns a list of command template aliases that the given command
        template depends on.
        """
        return [dep.alias for dep in self._dependencies]

    @property
    def file_parts(self):
        """ Returns a list of the file tokens in the list of parts. """
        return _search_for_files(self.parts)

    def eval(self):
        """ Returns a list of Command objects that can be evaluated as their
        string values. Each command will track it's preliminary dependencies,
        but these values should not be depended on for running commands.
        """
        max_size = _get_max_size(self.parts)
        parts_list = _grow([[]], max_size-1)

        counter = Ticker(max_size)
        parts = self.parts[:]
        while len(parts) > 0:
            parts_list, counter = _get_parts_list(parts,
                parts_list, counter)

        commands = []
        for i, parts in enumerate(parts_list):
            alias = self._get_alias(i+1)
            new_parts = copy.deepcopy(parts)
            commands.append(Command(alias=alias, parts=new_parts))
        return commands

    def _get_alias(self, index):
        """ Given an index, return the string alias for that command. """
        return '{}.{}'.format(self.alias, index)


def _get_parts_list(to_go, so_far=[[]], ticker=None):
    """ Iterates over to_go, building the list of parts. To provide
    items for the beginning, use so_far.
    """
    try:
        part = to_go.pop(0)
    except IndexError:
        return so_far, ticker

    # Lists of input groups
    if isinstance(part, list) and any(isinstance(e, list) for e in part):
        while len(part) > 0:
            so_far, ticker = _get_parts_list(part, so_far, ticker)
            ticker.tick()
    # Input Group
    elif isinstance(part, list) and any(isinstance(e, Input) for e in part):
        while len(part) > 0:
            so_far, ticker = _get_parts_list(part, so_far, ticker)
    # Magic Inputs
    elif isinstance(part, Input) and part.is_magic:
        inputs = part.eval()
        while len(inputs) > 0:
            so_far, ticker = _get_parts_list(inputs, so_far, ticker)
            ticker.tick()
    # Normal inputs
    elif isinstance(part, Input) and not part.is_magic:
        so_far[ticker.value].append(part)
    # Everything else
    else:
        so_far = _append(so_far, part)

    return so_far, ticker


def _get_max_size(parts, size=1):
    """ Given a list of parts, find the maximum number of commands
    contained in it.
    """
    max_group_size = 0
    for part in parts:
        if isinstance(part, list):
            group_size = 0
            for input_group in part:
                group_size += 1

            if group_size > max_group_size:
                max_group_size = group_size

    magic_size = _get_magic_size(parts)
    return max_group_size * magic_size


def _get_magic_size(parts, size=1):
    for part in parts:
        if isinstance(part, Input) and part.is_magic:
            magic_size = len(part.eval())
            if magic_size > size:
                return magic_size
        elif isinstance(part, list):
            size = _get_magic_size(part, size)
    return size


def _append(so_far, item):
    """ Appends an item to all items in a list of lists. """
    for sub_list in so_far:
        sub_list.append(item)
    return so_far


def _grow(list_of_lists, num_new):
    """ Given a list of lists, and a number of new lists to add, copy the
    content of the first list into the new ones, and add them to the list
    of lists.
    """
    first = list_of_lists[0]
    for i in range(num_new):
        list_of_lists.append(copy.deepcopy(first))
    return list_of_lists


def _search_for_files(parts):
    """ Given a list of parts, return all of the nested file parts. """
    file_parts = []
    for part in parts:
        if isinstance(part, list):
            file_parts.extend(_search_for_files(part))
        elif isinstance(part, FileToken):
            file_parts.append(part)
    return file_parts


