from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime


DATA_STORE = {
    "items": [
        {"id": 1, "name": "Item One", "value": 100},
        {"id": 2, "name": "Item Two", "value": 200},
        {"id": 3, "name": "Item Three", "value": 300},
    ]
}


def send_response(handler, status, data):
    body = json.dumps(data, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def parse_body(handler):
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


class APIHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"[{datetime.now().isoformat()}] {fmt % args}")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/")
        params = urllib.parse.parse_qs(parsed.query)

        if path == "/health":
            send_response(self, 200, {"status": "ok", "timestamp": datetime.now().isoformat()})

        elif path == "/items":
            items = DATA_STORE["items"]
            if "name" in params:
                name_filter = params["name"][0].lower()
                items = [i for i in items if name_filter in i["name"].lower()]
            send_response(self, 200, {"items": items, "count": len(items)})

        elif path.startswith("/items/"):
            try:
                item_id = int(path.split("/")[-1])
                item = next((i for i in DATA_STORE["items"] if i["id"] == item_id), None)
                if item:
                    send_response(self, 200, item)
                else:
                    send_response(self, 404, {"error": f"Item {item_id} not found"})
            except ValueError:
                send_response(self, 400, {"error": "Invalid item ID"})

        else:
            send_response(self, 404, {"error": "Route not found"})

    def do_POST(self):
        path = self.path.rstrip("/")

        if path == "/items":
            body = parse_body(self)
            if "name" not in body or "value" not in body:
                send_response(self, 400, {"error": "Fields 'name' and 'value' are required"})
                return
            new_id = max((i["id"] for i in DATA_STORE["items"]), default=0) + 1
            new_item = {"id": new_id, "name": str(body["name"]), "value": body["value"]}
            DATA_STORE["items"].append(new_item)
            send_response(self, 201, new_item)

        else:
            send_response(self, 404, {"error": "Route not found"})

    def do_PUT(self):
        path = self.path.rstrip("/")

        if path.startswith("/items/"):
            try:
                item_id = int(path.split("/")[-1])
                item = next((i for i in DATA_STORE["items"] if i["id"] == item_id), None)
                if not item:
                    send_response(self, 404, {"error": f"Item {item_id} not found"})
                    return
                body = parse_body(self)
                if "name" in body:
                    item["name"] = str(body["name"])
                if "value" in body:
                    item["value"] = body["value"]
                send_response(self, 200, item)
            except ValueError:
                send_response(self, 400, {"error": "Invalid item ID"})

        else:
            send_response(self, 404, {"error": "Route not found"})

    def do_DELETE(self):
        path = self.path.rstrip("/")

        if path.startswith("/items/"):
            try:
                item_id = int(path.split("/")[-1])
                item = next((i for i in DATA_STORE["items"] if i["id"] == item_id), None)
                if not item:
                    send_response(self, 404, {"error": f"Item {item_id} not found"})
                    return
                DATA_STORE["items"].remove(item)
                send_response(self, 200, {"deleted": item_id})
            except ValueError:
                send_response(self, 400, {"error": "Invalid item ID"})

        else:
            send_response(self, 404, {"error": "Route not found"})


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8080
    server = HTTPServer((HOST, PORT), APIHandler)
    print(f"Server running on http://{HOST}:{PORT}")
    print("Routes:")
    print("  GET    /health")
    print("  GET    /items")
    print("  GET    /items/<id>")
    print("  POST   /items")
    print("  PUT    /items/<id>")
    print("  DELETE /items/<id>")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
