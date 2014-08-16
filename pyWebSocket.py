import socket, threading, hashlib, base64, select

SOCKET_PORT = 9876

class WebSocketServer(threading.Thread):
    """
    A server receiving connection for websocket
    """
    
    def __init__(self,clientClass):
        """
        init the WebSocket Server
        """
        #assert isinstance(clientClass,WebSocketClient)
        
        print("Initializing WebSocket server...")
        threading.Thread.__init__(self)
        self.daemon = True
        self.clientClass=clientClass
        self.__webSock = socket.socket()
        self.__webSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__webSock.bind(('', SOCKET_PORT))
        self.__webSock.listen(5)
        self.client = []
        self.keepAlive = threading.Event()        
        self.start()
        print("WebSocket server initialized")

    def __del__(self):
        """
        destructor
        """
        print("destroying WebSocket")

    def stop(self):
        """
        stop the thread
        """
        print("Stopping WebSocket Thread...")
        self.keepAlive.clear()
        for client in self.client:
            client.stop()
        print("WebSocket Thread stopped")
    
    def run(self):
        """
        a thread receiving incoming websocket connection
        """
        self.keepAlive.set()

        while self.keepAlive.isSet():
            readable, writable, errors = select.select([self.__webSock],[],[])
            if readable == [self.__webSock]:
                conn, address = self.__webSock.accept()
                self.client.append(self.clientClass(self, conn, address))
                    
    def send2All(self,msg):
        """
        send a message to all opened client webSocket
        """

        for index, client in enumerate(self.client) :
            try:
                client.send(msg)
            except socket.error :
                self.client.pop(index)    

class WebSocketClient(threading.Thread):
    """
    A single connection (client) of the program
    """
    
    def __init__(self, parent, sock, addr):
        """
        init the client connection
        """
        self.parent = parent        
        threading.Thread.__init__(self)
        self.daemon = True
        self.__sock = sock
        self.__addr = addr
        self.keepAlive = threading.Event()
        self.__handshake()
        self.start()
        
    def __handshake(self):
        """
        handshake the client
        """
        data = self.__sock.recv(1024).decode("utf-8") #get the connection request
        
        data = data.split("\r\n")
        for i in data:
            if "Sec-WebSocket-Key" in i:
                break
                
        i = i.encode("ascii")+b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        hasher = hashlib.sha1()        
        key1 = i[len("Sec-WebSocket-Key: "):]
        hasher.update(key1)        
        key = base64.b64encode(hasher.digest()).decode("utf-8")
        handshake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\nUpgrade: WebSocket\r\nConnection: Upgrade\r\nWebSocket-Protocol: chat\r\nSec-WebSocket-Accept: "+str(key)+"\r\n\r\n"
        self.__sock.send(handshake.encode())
    
    def stop(self):
        """
        close the connection
        """
        self.keepAlive.clear()


    def run(self):
        """
        keep receiving data from the webSocket
        """
        self.keepAlive.set()
        while self.keepAlive.isSet():
            data = self.__sock.recv(1024)
            if not data: break
            self.__onreceive(data)
        self.onConnectionClose()

    def send(self, msg):
        """
        Send a message to this client
        """
        
        bytesFormatted=bytearray()
        bytesFormatted.append(129)
        
        indexStartRawData = -1

        if len(msg) <= 125:
            bytesFormatted.append(len(msg))
            indexStartRawData = 2

        elif len(msg) >= 126 and len(msg) <= 65535:
            bytesFormatted.append(126)
            bytesFormatted.append((len(msg) >> 8) & 255)
            bytesFormatted.append((len(msg)     ) & 255)
            indexStartRawData = 4

        else:
            bytesFormatted.append(127)
            bytesFormatted.append((len(msg) >> 56) & 255)
            bytesFormatted.append((len(msg) >> 48) & 255)
            bytesFormatted.append((len(msg) >> 40) & 255)
            bytesFormatted.append((len(msg) >> 32) & 255)
            bytesFormatted.append((len(msg) >> 24) & 255)
            bytesFormatted.append((len(msg) >> 16) & 255)
            bytesFormatted.append((len(msg) >>  8) & 255)
            bytesFormatted.append((len(msg)      ) & 255)
            indexStartRawData = 10

        # put raw data
        for val in msg:
            bytesFormatted.append(ord(val))
            
        self.__sock.send(bytesFormatted)

    def __onreceive(self, data):
        """
        Event called when a message is received from this client
        """

        secondByte = data[1]
        length = secondByte&127 # may not be the actual length in the two special cases

        indexFirstMask = 2 # if not a special case

        if length == 126: # the lenght is coded on two more bytes
            indexFirstMask = 4
        elif length == 127: # the lenght is coded on eight more bytes 
            indexFirstMask = 10 
            
        masks = data[indexFirstMask:indexFirstMask+4] # four bytes starting from indexFirstMask

        indexFirstDataByte = indexFirstMask + 4 # four bytes further

        decoded = '' #contain the decoded message

        j = 0
        for i in range(indexFirstDataByte,len(data)):
            unmasked = data[i]^masks[j%4] # the ^ is a xor
            decoded+=chr(unmasked)
            j+=1                        
        
        self.onReceive(decoded)

    def onReceive(self,msg):
        """
        receive handler
        """
        raise NotImplementedError

    def onConnectionClose(self):
        """
        connection closing handler
        """
        raise NotImplementedError

        
#if __name__=="__main__":
#    webSocketServer = WebSocketServer()
#    webSocketServer.join()

















        
