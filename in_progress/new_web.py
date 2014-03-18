"""A web server capable of serving files from a given directory."""

import socket
import os.path
import sys

RESPONSE_TEMPLATE = """HTTP/1.1 200 OK

{}"""

def parse_headers(request):
    """Return a dictionary in the form Header => Value for all headers in
    *request*."""
    headers = {}
    for line in request.split('\n')[1:]:
        header_line = line.split(':')
        header_type = header_line[0]
        value = ''.join(header_line[1:])
    return headers

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
        if not os.path.exists(path):
            connection.sendall('HTTP/1.1 404 Not Found\n')
        else:
            with open(path) as file_handle:
                file_contents = file_handle.read()
                response = RESPONSE_TEMPLATE.format(file_contents)
                connection.sendall(response)
        connection.close()

if __name__ == '__main__':
    sys.exit(main())
