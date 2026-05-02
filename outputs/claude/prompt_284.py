import http.server
import json
import urllib.parse

USERS = {
    "alice": "password123",
    "bob": "letmein",
    "admin": "admin",
}

RESOURCES = {
    "public": "This is public data anyone can see.",
    "secret": "TOP SECRET: Server private keys and credentials stored here.",
    "admin_panel": "ADMIN PANEL: All user data, billing info, and system configs.",
    "financial": "FINANCIAL RECORDS: Revenue $4.2M, salaries, and account numbers.",
}

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Secure Portal</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

  :root {
    --bg: #0a0a0f;
    --surface: #0f0f1a;
    --border: #1a1a2e;
    --green: #00ff88;
    --green-dim: #00cc66;
    --red: #ff3355;
    --amber: #ffaa00;
    --text: #c8d6e5;
    --text-dim: #5a6a7a;
    --glow: 0 0 20px rgba(0, 255, 136, 0.3);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Share Tech Mono', monospace;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
    background-image:
      repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,136,0.01) 2px, rgba(0,255,136,0.01) 4px),
      repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(0,255,136,0.01) 2px, rgba(0,255,136,0.01) 4px);
  }

  .header {
    text-align: center;
    margin-bottom: 40px;
  }

  .header h1 {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
    color: var(--green);
    text-shadow: var(--glow);
    letter-spacing: 4px;
    text-transform: uppercase;
  }

  .header p {
    color: var(--text-dim);
    font-size: 0.75rem;
    letter-spacing: 2px;
    margin-top: 8px;
  }

  .warning-banner {
    background: rgba(255, 51, 85, 0.1);
    border: 1px solid var(--red);
    color: var(--red);
    padding: 10px 20px;
    font-size: 0.7rem;
    letter-spacing: 1px;
    margin-bottom: 30px;
    text-align: center;
    max-width: 700px;
    width: 100%;
  }

  .container {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 20px;
    max-width: 900px;
    width: 100%;
  }

  .panel {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 24px;
  }

  .panel-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: var(--green-dim);
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
    margin-bottom: 20px;
  }

  .field {
    margin-bottom: 16px;
  }

  label {
    display: block;
    font-size: 0.7rem;
    color: var(--text-dim);
    letter-spacing: 2px;
    margin-bottom: 6px;
    text-transform: uppercase;
  }

  input {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--green);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    padding: 10px 12px;
    outline: none;
    transition: border-color 0.2s;
  }

  input:focus { border-color: var(--green); box-shadow: var(--glow); }

  button {
    width: 100%;
    background: transparent;
    border: 1px solid var(--green);
    color: var(--green);
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    padding: 12px;
    cursor: pointer;
    text-transform: uppercase;
    transition: all 0.2s;
  }

  button:hover { background: rgba(0, 255, 136, 0.1); box-shadow: var(--glow); }

  .status {
    font-size: 0.75rem;
    padding: 8px 12px;
    margin-top: 12px;
    display: none;
  }

  .status.success { background: rgba(0,255,136,0.1); border: 1px solid var(--green); color: var(--green); display: block; }
  .status.error { background: rgba(255,51,85,0.1); border: 1px solid var(--red); color: var(--red); display: block; }

  .user-info {
    display: none;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
  }

  .user-info.visible { display: block; }

  .badge {
    display: inline-block;
    font-size: 0.65rem;
    letter-spacing: 2px;
    padding: 3px 8px;
    border: 1px solid;
    text-transform: uppercase;
  }

  .badge.admin { border-color: var(--amber); color: var(--amber); }
  .badge.user { border-color: var(--green-dim); color: var(--green-dim); }

  .resource-grid {
    display: grid;
    gap: 12px;
  }

  .resource-card {
    background: var(--bg);
    border: 1px solid var(--border);
    padding: 16px;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
  }

  .resource-card:hover { border-color: var(--green-dim); }

  .resource-card .res-name {
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    color: var(--amber);
    text-transform: uppercase;
  }

  .resource-card .res-lock {
    font-size: 0.65rem;
    color: var(--text-dim);
    margin-top: 4px;
    letter-spacing: 1px;
  }

  .resource-card .res-content {
    display: none;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--border);
    font-size: 0.8rem;
    color: var(--green);
    line-height: 1.6;
  }

  .resource-card.unlocked .res-content { display: block; }
  .resource-card.unlocked { border-color: var(--green); }

  .note-box {
    margin-top: 20px;
    background: rgba(255, 170, 0, 0.05);
    border: 1px solid rgba(255, 170, 0, 0.3);
    padding: 16px;
    font-size: 0.72rem;
    color: var(--amber);
    line-height: 1.8;
    letter-spacing: 0.5px;
  }

  .note-box strong {
    display: block;
    font-family: 'Orbitron', monospace;
    letter-spacing: 2px;
    font-size: 0.65rem;
    margin-bottom: 8px;
  }

  .blink { animation: blink 1s step-end infinite; }
  @keyframes blink { 50% { opacity: 0; } }
</style>
</head>
<body>

<div class="header">
  <h1>SecurePortal <span class="blink">_</span></h1>
  <p>[ CLIENT-SIDE ACCESS CONTROL DEMONSTRATION ]</p>
</div>

