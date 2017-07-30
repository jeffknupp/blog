# What Is A Web Server Part 2: Headers And Cookies

Jump to other posts in this series 

1. [Part 1](http://jeffknupp.com/blog/2014/03/12/what-is-a-web-server/)

In [part one](http://jeffknupp.com/blog/2014/03/12/what-is-a-web-server/) we created a super-simple web server capable of handling a
simple subset of HTTP requests. In this post, we'll flesh out our web server a
bit more, adding support for header parsing, content negotiation, and cookies.
<!--more-->
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

The *Host* header is used to let the server know what address the request is
bound for (i.e. the IP address or Fully Qualified Domain Name and port). This is
mostly used by HTTP proxies to determine how to route the message and isn't of
much interest to us, aside from the fact that this header is *required* on all
HTTP/1.1 requests.

### Accept

The *Accept* header is used to signal to the server what sort of media types are
acceptable for the response. In this way, the client can issue requests that are
limited to a small set of media types. If this header isn't present (it almost
always, is, however) then the client is assumed to accept all media types.

Choosing the appropriate representation for a resource with multiple representations
(both *format* like JSON vs. HTML and *content* like languages) is called *Content Negotiation*.
If the server chooses a representation, it's performing *Server-driven Negotiation*. This 
is most often the case, since clients have a number of header fields to describe
their capabilities and preferences. 

Chief among these is the Accept header. By specifying "application/json", for example, in the Accept header of a request
for a resource that has both HTML and JSON representations, I'm essentially
forcing the server to send me the JSON representation (since that's all I
accept, as far as the server knows). Content Negotiation is most important when
dealing with REST APIs, as it's important that programmatic access to a resource
receive the proper representation (like JSON).

If, after examining the Accept header, the server determines it cannot fulfill
the request (because, while the resource exists, it doesn't exist in any of the
media types specified), an error is returned. Specifically, HTTP error code 406,
"Not Acceptable" is returned.

## Parsing Headers

Let's augment our initial implementation to properly parse headers and preform
rudimentary content negotiation. Take a look at the following, updated version
of the code:

    #!py
    """A web server capable of serving files from a given directory."""

    import logging
    import os.path
    import socket
    import sys

    RESPONSE_TEMPLATE = """HTTP/1.1 200 OK

    {}"""

    HTML_CONTENT_TYPES = ('text/html')
    JSON_CONTENT_TYPES = ('application/json')

    def parse_headers(request):
        """Return a dictionary in the form Header => Value for all headers in
        *request*."""
        headers = {}
        for line in request.split('\n')[1:]:
            # blank line separates headers from content
            if line == '\r':
                break
            header_line = line.partition(':')
            headers[header_line[0].lower()] = header_line[2].strip()
        return headers

    def is_content_type_negotiable(accepts, extension):
        """Return the content-type we must reply with or None if no acceptable
        content-type can be chosen."""

        # For now, just check if the extensions is included somewhere in the Accepts
        # header, or that Accepts is "*/*"
        return extension in accepts or accepts == '*/*'


    def main():
        """Main entry point for script."""
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind(('', int(sys.argv[1])))
        listen_socket.listen(1)
        document_root = sys.argv[2]

        while True:
            connection, address = listen_socket.accept()
            request = connection.recv(1024)
            headers = parse_headers(request)
            start_line = request.split('\n')[0]
            method, uri, version = start_line.split()
            path = document_root + uri
            extension = os.path.splitext(path)[1][1:]
            if 'accept' not in headers or not is_content_type_negotiable(
                    headers['accept'], extension):
                connection.sendall('HTTP/1.1 406 Not Acceptable\n')
            elif not os.path.exists(path):
                connection.sendall('HTTP/1.1 404 Not Found\n')
            else:
                with open(path) as file_handle:
                    file_contents = file_handle.read()
                    response = RESPONSE_TEMPLATE.format(file_contents)
                    connection.sendall(response)
            connection.close()

    if __name__ == '__main__':
        sys.exit(main())

There are two main changes to the code: a portion which parses header fields and
another that does simple content negotiation. The `parse_headers` function
splits each line after the start-line on the `:` character. To the left is the
name of the header field. Everything else is the value.

With the headers parsed, we can move on to content negotiation. In this
simplified version, we check to see if the extension of the file requested
is found within one of the values in the Accept header. `*/*` is interpreted as
"anything", while `type/*` is meant to mean "all forms of this type". We handle
the former (because it's easy) while ignoring the latter for the moment.

If you add an `.html` file to `/tmp` and request it, you should see it properly
returned. If, however, you manually set the Accept header to something like
`application/json`, you'll get back a `406` error, as expected.

## Cookies

*Cookies* are Key => Value pairs that the *server* sets on the client. If the
client supports cookies, any cookies set on the first request will be sent along
with subsequent requests. For example, let's track if a user has visited the
site before and print out a message if they have (note I'm changing from using
`curl` to `httpie` here, as the latter has a much nicer interface for all of
this).

How can we augment our server to handle this? It's a two step process. First,
the server must *set* the cookie on the client by sending a *Set-Cookie* header
with the name and value of the cookie. Second, the server must *recognize* the
cookie as one that it set on subsequent requests. An example will clear things
up a bit.

Imagine I change our server to add `Set-Cookie: HasVisited = 1` in the response headers.
If I use Chrome to connect to our server, the first time we visit the cookie
will get set within Chrome. The next time we use Chrome to visit the page,
Chrome sends its cookies in the `Cookie:` header field. We can parse that and
determine if `HasVisited = 1`, at which point we know that this user has visited
before.

Here's a quick and dirty way to accomplish that:

    #!py
    """A web server capable of serving files from a given directory."""

    import logging
    import os.path
    import socket
    import sys

    RESPONSE_TEMPLATE = """HTTP/1.1 200 OK
    {headers}

    {content}"""

    LOGGER = logging.getLogger(__name__)

    HTML_CONTENT_TYPES = ('text/html')
    JSON_CONTENT_TYPES = ('application/json')

    def parse_headers(request):
        """Return a dictionary in the form Header => Value for all headers in
        *request*."""
        headers = {}
        for line in request.split('\n')[1:]:
            # blank line separates headers from content
            if line == '\r':
                break
            header_line = line.partition(':')
            headers[header_line[0].lower()] = header_line[2].strip()
        return headers

    def is_content_type_negotiable(accepts, extension):
        """Return the content-type we must reply with or None if no acceptable
        content-type can be chosen."""

        # For now, just check if the extensions is included somewhere in the Accepts
        # header, or that Accepts is "*/*"
        return extension in accepts or accepts == '*/*'

    def response_with_cookies(content):
        return RESPONSE_TEMPLATE.format(headers='Set-Cookie: HasVisited = 1;',
                content=content)

    def main():
        """Main entry point for script."""
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind(('', int(sys.argv[1])))
        listen_socket.listen(1)
        document_root = sys.argv[2]

        while True:
            connection, address = listen_socket.accept()
            request = connection.recv(1024)
            headers = parse_headers(request)
            cookies = None
            if 'cookie' in headers:
                cookies = {e.split('=')[0]: e.split('=')[1] for e in headers['cookie'].split(';')}
            if 'HasVisited' in cookies:
                print 'User has already visited!'
            start_line = request.split('\n')[0]
            method, uri, version = start_line.split()
            path = document_root + uri
            extension = os.path.splitext(path)[1][1:]
            if 'accept' not in headers or not is_content_type_negotiable(
                    headers['accept'], extension):
                connection.sendall('HTTP/1.1 406 Not Acceptable\n')
            elif not os.path.exists(path):
                connection.sendall('HTTP/1.1 404 Not Found\n')
            else:
                with open(path) as file_handle:
                    file_contents = file_handle.read()
                    connection.sendall(response_with_cookies(file_contents))
            connection.close()

    if __name__ == '__main__':
        sys.exit(main())

As you can see, it's a two-step process: first we set the cookie on the response
header, then we recognize the cookie on the request header. Believe it or not,
but that's all there is to cookies. The powerful pieces of magic that allow
you to stay logged in to certain sites are just cookies set by the site's web server. 
Of course, they set and check them in a more robust way, but the theory is the
same.

## Summary

In part two, we added the ability to parse headers, perform content
negotiation, and set/get cookies. Though the code could use a bit of clean-up,
it's still only 74 lines of code. In the next post in this series, we'll touch
on the topic of authentication and caching, as well as perform some much-needed 
refactoring of the code. Until then, have fun playing around with your new web
server!
