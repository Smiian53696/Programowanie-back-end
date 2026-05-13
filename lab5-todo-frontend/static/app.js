const form = document.getElementById("taskForm");
const editForm = document.getElementById("editForm");
const feedback = document.getElementById("feedback");
const taskList = document.getElementById("taskList");
const resultInfo = document.getElementById("resultInfo");
const pageInfo = document.getElementById("pageInfo");

let currentPage = 1;
let totalPages = 1;
const limit = 5;

let activeSearch = "";
let activeOnlyUndone = false;


// pokazanie komunikatu na 3 sekundy
function showMessage(text, type) {
    feedback.textContent = text;
    feedback.className = type;

    setTimeout(() => {
        feedback.textContent = "";
        feedback.className = "";
    }, 3000);
}


// budowanie adresu z filtrami
function buildTasksUrl() {
    const params = new URLSearchParams();

    params.append("page", currentPage);
    params.append("limit", limit);

    if (activeSearch) {
        params.append("search", activeSearch);
    }

    if (activeOnlyUndone) {
        params.append("done", "false");
    }

    return `/tasks/?${params.toString()}`;
}


// pobieranie i renderowanie zadań
async function loadTasks() {
    try {
        const res = await fetch(buildTasksUrl());

        if (!res.ok) {
            showMessage("Błąd pobierania zadań", "err");
            return;
        }

        const data = await res.json();

        totalPages = data.pages || 1;

        resultInfo.textContent = `Znaleziono ${data.total} wyników`;
        pageInfo.textContent = `Strona ${data.page} z ${totalPages}`;

        document.getElementById("prevBtn").disabled = data.page <= 1;
        document.getElementById("nextBtn").disabled = data.page >= totalPages;

        if (data.items.length === 0) {
            taskList.innerHTML = "<li>Brak zadań.</li>";
            return;
        }

        taskList.innerHTML = data.items.map(task => `
            <li id="task-${task.id}">
                <input 
                    type="checkbox" 
                    ${task.done ? "checked" : ""}
                    onchange="toggleTask(${task.id}, this.checked)"
                >

                <strong class="${task.done ? "done" : ""}">
                    ${task.title}
                </strong>

                <p>${task.description}</p>

                <button onclick="openEdit(${task.id}, '${escapeText(task.title)}', '${escapeText(task.description)}', ${task.done})">
                    Edytuj
                </button>

                <button onclick="deleteTask(${task.id})">
                    Usuń
                </button>
            </li>
        `).join("");

    } catch (error) {
        console.log(error);
        showMessage("Brak połączenia z serwerem", "err");
    }
}


// proste zabezpieczenie tekstu do HTML
function escapeText(text) {
    return String(text)
        .replaceAll("\\", "\\\\")
        .replaceAll("'", "\\'")
        .replaceAll("\n", " ");
}


// dodawanie zadania
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
        const body = {
            title: document.getElementById("title").value.trim(),
            description: document.getElementById("description").value.trim()
        };

        const res = await fetch("/tasks/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        if (res.status === 201) {
            showMessage("Dodano zadanie", "ok");
            form.reset();
            currentPage = 1;
            loadTasks();
        } else {
            showMessage("Błąd dodawania zadania", "err");
        }

    } catch (error) {
        console.log(error);
        showMessage("Brak połączenia z serwerem", "err");
    }
});


// zmiana statusu done
async function toggleTask(id, done) {
    try {
        const res = await fetch(`/tasks/${id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                done: done
            })
        });

        if (res.ok) {
            showMessage("Zmieniono status zadania", "ok");
            loadTasks();
        } else {
            showMessage("Błąd zmiany statusu", "err");
        }

    } catch (error) {
        console.log(error);
        showMessage("Brak połączenia z serwerem", "err");
    }
}


// usuwanie zadania
async function deleteTask(id) {
    try {
        const res = await fetch(`/tasks/${id}`, {
            method: "DELETE"
        });

        if (res.status === 204) {
            showMessage("Usunięto zadanie", "ok");
            loadTasks();
        } else {
            showMessage("Błąd usuwania zadania", "err");
        }

    } catch (error) {
        console.log(error);
        showMessage("Brak połączenia z serwerem", "err");
    }
}


// otwarcie panelu edycji
function openEdit(id, title, description, done) {
    document.getElementById("editId").value = id;
    document.getElementById("editTitle").value = title;
    document.getElementById("editDescription").value = description;
    document.getElementById("editDone").checked = done;

    document.getElementById("editPanel").style.display = "block";
}


// zamknięcie panelu edycji
function closeEdit() {
    document.getElementById("editPanel").style.display = "none";
    editForm.reset();
}


// zapis edycji
editForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
        const id = document.getElementById("editId").value;

        const body = {
            title: document.getElementById("editTitle").value.trim(),
            description: document.getElementById("editDescription").value.trim(),
            done: document.getElementById("editDone").checked
        };

        const res = await fetch(`/tasks/${id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            showMessage("Zapisano zmiany", "ok");
            closeEdit();
            loadTasks();
        } else {
            showMessage("Błąd edycji zadania", "err");
        }

    } catch (error) {
        console.log(error);
        showMessage("Brak połączenia z serwerem", "err");
    }
});


// szukanie
document.getElementById("searchBtn").addEventListener("click", () => {
    activeSearch = document.getElementById("searchInput").value.trim();
    activeOnlyUndone = document.getElementById("onlyUndone").checked;
    currentPage = 1;
    loadTasks();
});


// czyszczenie filtrów
document.getElementById("clearBtn").addEventListener("click", () => {
    document.getElementById("searchInput").value = "";
    document.getElementById("onlyUndone").checked = false;

    activeSearch = "";
    activeOnlyUndone = false;
    currentPage = 1;

    loadTasks();
});


// poprzednia strona
document.getElementById("prevBtn").addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        loadTasks();
    }
});


// następna strona
document.getElementById("nextBtn").addEventListener("click", () => {
    if (currentPage < totalPages) {
        currentPage++;
        loadTasks();
    }
});


// start aplikacji
loadTasks();