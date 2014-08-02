from pyWebSocket import WebSocketServer, WebSocketClient
import json


class ClientConnection(WebSocketClient):
    """
    manage client connections
    """

    def __init__(self, parent, sock, addr):
        """
        init the connection
        """
        self.username=""
        WebSocketClient.__init__(self, parent, sock, addr)


    def onReceive(self,msg):
        """
        receive handler
        """
        try:
            data = json.loads(msg)
        except ValueError as e:
            self.send(json.dumps({"error":3,"desc":str(e)}))
            return
        print(msg);


        if "username" in data:          #username change
            for client in self.parent.client:
                if client.username==data["username"]:
                    self.send(json.dumps({"error":0,"desc":"username already in use"}))
                    break
            else:
                if self.username:
                    self.parent.send2All(json.dumps({"user":self.username,"status":"logout"}))    
                self.username = data["username"]
                self.parent.send2All(json.dumps({"user":self.username,"status":"login"}))

        if "msg" in data:  
            if "to" in data:
                for dest in data["to"]:
                    for client in self.parent.client:
                        if client.username==dest:
                            client.send(json.dumps({"from":self.username,"msg":data["msg"],"private":True}))
            else:
                self.parent.send2All(json.dumps({"from":self.username,"msg":data["msg"],"private":False}))
        if "latLng" in data:  
            self.parent.send2All(json.dumps({"from":self.username,"latLng":data["latLng"],"private":False}))

        if "status" in data:
            self.parent.send2All(json.dumps({"user":self.username,"status":data["status"]}))
        if "logout" in data:
            self.onConnectionClose();

    def onConnectionClose(self):
        """
        connection closing handler
        """
        self.parent.send2All(json.dumps({"user":self.username,"status":"logout"}))
        print(json.dumps({"user":self.username,"status":"logout"}))
        for client in self.parent.client:
            if client.username==self.username: 
                del client
    

def factoryClient(conn, address):
    return ClientConnection(conn, address);
    
if __name__=="__main__":
    ws=WebSocketServer(clientClass=ClientConnection)
    ws.join()