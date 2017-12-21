import datetime
import threading
import sys

lock = threading.Lock()

class my_session:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.time = datetime.datetime.now()

TIMEOUT = 600
users = {}
sessions = []

def read_users():
    with open("users.txt") as f:
        for line in f:
            user = line.split()
            users[user[0]] = user[1]


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(id=0)
def generate_session_id():
    global lock
    lock.acquire()
    if generate_session_id.id == sys.maxsize:
        generate_session_id.id = 0
    else:
        generate_session_id.id += 1
    return generate_session_id.id

def get_session(cookie):
    global lock
    key_pair = cookie.split('&')
    temporary = key_pair[0].split('=')
    lock.acquire()
    for i in sessions:
        if i.id == temporary[1]:
            return i
    else:
        return None

def add_session(s):
    global lock
    lock.acquire()
    sessions.append(s)
    lock.release()

def check_timed_out_sessions():
    global lock
    now = datetime.datetime.now()
    lock.acquire()
    for i in range(len(sessions)):
        duration =  sessions[i].time - now
        if duration.seconds >= TIMEOUT:
            sessions.pop(i)
    lock.release()
