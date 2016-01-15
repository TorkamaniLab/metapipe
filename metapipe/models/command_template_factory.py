""" A factory for building individual commands based on the full list
of commands and inputs.

author: Brian Schrader
since: 2016-01-12
"""


from .tokens import Input, Output, PathToken 
from .command import Command
from .command_template import CommandTemplate
from .grammar import OR_TOKEN


def get_command_templates(command_tokens, file_tokens=[], path_tokens=[]):
    """ Given a list of tokens from the grammar, return a 
    list of commands.
    """
    files = get_files(file_tokens)
    paths = get_paths(path_tokens)
    
    templates = _get_command_templates(command_tokens, files, paths)
        
    for command_template in templates:
        command_template.dependencies = _get_prelim_dependencies(
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
    return [input] + get_files(file_tokens)
    
    
def get_paths(path_tokens):
    """ Given a list of parser path tokens, return a list of path objects 
    for them.
    """
    if len(path_tokens) == 0:
        return []
    
    token = path_tokens.pop()
    path = PathToken(token.alias, token.path)
    return [path] + get_paths(path_tokens)
      

# Internal Implementation        

        
def _get_command_templates(command_tokens, files=[], paths=[], count=1):
    """ Reversivly create command templates. """
    if not command_tokens:
        return []
        
    command_token = command_tokens.pop()
    
    if command_token._or:
        and_or = 'or'
    else: 
        and_or = 'and'    
    
    command_token = _remove_extra_ors(command_token)
    
    parts = []
    for part in command_token:
        # Check for file
        try:
            parts.append(_get_file_by_alias(part, files, and_or))
            continue
        except (AttributeError, ValueError):
            pass
            
        # Check for path/string
        for cut in part.split():
            try:
                parts.append(_get_path_by_name(cut, paths))
                continue
            except ValueError:
                pass

            parts.append(cut)
            
    command_template = CommandTemplate(alias=str(count), parts=parts)
    [setattr(p, 'alias', command_template.alias) 
        for p in command_template.output_parts]
    return [command_template] + _get_command_templates(command_tokens,
        files, paths, count+1)
    
    
def _get_prelim_dependencies(command_template, all_templates):
    """ Given a command_template determine which other templates it 
    depends on. This should not be used as the be-all end-all of 
    dependencies and before calling each command, ensure that it's 
    requirements are  met.
    """
    deps = []
    for input in command_template.input_parts:
        if '.' not in input.alias:
            continue
        for template in all_templates:
            for output in template.output_parts:
                if input.fuzzy_match(output) and template not in deps:
                    deps.append(template)
                    break
    return deps
    
    
def _get_file_by_alias(part, files, and_or=''):
    """ Given a command part, find the file it represents. If not found, 
    then returns a new token representing that file. 
    :throws ValueError: if the value is not a command file alias.
    """    
    # Make Output
    if _is_output(part):
        return Output.from_string(part.pop())          
    
    # Search/Make Input
    else:
        inputs = []
        for cut in part.asList():
            input = Input(cut, filename=cut, and_or=and_or)
            for file in files:
                if file.alias == cut:
                    # Override the filename
                    input.filename = file.filename
                    inputs.append(input)
                    break
            else:
                inputs.append(input)
        return inputs

def _get_path_by_name(part, paths):
    """ Given a command part, find the path it represents. 
    :throws ValueError: if no valid file is found.
    """
    for path in paths:
        if path.alias == part:
            return path
    raise ValueError
    
    
def _is_output(part):
    """ Returns whether the given part represents an output variable. """
    if part[0].lower() == 'o':
        return True
    elif part[0][:2].lower() == 'o:':
        return True
    else: 
        return False
   
        
def _remove_extra_ors(command_token):
    """ Given a command token, remove the extraneous '||' from the 
    input files.
    """
    i, inside = 0, False
    while i < len(command_token):
        val = command_token[i]
        if val == OR_TOKEN:
            del command_token[i]
        i += 1
    return command_token
