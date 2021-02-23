from socket import socket, AF_INET, SOCK_STREAM, SO_RCVBUF, SOL_SOCKET
from threading import Thread
from json import dumps, loads
import sys

HOST = 'localhost'
PORT = 8080
QUEUE_LEN = 10
CODING = "utf-8"


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


def handler(client_socket, client_info, key):
    raw_message = read_from_socket(client_socket)
    message = raw_message.decode(CODING)
    payload = loads(message)
    if payload["key"] == key:

        print(f"Receive from: {client_info}, payload: {payload['value']}")

        result = str(2 * int(payload["value"]) / 13)
        data = {
            "response": result,
        }
        string_result = dumps(data)
        raw_payload = string_result.encode(CODING)
        client_socket.send(raw_payload)

    client_socket.close()


def main(key) -> None:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(QUEUE_LEN)
    while True:
        (client_socket, client_info) = sock.accept()
        t = Thread(target=handler, args=(client_socket, client_info, key,))
        t.start()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You should provide key as first argument")
        sys.exit(1)

    secret_key = sys.argv[1]
    main(key=secret_key)
