from __future__ import print_function

import sure

from metapipe.template import make_script

from .fixtures import *


def test_make_script():
    script = make_script('/usr/bin/sh', 'metapipe.script')
    script.should.equal("""#! /usr/bin/sh
set -e;

python -c "
import pickle

with open('metapipe.script', 'rb') as f:
    runtime = pickle.load(f)
    runtime.run()
"
""")
