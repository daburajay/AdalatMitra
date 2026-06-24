from models.timeline_model import TimelineEvent
from prompts.timeline_prompt import build_timeline_prompt
from services.llm_service import generate_response


def get_case_timeline(case_number: str):

    timeline = [
        TimelineEvent(
            event_date="01 Jan 2026",
            event_title="Case Filed",
            event_description="The case was officially registered.",
        ),
        TimelineEvent(
            event_date="15 Jan 2026",
            event_title="Notice Issued",
            event_description="Notice was sent to the respondent.",
        ),
        TimelineEvent(
            event_date="20 Feb 2026",
            event_title="Evidence Stage Started",
            event_description="Court started recording evidence.",
        ),
        TimelineEvent(
            event_date="15 Mar 2026",
            event_title="Hearing Adjourned",
            event_description="Matter postponed.",
        ),
        TimelineEvent(
            event_date="25 Jun 2026",
            event_title="Next Hearing",
            event_description="Next hearing scheduled.",
        ),
    ]

    return timeline


def explain_timeline(case_number: str, language: str):

    timeline = get_case_timeline(case_number)

    timeline_text = ""

    for event in timeline:

        timeline_text += (
            f"{event.event_date} - "
            f"{event.event_title} - "
            f"{event.event_description}\n"
        )

        prompt = build_timeline_prompt(
            case_number=case_number, timeline_text=timeline_text, language=language
        )

        return generate_response(prompt)
