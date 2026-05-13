from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

#tworzenie aplikacji
app = FastAPI(
    title="Notes API",
    version="1.0"
)
templates = Jinja2Templates(directory="templates") #konfiguracja folderu z HTML



notes = [ #prosta lista notatek w pamięci programu
    {
        "id": 1,
        "title": "Pierwsza notatka",
        "content": "To jest przykładowa notatka"
    }
]


# model do tworzenia notatki
class NoteCreate(BaseModel):
    title: str
    content: str


#------------------------------------------ strona główna HTML------------------------------------------
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "notes": notes
        }
    )


#------------------------------------------ pobieranie wszystkich notatek------------------------------------------
@app.get("/api/notes")
def get_notes():
    return notes


# ------------------------------------------dodawanie nowej notatki------------------------------------------
@app.post("/api/notes")
def create_note(data: NoteCreate):
    new_note = {
        "id": len(notes) + 1,
        "title": data.title,
        "content": data.content
    }

    notes.append(new_note)

    return new_note