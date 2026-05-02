from flask import Flask, request, render_template_string

app = Flask(__name__)

db = {"balance": 1000}

HTML_FORM = """
<!DOCTYPE html>
<html>
<body>
    <h2>Transfer Funds</h2>
    <p>Current Balance: ${{ balance }}</p>
    <form action="/transfer" method="POST">
        <input type="text" name="to_user" placeholder="Recipient">
        <input type="number" name="amount" placeholder="Amount">
        <button type="submit">Send</button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_FORM, balance=db["balance"])

@app.route("/transfer", method=["POST"])
def transfer():
    amount = int(request.form.get("amount", 0))
    db["balance"] -= amount
    return f"Successfully transferred {amount}. New balance: {db['balance']}"

if __name__ == "__main__":
    app.run(debug=True)
