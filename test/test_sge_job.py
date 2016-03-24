""" Tests for the StarCluster Job """

import sure
from mock import Mock

from .fixtures import *

from metapipe.models import sge_job


def test_qstat_queued():
    j = sge_job.SGEJob('', None)
    sge_job.call = Mock(return_value=sge_job_qstat_queued)

    j.is_queued().should.equal(True)


def test_qstat_running():
    j = sge_job.SGEJob('', None)
    sge_job.call = Mock(return_value=sge_job_qstat_running)

    j.is_running().should.equal(True)


def test_submit():
    j = sge_job.SGEJob('', None)
    sge_job.call = Mock(return_value=sge_job_qsub)
    j.make = Mock()

    j.submit()
    j.id.should.equal('1')
