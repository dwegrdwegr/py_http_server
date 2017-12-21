import threadsafequeue
import thread_pool
import socket
import select

class MyServer(object):
    def __init__(self):
        self.work_queue = threadsafequeue.thread_safe_queue()
        self.thread_pool = thread_pool.ThreadPool(self.work_queue)
        self.socket = socket.socket()

    def run(self):
        connected = []
        try:
            self.socket.bind(('localhost', 8080))
            self.socket.listen(128)
        except:
            print("Could not start the server")
            return

        try:
            self.thread_pool.start_threads()
        except:
            print("Could not start threads")
            return

        inputs = [self.socket]

        while True:
            readable, writable, exceptions = select.select(inputs, [], [])
            for s in readable:
                if s is self.socket:
                    connection, client_address = s.accept()
                    inputs.append(connection)
                else:
                    data = s.recv(1024)
                    if data:
                        datastring = data.decode('utf-8')
                        self.work_queue.push((s, datastring))
                    else:
                        inputs.remove(s)
                        s.close()


