""" Template scripts for pipelines.

author: Brian Schrader
since: 2015-12-22
"""

_script = """#! {shell}
set -e;

{commands}

python -c "
import pickle

with open('{temp}', 'rb') as f:
    queuemanager = pickle.load(f)
    queuemanager.submit_all()
"
"""

def make_script(shell='/bin/bash', temp='.metapipe', commands=''):
    return _script.format(temp=temp, shell=shell, commands='')
