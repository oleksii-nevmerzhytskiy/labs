from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SHUT_RDWR
import select
from httpParser import parseHttpRequests as parser
from json import dumps, loads
import time

QUEUE_LEN = 14
HOST = 'localhost'
PORT = 8080

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'

serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serversocket.bind((HOST, PORT))
serversocket.listen(QUEUE_LEN)
serversocket.setblocking(False)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)

try:
    connections = {}
    requests = {}
    responses = {}
    while True:
        events = epoll.poll(1)
        for fileno, event in events:
            if fileno == serversocket.fileno():
                connection, address = serversocket.accept()
                connection.setblocking(False)
                epoll.register(connection.fileno(), select.EPOLLIN)

                connections[connection.fileno()] = connection

                requests[connection.fileno()] = b''

            elif event is select.EPOLLIN:
                requests[fileno] += connections[fileno].recv(1024)
                if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                    epoll.modify(fileno, select.EPOLLOUT)
                    print('-' * 40 + '\n')
                    payload = (parser(requests[fileno].decode()))
                    print(payload)
            elif event is select.EPOLLOUT:

                value = loads(payload[3])
                intValue = int(value["value"])
                result = str(2 * intValue / 13)
                data = {
                    "response": result,
                }
                jsonMessage = str(dumps(data))
                contentLength = str(len(jsonMessage))
                date = time.ctime()
                response = 'HTTP/1.1 200 OK\r\n'
                response += 'Date: ' + date + '\r\n'
                response += 'Content-Type: text/plain\r\n'
                response += 'Content-Length: ' + contentLength + '\r\n\r\n'
                response += jsonMessage

                responses[connection.fileno()] = response.encode()
                byteswritten = connections[fileno].send(responses[fileno])
                responses[fileno] = responses[fileno][byteswritten:]
                if len(responses[fileno]) == 0:
                    epoll.modify(fileno, 0)
                    connections[fileno].shutdown(SHUT_RDWR)
            elif event is select.EPOLLHUP:
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]
                del requests[fileno]
                del responses[fileno]

finally:
    epoll.unregister(serversocket.fileno())
    epoll.close()
    serversocket.close()
