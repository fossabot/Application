import socket

class Connection:
    client = None
    sendStream = None
    receivedReader = None

    def __init__(self, socketPort=5555):
        self.client = socket.socket()
        self.client.connect(('localhost', socketPort))
        self.client.settimeout(5)

        #self.sendStream = PrintStream(client.getOutputStream())
        #self.receivedReader = BufferedReader(InputStreamReader(client.getInputStream()))

    def send(self, message):
        self.client.send(message)
        #received = self.client.recv(1024)
        print("Sended: " + message)
        #print("Received: " + received)

        return received
