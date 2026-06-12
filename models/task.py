from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.project import Project

class Task:
    def __init__(self, title: str, status: str = "pending", assigned_to: str = None):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        self._project = None

    @property
    def project(self) -> 'Project':
        return self._project

    @project.setter
    def project(self, value: 'Project'):
        self._project = value

    def mark_complete(self):
        self.status = "complete"

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "project": self._project.title if self._project else None
        }

    def __repr__(self):
        return f"Task(title={self.title}, status={self.status})"
