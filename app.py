import os
from flask import Flask, render_template, request, redirect, url_for, abort
import markdown

app = Flask(__name__)
NOTES_DIR = os.path.join(os.path.dirname(__file__))

def list_notes():
    return sorted([f for f in os.listdir(NOTES_DIR) if f.endswith('.md')])

@app.route('/')
def index():
    notes = list_notes()
    return render_template('index.html', notes=notes)

@app.route('/view/<path:filename>')
def view_note(filename):
    filepath = os.path.join(NOTES_DIR, filename)
    if not os.path.isfile(filepath):
        abort(404)
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    html = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    return render_template('view.html', content=html, filename=filename)

@app.route('/edit/<path:filename>', methods=['GET', 'POST'])
def edit_note(filename):
    filepath = os.path.join(NOTES_DIR, filename)
    if not os.path.isfile(filepath):
        abort(404)
    if request.method == 'POST':
        content = request.form.get('content', '')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return redirect(url_for('view_note', filename=filename))
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('edit.html', content=content, filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=82, debug=False)
