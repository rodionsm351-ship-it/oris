import itertools
from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)
app.json.sort_keys = False

notes = []
note_ids = itertools.count(1)

def find_note(note_id):
    return next((n for n in notes if n["id"] == note_id), None)

def load_notes():
    try:
        with open("notes.json", "r", encoding="utf-8") as f:
            load_notes = json.load(f)
            
            max_id = max((note["id"] for note in load_notes), default=0)

        return load_notes, max_id

    except FileNotFoundError:
        return [], 0

def save_notes():
    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

@app.get("/")
def index():
    return "<h1>Гостевая книга</h1>"

@app.get("/notes")
def list_notes():
    author = request.args.get("author")
    limit = request.args.get("limit")
    offset = request.args.get("offset")

    sort_by = request.args.get("sort_by")
    order_by = request.args.get("order_by")

    filtered_notes = notes.copy()

    if author is not None:
        filtered_notes = [
            note for note in filtered_notes
            if note["author"] == author
        ]

    if offset is not None:
            filtered_notes = filtered_notes[int(offset):]

    if limit is not None:
        filtered_notes = filtered_notes[:int(limit)]

    if sort_by is not None:
        if sort_by == "id":
            filtered_notes = sorted(filtered_notes, key=lambda note: note["id"])
        elif sort_by == "likes":
            filtered_notes = sorted(filtered_notes, key=lambda note: note["likes"])
        else:
            return jsonify(error="invalid sort_by parameter"), 400

    if order_by is not None:
        if order_by == "desc":
            filtered_notes = list(reversed(filtered_notes))
        elif order_by == "asc":
            pass
        else:
            return jsonify(error="invalid order_by parameter"), 400

    return jsonify(filtered_notes)

@app.get("/notes/authors")
def list_authors():
    authors = []

    for note in notes:
        if note["author"] is not None and note["author"] not in [author["author"] for author in authors]:
            authors.append({"author": note["author"], "notes": 1, "likes": note["likes"]})
        elif note["author"] is not None:
            for author in authors:
                if author["author"] == note["author"]:
                    author["notes"] += 1
                    author["likes"] += note["likes"]
                    break
        
    authors = sorted(authors, key=lambda author: author["author"])

    return jsonify(authors)

@app.get("/notes/<int:note_id>")
def get_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    return jsonify(note)

@app.post("/notes")
def create_note():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify(error="field 'text' (non-empty string) is required"), 400

    if "author" in data and not isinstance(data["author"], str) or not data["author"].strip():
        return jsonify(error="field 'author' must be a non-empty string"), 400

    note = {"id": next(note_ids), "author": data.get("author"), "text": data.get("text").strip(), "likes": 0}
    
    notes.append(note)
    save_notes()

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
    save_notes()
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

    save_notes()
    return jsonify(note)


@app.post("/notes/<int:note_id>/like")
def like_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    note["likes"] += 1
    save_notes()
    return jsonify(note)


@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404)
    notes.remove(note)
    save_notes()
    return "", 204


@app.delete("/notes")
def delete_author_notes():
    author = request.args.get("author")

    deleted = 0

    if author is not None:
        for note in notes:
            if note["author"] == author:
                deleted += 1
                notes.remove(note)

    if author is None:
        return jsonify(error="author parameter is required"), 400

    save_notes()
    return jsonify(deleted=deleted), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify(error="not found"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error="method not allowed"), 405


if __name__ == "__main__":
    notes, max_id = load_notes()
    note_ids = itertools.count(max_id + 1)

    app.run(debug=True)