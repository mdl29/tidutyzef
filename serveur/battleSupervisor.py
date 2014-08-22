import threading

class BattleSupervisor(threading.Thread):

    def __init__(self,client1,client2,s):

        threading.Thread.__init__(self)
        self.daemon = True
        self.clientClass=clientClass
        self.belligerent = [client1,client2]
        self.keepAlive = threading.Event()
        self.start()

    def stop(self):

        self.keepAlive.clear()
        for client in self.client:
            client.stop()

    def run(self):
        self.keepAlive.set()

        while self.keepAlive.isSet():
