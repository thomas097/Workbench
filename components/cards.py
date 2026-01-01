import streamlit as st
from datetime import datetime

if __package__:
    from .core import Badge
else:
    from core import Badge


_BADGES = {
    "in_progress": {"label": "In progress", "icon": ":material/pace:", "color": "yellow"},
    "favorite": {"label": "Favorite", "icon": ":material/star:", "color": "violet"}
}

def kanban_card(
        title: str, 
        description: str, 
        badges: list[str] = [], 
        attachments: list[str] = [],
        comments: list[str] = [],
        due: datetime | None = None,
        border: bool = True
        ) -> None:
    with st.container(border=border, horizontal=False):

        # First row
        with st.container(border=False, horizontal=True):
            st.markdown(f"**{title}**")

            st.space('stretch')

            # Row of badges
            if badges:
                with st.container(border=False, horizontal=True, horizontal_alignment='right', width='content'):
                    for badge_key in badges:
                        badge_args = _BADGES.get(badge_key, {'label': badge_key, 'color': 'grey'})
                        st.badge(**badge_args) #type:ignore

        # Second row
        st.write(description)

        # Third row
        with st.container(border=False, horizontal=True):
            with st.container(border=False, horizontal=True, horizontal_alignment='left', width='content'):
                # Edit button
                st.button(":material/border_color:", type='tertiary')

                # Attachments
                attachment_icon = f":material/attach_file: {len(attachments)}" if attachments else ":material/attach_file_off:"
                with st.popover(attachment_icon, type='tertiary', disabled=not attachments):
                    for attachment in attachments:
                        st.write(attachment)

                # Comments
                comments_icon = f":material/feedback: {len(comments)}" if comments else ":material/chat_bubble:"
                with st.popover(comments_icon, type='tertiary', disabled=not attachments):
                    for comment in comments:
                        st.write(comment)                 

            st.space('stretch')

            if due is not None:    
                # Due date
                if due.year == datetime.now().year:
                    due_date = due.strftime("%b %d").lstrip("0").replace(" 0", " ")
                else:
                    due_date = due.strftime("%b %d, %Y").replace(" 0", " ")
                st.button(label=f"**Due:** {due_date}", icon=":material/timelapse:", type='tertiary', disabled=True)


if __name__ == '__main__':
    kanban_card(
        title="Do the dishes", 
        description="This is some description of the task to be accomplished and optionally some aditional info regarding the execution of the task.",
        badges=["in_progress", "favorite", "lolz"],
        attachments=[
            "Path/To/File"
            ],
        comments=[],
        due=datetime.now()
        )