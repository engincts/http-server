import socket
import os
import mimetypes
import json
import threading

HOST, PORT = '0.0.0.0', 8080
STATIC_DIR = 'static'
ROUTES = {}


def route(path, method="GET"):
    def decorator(func):
        ROUTES[(method, path)] = func
        return func
    return decorator


def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'


def send_response(conn, status_code=200, content_type="text/plain", body="OK"):
    status_messages = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error",
        405: "Method Not Allowed"
    }
    status_text = status_messages.get(status_code, "Unknown")
    response = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body.encode())}\r\n\r\n" +
        body
    )
    conn.sendall(response.encode())


def render_template(file_path, context):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    for key, value in context.items():
        html = html.replace(f"{{{{ {key} }}}}", str(value))
    return html


@route("/api/hello", "GET")
def hello_handler():
    return 200, "application/json", json.dumps({"message": "Hello!"})

@route("/api/echo", "POST")
def echo_handler(body):
    try:
        data = json.loads(body)
        return 200, "application/json", json.dumps({"echo": data})
    except:
        return 500, "application/json", json.dumps({"error": "Invalid JSON"})


def handle_request(conn):
    try:
        request = conn.recv(1024).decode()
        if not request:
            return

        method, path, *_ = request.splitlines()[0].split()
        print(f"{method} {path}")

        headers, _, body = request.partition("\r\n\r\n")

        route_key = (method, path)
        if route_key in ROUTES:
            handler = ROUTES[route_key]
            if method == "POST":
                status, ctype, content = handler(body)
            else:
                status, ctype, content = handler()
            send_response(conn, status, ctype, content)
            return

        if method == "GET":
            if path == "/":
                path = "/index.html"
            file_path = os.path.join(STATIC_DIR, path.lstrip("/"))
            if not os.path.isfile(file_path):
                send_response(conn, 404, "text/html", "<h1>404 Not Found</h1>")
                return
            with open(file_path, 'rb') as f:
                content = f.read()
            mime_type = get_mime_type(file_path)
            headers = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {mime_type}\r\n"
                f"Content-Length: {len(content)}\r\n\r\n"
            ).encode()
            conn.sendall(headers + content)
        else:
            send_response(conn, 405, "text/plain", "Method Not Allowed")

    except Exception as e:
        send_response(conn, 500, "text/plain", f"Server Error: {str(e)}")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on http://{HOST}:{PORT}")
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_request, args=(conn,))
            thread.start()

if __name__ == "__main__":
    start_server()
