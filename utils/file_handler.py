import json
import os
from models.user import User
from models.project import Project
from models.task import Task

DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "db.json")

def save_data(users, projects, tasks):
    os.makedirs(DATA_DIR, exist_ok=True)
    data = {
        "users": [u.to_dict() for u in users],
        "projects": [p.to_dict() for p in projects],
        "tasks": [t.to_dict() for t in tasks]
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_data():
    if not os.path.exists(DB_FILE):
        return [], [], []

    with open(DB_FILE, "r") as f:
        data = json.load(f)

    User.clear_all()
    users = []
    projects = []
    tasks = []

    user_objs = {}
    for u_dict in data.get("users", []):
        user = User(u_dict["name"], u_dict["email"])
        users.append(user)
        user_objs[user.name] = user

    proj_objs = {}
    for p_dict in data.get("projects", []):
        proj = Project(p_dict["title"], p_dict["description"], p_dict["due_date"])
        projects.append(proj)
        proj_objs[proj.title] = proj
        user_name = p_dict.get("user")
        if user_name and user_name in user_objs:
            user_objs[user_name].add_project(proj)

    for t_dict in data.get("tasks", []):
        task = Task(t_dict["title"], t_dict["status"], t_dict["assigned_to"])
        tasks.append(task)
        proj_title = t_dict.get("project")
        if proj_title and proj_title in proj_objs:
            proj_objs[proj_title].add_task(task)

    return users, projects, tasks
