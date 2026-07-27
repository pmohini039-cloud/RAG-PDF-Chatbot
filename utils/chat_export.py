from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


def export_chat_as_txt(messages):
    """
    Returns chat history as text.
    """

    lines = []

    for message in messages:

        role = message["role"].capitalize()

        content = message["content"]

        lines.append(f"{role}:")
        lines.append(content)
        lines.append("")

    return "\n".join(lines)


def export_chat_as_pdf(messages):
    """
    Returns chat history as PDF bytes.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    for message in messages:

        role = message["role"].capitalize()

        content = message["content"]

        story.append(
            Paragraph(f"<b>{role}</b>", styles["Heading3"])
        )

        story.append(
            Paragraph(content.replace("\n", "<br/>"), styles["BodyText"])
        )

    doc.build(story)

    buffer.seek(0)

    return buffer