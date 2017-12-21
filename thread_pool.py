import threading
import multiprocessing
import my_thread

class ThreadPool(object):
    def __init__(self, work_queue):
        self.threads = []
        for i in range(multiprocessing.cpu_count()):
            self.threads.append(my_thread.my_thread(work_queue))

    def start_threads(self):
        for thread in self.threads:
            thread.start()

