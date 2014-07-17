title: Omega: The Last Python Web Framework
date: 2014-07-17 15:46
categories: python omega flask

The preparation for [my talk on Monday](http://www.slideshare.net/jeffknupp/building-automated-rest-apis-with-python)
at the Wharton Web Conference got me thinking a lot about the impedance mismatch 
between web frameworks and REST
APIs. The more you develop REST APIs with frameworks like Django or Flask, the
more clear it is that something is amiss. It's a subtle feeling of needing to
fight against the grain to accomplish your goal.

Which of course led me down another rabbit hole: server-side web frameworks in general.
There are two things they pretty much suck at right now: helping you write REST
APIs and supporting bidirectional communication over things like WebSockets.
<!--more-->
I wondered what would happen if you took the guts of Flask (i.e. Werkzeug) and
built around it a framework of frameworks. A way to write a real-time
application or a REST API or a series of simple templated pages or an entirely
static site or a ... well, you get the idea. I wondered, and then I started
writing.

My current progress is (as of ten minutes ago) called
["Omega"](http://www.github.com/jeffknupp/omega). It's a fully
functional framework in some regards, and a totally incomplete one in others.
Here, though, is what it would look like to have an automatically generated,
browsable REST API *with real-time chat* (bet you didn't see that coming).

    #!python

    """Code for the Twooter application."""
    from werkzeug import Response
    from omega.http.core import create_app
    from sqlalchemy import create_engine
    from gevent import monkey
    monkey.patch_all()
    from models import Twoot, User
    from sockets import ChatNamespace


    app = create_app(__name__)


    @app.route('/chat', methods=['POST'])
    def chat(request):
        """Route chat posts to the *chat* handler function. Broadcast the message
        to all users."""
        message = '{}: {}'.format(request.form['user'], request.form['message'])
        if message:
            ChatNamespace.broadcast('message', message)
        return Response()


    if __name__ == '__main__':
        app.engine(create_engine(
            'postgresql+psycopg2://jknupp@localhost/omega'))
        app.orm_resource(Twoot)
        app.orm_resource(User)
        app.namespace('/chats', ChatNamespace)
        app.auto_generate_home()
        app.run(debug=True)

And here are the `models.py` and `sockets.py` files:

(`models.py`)

    #!python

    import datetime

    from omega.http.orm import (
        Model,
        Column,
        String,
        DateTime,
        Integer,
        relationship,
        ForeignKey,
        )


    class User(Model):
        """A Twooter User"""
        __tablename__ = 'user'

        id = Column(Integer, primary_key=True)
        user_name = Column(String)
        joined_at = Column(DateTime, default=datetime.datetime.now())


    class Twoot(Model):
        """A Twoot message"""
        __tablename__ = 'twoot'

        id = Column(Integer, primary_key=True)
        content = Column(String)
        posted_at = Column(DateTime, default=datetime.datetime.now())
        user_id = Column(Integer, ForeignKey('user.id'))
        user = relationship(User)


(`sockets.py`)

    #!python

    from socketio.namespace import BaseNamespace

    class ChatNamespace(BaseNamespace):
        sockets = {}

        def on_chat(self, msg):
            self.emit('chat', msg)

        def recv_connect(self):
            print "Got a socket connection"
            self.sockets[id(self)] = self

        def disconnect(self, *args, **kwargs):
            print "Got a socket disconnection"
            if id(self) in self.sockets:
                del self.sockets[id(self)]
            super(ChatNamespace, self).disconnect(*args, **kwargs)

        @classmethod
        def broadcast(self, event, message):
            for ws in self.sockets.values():
                ws.emit(event, message)

Pretty minimal. I've become obsessed with the notion of auto-generating as much
as humanly possible so that the code required by the client is literally the
minimal amount of information that needs to be transmitted to describe how their
system should look. That means that Omega gives you Django admin-style
functionality out of the box, as well as django-rest-framework functionality on
the API side. Customization is possible, but the goal is to avoid it unless
absolutely necessary. It's taking the idea of an opinionated framework to the
extreme, all the way to look and feel (both of which are purposely hideous, at
the moment.

The thing is, though, you can copy that code, run it, use `curl` to interact
with the REST API, browse through it and edit stuff by hitting
`localhost:5000/`, and even connect two browser tabs to `localhost:5000/` and
hold a chat session between them. You can do all of that *right now*, in a way
that asks as little of you as possible.

## The Future

Omega is not done; I mean, it's barely usable. It will likely never be "done".
Instead, it's an experiment in taking a different tack than today's
"micro-frameworks". You might call it the first "macro-framework". Or you might
call it "Omega: The Last Framework". Either way, I'm guessing you've not seen
anything quite like it before.
