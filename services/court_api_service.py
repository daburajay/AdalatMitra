from models.case_model import CaseModel


def get_case_details(case_number: str):

    # Mock Data

    return CaseModel(
        case_number=case_number,
        petitioner="Ajay Kumar",
        respondent="State of Uttar Pradesh",
        court_name="District Court Muzaffarnagar",
        case_status="Pending",
        next_hearing_date="25 June 2026",
        case_stage="Evidence",
    )
