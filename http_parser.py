import re
from http_requests import *

class http_parser:
    def parse(self, http_string):
        temporary = http_string.split('\n')
        header = temporary[0].split()
        #header = re.split(':|: ', line)
        request = http_request_get() if header[0] == "GET" else http_request_post()
        request.method = header[0]
        request.url = header[1]
        request.http_version = header[2]
        request.headers = {}
        request.content = []
        for i in len(temporary):
            if temporary[i] == "\r":
                break
            header = re.split(':|: ', temporary[i])
            if header[1][-1] == '\r':
                header[1] = header[1][:-1]

            request.headers[header[0]] = header[1]

        i += 1
        while i < len(temporary):
            request.content.append(temporary[i])

        return request

