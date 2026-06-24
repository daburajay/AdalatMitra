def build_timeline_prompt(case_number: str, timeline_text: str, language: str):

    return f"""
You are AdalatMitra.

Reply ONLY in {language}.

Explain this court case timeline in simple language.

Use this format:

    📅 Case Timeline Summary

    📖 What Happened So Far

    ⚖ Current Stage

    👉 Next Expected Action

    Case Number:
        {case_number}

        Timeline:
            {timeline_text}
            """
