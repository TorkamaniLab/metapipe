# Extending Metapipe

Metapipe provides 2 extension points for developers to extend it's functionality: custom Queues and custom Job Types. In most cases, custom queues are an advanced feature that most users and developers will not need to worry about, but if you must, it is there.

To add support for a queue system not included with metapipe, all you need to do is add a job type.


## Custom Job types

All job types are subclasses of the `metapipe.models.Job` class. The base job class implements a lot of the functionality that is common between all job types, and has method stubs for the required functionality that needs to be implemented by any subclass. This section will cover what duty job subclasses have, how to subclass the main `Job` and what to fill in.


### The Root Job Class

The code for the main job class can be found [here][job]. To create your own job type, simply subclass this as follows:

```python
from metapipe.models import Job

class MyCustomJob(Job):

    def __repr__(self):
        return '<MyCustomJob: {}>'.format(self.cmd)
```

There are 6 methods you need to fill in to have a complete job class. Your full job subclass should have the following form:

```python 
class MyCustomJob(Job):

    def __repr__(self):
        return '<MyCustomJob: {}>'.format(self.cmd)

    # Override these...

    @property
    def cmd(self):
        """ Returns the command needed to submit the calculations. 
        Normally, this would be just running the command, however if 
        using a queue system, then this should return the command to 
        submit the command to the queue.
        """
        pass

    def submit(self):
        """ Submits the job to be run. If an external queue system is used,
        this method submits itself to that queue. Else it runs the job itself.
        :see: call
        """
        pass
        
    def is_running(self):
        """ Returns whether the job is running or not. """
        pass

    def is_queued(self):
        """ Returns whether the job is queued or not. 
        This function is only used if jobs are submitted to an external queue.
        """
        pass
        
    def is_complete(self):
        """ Returns whether the job is complete or not. """
        pass

    def is_error(self):
        """ Checks to see if the job errored out. """
        pass
```

The duty of the job types is to submit the jobs when asked by the queue, and to inform the queue about the status of jobs. The queue needs to know when a job is running, queued, complete, or when an error has occurred. 

Each of the `is_*` callbacks should return a boolean value, and the cmd property should return the bash command (as an array of strings) that can be called to run the job. The job class has an attribute `filename` that contains the value of the bash script containing the job command (i.e. `['bash', self.filename]`).

**IMPORTANT:** All of the above handlers are required for custom job types to function properly.

Here is the code for the `cmd` property of the `PBSJob` class:

```python
class PBSJob(Job):
    #...
    @property
    def cmd(self):
        return ['qsub', self.filename]
    #...
```

The `submit` call should do any logic pertaining to submitting the job or tracking the number of total submissions. For example, here is the code for submitting a job to the PBS queue:

```python
class PBSJob(Job):
    #...
    def submit(self, job):
        if self.attempts == 0:
            job.make()
        self.attempts += 1
        out = call(job.cmd)
        self.waiting = False
        self.id = out[:out.index('.')]
    #...
```

As you can see, it keeps track of the number of times the job was submitted, and then calls the `call` function, provided in the root job module, to execute the job. Since PBS assigns job ids to each job at submission-time, it also captures that information and saves it for later use.

[job]: https://github.com/TorkamaniLab/metapipe/blob/master/metapipe/models/job.py#L20
 
 
## Custom Queues

In the event that your analysis requires more control over the submission process for jobs, the metapipe module also allows for the customization of queue logic by subclassing `metapipe.models.Queue`. This section will cover how to subclass the root queue, but it is left to the reader to determine why you might want to do this. From personal experience, customizing the queue should be a very rare requirement.


### The Root Queue class

As is the case for custom job types, all queues inherit from the root Queue in `metapipe.models.Queue`, including the main `JobQueue` that is used by the metapipe command line tool.

To customize the response of the queue to various types of events subclass it and fill in the following methods, all the methods are optional so just omit any handlers that you don't need.

```python
class MyCustomQueue(object):
                    
    def __repr__(self):
        return '<MyCustomQueue: jobs=%s>' % len(self.queue)
                        
    # Callbacks...
        
    def on_start(self):
        """ Called when the queue is starting up. """
        pass

    def on_end(self):
        """ Called when the queue is shutting down. """
        pass
    
    def on_locked(self):
        """ Called when the queue is locked and no jobs can proceed. 
        If this callback returns True, then the queue will be restarted,
        else it will be terminated.
        """
        return True
        
    def on_tick(self):
        """ Called when a tick of the queue is complete. """
        pass
    
    def on_ready(self, job):
        """ Called when a job is ready to be submitted. 
        :param job: The given job that is ready.
        """ 
        pass
        
    def on_submit(self, job):
        """ Called when a job has been submitted. 
        :param job: The given job that has been submitted.
        """ 
        pass
        
    def on_complete(self, job):
        """ Called when a job has completed. 
        :param job: The given job that has completed.
        """ 
        pass
        
    def on_error(self, job):
        """ Called when a job has errored. 
        :param job: The given job that has errored.
        """ 
        pass
```
 
 
## Using Your Custom Code

Once you have subclassed and filled in the required code for your custom job type or queue, it is time to use your code. If your code adapts metapipe to work on a common computing platform, or system then please consider contributing to the metapipe project. This helps the rest of the community use a broader range of hardware to solve our problems!


### Building your custom pipeline

Use the following code to build your pipeline. This code is taken directly from [metapipe's app.py][app] tool which is the command line tool that metapipe uses to build pipelines.

```python
import MyCustomJob

JOB_TYPES = {
    'my_custom_job_type': MyCustomJob
}

parser = Parser(config)
try:
    command_templates = parser.consume()
except ValueError as e:
    raise SyntaxError('Invalid config file. \n%s' % e)

pipeline = Runtime(command_templates, JOB_TYPES, 'my_custom_job_type')
```

**IMPORTANT:** Adding custom queues is coming soon!

For more information on how to script metapipe once you have custom jobs, see [Scripting Metapipe](scripting.html)
 
 
