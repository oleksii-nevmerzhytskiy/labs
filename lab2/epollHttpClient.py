from socket import socket, AF_INET, SOCK_STREAM, SO_RCVBUF, SOL_SOCKET
from httpParser import parseHttpResponse as parser
from json import dumps, loads

HOST = 'localhost'
PORT = 8080


def read_from_socket(s: socket) -> bytearray:
    data = bytearray()
    buff_size = s.getsockopt(SOL_SOCKET, SO_RCVBUF)
    while True:
        chunk = s.recv(buff_size)
        if chunk:
            data += chunk
        if len(chunk) == 0 or chunk[-1:] == b'\n':
            break
    return data


for num in range(14):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((HOST, PORT))
    data = {
        "value": num,
    }
    content = ('GET / HTTP/1.1\n\n')
    content += dumps(data)
    sock.send(content.encode())

    Response = read_from_socket(sock).decode()
    parsedResponse = (parser(Response))
    print('-' * 40 + '\n')
    print(parsedResponse)
    value = loads(parsedResponse[2])["response"]
    print(f'Value: {value}')
    sock.close()
