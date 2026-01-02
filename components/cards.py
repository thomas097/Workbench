import streamlit as st
from datetime import datetime

if __package__:
    from ._core import Badge, Attachment, Remark
else:
    from _core import Badge, Attachment, Remark


_BADGES = {
    "in_progress": Badge(label="In progress", icon=":material/pace:", color="yellow"),
    "favorite": Badge(label="Favorite", icon=":material/star:", color="violet")
}

def _format_date(date: datetime) -> str:
    if date.year == datetime.now().year:
        return date.strftime("%b %d").lstrip("0").replace(" 0", " ")
    else:
        return date.strftime("%b %d, %Y").replace(" 0", " ")

def kanban_card(
        title: str, 
        description: str, 
        badges: list[str] = [], 
        attachments: list[Attachment] = [],
        remarks: list[Remark] = [],
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
                        badge = _BADGES.get(badge_key, Badge(label=badge_key)) # TODO: replace with DEFAULT_BADGE
                        st.badge(label=badge.label, icon=badge.icon, color=badge.color)

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
                        attachment_card(attachment)

                    if st.button(label=":material/add:", key="add_attachment_buttonn", width='stretch'):
                        pass # TODO

                # Comments
                remark_icon = f":material/feedback: {len(remarks)}" if remarks else ":material/chat_bubble:"
                with st.popover(remark_icon, type='tertiary', disabled=not remarks):
                    for remark in remarks:
                        remark_card(remark)     

                    if st.button(label=":material/add:", key="add_remark_button", width='stretch'):
                        pass # TODO        

            st.space('stretch')

            if due is not None:    
                st.button(label=f"**Due:** {_format_date(due)}", icon=":material/timelapse:", type='tertiary', disabled=True)


def attachment_card(attachment: Attachment) -> None:
    st.write(attachment.filepath)

def remark_card(remark: Remark) -> None:
    with st.container(border=True, horizontal=False, width='stretch'):
        with st.container(border=False, horizontal=True, width='stretch'):
            st.markdown(f"**{remark.author}**") 

            for _ in range(10): st.space('stretch')
            
            st.markdown(f"_{_format_date(remark.date)}_")

        st.write(remark.text)


if __name__ == '__main__':
    kanban_card(
        title="Name of task", 
        description="Description goes here...",
        badges=["in_progress", "favorite", "lolz"],
        attachments=[
            Attachment(filepath="filename.pdf")
            ],
        remarks=[
            Remark(author="Thomas", date=datetime.now(), text="Completely disagree with all this and more!")
            ],
        due=datetime.now()
        )