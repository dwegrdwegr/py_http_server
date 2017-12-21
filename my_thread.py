import threading
import http_parser
import http_response

class my_thread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        parser = http_parser.http_parser()
        while True:
            socket, data = self.queue.pop()
            try:
                request = parser.parse(data)
                response = request.process()
            except:
                response = http_response.generate_bad_request()
            finally:
                socket.send(str(response))