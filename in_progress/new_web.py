"""A web server capable of serving files from a given directory."""

import logging
import os.path
import socket
import sys

RESPONSE_TEMPLATE = """HTTP/1.1 200 OK

{}"""

LOGGER = logging.getLogger(__name__)

HTML_CONTENT_TYPES = ('text/html')
JSON_CONTENT_TYPES = ('application/json')

def parse_headers(request):
    """Return a dictionary in the form Header => Value for all headers in
    *request*."""
    headers = {}
    for line in request.split('\n')[1:]:
        # blank line separates headers from content
        if not line:
            break
        header_line = line.split(':')
        headers[header_line[0].lower()] = ''.join(header_line[1:]).strip()
    return headers

def is_content_type_negotiable(accepts, extension):
    """Return the content-type we must reply with or None if no acceptable
    content-type can be chosen."""

    # For now, just check if the extenions is included somewhere in the Accepts
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
            connection.sendall('HTTP/1.1 409 !!!\n')
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
