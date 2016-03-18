""" Template scripts for pipelines.

author: Brian Schrader
since: 2015-12-22
"""

_script = """#! {shell}
set -e;

python - <<END
import pickle

with open('{temp}', 'rb') as f:
    runtime = pickle.load(f)
    runtime.run()
END
"""

def make_script(shell='/bin/bash', temp='.metapipe'):
    return _script.format(temp=temp, shell=shell)
