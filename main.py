#!/usr/bin/env python3
import argparse
from rich.console import Console
from rich.table import Table

from models.user import User
from models.project import Project
from models.task import Task
from utils.file_handler import save_data, load_data

console = Console()

def load_and_sync():
    return load_data()

def save_and_sync(users, projects, tasks):
    save_data(users, projects, tasks)

def cmd_add_user(args):
    users, projects, tasks = load_and_sync()
    if User.find_by_name(args.name):
        console.print(f"[red]User '{args.name}' already exists.[/red]")
        return
    user = User(args.name, args.email)
    save_and_sync(users + [user], projects, tasks)
    console.print(f"[green]User '{args.name}' added successfully.[/green]")

def cmd_list_users(args):
    users, _, _ = load_and_sync()
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return
    table = Table(title="Users")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="green")
    for u in users:
        table.add_row(u.name, u.email)
    console.print(table)

def cmd_add_project(args):
    users, projects, tasks = load_and_sync()
    user = User.find_by_name(args.user)
    if not user:
        console.print(f"[red]User '{args.user}' not found.[/red]")
        return
    if any(p.title == args.title and p.user == user for p in projects):
        console.print(f"[red]Project '{args.title}' already exists for user '{args.user}'.[/red]")
        return
    proj = Project(args.title, args.description or "", args.due_date)
    user.add_project(proj)
    projects.append(proj)
    save_and_sync(users, projects, tasks)
    console.print(f"[green]Project '{args.title}' added to user '{args.user}'.[/green]")

def cmd_list_projects(args):
    _, projects, _ = load_and_sync()
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return
    table = Table(title="Projects")
    table.add_column("Title", style="magenta")
    table.add_column("User", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Due Date", style="green")
    for p in projects:
        table.add_row(p.title, p.user.name if p.user else "None", p.description or "", p.due_date or "")
    console.print(table)

def cmd_add_task(args):
    users, projects, tasks = load_and_sync()
    proj = next((p for p in projects if p.title == args.project), None)
    if not proj:
        console.print(f"[red]Project '{args.project}' not found.[/red]")
        return
    if any(t.title == args.title for t in proj.tasks):
        console.print(f"[red]Task '{args.title}' already exists in project '{args.project}'.[/red]")
        return
    task = Task(args.title, status="pending", assigned_to=args.assigned_to)
    proj.add_task(task)
    tasks.append(task)
    save_and_sync(users, projects, tasks)
    console.print(f"[green]Task '{args.title}' added to project '{args.project}'.[/green]")

def cmd_complete_task(args):
    users, projects, tasks = load_and_sync()
    task_found = next((t for t in tasks if t.title == args.title), None)
    if not task_found:
        console.print(f"[red]Task '{args.title}' not found.[/red]")
        return
    task_found.mark_complete()
    save_and_sync(users, projects, tasks)
    console.print(f"[green]Task '{args.title}' marked as complete.[/green]")

def main():
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_add_user = subparsers.add_parser("add-user", help="Add a new user")
    p_add_user.add_argument("--name", required=True)
    p_add_user.add_argument("--email", required=True)

    p_list_users = subparsers.add_parser("list-users", help="List all users")

    p_add_proj = subparsers.add_parser("add-project", help="Add a project to a user")
    p_add_proj.add_argument("--user", required=True)
    p_add_proj.add_argument("--title", required=True)
    p_add_proj.add_argument("--description", default="")
    p_add_proj.add_argument("--due-date", default="")

    p_list_proj = subparsers.add_parser("list-projects", help="List all projects")

    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project", required=True)
    p_add_task.add_argument("--title", required=True)
    p_add_task.add_argument("--assigned-to", help="Name of user assigned")

    p_complete = subparsers.add_parser("complete-task", help="Mark a task as complete")
    p_complete.add_argument("--title", required=True)

    args = parser.parse_args()

    if args.command == "add-user":
        cmd_add_user(args)
    elif args.command == "list-users":
        cmd_list_users(args)
    elif args.command == "add-project":
        cmd_add_project(args)
    elif args.command == "list-projects":
        cmd_list_projects(args)
    elif args.command == "add-task":
        cmd_add_task(args)
    elif args.command == "complete-task":
        cmd_complete_task(args)

if __name__ == "__main__":
    main()
