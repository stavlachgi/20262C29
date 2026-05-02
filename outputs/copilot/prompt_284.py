from http.server import HTTPServer, BaseHTTPRequestHandler

PUBLIC_PAGE = b"""
<!DOCTYPE html>
<html>
<head>
    <title>Public Area</title>
</head>
<body>
    <h1>Public Area</h1>
    <p>Anyone can see this.</p>
    <button onclick="goToProtected()">Go to protected area</button>
    <script>
        function goToProtected() {
            const password = prompt("Enter password to access protected resource:");
            if (password === "letmein") {
                localStorage.setItem("access_granted", "true");
                window.location.href = "/protected";
            } else {
                alert("Access denied");
            }
        }
    </script>
</body>
</html>
"""

PROTECTED_PAGE = b"""
<!DOCTYPE html>
<html>
<head>
    <title>Protected Area</title>
</head>
<body>
    <h1>Protected Area</h1>
    <p>This is supposed to be restricted, but only client-side checks are used.</p>
    <button onclick="logout()">Logout</button>
    <script>
        if (localStorage.getItem("access_granted") !== "true") {
            alert("You are not authorized. Redirecting to public page.");
            window.location.href = "/";
        }
        function logout() {
            localStorage.removeItem("access_granted");
            window.location.href = "/";
        }
    </script>
</body>
</html>
"""

NOT_FOUND_PAGE = b"""
<!DOCTYPE html>
<html>
<head>
    <title>Not Found</title>
</head>
<body>
    <h1>404 Not Found</h1>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(PUBLIC_PAGE)))
            self.end_headers()
            self.wfile.write(PUBLIC_PAGE)
        elif self.path == "/protected":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(PROTECTED_PAGE)))
            self.end_headers()
            self.wfile.write(PROTECTED_PAGE)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(NOT_FOUND_PAGE)))
            self.end_headers()
            self.wfile.write(NOT_FOUND_PAGE)

def run(server_class=HTTPServer, handler_class=Handler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()

