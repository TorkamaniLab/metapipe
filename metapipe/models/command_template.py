""" A template for creating commands. 

author: Brian Schrader
since: 2016-01-13
"""

import copy, collections

from .tokens import Input, Output, FileToken, PathToken
from .command import Command


class Ticker(object):
    
    def __init__(self, maxlen, value=0):
        self.maxlen = maxlen
        self.value = value
        
    def tick(self, n=1):
        self.value += n
        if self.value >= self.maxlen:
            self.value -= self.maxlen


class CommandTemplate(object):
    
    def __init__(self, alias, parts=[], dependencies=[]):
        self.alias = alias
        self.parts = parts
        self.dependencies = dependencies
        
    def __repr__(self):
        return '<CommandTemplate: {}, {} part(s), {} dep(s)>'.format(self.alias, 
            len(self.parts), len(self.dependencies))

    @property
    def input_parts(self):
        """ Returns a list of the input tokens in the list of parts. """
        return [part for part in self.file_parts
            if isinstance(part, Input)]
        
    @property
    def output_parts(self):
        """ Returns a list of the output tokens in the list of parts. """
        return [part for part in self.file_parts
            if isinstance(part, Output)]

    @property
    def file_parts(self):
        """ Returns a list of the file tokens in the list of parts. """
        file_parts = []
        for part in self.parts:
            try:
                for sub_part in part:
                    if isinstance(sub_part, FileToken):
                        file_parts.append(sub_part)
            except TypeError:
                if isinstance(part, FileToken):
                    file_parts.append(part)
        return file_parts
        
    @property
    def path_parts(self):
        """ Returns a list of the path tokens in the list of parts. """
        return [part for part in self.parts
            if isinstance(part, PathToken)]
    
    def eval(self):
        """ Returns a list of Command objects that can be evaluated as their 
        string values. Each command will track it's preliminary dependencies, 
        but these values should not be depended on for running commands. 
        """
        max_size = sum(_get_max_size(self.parts))
        parts_list = _grow([[]], max_size-1)

        counter = Ticker(max_size)
        parts = self.parts[:]
        while len(parts) > 0:
            parts_list, counter = _get_parts_list(parts, 
                parts_list, counter)

        commands = []
        for i, parts in enumerate(parts_list):
            alias = self._get_alias(i+1)
            deps = self._get_dependencies(parts)
            parts = copy.deepcopy(parts)
            commands.append(Command(alias=alias, parts=parts,
                dependencies=deps))
        return commands
            
    def _get_alias(self, index):    
        """ Given an index, return the string alias for that command. """
        return '{}.{}'.format(self.alias, index)
        
    def _get_dependencies(self, parts):
        """ Given a list of parts, return all of the dependencies for those 
        parts. The dependencies are a subset of the global template 
        dependencies.
        """
        deps = []
        for part in parts:
            for dep in self.dependencies:
                for dep_file_part in dep.file_parts:
                    if dep_file_part == part:
                        deps.append(part)
        return deps
        
                
def _get_parts_list(to_go, so_far=[[]], ticker=None):
    """ Iterates over to_go, building the list of parts. To provide 
    items for the beginning, use so_far.
    """
    try:
        part = to_go.pop(0)
    except IndexError:
        return so_far, ticker

    # Lists of lists
    if isinstance(part, list) and any(isinstance(e, list) for e in part):
        while len(part) > 0:
            so_far, ticker = _get_parts_list(part, so_far, ticker)
            ticker.tick()
    # Single lists
    elif isinstance(part, list):
        for item in part:
            so_far[ticker.value].append(item)
    # Static inputs
    elif isinstance(part, Input):
        so_far[ticker.value].append(part)
    # Everything else
    else:
        so_far = _append(so_far, part)
        
    return so_far, ticker

                
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
    
    
def _get_max_size(parts):
    """ Given a list of parts, find the maximum number of commands 
    contained in it.
    """
    sizes = []
    print('parts', parts)
    for part in parts:
        if isinstance(part, list):
            # The inputs lists should be the same size, but just in case.
            if len(part) > sum(sizes):
                sizes.append(len(part))
    return sizes
