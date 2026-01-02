import os
import json

if __package__:
    from ._core import Workbench, Project, Task
    from ._utils import normalize_path_component
else:
    from _core import Workbench, Project, Task
    from _utils import normalize_path_component


class Backend:
    def __init__(self, employee: str, data_dir: str = "workbenches") -> None:
        employee_path = normalize_path_component(employee)
        self._outfile = os.path.join(data_dir, f"{employee_path}.json")

        if os.path.exists(self._outfile):
            print(f"Loading data from '{self._outfile}'")
            self._workbench: Workbench = self._load()
        else:
            print(f"Creating Workbench for new employee '{employee}' at '{self._outfile}'")
            self._workbench = Workbench(employee=employee, projects=[])

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

    backend = Backend(employee="Thomas")
    backend.workbench.projects.append(
        Project(
            name="Test project",
            start_date=datetime.now(),
            end_date=datetime.now(),
            lead="John Doe",
            code="12345",
            is_task=False,
            task_number='0',
            task_name="Some WP",
            task_lead="Alice Doe",
            priority=3,
            tasks=[]
        )
    )
    backend.save()
    del backend
    
    new_backend = Backend(employee="Thomas")
    assert len(new_backend.workbench.projects) == 1

        

        


