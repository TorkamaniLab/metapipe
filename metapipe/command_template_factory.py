""" A factory for building individual commands based on the full list
of commands and inputs.

author: Brian Schrader
since: 2016-01-12
"""

try:
    from metapipe.models import Command, Input, Output, Path 
except ImportError:
    from models import Command, Input, Output, Path


class CommandTemplateFactory(object):

    def get_command_templates(command_tokens, file_tokens=[], path_tokens=[]):
        """ Given a list of tokens from the grammar, return a 
        list of commands.
        """
        files = self.get_files(file_tokens)
        paths = self.get_paths(path_tokens)
        
        templates = reverse(self._get_command_templates(command_tokens, 
            files, paths))
            
        for command_template in templates:
            command_template.dependencies = self._get_prelim_dependencies(
                command_template, templates)
        return templates
        
    def get_files(file_tokens):
        """ Given a list of parser file tokens, return a list of input objects 
        for them.
        """
        if not file_tokens:
            return []
        
        token = file_tokens.pop()
        try: 
            filename = token.filename
        except AttributeError:
            filename = ''
                                
        input = Input(token.alias, filename)
        return get_files(file_tokens).append(input)
        
    def get_paths(path_tokens):
        """ Given a list of parser path tokens, return a list of path objects 
        for them.
        """
        if not path_tokens:
            return []
        
        token = path_tokens.pop()
        path = Path(token.alias, token.path)
        return get_paths(path_tokens).append(path)
            
    def _get_command_templates(command_tokens, files=[], paths=[], count=1)
        if not command_tokens:
            return []
            
        command_token = command_tokens.pop()
        
        parts = []
        for part in command_token:
            try:
                parts.append(self._get_file_by_alias(part, files))
                continue
            except AttributeError, ValueError:
                pass
            
            try:
                parts.append(self._get_path_by_name(part, paths))
                continue
            except ValueError:
                pass
            
            parts.append(part)
                
        command_template = CommandTemplate(alias=count, parts=parts)
        return self._get_command_templates(command_tokens,
            files, paths, count+1).append(command_template)
        
    def _get_prelim_dependencies(command_template, all_templates):
        """ Given a command_template determine which other templates it 
        depends on. This should not be used as the be-all end-all of 
        dependencies and before calling each command, ensure that it's 
        requirements are  met.
        """
        deps = {}
        for template in all_templates:
            for part in template:
                if part in command_template.file_parts:
                    deps.add(template)
        return deps
        
    def _get_file_by_alias(part, files):
        """ Given a command part, find the file it represents. If not found, 
        then returns a new token representing that file. 
        :throws AttributeError: if the value is not a command file alias.
        """
        for file in files:
            if file.alias == part:
                return path
        if self._is_output(part):
            return Output.from_string(part)          
        else:
            return Input(part)
        
    def _get_path_by_name(part, paths):
        """ Given a command part, find the path it represents. 
        :throws ValueError: if no valid file is found.
        """
        for path in paths:
            if path.alias == part:
                return path            
        raise ValueError
