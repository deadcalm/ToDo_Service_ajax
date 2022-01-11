const form = document.querySelector('#form-add-todo');
const titleInput = document.querySelector('#title-input');
const descriptionInput = document.querySelector('#description-input');
const todosList = document.querySelector('#todos');

const filterTitle = document.querySelector('#filterTitle');
const filterDone = document.querySelector('#filterDone');

const error = document.createElement('div');
error.classList.add('alert', 'alert-danger');
error.style.display = "None";
form.insertBefore(error, form.firstChild);
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    error.style.display = "None";
    try {
        const response = await fetch('/api/todos/add_todo', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: titleInput.value,
                description: descriptionInput.value,
            }),
        });
        if (!response.ok) {
            error.textContent = await response.text();
            error.style.display = "block";
            return;
        }
        const newTodo = await response.json();
       
        const tr = document.createElement('tr');
        tr.id = "todo" + newTodo.id;

        const td_header = document.createElement('td');
        const td_description = document.createElement('td');
        const td_delete = document.createElement('td');

        td_header.style="overflow-wrap: break-word; max-width: 200px;";
        td_description.style="overflow-wrap: break-word; max-width: 200px;";

        td_header.textContent = newTodo.title;
        td_description.textContent = newTodo.description;

        const buttonRemove = document.createElement('button');
        buttonRemove.classList.add('btn', 'btn-primary');
        buttonRemove.textContent = 'X';
        buttonRemove.onclick = () => deleteTodo(newTodo.id);
        
        td_delete.appendChild(buttonRemove);
        tr.appendChild(td_header);
        tr.appendChild(td_description);
        tr.appendChild(td_delete);
        todosList.appendChild(tr);
        
        titleInput.value = "";
        descriptionInput.value = "";
    } catch (e) {
        alert(e.message);
    }
});

async function completeTodo(todo_id) {
    try {
        const response = await fetch('/api/todos/complete_todo', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                todo_id: todo_id
            }),
        });
        if (!response.ok) {
            alert(await response.text());
            return;
        }
        const h5 = document.querySelector('#todo'+ todo_id +">h5");
        const div = document.querySelector('#todo'+ todo_id +">div");
        if (h5.classList.contains("my-text-decoration")) {
            h5.classList.remove("my-text-decoration");
            div.classList.remove("my-text-decoration");
        } else {
            h5.classList.add("my-text-decoration");
            div.classList.add("my-text-decoration");
        }
    } catch (e) {
        alert(e.message);
    }
}

async function deleteTodo(todo_id) {
    try {
        const response = await fetch('/api/todos/delete_todo', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                todo_id: todo_id
            }),
        });
        if (!response.ok) {
            alert(await response.text());
            return;
        }
        document.querySelector('#todo'+ todo_id).remove();
    } catch (e) {
        alert(e.message);
    }
}

function toFilter() {
    const todosTrs = todosList.querySelectorAll("tr");
    const title = filterTitle.value;
    const done = filterDone.value;
    todosTrs.forEach(x => {
        const todo = getDataFromCard(x);
        if (todo.title.includes(title) && doneIsEqual(todo.done, done)) {
            x.style.display = ""; // display it
        } else {
            x.style.display = "none"; // remove it
        }
    });
}

function getDataFromCard(tr) {
    const tds = tr.querySelectorAll("td");
    const title = tds[0].textContent;
    const description = tds[1].textContent;
    const done = true;
    const todo = {
        title,
        description,
        done
      };
    return todo;
}

function doneIsEqual(b, s) { //b is bool, s is string
    if (s == "Done") return b;
    if (s == "Not done") return !b;
    return true; // No matter
}