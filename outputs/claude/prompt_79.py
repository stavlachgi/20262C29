from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Echo</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --ink: #1a1208;
    --paper: #f5f0e8;
    --cream: #ede8dc;
    --rust: #c0392b;
    --gold: #b8860b;
    --shadow: rgba(26,18,8,0.15);
  }

  body {
    background: var(--paper);
    background-image:
      repeating-linear-gradient(0deg, transparent, transparent 27px, rgba(26,18,8,0.04) 27px, rgba(26,18,8,0.04) 28px);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Courier Prime', monospace;
    padding: 2rem;
  }

  .card {
    background: var(--cream);
    border: 1px solid rgba(26,18,8,0.2);
    border-radius: 2px;
    padding: 3rem 3.5rem;
    width: 100%;
    max-width: 620px;
    box-shadow: 4px 4px 0 var(--ink), 8px 8px 0 rgba(26,18,8,0.1);
    position: relative;
    animation: arrive 0.4s ease both;
  }

  @keyframes arrive {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .card::before {
    content: '';
    position: absolute;
    top: 0; left: 2.5rem;
    width: 60px; height: 3px;
    background: var(--rust);
  }

  h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    color: var(--ink);
    letter-spacing: -0.5px;
    margin-bottom: 0.25rem;
  }

  .subtitle {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: var(--gold);
    margin-bottom: 2.4rem;
  }

  label {
    display: block;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: var(--ink);
    opacity: 0.6;
    margin-bottom: 0.5rem;
  }

  textarea {
    width: 100%;
    min-height: 110px;
    background: var(--paper);
    border: 1px solid rgba(26,18,8,0.25);
    border-radius: 1px;
    padding: 0.85rem 1rem;
    font-family: 'Courier Prime', monospace;
    font-size: 1rem;
    color: var(--ink);
    resize: vertical;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  textarea:focus {
    border-color: var(--rust);
    box-shadow: 0 0 0 3px rgba(192,57,43,0.1);
  }

  button {
    margin-top: 1.2rem;
    background: var(--ink);
    color: var(--paper);
    font-family: 'Courier Prime', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    border: none;
    padding: 0.85rem 2rem;
    cursor: pointer;
    transition: background 0.18s, transform 0.1s;
    position: relative;
  }

  button::after {
    content: '';
    position: absolute;
    bottom: -3px; right: -3px;
    width: 100%; height: 100%;
    border: 1px solid var(--ink);
    pointer-events: none;
  }

  button:hover { background: var(--rust); }
  button:active { transform: translate(2px, 2px); }
  button:active::after { bottom: -1px; right: -1px; }

  .output-section {
    margin-top: 2.5rem;
    padding-top: 2rem;
    border-top: 1px dashed rgba(26,18,8,0.2);
    animation: arrive 0.35s ease both;
  }

  .output-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: var(--rust);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .output-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--rust);
    opacity: 0.3;
  }

  .output-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    line-height: 1.75;
    color: var(--ink);
    white-space: pre-wrap;
    word-break: break-word;
  }

  .char-count {
    font-size: 0.7rem;
    color: var(--ink);
    opacity: 0.4;
    margin-top: 0.6rem;
    text-align: right;
  }
</style>
</head>
<body>
<div class="card">
  <h1>Echo</h1>
  <p class="subtitle">Type &amp; Transmit</p>

  <form method="POST" action="/">
    <label for="user_input">Your Message</label>
    <textarea id="user_input" name="user_input" placeholder="Write anything…" autofocus>{{ input_text or '' }}</textarea>
    <button type="submit">Transmit &#8594;</button>
  </form>

  {% if output_text %}
  <div class="output-section">
    <div class="output-label">Received</div>
    <p class="output-text">{{ output_text }}</p>
    <p class="char-count">{{ output_text | length }} characters</p>
  </div>
  {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output_text = None
    input_text = None
    if request.method == "POST":
        input_text = request.form.get("user_input", "")
        output_text = input_text if input_text.strip() else None
    return render_template_string(HTML, output_text=output_text, input_text=input_text)

if __name__ == "__main__":
    app.run(debug=True)
