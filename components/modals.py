import streamlit as st

if __package__:
    from ._core import Workbench, Project, _PRIORITIES
else:
    from _core import Workbench, Project, _PRIORITIES


def _validate_code(code: str | None) -> str | None:
    if code is None:
        return None

    if all(ch in '1234567890.-' for ch in code):
        return code
    else:
        st.warning("Code may only contain '1234567890.-'")
        return None


def _text_input(label: str, placeholder: str, mandatory: bool, warning: str | None = None) -> str | None:
    text = st.text_input(
        label=label,
        placeholder=placeholder,
        value=None
        )
    if mandatory and text == "":
        if not warning:
            raise RuntimeError("Text input is mandatory but `warning` was not set.")
        st.warning(warning)
        text = None
    return text


@st.dialog("Add Project")
def add_project_modal(workbench: Workbench) -> None:
    project_name = _text_input(
        label="Project name*",
        placeholder="e.g. 'New project'",
        mandatory=True,
        warning="Please specify a project name."
        )
    
    project_lead = _text_input(
        label="Project lead*",
        placeholder="e.g. 'John Doe'",
        mandatory=True,
        warning="Please specify a project lead."
        )
    
    project_code = _text_input(
        label="Project Code",
        placeholder="e.g. '123.456.7'",
        mandatory=True,
        warning="Please specify a project code."
        )
    project_code = _validate_code(project_code)
    
    with st.container(border=True, width='stretch'):
        is_task = st.toggle(
            label="Is task?",
            help="Whether the project is a subproject or work package (WP)."
            )
        
        if is_task:
            task_name = _text_input(
                label="Task name*",
                placeholder="e.g. 'New Task'",
                mandatory=True,
                warning="Please specify a task name."
                )
            
            task_lead = _text_input(
                label="Project lead*",
                placeholder="e.g. 'Peter Parker'",
                mandatory=True,
                warning="Please specify a task lead."
                )
            
            task_number = _text_input(
                label="Task number",
                placeholder="e.g. '1' or '2.2'",
                mandatory=True,
                warning="Please specify a task number."
                )
            task_number = _validate_code(task_number)
            
        else:
            task_name = None
            task_lead = None
            task_number = None

    # Set start and end dates
    start_date = st.date_input(
        label="Start date",
        value=None
        )

    end_date = st.date_input(
        label="End date",
        min_value=start_date,
        value=start_date,
        disabled=not start_date
        )

    # Set priority
    priority = st.select_slider(
        label="Priority",
        options=["Low", "Medium", "High"]
    )
    
    # Validate whether name is already in use
    is_legal = workbench.is_legal_new_project_name(
        project_name=project_name, 
        task_name=task_name
        )
    
    st.caption(r"\*Mandatory field")
    
    submit = st.button(
        label="Submit",
        key="add_project_submit_button",
        type="secondary",
        icon=":material/upload:",
        use_container_width=True,
        disabled=not (is_legal and project_name and project_lead and (not is_task or (task_name and task_lead)))
    )
    if submit and project_name and project_lead and (not is_task or (task_name and task_lead)):
        project = Project(
            name=project_name,
            start_date=start_date,
            end_date=end_date,
            lead=project_lead,
            code=project_code or '',
            is_task=is_task,
            task_number=task_number,
            task_name=task_name,
            task_lead=task_lead,
            priority=_PRIORITIES.get(priority, 0),
            tasks=[]
        )
        workbench.projects.append(project)
        st.rerun()
    

if __name__ == '__main__':
    add_project_modal(Workbench("Thomas", projects=[]))