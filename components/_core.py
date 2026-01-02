from typing import Literal
from datetime import date
from dataclasses import dataclass


_PRIORITIES = {'Low': 1, 'Medium': 2, 'High': 3}


@dataclass
class Badge:
    label: str
    icon: str | None = None
    color: Literal['red', 'orange', 'yellow', 'blue', 'green', 'violet', 'gray', 'primary'] = 'gray'

    @classmethod
    def from_dict(cls, d):
        return cls(**d)   
    
    def as_dict(self) -> dict:
        return {
            'label': self.label,
            'icon': self.icon,
            'color': self.color
        }

@dataclass
class Attachment:
    filepath: str

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
    
    def as_dict(self) -> dict:
        return {'filepath': self.filepath}

@dataclass
class Remark:
    author: str
    date: date
    text: str

    @classmethod
    def from_dict(cls, d):
        return cls(
            author=d['author'],
            date=date.fromisoformat(d['date']),
            text=d['text']
        )
    
    def as_dict(self) -> dict:
        return {
            'author': self.author,
            'date': self.date.isoformat(),
            'text': self.text
            }


@dataclass
class Task:
    name: str
    description: str
    badges: list[Badge]
    attachments: list[Attachment]
    remarks: list[Remark]
    due: date | None

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d['name'],
            description=d['description'],
            badges=[Badge.from_dict(badge) for badge in d['badges']],
            attachments=[Attachment.from_dict(attachment) for attachment in d['attachments']],
            remarks=[Remark.from_dict(remark) for remark in d['remarks']],
            due=date.fromisoformat(d['due']) if d['due'] else None,
        )
    
    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'badges': [badge.as_dict() for badge in self.badges],
            'attachments': [attachment.as_dict() for attachment in self.attachments],
            'remarks': [remark.as_dict() for remark in self.remarks],
            'due': self.due.isoformat() if self.due else None
            }


@dataclass
class Project:
    name: str
    start_date: date | None
    end_date: date | None
    lead: str
    code: str
    is_task: bool
    task_number: str | None
    task_name: str | None
    task_lead: str | None
    priority: int
    tasks: list[Task]

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d['name'],
            start_date=date.fromisoformat(d['start_date']) if d['start_date'] else None,
            end_date=date.fromisoformat(d['end_date']) if d['end_date'] else None,
            lead=d['lead'],
            code=d['code'],
            is_task=d['is_task'],
            task_number=d['task_number'],
            task_name=d['task_name'],
            task_lead=d['task_lead'],
            priority=d['priority'],
            tasks=[Task.from_dict(task) for task in d['tasks']]
        )
    
    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'lead': self.lead,
            'code': self.code,
            'is_task': self.is_task,
            'task_number': self.task_number,
            'task_name': self.task_name,
            'task_lead': self.task_lead,
            'priority': self.priority,
            'tasks': [task.as_dict() for task in self.tasks]
            }
    
@dataclass
class Workbench:
    employee: str
    projects: list[Project]

    @classmethod
    def from_dict(cls, d):
        return cls(
            employee=d['employee'],
            projects=[Project.from_dict(proj) for proj in d['projects']]
        )
    
    def as_dict(self) -> dict:
        return {
            'employee': self.employee,
            'projects': [proj.as_dict() for proj in self.projects]
        }
    
    def is_legal_new_project_name(self, project_name: str | None, task_name: str | None) -> bool:   
        if not project_name:
            return False
        existing_projects = [f"{project.name}_{project.task_name}" for project in self.projects]     
        return f"{project_name}_{task_name}" not in existing_projects