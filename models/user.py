from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from models.project import Project

class Person:
    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def email(self):
        return self._email

    def __str__(self):
        return f"{self.name} <{self.email}>"

class User(Person):
    _all_users = []

    def __init__(self, name: str, email: str):
        super().__init__(name, email)
        self._projects = []
        User._all_users.append(self)

    @property
    def projects(self) -> List['Project']:
        return self._projects

    def add_project(self, project: 'Project'):
        if project not in self._projects:
            self._projects.append(project)
            project.user = self

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "projects": [p.title for p in self._projects]
        }

    @classmethod
    def find_by_name(cls, name: str):
        for u in cls._all_users:
            if u.name.lower() == name.lower():
                return u
        return None

    @classmethod
    def clear_all(cls):
        cls._all_users = []

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"
