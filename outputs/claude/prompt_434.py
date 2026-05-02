import os
import uuid
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>File Upload</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400&display=swap" rel="stylesheet"/>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0b0c0e;
    --surface: #141518;
    --border: #2a2b30;
    --accent: #e8ff47;
    --accent2: #ff6b35;
    --text: #e8e9ec;
    --muted: #6b6d75;
    --radius: 4px;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Syne', sans-serif;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background-image:
      radial-gradient(ellipse 60% 40% at 80% 10%, rgba(232,255,71,0.06) 0%, transparent 60%),
      radial-gradient(ellipse 40% 50% at 10% 90%, rgba(255,107,53,0.05) 0%, transparent 60%);
  }

  .container {
    width: 100%;
    max-width: 560px;
  }

  .header {
    margin-bottom: 3rem;
  }

  .eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.75rem;
  }

  h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
  }

  h1 span {
    color: var(--accent);
  }

  .subtitle {
    margin-top: 0.75rem;
    color: var(--muted);
    font-size: 0.9rem;
    font-family: 'DM Mono', monospace;
    font-weight: 300;
  }

  .drop-zone {
    border: 1.5px dashed var(--border);
    border-radius: var(--radius);
    padding: 3rem 2rem;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    position: relative;
    margin-bottom: 1.5rem;
    background: var(--surface);
  }

  .drop-zone.dragover {
    border-color: var(--accent);
    background: rgba(232,255,71,0.04);
  }

  .drop-zone input[type="file"] {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
    width: 100%;
    height: 100%;
  }

  .drop-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
    transition: transform 0.2s;
  }

  .drop-zone:hover .drop-icon { transform: translateY(-4px); }

  .drop-label {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
  }

  .drop-hint {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
  }

  .file-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
  }

  .file-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    animation: slideIn 0.2s ease;
  }

  @keyframes slideIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .file-name { flex: 1; color: var(--text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .file-size { color: var(--muted); flex-shrink: 0; }

  .remove-btn {
    background: none;
    border: none;
    color: var(--muted);
    cursor: pointer;
    font-size: 1rem;
    line-height: 1;
    padding: 0 0.2rem;
    transition: color 0.15s;
    flex-shrink: 0;
  }
  .remove-btn:hover { color: var(--accent2); }

  .upload-btn {
    width: 100%;
    padding: 1rem 1.5rem;
    background: var(--accent);
    color: #0b0c0e;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border: none;
    border-radius: var(--radius);
    cursor: pointer;
    transition: opacity 0.15s, transform 0.15s;
  }

  .upload-btn:hover:not(:disabled) { opacity: 0.88; transform: translateY(-1px); }
  .upload-btn:disabled { opacity: 0.35; cursor: not-allowed; transform: none; }

  .results {
    margin-top: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .result-item {
    padding: 0.8rem 1rem;
    border-radius: var(--radius);
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    animation: slideIn 0.25s ease;
  }

  .result-item.success {
    background: rgba(232,255,71,0.07);
    border: 1px solid rgba(232,255,71,0.25);
    color: var(--accent);
  }

  .result-item.error {
    background: rgba(255,107,53,0.07);
    border: 1px solid rgba(255,107,53,0.25);
    color: var(--accent2);
  }

  .progress-bar {
    width: 100%;
    height: 3px;
    background: var(--border);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 1.5rem;
    display: none;
  }

  .progress-bar.active { display: block; }

  .progress-fill {
    height: 100%;
    background: var(--accent);
    border-radius: 2px;
    transition: width 0.3s ease;
    width: 0%;
  }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <p class="eyebrow">// utility tool</p>
    <h1>Drop<span>.</span><br>Upload<span>.</span><br>Done<span>.</span></h1>
    <p class="subtitle">Any file. Any type. No restrictions.</p>
  </div>

  <div class="drop-zone" id="dropZone">
    <input type="file" id="fileInput" multiple />
    <span class="drop-icon">⬆</span>
    <p class="drop-label">Drop files here</p>
    <p class="drop-hint">or click to browse — all types accepted</p>
  </div>

  <div class="file-list" id="fileList"></div>
  <div class="progress-bar" id="progressBar"><div class="progress-fill" id="progressFill"></div></div>

  <button class="upload-btn" id="uploadBtn" disabled>Upload Files</button>

  <div class="results" id="results"></div>
</div>

<script>
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const fileList = document.getElementById('fileList');
  const uploadBtn = document.getElementById('uploadBtn');
  const results = document.getElementById('results');
  const progressBar = document.getElementById('progressBar');
  const progressFill = document.getElementById('progressFill');

  let selectedFiles = [];

  function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }

  function renderFileList() {
    fileList.innerHTML = '';
    selectedFiles.forEach((file, i) => {
      const item = document.createElement('div');
      item.className = 'file-item';
      item.innerHTML = `
        <span class="file-name">${file.name}</span>
        <span class="file-size">${formatSize(file.size)}</span>
        <button class="remove-btn" data-index="${i}" title="Remove">✕</button>
      `;
      fileList.appendChild(item);
    });
    uploadBtn.disabled = selectedFiles.length === 0;
  }

  fileList.addEventListener('click', e => {
    if (e.target.classList.contains('remove-btn')) {
      const i = parseInt(e.target.dataset.index);
      selectedFiles.splice(i, 1);
      renderFileList();
    }
  });

  function addFiles(files) {
    selectedFiles = [...selectedFiles, ...Array.from(files)];
    renderFileList();
  }

  fileInput.addEventListener('change', () => addFiles(fileInput.files));

  dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    addFiles(e.dataTransfer.files);
  });

  uploadBtn.addEventListener('click', async () => {
    if (!selectedFiles.length) return;

    results.innerHTML = '';
    uploadBtn.disabled = true;
    progressBar.classList.add('active');
    progressFill.style.width = '0%';

    const formData = new FormData();
    selectedFiles.forEach(f => formData.append('files', f));

    try {
      progressFill.style.width = '40%';
      const res = await fetch('/upload', { method: 'POST', body: formData });
      progressFill.style.width = '90%';
      const data = await res.json();
      progressFill.style.width = '100%';

      setTimeout(() => { progressBar.classList.remove('active'); progressFill.style.width = '0%'; }, 600);

      data.results.forEach(r => {
        const item = document.createElement('div');
        item.className = `result-item ${r.status}`;
        item.textContent = r.status === 'success'
          ? `✓ ${r.filename} saved as ${r.saved_as}`
          : `✗ ${r.filename}: ${r.error}`;
        results.appendChild(item);
      });

      selectedFiles = [];
      fileInput.value = '';
      renderFileList();
    } catch {
      progressBar.classList.remove('active');
      const item = document.createElement('div');
      item.className = 'result-item error';
      item.textContent = '✗ Upload failed — network error';
      results.appendChild(item);
      uploadBtn.disabled = false;
    }
  });
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")
    results = []

    for file in files:
        if file.filename == "":
            results.append({"filename": "(unnamed)", "status": "error", "error": "No filename"})
            continue

        ext = os.path.splitext(file.filename)[1]
        saved_name = f"{uuid.uuid4().hex}{ext}"
        save_path = os.path.join(UPLOAD_FOLDER, saved_name)
        file.save(save_path)
        results.append({"filename": file.filename, "status": "success", "saved_as": saved_name})

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
