import itertools
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

notes = []
note_ids = itertools.count(1)

def find_note(note_id):
    return next((n for n in notes if n["id"] == note_id), None)

@app.get("/")
def index():
    return "<h1>Гостевая книга</h1>"

@app.get("/notes")
def list_notes_filtered():
    author = request.args.get("author")
    limit = request.args.get("limit")
    offset = request.args.get("offset")

    filtered_notes = notes

    if author is not None:
        filtered_notes = [
            note for note in filtered_notes
            if note["author"] == author
        ]

    if offset is not None:
            filtered_notes = filtered_notes[int(offset):]

    if limit is not None:
        filtered_notes = filtered_notes[:int(limit)]

    return jsonify(filtered_notes)

@app.post("/notes")
def create_note():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400

    if "author" in data and not isinstance(data["author"], str) or not data["author"].strip():
        return jsonify(error="field 'author' must be a non-empty string"), 400

    note = {"id": next(note_ids), "author": data.get("author"), "text": data.get("text").strip()}
    notes.append(note)
    return jsonify(note), 201

@app.put("/notes/<int:note_id>")
def update_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' is required"), 400

    if "author" in data and not isinstance(data["author"], str) or not data["author"].strip():
        return jsonify(error="field 'author' must be a non-empty string"), 400

    note["text"] = data["text"].strip()
    if "author" in data:
        note["author"] = data["author"].strip()
    return jsonify(note)

@app.patch("/notes/<int:note_id>")
def patch_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON object is required"), 400

    if "text" in data:
        if not isinstance(data["text"], str) or not data["text"].strip():
            return jsonify(error="field 'text' is required"), 400
        note["text"] = data["text"].strip()

    if "author" in data:
        if not isinstance(data["author"], str) or not data["author"].strip():
            return jsonify(error="field 'author' must be a non-empty string"), 400
        note["author"] = data["author"].strip()

    return jsonify(note)

@app.get("/notes/<int:note_id>")
def get_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    return jsonify(note)

@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    notes.remove(note)
    return "", 204

@app.errorhandler(404)
def not_found(error):
    return jsonify(error="not found"), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error="method not allowed"), 405

if __name__ == "__main__":
    app.run(debug=True)