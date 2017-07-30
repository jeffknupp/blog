# Python and Flask Are Ridiculously Powerful

As a developer, I sometimes forget the power I wield. It's easy to forget that,
when something doesn't work the way I'd like, I have the power to change it.
Yesterday, I was reminded of this fact as I finally got fed up with the way
payments are processed for [my book](http://www.jeffknupp.com/writing-idiomatic-python-ebook/).
After being unhappy with the *three* different digital-goods payment processors
I've used since the book came out, I took two hours and wrote my own solution
using Python and [Flask](http://flask.pocoo.org). That's right. *Two hours*. 
It's now powering my book payment processing and the flow is so incredibly
simple that you can buy the book and begin reading it in 20 seconds.

Read on to find out how I created my own digital goods payment solution in an
evening.

<!--more-->

# Payment Processor Purchase Problems

When I began selling the book, I used a combination of two services (one for 
credit cards and another for PayPal). Eventually, I found a single 
processor capable of supporting both. I've never been happy, though, with any of
them. The most recent processor required users to create an account on the
merchant's system and enter their mailing address (though there was no 
use for it).

Additionally, I've had a terrible time trying to get Google Analytics to
properly track visitor flow through the entire visit, including the checkout 
process. I always sensed that, if I were able to get that working and run 
A/B tests on my book page, I could greatly increase sales. Without proper 
tracking however, I was out of luck.

Lastly, sending out book updates is terribly time-consuming using three different
processors. None supported updates well, and I wanted a one-click solution to
sending out book updates. Finding a service that supported that was basically
impossible.

# Oh Yeah, I'm a Programmer

After receiving an email from a customer yesterday about how difficult the
payment process was and informing me that I'm likely losing sales because of
it, I got fed up. I decided to roll my own digital goods management solution. It
needed the following work-flow:

> When a customer clicks the "Buy Now" button, they should be asked to enter only
their email address and credit card info, click "Confirm", and be taken to a
unique URL to download the book (generated specifically for that purchase). An 
email should be sent to the customer containing the generated URL (in case the customer 
needs to re-download the book). There should be a limit to the number of 
times (5) they can download it. The purchase and customer information should be
stored in a database, and sending out updates should be a one-command affair.

Clearly, it's not that complicated. The trickiest part would be dynamically generating 
a unique URL that linked to the proper version of the book. Everything else
seemed straightforward.

# "Flask to the Rescue," or "A Digital Goods Payment Solution in 100 Lines of Code"

Spoiler alert: the resulting application is exactly 100 lines of code. Flask is
a great choice for a web application of this size. It doesn't require a ton of
boilerplate (*cough* like Django *cough*) but has good plugin support. Bottle
would have been another fine choice, but I've used Flask more recently, so
that's what I chose.

To begin, I needed to decide how I was going to store the customer and purchase
information. I decided to use [SQLAlchemy](http://www.sqlalchemy.org), since
I've got a lot of experience with it because of
[sandman](http://www.sandman.io). Flask has a plugin, Flask-SQLAlchemy, that
makes using the two together easy. Since I don't need anything too fancy
database-wise, I chose SQLite as my database back-end. 

Having made these decisions, I created a file named `app.py` and created the following models:

    #!py
    class Product(db.Model):
        __tablename__ = 'product'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)
        file_name = db.Column(db.String)
        version = db.Column(db.String)
        is_active = db.Column(db.Boolean, default=True)
        price = db.Column(db.Float)

    class Purchase(db.Model):
        __tablename__ = 'purchase'
        uuid = db.Column(db.String, primary_key=True)
        email = db.Column(db.String)
        product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
        product = db.relationship(Product)
        downloads_left = db.Column(db.Integer, default=5)

After adding the five different versions of the book to the database (I created
a `populate_db.py` file and added them as SQLAlchemy models), I needed to decide
how I was going to actually process payments. Luckily,
[Stripe](http://www.stripe.com) makes accepting credit card payments stupidly
easy, and I already had an account with them. Their "checkout.js" solution
creates a form and button on your page. When the button is clicked, a simple and
attractive payment overlay is displayed.

<img src="http://www.jeffknupp.com/images/payment.jpg">

The `action` attribute of the form points to the page on your site that the user
should be taken to after a successful payment. I added 5 of these buttons to my
book sales site and added another hidden form field to contain the `product_id`
(an integer between 1 and 5) of the product that was purchased.

## Processing Payments

Clearly, I needed an endpoint in my application to process a successfully
charged card. I added the following function to do so:

    #!py
    @app.route('/buy', methods=['POST'])
    def buy():
        stripe_token = request.form['stripeToken']
        email = request.form['stripeEmail']
        product_id = request.form['product_id']
        product = Product.query.get(product_id)
        try:
            charge = stripe.Charge.create(
                    amount=int(product.price * 100),
                    currency='usd',
                    card=stripe_token,
                    description=email)
        except stripe.CardError, e:
            return """<html><body><h1>Card Declined</h1><p>Your chard could not
            be charged. Please check the number and/or contact your credit card
            company.</p></body></html>"""
        print charge
        purchase = Purchase(uuid=str(uuid.uuid4()),
                email=email,
                product=product)
        db.session.add(purchase)
        db.session.commit()
        message = Message(
                subject='Thanks for your purchase!',
            sender="jeff@jeffknupp.com", 
            html="""<html><body><h1>Thanks for buying Writing Idiomatic Python!</h1>
    <p>If you didn't already download your copy, you can visit 
    <a href="http://buy.jeffknupp.com/{}">your private link</a>. You'll be able to
    download the file up to five times, at which point the link will
    expire.""".format(purchase.uuid),
            recipients=[email])
        with mail.connect() as conn:
            conn.send(message)
        return redirect('/{}'.format(purchase.uuid))

As you can see, I took a few shortcuts with the code (since I was coding
angrily...). First, I have inline HTML to be returned from an unsuccessful
charge and for the email that is sent upon purchase. That should be extracted
to a global variable or, better, contained in a separate file. Second, I didn't do any
error checking when creating the `Purchase` object. But really, the only thing 
that could go wrong is trying to insert a duplicate `uuid`, which doesn't
concern me due to the probability of it happening (read: vanishingly small).

You can see I'm using a `mail` object. This comes from the Flask-Mail package,
which makes sending email painless. I simply set it up to use GMail as the mail
server and everything Just Worked. 

## OK, Now Give Me The Book

Now that I had the payment portion sorted out, I needed to add an endpoint for
initiating downloads after a purchase. Since I'm using UUIDs as a primary key, I
can also use them as the URL for the download endpoint. When someone hits the
endpoint, I simply need to check that the UUID contained in the URL matches the
UUID of a purchase in the database. If it does, serve the book file and
decrement the `downloads_left` attribute. If not, return a `404` error.
Here's the code I came up with:

    #!py
    @app.route('/<uuid>')
    def download_file(uuid):
        purchase = Purchase.query.get(uuid)
        if purchase:
            if purchase.downloads_left <= 0:
                return """<html><body><h1>No downloads left!</h1><p>You have
                exceeded the allowed number of downloads for this file. Please email
                jeff@jeffknupp.com with any questions.</p></body></html>"""
            purchase.downloads_left -= 1
            db.session.commit()
            return send_from_directory(directory='files',
                    filename=purchase.product.file_name, as_attachment=True)
        else:
            abort(404)

Very straightforward. Using the UUID as a URL variable, search for a purchase.
If it exists, just check that there are still downloads left and serve the file
attribute of the purchase's product. Otherwise, here's a `404` for you.

Lastly, I needed to add a test endpoint that would allow me to simulate the
purchase process. Here's the code for that endpoint and the portion that runs
the app:

    #!py
    @app.route('/test')
    def test():
        return """<http><body><form action="buy" method="POST">
    <script
        src="https://checkout.stripe.com/checkout.js" class="stripe-button"
        data-key="pk_test_w3qNBkDR8A4jkKejBmsMdH34"
        data-amount="999"
        data-name="jeffknupp.com"
        data-description="Writing Idiomatic Python 3 PDF ($9.99)">
    </script>
    <input type="hidden" name="product_id" value="2" />
    </form>
    </body>
    </html>
    """
    if __name__ == '__main__':
        sys.exit(app.run(debug=True))
        
# With Great Power Comes... Moar Power!

I was actually surprised at how quickly and easily I got this working. The
entire application is *a single file containing 100 lines of code*. And it
replaces a very important service I use everyday, one with which I've never been
happy. Finally, I can track purchases without issue, which I'm convinced will
increase sales.

It's nice to be reminded that, as developers, we have a lot of power to shape
our interactions with the digital world. I, for one, often forget that if I don't
like the way some piece of technology works, I can change it. From
automating mechanical tasks like data entry to automatically sorting and
organizing email, developers have the power to simplify their everyday tasks.

Having libraries like Flask in your tool belt is crucial to 
solving these sorts of problems, though. As you progress as a developer, you
should be building up a set of tools that work for "core"
problem domains. Flask is a perfect example, since needing to throw together a 
web app is a common problem.

And of course, sharing what you made is critical as well. I would be remiss if I
created something useful for myself and didn't share it with others. "Sharing"
means more than "putting in a public GitHub repo". You also need to let people
know about it. From mailing lists to forums to personal blogs, there's no
shortage of avenues for making others aware of what you've created. I always try
to give back to the community, since I've gained so much from it.
