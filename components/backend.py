import os
import toml
import json

if __package__:
    from ._core import Workbench, Project
    from ._utils import normalize_path_component
else:
    from _core import Workbench, Project
    from _utils import normalize_path_component



class SessionManager:
    _SESSION_PATH = ".streamlit/session.toml"

    @staticmethod
    def get_username() -> str | None:
        if not os.path.exists(SessionManager._SESSION_PATH):
            return None
        
        with open(SessionManager._SESSION_PATH, mode='r', encoding='utf-8') as file:
            return toml.load(file).get('username', None)

    @staticmethod
    def register_username(username: str) -> None:
        with open(SessionManager._SESSION_PATH, mode='w', encoding='utf-8') as file:
            toml.dump({'username': username}, f=file)


class Session:
    def __init__(self, user: str, data_dir: str = "workbenches") -> None:
        user_path = normalize_path_component(user)
        self._outfile = os.path.join(data_dir, f"{user_path}.json")

        if os.path.exists(self._outfile):
            print(f"Loading data from '{self._outfile}'")
            self._workbench: Workbench = self._load()
        else:
            print(f"Creating Workbench for new user '{user}' at '{self._outfile}'")
            self._workbench = Workbench(user=user, projects=[])
            self.save()

    @property
    def workbench(self) -> Workbench:
        return self._workbench

    def save(self) -> None:
        with open(self._outfile, mode='w', encoding='utf-8') as file:
            json.dump(self._workbench.as_dict(), fp=file)

    def _load(self) -> Workbench:
        with open(self._outfile, mode='r', encoding='utf-8') as file:
            data = json.load(file)
        return Workbench.from_dict(data)    


if __name__ == '__main__':
    from datetime import datetime

    session = Session(user="Thomas")
    session.workbench.projects.append(
        Project(
            name="Test project",
            start_date=datetime.now(),
            end_date=datetime.now(),
            lead="John Doe",
            code="12345",
            is_task=False,
            task_number='0',
            task_name="Some Task",
            task_lead="Alice Doe",
            priority=3,
            tasks=[]
        )
    )
    session.save()
    del session
    
    new_session = Session(user="Thomas")
    assert len(new_session.workbench.projects) == 1

        

        