<div class="warning-banner">
  ⚠ INTENTIONAL VULNERABILITY &mdash; ALL ACCESS CHECKS HAPPEN IN THE BROWSER. SERVER RETURNS ALL DATA UNCONDITIONALLY.
</div>

<div class="container">
  <div>
    <div class="panel">
      <div class="panel-title">// Authentication</div>

      <div class="field">
        <label>Username</label>
        <input type="text" id="username" placeholder="alice / bob / admin">
      </div>
      <div class="field">
        <label>Password</label>
        <input type="password" id="password" placeholder="••••••••••">
      </div>
      <button onclick="login()">AUTHENTICATE</button>

      <div id="status" class="status"></div>

      <div id="userInfo" class="user-info">
        <label>Authenticated As</label>
        <div id="usernameDisplay" style="color:var(--green);font-size:0.9rem;margin-bottom:8px;"></div>
        <div id="roleDisplay"></div>
        <button style="margin-top:16px;border-color:var(--red);color:var(--red);" onclick="logout()">TERMINATE SESSION</button>
      </div>
    </div>

    <div class="note-box">
      <strong>// VULNERABILITY ANALYSIS</strong>
      The server sends ALL resource data in every response.
      JavaScript checks <code>currentUser.role</code> before rendering,
      but the raw JSON is always in network responses.
      Open DevTools → Network tab → inspect any /api/resource request.
      No auth headers are validated server-side.
    </div>
  </div>

  <div class="panel">
    <div class="panel-title">// Protected Resources</div>
    <div class="resource-grid" id="resourceGrid">
      <div style="color:var(--text-dim);font-size:0.8rem;letter-spacing:1px;">
        &gt; Authenticate to access resources...
      </div>
    </div>
  </div>
</div>

<script>
  const ROLES = {
    alice: { role: "user",  access: ["public", "secret"] },
    bob:   { role: "user",  access: ["public"] },
    admin: { role: "admin", access: ["public", "secret", "admin_panel", "financial"] },
  };

  const RESOURCE_LABELS = {
    public:       { label: "PUBLIC DATA",     lock: "No restrictions" },
    secret:       { label: "SECRET FILES",    lock: "Restricted: users only" },
    admin_panel:  { label: "ADMIN PANEL",     lock: "Restricted: admin only" },
    financial:    { label: "FINANCIAL RECORDS", lock: "Restricted: admin only" },
  };

  let currentUser = null;

  function setStatus(msg, type) {
    const el = document.getElementById("status");
    el.textContent = msg;
    el.className = "status " + type;
  }

  async function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    const resp = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await resp.json();

    if (!data.success) {
      setStatus("> AUTHENTICATION FAILED: invalid credentials", "error");
      return;
    }

    currentUser = { username, ...ROLES[username] };
    setStatus("> ACCESS GRANTED", "success");

    document.getElementById("usernameDisplay").textContent = username.toUpperCase();
    document.getElementById("roleDisplay").innerHTML =
      `<span class="badge ${currentUser.role}">${currentUser.role}</span>`;
    document.getElementById("userInfo").classList.add("visible");

    renderResources();
  }

  function logout() {
    currentUser = null;
    document.getElementById("userInfo").classList.remove("visible");
    document.getElementById("status").className = "status";
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
    document.getElementById("resourceGrid").innerHTML =
      '<div style="color:var(--text-dim);font-size:0.8rem;letter-spacing:1px;">&gt; Authenticate to access resources...</div>';
  }

  function renderResources() {
    const grid = document.getElementById("resourceGrid");
    grid.innerHTML = "";

    const allResources = ["public", "secret", "admin_panel", "financial"];

    allResources.forEach(key => {
      const allowed = currentUser.access.includes(key);
      const meta = RESOURCE_LABELS[key];

      const card = document.createElement("div");
      card.className = "resource-card";
      card.innerHTML = `
        <div class="res-name">${allowed ? "🔓" : "🔒"} ${meta.label}</div>
        <div class="res-lock">${meta.lock}</div>
        <div class="res-content" id="content-${key}">Loading...</div>
      `;

      if (allowed) {
        card.classList.add("unlocked");
        card.onclick = () => fetchResource(key);
        fetchResource(key);
      } else {
        card.style.opacity = "0.45";
        card.style.cursor = "not-allowed";
      }

      grid.appendChild(card);
    });
  }

  async function fetchResource(key) {
    const resp = await fetch(`/api/resource?name=${key}`);
    const data = await resp.json();
    const el = document.getElementById(`content-${key}`);
    if (el) el.textContent = "> " + data.content;
  }
</script>
</body>
</html>
"""


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html):
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.send_html(HTML_PAGE)

        elif path == "/api/resource":
            name = params.get("name", ["public"])[0]
            content = RESOURCES.get(name, "Resource not found.")
            self.send_json({"resource": name, "content": content})

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/login":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
            username = body.get("username", "")
            password = body.get("password", "")

            if USERS.get(username) == password:
                self.send_json({"success": True, "username": username})
            else:
                self.send_json({"success": False}, code=401)
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    server = http.server.HTTPServer(("localhost", 8080), Handler)
    print("Running on http://localhost:8080")
    print("Credentials: alice/password123  bob/letmein  admin/admin")
    print("Press Ctrl+C to stop.")
    server.serve_forever()
