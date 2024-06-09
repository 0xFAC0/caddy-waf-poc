#!/bin/env python3

import os
import socket
import json
import requests

PORT=9191 # TODO ENV
BIND_ADDR="172.17.0.1" # TODO ENV

BUFFER_SIZE=4096

def server():
    if not os.environ["WEFREI_API_KEY"]:
        print(f"Please specify API_KEY environnement variable")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((BIND_ADDR, PORT))
    print(f"listener binded to {BIND_ADDR}:{PORT}")
    s.listen()

    while True:
        conn, addr = s.accept()
        if not conn:
            print(f"accept() -> nil, quitting")
            break
        print(f"new client: addr={addr}")
        data = b''
        while True:
            chunk = conn.recv(BUFFER_SIZE)
            if not chunk:
                continue
            data += chunk
            print(f'recv chunk..')
            try:
                fmt_data = json.loads(data)
            except Exception as e:
                print(f"could not parse data chunk: {e}\ndata chunk:\n{data}")
                continue

            print(f"new log entry:\n{fmt_data}")
            r = requests.post(
                "http://192.168.10.3/api/logs",
                headers={
                    'content-type':'application/json',
                    'API_KEY': os.environ["WEFREI_API_KEY"]
                    },
                data=json.dumps(fmt_data)
                )
            print(f"srv res: {r.status_code} {r.text}")
            data = b''


if __name__ == "__main__":
    server()