from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'notes.db'


# Initialize Database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# Home Route
@app.route('/')
def home():
    return render_template('index.html')


# Add Note
@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.json
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Note cannot be empty'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO notes (content) VALUES (?)',
        (content,)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Note added successfully'})


# Get Notes
@app.route('/get_notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM notes ORDER BY id DESC')
    notes = cursor.fetchall()

    conn.close()

    notes_list = [
        {'id': note[0], 'content': note[1]}
        for note in notes
    ]

    return jsonify(notes_list)


# Edit Note
@app.route('/edit_note/<int:note_id>', methods=['PUT'])
def edit_note(note_id):
    data = request.json
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content cannot be empty'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        'UPDATE notes SET content = ? WHERE id = ?',
        (content, note_id)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Note updated successfully'})


# Delete Note
@app.route('/delete_note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        'DELETE FROM notes WHERE id = ?',
        (note_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Note deleted successfully'})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)