title: A Celery-like Python Task Queue in 55 Lines of Code
date: 2014-02-11 10:00
categories: python celery brokest

[Celery](http://docs.celeryproject.org/en/latest/) is probably the best known
task queuing Python package around. It makes asynchronous execution of Python
code both possible and reasonably straightforward. It does, however, come with a
good deal of complexity, and it's not as simple to use as I would like (i.e. for
many use cases it's overkill). So I wrote a distributed Python task queue. In 55
lines of code (caveat: using two awesome libraries).

<!--more-->

## Background

What does a distributed task queue do? It takes code like the following (taken
from the documentation for [RQ](http://python-rq.org/), another Celery alternative):

    #!py
    import requests

    def count_words_in_page(url):
        resp = requests.get(url)
        return len(resp.text.split())

and allows it to be sent to a worker process (possibly on another machine) for
execution. The worker process then sends back the results after the calculation
is complete. In the meantime, the sender doesn't have to block waiting for the
(possibly expensive) calculation to complete. They can just periodically check
if the results are ready.

So what's the absolute simplest way we could do this?
I submit to you, `brokest.py`:

    #!py
    """Broker-less distributed task queue."""
    import pickle

    import zmq
    import cloud

    HOST = '127.0.0.1'
    PORT = 9090
    TASK_SOCKET = zmq.Context().socket(zmq.REQ)
    TASK_SOCKET.connect('tcp://{}:{}'.format(HOST, PORT))

    class Worker(object):
        """A remote task executor."""

        def __init__(self, host=HOST, port=PORT):
            """Initialize worker."""
            self.host = host
            self.port = port
            self._context = zmq.Context()
            self._socket = self._context.socket(zmq.REP)

        def start(self):
            """Start listening for tasks."""
            self._socket.bind('tcp://{}:{}'.format(self.host, self.port))
            while True:
                runnable_string = self._socket.recv_pyobj()
                runnable = pickle.loads(runnable_string)
                self._socket.send_pyobj('')
                args = self._socket.recv_pyobj()
                self._socket.send_pyobj('')
                kwargs = self._socket.recv_pyobj()
                response = self._do_work(runnable, args, kwargs)
                self._socket.send_pyobj(response)

        def _do_work(self, task, args, kwargs):
            """Return the result of executing the given task."""
            print('Running [{}] with args [{}] and kwargs [{}]'.format(
                task, args, kwargs))
            return task(*args, **kwargs)

    def queue(runnable, *args, **kwargs):
        """Return the result of running the task *runnable* with the given 
        arguments."""
        runnable_string = cloud.serialization.cloudpickle.dumps(runnable)
        TASK_SOCKET.send_pyobj(runnable_string)
        TASK_SOCKET.recv()
        TASK_SOCKET.send_pyobj(args)
        TASK_SOCKET.recv()
        TASK_SOCKET.send_pyobj(kwargs)
        results = TASK_SOCKET.recv_pyobj()
        return results

    if __name__ == '__main__':
        w = Worker()
        w.start()

And to use it? Here's the complete contents of `app.py`:

    #!py
    import requests
    from brokest import queue

    def count_words_in_page(url):
        resp = requests.get(url)
        return len(resp.text.split())

    result = queue(count_words_in_page, 'http://www.jeffknupp.com')
    print result

Rather than calling the function directly, you simply call `brokest.queue` with
the function and it arguments as arguments. While the current implementation is
blocking, it would be trivially easy to make it non-blocking. Adding multiple
workers is just a matter of adding code to make use of a config file with their
locations.

Clearly, the stars here are `zmq` and `cloud`. [ZeroMQ](http://zeromq.org/)
makes creating distributed systems a lot easier, and the documentation is chock
full of ZeroMQ design patterns (ours is probably the simplest one, Request-Reply).

`cloud` is the LGPL'd [PiCloud](http://www.picloud.com) library. PiCloud is a
company whose value proposition is that they let you seamlessly run
computationally intensive Python code using Amazon EC2 for computing resources.
Part of making that a reality, though, required a way to pickle functions *and their dependencies*
(functions are not normally directly pickle-able). In our example, the `Worker`
is able to make use of code using `requests` library despite not having imported it.
It's the secret sauce that makes this all possible.

## Is This For Real?

The code works, but my intention was not to create a production quality
distributed task queue. Rather, it was to show how new libraries are making it
easier than ever to create distributed systems. Having a way to pickle code
objects and their dependencies is a *huge* win, and I'm angry I hadn't heard of
PiCloud earlier.

One of the best things about being a programmer is the ability to tinker not
just with things, but with *ideas*. I can take existing ideas and tweak them, or
combine existing ideas in new ways. I think `brokest` is an interesting example
of how easy it has become to create distributed systems.
