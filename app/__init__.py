from flask import Flask, render_template, session, request, redirect, jsonify
app = Flask(__name__)

from .entities import User, Todo
from .storage import Storage


@app.route('/')
def home():
    if "user_id" in session:
        user = Storage.get_user_by_id(session["user_id"])
        return render_template('pages/index.html', user=user)

    return render_template('pages/index.html')


@app.route('/login')
def login():
    if "user_id" in session:
        return redirect('/')
    return render_template('pages/login.html')


@app.route('/login', methods=['POST'])
def login_action():
    if "user_id" in session:
        return redirect('/')
    email = request.form["email"]
    password = request.form["password"]
    errors = []
    
    if not email:
        errors.append('Email is empty.')
    if not password:
        errors.append("Password is empty.")

    user = Storage.get_user_by_email_and_password(email, password)
    if not user:
        errors.append('Invalid email or password.')
    if errors:
        return render_template('pages/login.html', error='\n'.join(errors))

    session["user_id"] = user.id
    
    return redirect('/todos')


@app.route('/registration')
def registration():
    if "user_id" in session:
        return redirect('/')
    return render_template('pages/registration.html')


@app.route('/registration', methods=['POST'])
def registration_action():
    if "user_id" in session:
        return redirect('/')
    email = request.form["email"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    errors = []

    if not email:
        errors.append("Email is empty. Please enter your Email.")
    if not password1:
        errors.append("Please enter your password.")
    if password1 != password2:
        errors.append("Passwords are not equel.")
    if Storage.is_email_used(email):
        errors.append("Email is already used.")
    if errors:
        return render_template('pages/registration.html', error= '\n'.join(errors))
    
    Storage.add_user(User(None, email, password1))

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/login')


@app.route('/todos')
def todos():
    if "user_id" not in session:
        return redirect('/login')
    
    user = Storage.get_user_by_id(session["user_id"])
    todos = Storage.get_todos_by_user_id(user.id)
    return render_template('pages/todos.html', user=user, todos=todos)


@app.route('/todos', methods=['POST'])
def todos_add_new_todo():
    if "user_id" not in session:
        return redirect('/login')

    title = request.form["title"]
    description = request.form["description"]
    user = Storage.get_user_by_id(session["user_id"])
    todos = Storage.get_todos_by_user_id(user.id)
    errors = []

    if not title:
        errors.append("Title is empty. Please enter title.")
    if not description:
        errors.append("Please enter description.")
    if errors:
        return render_template('pages/todos.html', error='\n'.join(errors), user=user, todos=todos)
    
    todo = Storage.create_todo(title, description, user.id)
    todos.append(todo)

    return render_template('pages/todos.html', user=user, todos=todos)


@app.route('/todos/delete<todo_id>')
def delete_todo(todo_id):
    if "user_id" not in session:
        return redirect('/login')
    
    user_id = session["user_id"]
    Storage.delete_todo(todo_id, user_id)
    return redirect('/todos')


@app.route('/api/todos/add_todo', methods=['POST'])
def api_add_todo():
    if "user_id" not in session:
        return 'Not authorized!', 401
    
    title = request.json["title"]
    description = request.json["description"]
    errors = []

    if not title:
        errors.append("Title is empty. Please enter title.")
    if not description:
        errors.append("Please enter description.")
    if errors:
        return '\n'.join(errors), 400

    todo = Storage.create_todo(title, description, session["user_id"])
    
    return jsonify(todo.__dict__) 
    

@app.route('/api/todos/delete_todo', methods=['POST'])
def api_delete_todo():
    if "user_id" not in session:
        return 'Not authorized!', 401
    
    todo_id = request.json["todo_id"]

    Storage.delete_todo(todo_id, session["user_id"])
    
    return '', 200


@app.route('/api/todos/complete_todo', methods=['POST'])
def api_complete_todo():
    if "user_id" not in session:
        return 'Not authorized!', 401
    
    todo_id = request.json["todo_id"]

    todo = Storage.get_todo_by_todo_id(todo_id, session["user_id"])
    
    if todo.done == 1:
        todo.done = 0
    else:
        todo.done = 1

    Storage.update_todo(todo, session["user_id"])
    
    return '', 200