from typing import Literal
from datetime import datetime
from dataclasses import dataclass, field


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
    date: datetime
    text: str

    @classmethod
    def from_dict(cls, d):
        return cls(
            author=d['author'],
            date=datetime.fromisoformat(d['date']),
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
    due: datetime

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d['name'],
            description=d['description'],
            badges=[Badge.from_dict(badge) for badge in d['badges']],
            attachments=[Attachment.from_dict(attachment) for attachment in d['attachments']],
            remarks=[Remark.from_dict(remark) for remark in d['remarks']],
            due=datetime.fromisoformat(d['due']),
        )
    
    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'badges': [badge.as_dict() for badge in self.badges],
            'attachments': [attachment.as_dict() for attachment in self.attachments],
            'remarks': [remark.as_dict() for remark in self.remarks],
            'due': self.due.isoformat()
            }


@dataclass
class Project:
    name: str
    start_date: datetime
    end_date: datetime
    lead: str
    code: str
    is_task: bool
    task_number: int
    task_name: str
    task_lead: str
    priority: int
    tasks: list[Task]

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d['name'],
            start_date=datetime.fromisoformat(d['start_date']),
            end_date=datetime.fromisoformat(d['end_date']),
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
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
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