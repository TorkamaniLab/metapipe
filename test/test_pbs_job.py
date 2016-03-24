""" Tests for the Torque/PBS Job """

import sure
from mock import Mock

from .fixtures import *

from metapipe.models import pbs_job


def test_qstat_queued():
    j = pbs_job.PBSJob('', None)
    pbs_job.call = Mock(return_value=pbs_job_qstat_queued)

    j.is_queued().should.equal(True)


def test_qstat_running():
    j = pbs_job.PBSJob('', None)
    pbs_job.call = Mock(return_value=pbs_job_qstat_running)

    j.is_running().should.equal(True)


def test_qstat_exception():
    j = pbs_job.PBSJob('', None)
    pbs_job.call = Mock(return_value=('', None))

    j.is_running().should.equal(False)


def test_submit():
    j = pbs_job.PBSJob('', None)
    pbs_job.call = Mock(return_value=pbs_job_qsub)
    j.make = Mock()

    j.submit()
    j.id.should.equal('9974279')
