import threading
from socket import socket, AF_INET, SOCK_STREAM, SO_RCVBUF, SOL_SOCKET
from json import dumps, loads
from threading import Thread
import time

HOST = 'localhost'
PORT = 8080
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


def request_to_server(num: int):
    sock = socket(AF_INET, SOCK_STREAM)

    sock.connect((HOST, PORT))
    if num == 5:
        time.sleep(5)


    request_payload = dumps(num) + '\n'


    request_raw = request_payload.encode(CODING)
    sock.send(request_raw)
    payload_raw = read_from_socket(sock)
    decode_payload_faw = payload_raw.decode(CODING)

    payload = loads(decode_payload_faw)
    sock.close()

    print(f"Receive: {num}, {payload}")


def main() -> None:
    threads = []
    for i in range(1, 15):
        t = Thread(target=request_to_server, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
