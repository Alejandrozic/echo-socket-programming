"""
    Echo Server

    Developer for CS3622 Fundamentals of Data Communications class project.

    Assignment

    1) Reverse echo server
        A reverse echo server receives a message from a client over TCP socket 
        and replies the same message back to the source in reverse order. For 
        example, if a sever gets a message “GOOD” from a client, then the reverse 
        echo server sends back the message “DOOG” to the client. The server program 
        should be terminated if it gets “end” message from a client after it replies 
        “dne” message to the client. Note that please use port number over 5000.
"""

import types
import socket
import selectors
from typing import List, Tuple

#
# SERVER Class
#

class EchoServer:
    
    """
        Context Manager for a Echo Server.

        EXPECTED USAGE:
        
            with EchoServer(host='{ip}}', port= {port}) as es:
                while True:
                    events = es.has_events()
                    for key, mask in events:
                        if key.data is None:
                            es.accept(key.fileobj)
                        else:
                            es.process(key, mask)
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()
        self.sel_timeout = None

    def __enter__(self):
        """ Python Context Manager ENTER (ie. defines how to start a session) """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()
        print(f"[EchoServer] [LISTEN] {(self.host, self.port)}")
        self.sel.register(sock, selectors.EVENT_READ, data=None)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ Python Context Manager EXIT (ie. defines how to close a session) """
        self.sel.close()
        print('[EchoServer] [CLOSE]')

    def accept(
            self,
            sock: socket.socket,
        ) -> None:
        """ Accepts a connection request from a client. """
        conn, addr = sock.accept()
        print(f'[EchoServer] [ACCEPTED CONNECTION] from {addr}')
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)

    def has_events(self) -> List[Tuple[selectors.SelectorKey, int]]:
        """ Returns events if data is received from a client. """
        return self.sel.select(timeout=self.sel_timeout)

    def process(
            self,
            key: selectors.SelectorKey,
            mask: int,
        ) -> None:
        """ 
            Receives text data fromt a client, and respones to the client with the
            reverse of the text. Additionally, termiantes the client connection
            if the client sends 'end' text.
        """
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data.outb += recv_data
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                text_reversed = data.outb.decode('utf8')[::-1]
                text_reversed_bytes = str.encode(text_reversed)
                sent = sock.send(text_reversed_bytes)
                data.outb = data.outb[sent:]
                if text_reversed == 'dne':
                    self.sel.unregister(sock)
                    sock.close()
                    print(f'[EchoServer] [ACCEPTED CLOSE REQUEST]')


#
# SERVER DRVIER {run}
#

if __name__ == '__main__':
    # Connect using Custom Built Context Manager
    with EchoServer(host='127.0.0.1', port= 6000) as es:
        while True:
            events = es.has_events()
            for key, mask in events:
                if key.data is None:
                    # First request to CONNECT
                    es.accept(key.fileobj)
                else:
                    # Subsequent Requests to process data
                    es.process(key, mask)
