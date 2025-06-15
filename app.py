import os
from flask import Flask, render_template, request, redirect, url_for, abort
import markdown

app = Flask(__name__)
NOTES_DIR = os.path.join(os.path.dirname(__file__))

def list_dir(rel_path=''):
    abs_path = os.path.join(NOTES_DIR, rel_path)
    if not os.path.isdir(abs_path):
        abort(404)
    entries = []
    for name in sorted(os.listdir(abs_path)):
        full = os.path.join(abs_path, name)
        if os.path.isdir(full):
            entries.append({'type': 'dir', 'name': name, 'path': os.path.join(rel_path, name).replace('\\', '/')})
        elif name.endswith('.md'):
            entries.append({'type': 'file', 'name': name, 'path': os.path.join(rel_path, name).replace('\\', '/')})
    return entries

@app.route('/')
def index():
    entries = list_dir('')
    return render_template('browse.html', entries=entries, current_path='')

@app.route('/browse/<path:subpath>')
def browse(subpath):
    entries = list_dir(subpath)
    return render_template('browse.html', entries=entries, current_path=subpath)

@app.route('/view/<path:filename>')
def view_note(filename):
    path = os.path.join(NOTES_DIR, filename)
    if not os.path.isfile(path):
        abort(404)
    text = open(path, encoding='utf-8').read()
    html = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    return render_template('view.html', content=html, filename=filename)

@app.route('/edit/<path:filename>', methods=['GET', 'POST'])
def edit_note(filename):
    path = os.path.join(NOTES_DIR, filename)
    if not os.path.isfile(path):
        abort(404)
    if request.method == 'POST':
        open(path, 'w', encoding='utf-8').write(request.form['content'])
        return redirect(url_for('view_note', filename=filename))
    text = open(path, encoding='utf-8').read()
    return render_template('edit.html', content=text, filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=82, debug=False)
