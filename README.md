# 📝 Notes API with FastAPI + C Tools

This project is a **FastAPI-based Notes application** that integrates with a custom **C executable (`tools.c`)** for:
- Word counting  
- Caesar cipher encryption  
- Caesar cipher decryption  

Notes are stored in a **SQLite database**.  
Encryption/decryption is handled by the compiled C program (`tools.exe` on Windows / `tools` on Linux/macOS).  

---

## ⚡ Features
- **Create Notes** → store plaintext notes  
- **Get Notes** → retrieve stored notes by ID  
- **Encrypt Notes** → encrypt and store the encrypted version  
- **Decrypt Notes** → view decrypted text, or store decrypted version back into the database  
- **Word Count** → count words in a note (decrypted first if encrypted)  
- **Delete Notes** → remove specific notes or clear the entire database  

---

## 📂 Project Structure
```
project/
│── main.py          # FastAPI app
│── tools.c          # C code with wordcount/encrypt/decrypt
│── tools.exe        # Compiled C program (Windows)
│── notes.db         # SQLite database (auto-created)
│── README.md        # Documentation
```

---

## 🛠️ Setup & Run

### 1. Clone Repository
```bash
git clone https://github.com/arungunayo/NotesAPI.git
cd NotesAPI
```

### 2. Install Python Dependencies
```bash
pip install fastapi uvicorn pydantic
```

### 3. Compile the C Tools
**On Linux/macOS:**
```bash
gcc tools.c -o tools
```

**On Windows (MinGW):**
```bash
gcc tools.c -o tools.exe
```

### 4. Run the FastAPI Server
```bash
uvicorn main:app --reload
```

Server will start at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)  

Interactive API docs:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

---

## 🔗 API Endpoints

### Notes Management
- `POST   /notes` → create a new note  
- `GET    /notes/{id}` → fetch a note by ID  
- `DELETE /notes/{id}` → delete a specific note  
- `DELETE /notes` → clear all notes  

### Encryption / Decryption
- `GET /notes/{id}/encrypt?shift=3` → encrypt note and update DB  
- `GET /notes/{id}/decrypt?shift=3&store=false` → decrypt note but don’t update DB  
- `GET /notes/{id}/decrypt?shift=3&store=true` → decrypt note and store plaintext back in DB  

### Word Count
- `GET /notes/{id}/wordcount?shift=3` → get word count of decrypted note  

---

## 🧪 Example Usage with `curl`

### Create a Note
```bash
curl -X POST "http://127.0.0.1:8000/notes"      -H "Content-Type: application/json"      -d '{"content":"This is my first note"}'
```

### Get a Note
```bash
curl -X GET "http://127.0.0.1:8000/notes/1"
```

### Encrypt a Note
```bash
curl -X GET "http://127.0.0.1:8000/notes/1/encrypt?shift=3"
```

### Decrypt a Note (show only)
```bash
curl -X GET "http://127.0.0.1:8000/notes/1/decrypt?shift=3&store=false"
```

### Decrypt a Note (and store plaintext back)
```bash
curl -X GET "http://127.0.0.1:8000/notes/1/decrypt?shift=3&store=true"
```

### Word Count of a Note
```bash
curl -X GET "http://127.0.0.1:8000/notes/1/wordcount?shift=3"
```

### Delete a Specific Note
```bash
curl -X DELETE "http://127.0.0.1:8000/notes/1"
```

### Clear All Notes
```bash
curl -X DELETE "http://127.0.0.1:8000/notes"
```

---
