""" A template for creating commands. 

author: Brian Schrader
since: 2016-01-13
"""

import copy

from .tokens import Input, Output, FileToken, PathToken
from .command import Command


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
        max_size = _get_max_size(self.parts)                                   
        parts_list = _grow([[]], max_size-1)
        counter = 0
        
        parts = self.parts[:]
        while len(parts) > 0:
            parts_list, counter = _get_parts_list(parts, 
                parts_list, counter)
        
        commands = []
        parts_list.reverse()    # Generated backwards.
        for i, parts in enumerate(parts_list):
            parts.reverse()
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
        
                
def _get_parts_list(to_go, so_far=[[]], current=0):
    """ Iterates over to_go, building the list of parts. To provide 
    items for the beginning, use so_far.
    """
    part = to_go.pop()
    
    if isinstance(part, str):
        return _append(so_far, part), current
        
    try:
        part.reverse()
        for sub_part in part:
            result = sub_part.eval()
            if isinstance(result, str):
                so_far[current].append(sub_part)
            else:
                for token in result:
                    so_far[current].append(token)
                    current += 1
        current += 1
        return so_far, current
    except (TypeError, AttributeError):
        return _append(so_far, part), current

                
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
    max_size = 0
    for part in parts:
        if not isinstance(part, list):
            continue
        for item in part:
            result = item.eval()
            if isinstance(result, list):
                max_size += len(item.eval())
            else:
                max_size += 1
                break      
    return max_size
