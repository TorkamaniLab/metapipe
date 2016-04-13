from __future__ import print_function

import sure

from metapipe.templates import env

from .fixtures import *

template = env.get_template('output_script.tmpl.sh')

def test_make_script():

    script = template.render(shell='/usr/bin/sh', temp='metapipe.script')
    script.should.equal("""#! /usr/bin/sh
set -e;



python - <<END
import pickle

with open('metapipe.script', 'rb') as f:
    runtime = pickle.load(f)
    runtime.run()
END""")
