from socket import socket, AF_INET, SOCK_STREAM, SO_RCVBUF, SOL_SOCKET
from json import dumps, loads
from threading import Thread
import sys

HOST = 'localhost'
PORT = 8080
CODING = "utf-8"
NUMBER_OF_CONNECTIONS = 14


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


def request_to_server(num: int, key):
    sock = socket(AF_INET, SOCK_STREAM)

    sock.connect((HOST, PORT))

    data = {
        "key": key,
        "value": num,
    }

    request_payload = dumps(data) + '\n'

    request_raw = request_payload.encode(CODING)
    sock.send(request_raw)
    payload_raw = read_from_socket(sock)
    decode_payload_raw = payload_raw.decode(CODING)

    payload = loads(decode_payload_raw)

    sock.close()

    print(f"Receive: {num}, {payload['response']}")


def main(key) -> None:
    threads = []
    for i in range(NUMBER_OF_CONNECTIONS):
        t = Thread(target=request_to_server, args=(i, key,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You should provide key as first argument")
        sys.exit(1)

    secret_key = sys.argv[1]
    main(key=secret_key)
