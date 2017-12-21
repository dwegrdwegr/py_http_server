import my_utility
import http_response

login_html = """<!DOCTYPE html>
                <html>
                    <head>
                        <link rel=\"shorcut icon\" href=\"data:image/x-icon;,\" type=\"image/x-icon\">
                    </head>
                    <body>
                        <h1>Login</h1>
                        <form action=\"/login.html\" method=\"post\">"
                            Username:<br>"
                            <input type=\"text\" name=\"username\"><br>
                            Password:<br>
                            <input type=\"password\" name=\"password\"><br><br>
                            <input type=\"submit\" value=\"Submit\">
                        </form>
                        {error}
                    </body>
                </html>
"""

hello_html = """<!DOCTYPE html>
                <html>
                    <head>
                        <link rel=\"shorcut icon\" href=\"data:image/x-icon;,\" type=\"image/x-icon\">
                    </head>
                    <body>
                        <h1>Welcome<h1>
                        Nice to see you {username}
                    </body>
                </html>"""

class http_request_get:
    def process(self):
        my_utility.check_timed_out_sessions()
        response = http_response()
        if self.url == "/login.html":
            cookie = self.headers.get("Cookie")
            if cookie == None:
                session = my_utility.get_session(cookie)
                if session == None:
                    response.http_version = "HTTP/1.1"
                    response.status_code = "200"
                    response.status_desc = "OK"
                    response.headers["Content-Type"] = "text/html; charset=UTF-8"
                    response.content = login_html.replace("{error}", "")
                    response.headers["Content-Length"] = str(len(response.content))
                else:
                    response.http_version = "HTTP/1.1"
                    response.status_code = "200"
                    response.status_desc = "OK"
                    response.headers["Content-Type"] = "text/html; charset=UTF-8"
                    response.content = hello_html.replace("{username}", session.username)
                    response.headers["Content-Length"] = str(len(response.content))
            else:
                response.http_version = "HTTP/1.1"
                response.status_code = "200"
                response.status_desc = "OK"
                response.headers["Content-Type"] = "text/html; charset=UTF-8"
                response.content = login_html.replace("{error}", "")
                response.headers["Content-Length"] = str(len(response.content))
        else:
            response.http_version = "HTTP/1.1"
            response.status_code = "404"
            response.status_desc = "Not found"
        return response




class http_request_post:
    def process(self):
        my_utility.check_timed_out_sessions()
        response = http_response()
        post = {}
        if self.url == "/login.html":
            temporary = self.content.split('&')
            for v in temporary:
                keyvalue = v.split('=')
                key = keyvalue[0]
                value = keyvalue[1]
                post[key] = value
            username = post.get("username")
            if username == None:
                response.http_version = "HTTP/1.1"
                response.status_code = "400"
                response.status_desc = "Bad request"
            else:
                user = my_utility.users.get(username)
                if user == None:
                    response.http_version = "HTTP/1.1"
                    response.status_code = "400"
                    response.status_desc = "User not found"
                    response.headers["Content-Type"] = "text/html; charset=UTF-8"
                    response.content = login_html.replace("{error}", "User not found")
                    response.headers["Content-Length"] = str(len(response.content))
                else:
                    if user.password == post.get("password"):
                        response.http_version = "HTTP/1.1"
                        response.status_code = "200"
                        response.status_code = "OK"
                        response.headers["Content-Type"] = "text/html; charset=UTF-8"
                        response.content = hello_html.replace("{username}", user.name)
                        response.headers["Content-Length"] = str(len(response.content))
                        session_id = str(my_utility.generate_session_id())
                        response.headers["Set-Cookie"] = "id=" + session_id + "; Max-Age=" + str(my_utility.timeout)
                        new_session = my_utility.my_session( session_id, username )
                        my_utility.add_session(new_session)
                    else:
                        response.http_version = "HTTP/1.1"
                        response.status_code = "400"
                        response.status_desc = "Invalid password"
                        response.headers["Content-Type"] = "text/html; charset=UTF-8"
                        response.content = login_html.replace("{error}", "Invalid password")
                        response.headers["Content-Length"] = str(len(response.content))
        else:
            response.http_version = "HTTP/1.1"
            response.status_code = "404"
            response.status_desc = "Not found"
        return response


