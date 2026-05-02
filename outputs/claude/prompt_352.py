from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "insecure-secret-key"

users = {
    "alice": {"password": "password123", "balance": 10000, "email": "alice@example.com"}
}

HTML_BASE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --ink: #0d0d0d;
    --paper: #f5f0e8;
    --red: #c0392b;
    --green: #1a7a4a;
    --gold: #b8860b;
    --border: 2px solid var(--ink);
    --shadow: 4px 4px 0 var(--ink);
  }
  body {
    background: var(--paper);
    color: var(--ink);
    font-family: 'DM Mono', monospace;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background-image: repeating-linear-gradient(
      0deg, transparent, transparent 39px, #d9d3c5 39px, #d9d3c5 40px
    );
  }
  .card {
    background: #fff;
    border: var(--border);
    box-shadow: var(--shadow);
    padding: 2.5rem;
    width: 100%;
    max-width: 480px;
  }
  h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    letter-spacing: -0.03em;
    margin-bottom: 0.25rem;
  }
  h2 {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.3rem;
    margin-bottom: 1.5rem;
    border-bottom: var(--border);
    padding-bottom: 0.75rem;
  }
  .subtitle {
    font-size: 0.75rem;
    opacity: 0.5;
    margin-bottom: 2rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }
  label {
    display: block;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 500;
    margin-bottom: 0.4rem;
    margin-top: 1.2rem;
  }
  input[type=text], input[type=password], input[type=number] {
    width: 100%;
    padding: 0.65rem 0.85rem;
    border: var(--border);
    background: var(--paper);
    font-family: 'DM Mono', monospace;
    font-size: 0.9rem;
    outline: none;
    transition: box-shadow 0.15s;
  }
  input:focus { box-shadow: var(--shadow); }
  button, .btn {
    display: inline-block;
    margin-top: 1.5rem;
    width: 100%;
    padding: 0.8rem 1rem;
    background: var(--ink);
    color: var(--paper);
    border: var(--border);
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.05em;
    cursor: pointer;
    box-shadow: var(--shadow);
    transition: transform 0.1s, box-shadow 0.1s;
    text-decoration: none;
    text-align: center;
  }
  button:hover, .btn:hover {
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0 var(--ink);
  }
  button:active, .btn:active {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0 var(--ink);
  }
  .btn-ghost {
    background: transparent;
    color: var(--ink);
    margin-top: 0.75rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    font-weight: 400;
  }
  .alert {
    padding: 0.75rem 1rem;
    border: var(--border);
    margin-bottom: 1.25rem;
    font-size: 0.85rem;
  }
  .alert-error { border-color: var(--red); color: var(--red); background: #fdf0ef; }
  .alert-success { border-color: var(--green); color: var(--green); background: #edf7f2; }
  .balance-box {
    background: var(--ink);
    color: var(--paper);
    padding: 1.25rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .balance-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.12em; opacity: 0.6; }
  .balance-amount { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.8rem; }
  .tag {
    display: inline-block;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 0.2rem 0.5rem;
    border: 1px solid var(--gold);
    color: var(--gold);
    margin-bottom: 1.5rem;
  }
  .nav { display: flex; gap: 0.75rem; margin-top: 0; }
  .nav .btn { margin-top: 0; flex: 1; font-size: 0.8rem; }
  .history { margin-top: 1.5rem; border-top: var(--border); padding-top: 1rem; }
  .history-item {
    display: flex; justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px dashed #ccc;
    font-size: 0.82rem;
  }
  .debit { color: var(--red); }
</style>
</head>
<body>
{% block body %}{% endblock %}
</body>
</html>
"""

LOGIN_PAGE = HTML_BASE.replace("{% block body %}{% endblock %}", """
<div class="card">
  <h1>SecureBank</h1>
  <p class="subtitle">Personal Banking Portal</p>
  <h2>Sign In</h2>
  {% if error %}
  <div class="alert alert-error">{{ error }}</div>
  {% endif %}
  <form method="POST" action="/login">
    <label>Username</label>
    <input type="text" name="username" placeholder="alice" required autofocus>
    <label>Password</label>
    <input type="password" name="password" placeholder="••••••••" required>
    <button type="submit">Log In →</button>
  </form>
</div>
""")

DASHBOARD_PAGE = HTML_BASE.replace("{% block body %}{% endblock %}", """
<div class="card">
  <h1>SecureBank</h1>
  <span class="tag">⚠ No CSRF Protection</span>
  <div class="balance-box">
    <div>
      <div class="balance-label">Available Balance</div>
      <div class="balance-amount">${{ balance }}</div>
    </div>
    <div style="font-size:0.75rem;opacity:0.5;">{{ username }}</div>
  </div>
  {% if message %}
  <div class="alert alert-{{ msg_type }}">{{ message }}</div>
  {% endif %}
  <h2>Transfer Funds</h2>
  <form method="POST" action="/transfer">
    <label>Recipient</label>
    <input type="text" name="recipient" placeholder="username or account" required>
    <label>Amount (USD)</label>
    <input type="number" name="amount" placeholder="0.00" min="1" required>
    <button type="submit">Send Transfer →</button>
  </form>
  <div class="history">
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">Recent Activity</div>
    {% for tx in transactions %}
    <div class="history-item">
      <span>→ {{ tx.recipient }}</span>
      <span class="debit">-${{ tx.amount }}</span>
    </div>
    {% endfor %}
    {% if not transactions %}
    <div style="font-size:0.8rem;opacity:0.4;padding:0.5rem 0;">No transactions yet.</div>
    {% endif %}
  </div>
  <div class="nav" style="margin-top:1.5rem;">
    <a class="btn btn-ghost" href="/logout">Log Out</a>
    <a class="btn" href="/change-email">Change Email</a>
  </div>
</div>
""")

CHANGE_EMAIL_PAGE = HTML_BASE.replace("{% block body %}{% endblock %}", """
<div class="card">
  <h1>SecureBank</h1>
  <span class="tag">⚠ No CSRF Protection</span>
  <h2>Change Email Address</h2>
  {% if message %}
  <div class="alert alert-{{ msg_type }}">{{ message }}</div>
  {% endif %}
  <p style="font-size:0.82rem;opacity:0.6;margin-bottom:0.5rem;">Current: <strong>{{ email }}</strong></p>
  <form method="POST" action="/change-email">
    <label>New Email Address</label>
    <input type="text" name="new_email" placeholder="new@example.com" required>
    <button type="submit">Update Email →</button>
  </form>
  <a class="btn btn-ghost" href="/dashboard">← Back to Dashboard</a>
</div>
""")

transactions = []


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username in users and users[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    return render_template_string(LOGIN_PAGE, title="Login — SecureBank", error=error)


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    user = users[username]
    message = session.pop("message", None)
    msg_type = session.pop("msg_type", "success")
    user_transactions = [t for t in transactions if t["from"] == username]
    return render_template_string(
        DASHBOARD_PAGE,
        title="Dashboard — SecureBank",
        username=username,
        balance=user["balance"],
        message=message,
        msg_type=msg_type,
        transactions=user_transactions[-5:][::-1],
    )


@app.route("/transfer", methods=["POST"])
def transfer():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    recipient = request.form.get("recipient", "").strip()
    try:
        amount = int(request.form.get("amount", 0))
    except ValueError:
        amount = 0

    if amount <= 0:
        session["message"] = "Invalid transfer amount."
        session["msg_type"] = "error"
    elif amount > users[username]["balance"]:
        session["message"] = "Insufficient funds."
        session["msg_type"] = "error"
    elif not recipient:
        session["message"] = "Recipient is required."
        session["msg_type"] = "error"
    else:
        users[username]["balance"] -= amount
        transactions.append({"from": username, "recipient": recipient, "amount": amount})
        session["message"] = f"Transferred ${amount} to {recipient}."
        session["msg_type"] = "success"

    return redirect(url_for("dashboard"))


@app.route("/change-email", methods=["GET", "POST"])
def change_email():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    message = None
    msg_type = "success"

    if request.method == "POST":
        new_email = request.form.get("new_email", "").strip()
        if new_email:
            users[username]["email"] = new_email
            message = f"Email updated to {new_email}."
        else:
            message = "Email cannot be empty."
            msg_type = "error"

    return render_template_string(
        CHANGE_EMAIL_PAGE,
        title="Change Email — SecureBank",
        email=users[username]["email"],
        message=message,
        msg_type=msg_type,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
