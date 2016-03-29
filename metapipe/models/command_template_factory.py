""" A factory for building individual commands based on the full list
of commands and inputs.

author: Brian Schrader
since: 2016-01-12
"""


from .tokens import Input, Output, PathToken, CommentToken
from .command import Command
from .command_template import CommandTemplate
from .grammar import OR_TOKEN, AND_TOKEN


def get_command_templates(command_tokens, file_tokens=[], path_tokens=[],
    job_options=[]):
    """ Given a list of tokens from the grammar, return a
    list of commands.
    """
    files = get_files(file_tokens)
    paths = get_paths(path_tokens)
    job_options = get_options(job_options)

    templates = _get_command_templates(command_tokens, files, paths,
        job_options)

    for command_template in templates:
        command_template._dependencies = _get_prelim_dependencies(
            command_template, templates)
    return templates


def get_files(file_tokens, cwd=None):
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

    if cwd:
        input = Input(token.alias, filename, cwd=cwd)
    else:
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


def get_options(options):
    """ Given a list of options, tokenize them. """
    return _get_comments(options)


# Internal Implementation


def _get_command_templates(command_tokens, files=[], paths=[], job_options=[],
    count=1):
    """ Reversivly create command templates. """
    if not command_tokens:
        return []

    comment_tokens, command_token = command_tokens.pop()
    parts = []

    parts += job_options + _get_comments(comment_tokens)
    for part in command_token[0]:
        # Check for file
        try:
            parts.append(_get_file_by_alias(part, files))
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
        files, paths, job_options, count+1)


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
                if input.fuzzy_match(output):
                    deps.append(template)
                    break
    return list(set(deps))


def _get_file_by_alias(part, files):
    """ Given a command part, find the file it represents. If not found,
    then returns a new token representing that file.
    :throws ValueError: if the value is not a command file alias.
    """
    # Make Output
    if _is_output(part):
        return Output.from_string(part.pop())

    # Search/Make Input
    else:
        inputs = [[]]

        if part.magic_or:
            and_or = 'or'
        else:
            and_or = 'and'

        for cut in part.asList():
            if cut == OR_TOKEN:
                inputs.append([])
                continue
            if cut == AND_TOKEN:
                continue

            input = Input(cut, filename=cut, and_or=and_or)
            for file in files:
                if file.alias == cut:
                    # Override the filename
                    input.filename = file.filename
                    inputs[-1].append(input)
                    break
            else:
                inputs[-1].append(input)


        return [input for input in inputs if input]


def _get_path_by_name(part, paths):
    """ Given a command part, find the path it represents.
    :throws ValueError: if no valid file is found.
    """
    for path in paths:
        if path.alias == part:
            return path
    raise ValueError

def _get_comments(parts):
    """ Given a list of parts representing a list of comments, return the list
    of comment tokens
    """
    return [CommentToken(part) for part in parts]


def _is_output(part):
    """ Returns whether the given part represents an output variable. """
    if part[0].lower() == 'o':
        return True
    elif part[0][:2].lower() == 'o:':
        return True
    elif part[0][:2].lower() == 'o.':
        return True
    else:
        return False

