title: What Is A Web Server?
date: 2014-03-12 09:09
categories: #python #flask #web #webserver

A recent post, titled ["What Is A Web Framework"](!!) received quite a positive
response. A number of readers, though, wanted me to do a deeper dive into web
servers themselves. You may have heard of *web servers* like Apache(!!) or
[nginx](!!). Ever wondered how they work? In this post, we'll cover what a web
server is, why they exist, and how to build your own.
<!--more-->

## What is a "server"

Part of the confusion around web servers comes from that second word, "server".
What is a server? How is it different from an application? Is a server a
physical thing?

Confusingly, most developers use the term "server" to refer both to physical
machines without a GUI interface (i.e. solely to run other applications) *and* long-running
programs. It's the second definition we're interested in. A web server is simply
a *long-running program responsible for responding to HTTP requests*.

That's it? It's just a program? Like any other program? Yep. That's it. Though
web servers are typically viewed as black boxes by application developers, they
are nothing more than programs that open a socket on port 80 (the universally
agreed upon HTTP traffic port), listen for HTTP requests, and answer those
requests with HTTP responses.

Modern web servers, of course, have many other features. All of them, however,
somehow enhance the web server's main capabilities: responding to HTTP requests.
If you've ever written an *echo server*, a server which simply parrots back
whatever message was sent to it, a web server is not much different. It simply
does more with the incoming message to craft its response.

## The simplest web server

In [the previous post](!!), I described the simplest possible web server.
Much like an echo server, its reply to messages is fixed. Rather than echoing
back the input message, however, it always responds with a static, stock
message. The code for such a server follows:

    #!py
    import socket

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.bind(('', 80)) # remember, 80 is the port for HTTP traffic
    listen_socket.listen(1)
    connection, address = listen_socket.accept()
    while True:
        connection.recv(1024)
        connection.sendall("""HTTP/1.1 200 OK
        Content-type: text/html


        <html>
            <body>
                <h1>Hello, World!</h1>
            </body>
        </html>""")
        connection.close()

We can just barely call this code a web server, since it doesn't actually
properly respond to the incoming request. It does, however, provide a valid
response. HTTP messages are plain-text messages that can be inspected via a
simple `socket.read()` call.

### The HTTP protocol

HTTP is the protocol that powers the web. In its simplest form, it consists of
two messages: a request and a response. An HTTP *request* can request an HTML
document, provide data to an application (like a filled out form), request that
data be deleted, and much more. An HTTP *response* let's the *client* (i.e. your
browser) know what happened as a result of the request and includes any data
that the client requested.

HTTP requests come in many flavors (called *methods* or *verbs*), but all share
the same structure. HTTP requests, like all HTTP messages, are line delimited.
The first line is special: the *start-line*. The start-line consists of
three parts: the *method*, the *URI*, and the HTTP *version*. The method is one
of `GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS, TRACE, CONNECT`. `GET` is by
far the most common, used to request a specific resource. The version is which
version of the HTTP protocol the request is using.

The request indicates
*which* resource using the URI, or Uniform Resource Identifier. A URI is like a
URL, but the www.something.com portion is left off. This isn't an issue, since 
that portion is used to find the address to send the request to and we've
already got the delivered request. URIs look like file-system paths, beginning
with the *root*, a forward slash. In fact, they map so well to file-system paths
that the default behavior of most web servers is to treat them as such.

`/` is often called the *document root* or *root directory*. It indicates the
directory on the web server machine from which to start when searching for a
resource. For example `/srv/www/public_html` may be the document root of my web
server. If the URI requests `/images/foo.jpg`, the web server will try to send
the file `/srv/www/public_html/images/foo.jpg` in response.

Besides the start-line, there there are two other portions of the request:
*headers* and the *message-body*. Headers are meta-information about the request, indicating to the web
server, for example, that it is fine to `gzip` resources before sending them
(through the `Accept` header). Headers are each on their own line, in a `Key:
Value`-style format. 

The message body is blank for `GET` requests asking for a resource. It contains
data when other methods, such as `POST`, are used to send data to the web
server.

HTTP responses are similar enough to HTTP requests that it's not necessary to
break them down in detail. One difference, however, is the inclusion of a
*status code*, a three-digit code used to indicate what action the web server
took and how to interpret the message-body.


