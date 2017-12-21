import threading
import queue

class thread_safe_queue:
    def __init__(self):
        self.cond_var = threading.Condition()
        self.queue = queue.deque()

    def pop(self):
        with self.cond_var:
            while len(self.queue) == 0:
                self.cond_var.wait()
            work = self.queue.pop()
            return work

    def push(self, work):
        with self.cond_var:
            self.queue.append(work)
            self.cond_var.notify()