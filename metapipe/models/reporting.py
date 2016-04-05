""" A series of mixins for reporting. """
from datetime import datetime as dt

from metapipe.templates import env
template = env.get_template('progress-report.tmpl.html')


class BaseReportingMixin(object):
    """ An abstract mixin for reporting. """

    message_format = '%Y-%m-%d %H:%M:%S'

    def render(self, message, progress):
        """ Render the output of the report. """
        pass


class HtmlReportingMixin(BaseReportingMixin):
    """ A reporting mixin that writes progress to an HTML report. """

    messages = []
    output = 'metapipe.report.html'

    def render(self, message, progress):
        msg = Message(dt.strftime(dt.now(), self.message_format), message)
        self.messages.insert(0, msg)
        with open(self.output, 'w') as f:
            f.write(self.template.render(
                name=self.name,
                messages=self.messages, progress=progress, jobs=sorted(self.real_jobs)))


class TextReportingMixin(BaseReportingMixin):
    """ A reporting mixin that prints any progress to the console. """

    def render(self, message, progress):
        print('[{}%] {} {}'.format(progress, dt.strftime(dt.now(),
            self.message_format), message))


class Message(object):
    def __init__(self, time, text):
        self.time = time
        self.text = text
