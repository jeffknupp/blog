import socket
import os.path
import sys

DOCUMENT_ROOT = '/tmp'

def send_error(connection):
    connection.sendall(
    """HTTP/1.1 404 Not Found
""")


listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind(('', int(sys.argv[1])))
listen_socket.listen(1)
while True:
    connection, address = listen_socket.accept()
    request = connection.recv(1024)
    start_line = request.split('\n')[0]
    method, uri, version = start_line.split()
    path = '/tmp' + uri
    if not os.path.exists(path):
        send_error(connection)
    else:
        with open(path) as file_handle:
            file_contents = file_handle.read()
            response = """HTTP/1.1 200 OK
Content-Length: {}
Content-Type: text/html

{}""".format(
                    len(file_contents),
                    file_contents)
            print response
            print file_contents
            connection.sendall(response)
    connection.close()


