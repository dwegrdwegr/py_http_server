class http_response:
    def __init__(self, content, http_v, status_code, status_desc):
        self.content = content
        self.http_v = http_v
        self.status_code = status_code
        self.status_desc = status_desc
        self.headers = {}

    def __str__(self):
        str = self.http_v + " " + self.status_code + " " + self.status_desc + "\r\n"
        if len(self.headers) != 0:
            for key, value in self.headers.items():
                str += key + ": " + value + "\r\n"

        str += "\r\n"
        str += self.content
        str += "\r\n\r\n"
        return str

def generate_bad_request():
    return http_response("","HTTP/1.1","400", "Bad request")