
import unittest, time, sys

sys.path.insert(0, '../')
from job import Job
from queuemanager import Queue

def test_queue():
    queue = Queue(log_dir='/tmp/')
    queue.push(Job(job_cmd='test1.sh', name='Test1', depends_on=[]))
    queue.push(Job(job_cmd='test2.sh', name='Test2', depends_on=['Test1']))
    queue.push(Job(job_cmd='test5.sh', name='Test5',
        depends_on=['Test1', 'Test0']))
    queue.submit_all()


if __name__ == '__main__':
    test_queue()
