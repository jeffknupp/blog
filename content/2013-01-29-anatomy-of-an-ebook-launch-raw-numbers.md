title: Anatomy of an eBook Launch: Raw Numbers
date: 2013-01-29 16:18
categories: ebook python idiomatic freelance

On January 24th, I officially "launched" my eBook [Writing Idiomatic Python](www.jeffknupp.com/writing-idiomatic-python-ebook). I had no idea what to expect and even less of an idea about what I should do to promote it. So I did the easiest thing: posted to reddit ([/r/python](http://www.reddit.com/r/python/) to be specific). Aside from a [post to hacker news](http://news.ycombinator.com/item?id=5112211) not about the book itself and a single tweet, posting on reddit was the only thing I did.

**And that was enough.**

The post got a few upboats and stayed on the front page of /r/python for 5 days
(and was the top post for about 2 days). The traffic, from reddit alone mind
you, sold a lot of books (the exact numbers are discussed later).

<!--more-->

## Some Raw Numbers

Between the 24th and 29th, I received 10,002 page views during 6,052 visits from
4,848 visitors. As you can see below, the majority of these came during the first two days (1,570
visits on the 24th and 1,896 on the 25th).

<div id="visitor_div">
</div>

## Missteps

When I started, I only offered PDF versions of the book ($8.99) with payment via credit
card. Much of the early feedback fell in to one of three categories:

* I want to buy the book but can't pay via credit card. Can you enable payments
    via (PayPal, Google Checkout, etc)
* I want to read the book on my mobile device. Can you offer the book in the
    **epub** format?
* I want to buy both versions of the book, but $18 is more than I'm willing to
    spend.

Needless to say I got right to work. By Friday morning I set up PayPal and
Google Checkout as payment options. A few hours later, I offered a bundle of all
versions and all formats of the book for $12.99 (roughly 50% more than the cost
of the book in a single version/format.) Both of these helped, but one had a
considerably larger impact.

**The 'bundle' option quickly became the most popular. I was now making 50% more per sale.**

I had effectively increased the price of the most commonly purchased item from $8.99 to $12.99.
Apparently, either a lot of people wanted the contents of the bundle or, more
likely, the bundle's price was very attractive compared to a single version.

## Sales Numbers

<div id="units_chart">
</div>

<div id="sales_chart">
</div>

**Total Sales: $2,526.65**

## Free copies and returns

As I specify on the landing page for the 
 [book](www.jeffknupp.com/writing-idiomatic-python-ebook), I'm happy to send out
free copies of the book to those without the financial means to purchase it. To
date I've given out roughly 30 free copies in various versions/formats. Everyone
has been quite appreciative and I've noticed I get the most feedback from those
who got it for free. I have no idea why that is, but I enjoy the feedback.

Has this materially impacted sales? Possibly, but the effect is likely
minuscule. I know the number of free versions I sent out, so that accounts for
all possible lost sales (unless seeing that I offer a free version stops some
people who would otherwise have purchased it. Not likely, but stranger things
have happened).

I also offer a 30 day money back guarantee. To date I've had (and successfully
processed) 3 return requests. Doing so is quite painless through both of my
payment gateways. Again, I know the exact impact this policy has on sales 
and am happy with it. I'd much rather return money to someone who didn't find
the information helpful than have a bunch of random, tech-savvy people pissed at
me.

## In summary

Let me get this out of the way: these numbers are far better than I expected 
or hoped for. Clearly, if I had more free time leading up to the release, I
would have done more marketing. But, as with the book itself, all of this is
done in my spare time (I have a full-time, non eBook writing job). Given the
amount of effort I put into marketing, I'm frankly astounded at the results.

Obviously, sales have been dropping off sharply as the traffic from reddit
fades. That's fine. In fact, the whole point of this is to: a) help people learn
Python and b) build a source of passive income. Aside from additions and updates 
to the book itself, my profit per month from this project will simply be a
function of the effort I put into sales/marketing (modulo some small number of
sales I would get by doing nothing).

Passive income is a powerful idea and has been discussed ad nauseum, so I won't
beat a dead horse. Until you actually see passive income flowing into your bank
account, though, it's difficult to appreciate just how incredible a thing it is.

One more thing: because of this project, I've gained a lot of email newsletter
subscribers. Hopefully, these (wonderful!) people will at least take a glance 
the *next* time I release a project. That makes the whole "initial marketing"
thing a lot easier...


<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">

// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart() {

var visitor_data = new google.visualization.DataTable();
visitor_data.addColumn('string', 'Date');
visitor_data.addColumn('number', 'Visitors');
visitor_data.addColumn('number', 'Page Views');
visitor_data.addRows([
['01-24-13', 1570, 2911],
['01-25-13', 1896, 3151],
['01-26-13', 745, 1138],
['01-27-13', 621, 995],
['01-28-13', 830, 1224],
['01-29-13', 591, 887]]);

var options = {
    title: 'Traffic to jeffknupp.com between 1-24 and 1-29',
    hAxis: {title: 'Date'}}

var visitor_chart = new google.visualization.AreaChart(document.getElementById('visitor_div'));
        visitor_chart.draw(visitor_data, options);
// Create the data table.
var data = new google.visualization.DataTable();
data.addColumn('string', 'Version');
data.addColumn('number', 'Units Sold');
data.addColumn('number', 'Sales ($)');
data.addRow(['2.7.3 ePub',	10, {v: 89.90, f: '$89.90'}]);
data.addRow(['2.7.3 PDF',	66, {v: 593.34, f: '$593.34'}]);
data.addRow(['3.3 ePub',	3, {v: 26.97, f: '$26.97'}]);
data.addRow(['3.3 PDF',	20, {v: 179.80, f: '$179.80'}]);
data.addRow(['All Versions and Formats',	126, {v: 1636.64, f: '$1636.64'}]);

var view = new google.visualization.DataView(data);
view.setColumns([0, 1]);
// Set chart options
var options = {'title':'Units Sold by Version',
                'width':500,
                'height':300,};

// Instantiate and draw our chart, passing in some options.
var units_chart = new google.visualization.BarChart(document.getElementById('units_chart'));
units_chart.draw(view, options);


view.setColumns([0, 2]);
options = {'title':'Total Sales by Version',
                'width':500,
                'height':300,
                'hAxis': {'format': '$####.##', 'title': 'Sales (in USD)'}};


var sales_chart = new google.visualization.BarChart(document.getElementById('sales_chart'));
sales_chart.draw(view, options);
}
</script>
