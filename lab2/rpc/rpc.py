import constRPC
import time
import threading
import logging

from context import lab_channel

id = 0


class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self


class Client:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None
        self.ids = {}
        self.logger = logging.getLogger('vs2lab.rpc.Client')

    def run(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')
        t = threading.Thread(target=self.wait_for_reply)
        t.daemon = True
        t.start()

    def wait_for_reply(self):
        while True:
            id, data = self.chan.receive_from(self.server)[1]  # wait for response
            self.logger.info(f"Client got data for id {id}")
            if isinstance(data, str) and data == constRPC.OK:
                self.logger.info(f"Ack for {id}")
                continue

            if callback := self.ids.get(id):
                del self.ids[id]
                callback(data)


    def stop(self):
        self.chan.leave('client')

    def append(self, data, db_list, callback):
        global id
        assert isinstance(db_list, DBList)
        msglst = (constRPC.APPEND, data, db_list, id)  # message payload
        self.ids.update({id: callback})
        id += 1
        self.chan.send_to(self.server, msglst)  # send msg to server


class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3
        self.logger = logging.getLogger('vs2lab.rpc.Server')

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)

    def run(self):
        self.chan.bind(self.server)
        while True:
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                msgrpc = msgreq[1]  # fetch call & parameters
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    self.chan.send_to({client}, {msgrpc[3], constRPC.OK})
                    time.sleep(10)
                    self.logger.info("Server finished waiting")
                    self.chan.send_to({client}, {msgrpc[3], result})  # return response
                else:
                    pass  # unsupported request, simply ignore
