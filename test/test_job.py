""" Tests making and submitting jobs. """


import unittest, time, sys

sys.path.insert(0, '../')
from job import Job


class JobTest(object):

    def test_new(self):
        job = Job(job_cmd='test.sh', name='Test', log='job.log',
                completion_file='log', completion='Done!')
        job.submit()
        while not job.complete and not job.error:
            time.sleep(2)

if __name__ == '__main__':
    jt = JobTest()
    jt.test_new()

    #suite = unittest.TestLoader().loadTestsFromTestCase(JobTest)
    #unittest.TextTestRunner(verbosity=2).run(suite)
