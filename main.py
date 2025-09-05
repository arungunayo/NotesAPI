from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import subprocess
import os

app = FastAPI()

# Path to the tools exe
TOOLS = "./tools.exe" if os.name == "nt" else "./tools"

# Database init
conn = sqlite3.connect("notes.db", check_same_thread=False)
cursor = conn.cursor()
# creating a table if not already init
cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)")
conn.commit()

# Model init
class NoteIn(BaseModel):
    content: str
# creating a note
@app.post("/notes")
def create_note(note: NoteIn):
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (note.content,))
    conn.commit()
    note_id = cursor.lastrowid
    return {"id": note_id, "content": note.content}

# getting/extracting note from db
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "content": row[1]}
    return {"error": "Note not found"}

# word count from tools.exe
@app.get("/notes/{note_id}/wordcount")
def wordcount_note(note_id: int, shift: int = 3):
    cursor.execute("SELECT content FROM notes WHERE id=?", (note_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Note not found"}
    stored_content = row[0]

    try:
        # First, attempt to decrypt (in case it's encrypted)
        result = subprocess.run(
            [TOOLS, "decrypt", stored_content, str(shift)],
            capture_output=True,
            text=True,
            check=True
        )
        decrypted_content = result.stdout.strip()

        # If decrypted text is empty or invalid, fall back to original
        content_for_count = decrypted_content if decrypted_content else stored_content

        # Now run wordcount on decrypted/plaintext
        result_wc = subprocess.run(
            [TOOLS, "wordcount", content_for_count],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "id": note_id,
            "content": content_for_count,
            "word_count": int(result_wc.stdout.strip())
        }
    except Exception as e:
        return {"error": str(e)}


# encrypting through tools.exe
@app.get("/notes/{note_id}/encrypt")
def encrypt_note(note_id: int, shift: int = 3):
    cursor.execute("SELECT content FROM notes WHERE id=?", (note_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Note not found"}
    content = row[0]

    try:
        result = subprocess.run(
            [TOOLS, "encrypt", content, str(shift)],
            capture_output=True,
            text=True,
            check=True
        )
        encrypted = result.stdout.strip()

        # update database with encrypted content
        cursor.execute("UPDATE notes SET content=? WHERE id=?", (encrypted, note_id))
        conn.commit()

        return {"id": note_id, "original": content, "encrypted": encrypted, "message": "Note encrypted and saved"}
    except Exception as e:
        return {"error": str(e)}

# decrypting through tools.exe
@app.get("/notes/{note_id}/decrypt")
def decrypt_note(note_id: int, shift: int = 3, store: bool = False):
    cursor.execute("SELECT content FROM notes WHERE id=?", (note_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Note not found"}
    content = row[0]

    try:
        result = subprocess.run(
            [TOOLS, "decrypt", content, str(shift)],
            capture_output=True,
            text=True,
            check=True
        )
        decrypted = result.stdout.strip()

        if store:
            # update database with decrypted text
            cursor.execute("UPDATE notes SET content=? WHERE id=?", (decrypted, note_id))
            conn.commit()
            return {"id": note_id, "stored": True, "decrypted": decrypted}

        # just show decrypted text without updating DB
        return {"id": note_id, "stored": False, "decrypted": decrypted}
    except Exception as e:
        return {"error": str(e)}


# deleting notes
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    # deleting all them notes
    cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    row = cursor.fetchone()
    if not row:
        return {"error": "Note not found"}
    # specific delete from db
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    return {"message": f"Note {note_id} deleted successfully"}


