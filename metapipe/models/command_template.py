""" A template for creating commands. 

author: Brian Schrader
since: 2016-01-13
"""

from models import FileToken, PathToken


class CommandTemplate(object):
    
    def __init__(alias, parts=[], dependencies=[]):
        self.alias = alias
        self.parts = parts
        self.dependencies = dependencies

    @property
    def file_parts(self):
        """ Returns a list of the file tokens in the list of parts. """
        return [part for part in self.parts:
            if isinstance(FileToken, part)]

    @property
    def path_parts(self):
        """ Returns a list of the path tokens in the list of parts. """
        return [part for part in self.parts:
            if isinstance(PathToken, part)]
    
    def eval(self):
        """ Returns a list of Command objects that can be evaluated as their 
        string values.
        """
        all_parts, max_len = [], 1
        for part in self.parts:
            if part in self.file_parts:
                result = part.eval()
                if isinstance(list, result):
                    max_len = len(result) if len(result) > max_len else max_len
                all_parts.append(result)
            else:
                all_parts.append(part)
        
        commands = []
        for i in range(max_len):
            alias = self._get_alias(i)
            parts = self._get_parts(i, all_parts)
            deps = self._get_dependencies(parts)
            
            commands.append(Command(alias=alias, parts=parts,
                dependencies=deps))
        return commands
    
    def _get_parts(self, index, all_parts):
        """ Given an index, and all of the total parts, return the list of parts 
        for that index.
        """
        parts = []
        for part in all_parts:
            if isinstance(list, part):
                parts.append(part[index])
            else:
                parts.append(part)
        return parts

    def _get_alias(self, index):    
        """ Given an index, return the string alias for that command. """
        return '{}.{}'.format(self.alias, i)
        
    def _get_dependencies(self, parts):
        """ Given a list of parts, return all of the dependencies for those 
        parts. The dependencies are a subset of the global template 
        dependencies.
        """
        return { part for part in parts:
            if part in self.file_parts }
                    
