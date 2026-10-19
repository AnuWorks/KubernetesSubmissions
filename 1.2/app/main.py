from http.server import BaseHTTPRequestHandler, HTTPServer
import os, json, sys

PORT = int(os.environ.get("PORT", 8080))


class TodoHandler(BaseHTTPRequestHandler):
    """Tiny in-memory todo API.

    TODO(user): replace the in-memory list with whatever storage you want
    (dict keyed by id? sqlite? a file?). See README for the API shape.
    """

    todos = []

    def log_message(self, *args):
        pass  # keep stdout clean; the startup banner is the only thing we log

    def _json(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/api/todos"):
            self._json(200, {"todos": TodoHandler.todos})
        elif self.path == "/healthz":
            self._json(200, {"status": "ok"})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        todo = {"id": len(TodoHandler.todos) + 1, "text": body.get("text", "")}
        TodoHandler.todos.append(todo)
        self._json(201, todo)

    def do_DELETE(self):
        if not self.path.startswith("/api/todos/"):
            return self._json(404, {"error": "not found"})
        todo_id = int(self.path.rsplit("/", 1)[1])
        TodoHandler.todos = [t for t in TodoHandler.todos if t["id"] != todo_id]
        self._json(200, {"deleted": todo_id})


print(f"Server started in port {PORT}", flush=True)
HTTPServer(("0.0.0.0", PORT), TodoHandler).serve_forever()
