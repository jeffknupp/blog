title: A Python App to See What People Are Saying About You
date: 2014-01-31 11:26
categories: python flask eavesdropper

I've been taking stock of the digital services I use (and pay for) but am
unhappy with. Digital goods sales (for my book) has already been taken care of
by [bull](http://www.github.com/jeffknupp/bull). Next on my list is tracking
mentions of my site across the Internet. In this article, we'll build a simple
(but fully functional) web application that searches for and displays mentions
of a particular keyword (in my case, "jeffknupp.com").
<!--more-->
I should mention that I use a service to do this already: [mention](http://www.mention.net).
It's *OK*, but I'm reaching their quota for the free service, and I can't stand
their mobile app, so I'd rather have something tailored for myself. And, as I've
recently discovered with `bull`, writing a service like this from scratch can be
done quite quickly. If you know of a better application for tracking mentions,
by the way, please let me know!

## Twitter

I'll focus initially on Twitter, as much/most of the commentary on my site
likely occurs there (as opposed to blogs or newsgroups). I wanted to try out a
new Python Twitter client anyway ([birdy](https://github.com/inueni/birdy)), so
I decided to use `birdy` for my Twitter interactions.

At the very least, I need to be able to persist mentions of my site in a database.
Any problem with the word "database" in it can usually be answered with
"SQLAlchemy," and this is no exception. Let's create some SQLAlchemy models for
our database:

    #!py
    """Database models for the eavesdropper application."""

    import datetime

    from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
    from sqlalchemy.orm import relationship, backref
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class Source(Base):

        __tablename__ = 'source'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String)

    class Mention(Base):
        """A Mention from a particular source."""

        __tablename__ = 'mention'
        id = Column(Integer, primary_key=True, autoincrement=True)
        domain_id = Column(String)
        source_id = Column(Integer, ForeignKey('source.id'))
        source = relationship(Source)
        text = Column(String)
        associated_user = Column(String)
        seen = Column(Boolean, default=False)
        recorded_at = Column(DateTime, default=datetime.datetime.now)
        occurred_at = Column(DateTime, default=datetime.datetime.now)

        def __str__(self):
            """Return the string representation of a mention."""
            return self.text

        def to_json(self):
            return {
                    'id': self.id,
                    'domain_id': self.domain_id,
                    'source': self.source.name,
                    'text': self.text,
                    'associated_user': self.associated_user,
                    'seen': self.seen,
                    'recorded_at': str(self.recorded_at),
                    'occurred_at': str(self.occurred_at)}

Nothing very surprising here. I create two models, one to represent a data
source (like "Twitter"), and another to model the actual mention of the keyword
I'm interested in. The only interesting thing is the `to_json` function. Since I
know that I'll be creating a web application with a dynamic front-end, I imagine
I'll be sending this data as JSON quite often. Hence the existence of `to_json`.

After creating a `models.py` file, I usually follow up with a
`populate_db.py` file to insert initial data into the database. Here are the
contents of that file:

    #!py
    from sqlalchemy import create_engine
    from models import Source, Mention, Base
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///sqlite.db')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine) 
    session = Session()

    s = Source(id=1, name='Twitter')
    m = Mention(id=1, source=s, text='jeffknupp.com is the best website ever!')
    session.add(s)
    session.add(m)
    session.commit()

Again, nothing crazy here. It simply creates a single Source and Mention object
and inserts them into the database.

## Tweet collection, the Python way

We're now ready to begin the application proper. I'll begin with a skeleton of
the application, filling in the docstrings for classes and functions but nothing
else. Here is the skeleton:
    """Find and record references to a person or brand on the Internet."""

    #!py
    import sys
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def index():
        """Return the main view for mentions."""

    @app.route('/update/<source>', methods=['POST'])
    def get_updates_for_source(source):
        """Return the number of updates found after getting new data from
        *source*."""

    @app.route('/read/<id>', methods=['POST'])
    def read(id):
        """Mark a particular mention as having been read."""

    @app.route('/mentions')
    def show_mentions():
        """Return a list of all mentions in JSON."""
        
    def main():
        """Main entry point for script.""""
        app.run()

    if __name__ == '__main__':
        sys.exit(main())

Since I'm going to be adding more sources in the near future, I decided that the
source-specific retrieval code should live in a separate file. Here's the
skeleton for `twitter.py`, where most of the heavy lifting is done:

    #!py
    from birdy.twitter import AppClient

    from models import Source, Mention

    CONSUMER_KEY = 'xxxx'
    CONSUMER_SECRET = 'xxxx'
    client = AppClient(CONSUMER_KEY, CONSUMER_SECRET)
    access_token = client.get_access_token()
    QUERIES = ['jeffknupp.com', 'jeffknupp']

    def get_twitter_mentions():
        """Return the number of new mentions found on Twitter."""

Let's implement that single function, `get_twitter_mentions`, now.
First, we'll need a list to keep track of all mentions across all queries (since
multiple query terms are supported).

    #!py
    statuses = []
    for query in QUERIES:
        response = client.api.search.tweets.get(q=query, count=100)
        statuses += response.data.statuses

I'm happy with how easy `birdy` is to use, although this is an admittedly simple
use. Anyway, now that we have all the status updates containing our queries,
let's prepare to insert *only the new ones* into the database:

    #!
    session = Session()
    twitter = session.query(Source).get(1)
    for status in statuses:

We need to iterate over each status object, which `birdy` returns as a
`JSONObject` (basically a dictionary who's keys are available as attributed).
We want the `get_twitter_mentions` function to be (logically) idempotent. That
is, if we execute the function multiple times, our database does not contain
duplicate results. To achieve this, we need to check for any `Mention` objects that have 
the same `domain_id`, which is the unique identifying ID in the source system (i.e. the unique ID Twitter assigned
the tweet). 

    #!py
        if not session.query(Mention).filter(Mention.domain_id==status.id_str).count():


Easy enough. Now let's actually create the `Mention` object we're going to
insert:

    #!py
            created_at = datetime.datetime.strptime(status.created_at, r"%a %b %d %H:%M:%S +0000 %Y")
            m = Mention(text=status.text,
                    associated_user='{} ({})'.format(status.user.screen_name,
                        status.user.followers_count),
                        recorded_at=datetime.datetime.now(),
                        occurred_at=created_at,
                        source=twitter,
                        domain_id=status.id_str)
            session.add(m)
    session.commit()

After going back and adding a simple count of the new `Mention` objects, here's
the completed function in its entirety:

    #!py
    def get_twitter_mentions():
        """Return the number of new mentions found on Twitter."""
        statuses = []
        for query in QUERIES:
            response = client.api.search.tweets.get(q='jeffknupp.com', count=100)
            statuses += response.data.statuses
        session = Session()
        twitter = session.query(Source).get(1)
        new_mentions = 0
        for status in statuses:
            if not session.query(Mention).filter(Mention.domain_id==status.id_str).count():
                created_at = datetime.datetime.strptime(status.created_at, r"%a %b %d %H:%M:%S +0000 %Y")
                m = Mention(text=status.text,
                        associated_user='{} ({})'.format(status.user.screen_name,
                            status.user.followers_count),
                            recorded_at=datetime.datetime.now(),
                            occurred_at=created_at,
                            source=twitter,
                            domain_id=status.id_str)
                new_mentions += 1
                session.add(m)
        session.commit()
        return new_mentions

## Back to the app

Now it's time to implement the main application logic. Let's return to `app.py`,
the file in which we created our skeleton. I know that the `index` function is
just going to return a rendered template, since the querying for `Mention`s
will happen on the client side. Thus, `index` is trivial:

    #!py
    @app.route('/')
    def index():
        """Return the main view for mentions."""
        return render_template('index.html')

The code to return all `Mention` objects as JSON seems simple, so let's
implement that next:

    #!py
    @app.route('/mentions')
    def show_mentions():
        """Return a list of all mentions in JSON."""
        session = db.session()
        mentions = session.query(Mention).all()
        values = [mention.to_json() for mention in mentions]
        response = make_response()
        response.data = json.dumps(values)
        return response
 
 Again, nothing too crazy. Hitting the `/mentions` endpoint will return a JSON
 list of all `Mention` objects in the database.

 Since the purpose is similar, let's implement the `read` function next:

    #!py
    @app.route('/read/<id>', methods=['POST'])
    def read(id):
        """Mark a particular mention as having been read."""
        session = db.session()
        mention = session.query(Mention).get(id)
        mention.seen = True
        session.add(mention)
        session.commit()
        return jsonify({'success': True})

We simply use the `<id>` parameter passed in via the URL as the primary key in
our database look up. Then we simply changed `seen` to `True` and save the object
back to the database. We return a token response that's not of much interest
(really, a HTTP 204 would have been more appropriate, but I was lazy).

The rest is just mop up. Here's the implementation for `get_updates_for_source`
(which allows us to request updates via an HTTP request) :

    #!py
    @app.route('/update/<source>', methods=['POST'])
    def get_updates_for_source(source):
        """Return the number of updates found after getting new data from
        *source*."""
        if source == 'twitter':
            updates = get_twitter_mentions()
            return jsonify({'updates': updates})

And that's the last part of the file. To recap, here's what the completed file
looks like:

    #!py
    """Find and record references to a person or brand on the Internet."""

    import sys
    import json
    import pprint
    import argparse

    from flask import Flask, make_response, render_template, jsonify, send_from_directory
    from flask.ext.sqlalchemy import SQLAlchemy
    from birdy.twitter import AppClient

    from models import Source, Mention, Base
    from twitter import get_twitter_mentions

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///sqlite.db'
    db = SQLAlchemy(app)

    @app.route('/')
    def index():
        """Return the main view for mentions."""
        return render_template('index.html')

    @app.route('/update/<source>', methods=['POST'])
    def get_updates_for_source(source):
        """Return the number of updates found after getting new data from
        *source*."""
        if source == 'twitter':
            updates = get_twitter_mentions()
            return jsonify({'updates': updates})


    @app.route('/read/<id>', methods=['POST'])
    def read(id):
        """Mark a particular mention as having been read."""
        session = db.session()
        mention = session.query(Mention).get(id)
        mention.seen = True
        session.add(mention)
        session.commit()
        return jsonify({})

    @app.route('/mentions')
    def show_mentions():
        """Return a list of all mentions in JSON."""
        session = db.session()
        mentions = session.query(Mention).all()
        values = [mention.to_json() for mention in mentions]
        response = make_response()
        response.data = json.dumps(values)
        return response
        
    def main():
        """Main entry point for script.""""
        app.run()

    if __name__ == '__main__':
        sys.exit(main())

## Client-side rendering with React.js

I've been looking for an excuse to learn Facebook's [React.js](http://facebook.github.io/react/)
framework, and this is the perfect opportunity. I won't go into detail about the
implementation because a) I'm sure there's a better way to do it and b) I'm not
an authority (by any means) on the subject.

Regardless, using React, I was able to create a page that displays all mentions.
Unread mentions are presented in a well. Once clicked, the asynchronously send a
`/read` request to the database and change their appearance (by changing their
CSS class). So basically there's a visual difference between read and unread
items and it's updated dynamically.

Here's the contents of index.html (which you may notice is *very* similar to the
React tutorial code...):

    #!html
    <!doctype html>
    <html>
    <head>
        <script src="http://fb.me/react-0.8.0.js"></script>
        <script src="http://fb.me/JSXTransformer-0.8.0.js"></script>
        <script src="http://code.jquery.com/jquery-1.10.0.min.js"></script>
        <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
    <div class="container">
        <div class="row">
            <div class="col-md-6 col-md-offset-3" >
                <div id="content">
                </div>
                <script type="text/jsx">
                /**
                * @jsx React.DOM
                */
                var MentionBox = React.createClass({
                    getInitialState: function() {
                        return {data: []}
                    },
                    loadCommentsFromServer: function() {
                        $.ajax({
                            url: '/mentions',
                            dataType: 'json',
                            success: function (data) {
                                this.setState({data: data});
                            }.bind(this),
                            error: function (xhr, status, err) {
                                console.error("/mentions", status, err.toString());
                            }.bind(this)
                        });
                    },
                    componentWillMount: function() {
                        this.loadCommentsFromServer();
                        setInterval(this.loadCommentsFromServer, this.props.pollInterval);
                    },
                    render: function() {
                        return (
                            <div className="mentionBox">
                            <h1>Mentions</h1>
                            <MentionList data={this.state.data}/>
                            </div>
                            );
                    }
                });

                var MentionList = React.createClass({
                    render: function() {
                        var mentions = this.props.data.map( function(mention) {
                            return <Mention mention={mention}></Mention>;
                        });

                        return (
                            <div className="mentionList">
                                {mentions}
                            </div>
                        );
                    }
                });

                var Mention = React.createClass({
                    getInitialState: function() {
                        return {seen: this.props.mention.seen}
                    },
                    markRead: function() {
                        var id= 
                    $.ajax({
                            type: 'POST',
                            url: '/read/' + this.props.mention.id,
                            dataType: 'json',
                            success: function (data) {
                                this.setState({seen: true});
                            }.bind(this),
                            error: function (xhr, status, err) {
                                console.error("/mentions", status, err.toString());
                            }.bind(this)
                        });
                    },
                    render: function() {
                        return (
                                <div className={this.state.seen ? true : "well" } onClick={this.markRead}>
                                    <div className="pull-right">
                                        <h6>
                                        {this.props.mention.source}
                                        </h6>
                                    </div>
                                    <h4>{this.props.mention.associated_user} <small> &nbsp; at {this.props.mention.occurred_at}</small></h4>
                                        <p>{this.props.mention.text}</p>
                                </div>
                        );
                    }
                });

                React.renderComponent(
                        <MentionBox url="/mentions" pollInterval={20000} />,
                        document.getElementById('content')
                );
                </script>
            </div>
        </div>
    </div>
    </body>
    </html>

That gives me this:

<img src="/static/img/eavesdropper.jpeg" />

I decided to call the project "eavesdropper" as it's constantly listening to
what others are saying :). In the next post about this project, I'll show you
how to extend the project to pull from multiple sources. Until then, thanks for
reading!
