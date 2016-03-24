""" Tests for the StarCluster Job """

import sure
from mock import Mock

from .fixtures import *

from metapipe.models.tokens import *


# Input tokens

def test_eval_cwd():
    """ Tests if the cwd property is conserved. """
    i = Input('1', 'metapipe.1.1.output', cwd='/etc/metapipe')
    i.path.should.equal('/etc/metapipe/metapipe.1.1.output')
