Jump to other posts in this series 

1. [Part 1](!!!)
2. [Part 2](!!!)

In [part one](!!!), we created a super-simple web server capable of handling a
simple subset of HTTP requests. In this post, we'll flesh out our webserver a
bit more, adding support for header parsing, content negotiation, and cookies.

## Parsing headers

Recall that HTTP *headers* are Key => Value pairs that contain
"meta-information" about the request or response they are sent on. Just as 
with HTTP methods, some header fields are used more often than others. Three in
particular are included in almost every request:

1. User-Agent
1. Host
1. Accept

Let's examine these in a bit more detail.

### User-Agent

The *User-Agent* header is used to give the server information about the *agent*
a user (or system) is using to make the request. In normal web browsing, the
agent is your browser itself; the browser makes HTTP requests on your behalf.
For programmatic HTTP requests, the User-Agent is normally the name of whatever
HTTP library the application is using. If we use the program `curl` to make a
request to our server (start the server by typing `python <name_of_script.py>
8080 /tmp` and make sure you have a file named `hello.txt` in your `/tmp`
directory) by typing `curl --verbose localhost:8080/hello.txt`, we see the 
User-Agent is reported as `curl/7.30.0`. This indicates to the server that the
request was made by a client using version `7.30.0` of `curl` (or `libcurl`, the
`curl` library).

This information is especially useful when the request is sent by a browser.
When I point Chrome at `localhost:8080/hello.txt` and ask our server to print
out the User-Agent header (more on how to do that in a bit), I get the following
string:

> Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36

You can see that not only is the type of browser I'm using sent, the rendering
library ("AppleWebKit") and OS are also specified. Since different versions of
different browsers support different HTML/CSS features, a web application may
use this information to modify a page so that it renders properly on the
client's browser, regardless of which browser they're using.

### Host

The *Host* header is used to let the server know from where the request
originated.
