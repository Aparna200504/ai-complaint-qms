import json

from app.models.schemas import ComplaintForm
from app.services.groq_service import client
from app.config import GROQ_EXTRACTION_MODEL


SYSTEM_PROMPT = """
You are a pharmaceutical QMS complaint editing assistant.

You receive:
1. The current ComplaintForm.
2. A user instruction describing a requested change.

Your task is to return the COMPLETE updated ComplaintForm as valid JSON.

Rules:

1. Change ONLY the fields explicitly requested by the user.
2. Preserve every other existing field exactly as it is.
3. Never invent information.
4. Never remove existing information unless the user explicitly asks to remove it.
5. If the user asks to clear a field, set that field to null.
6. Return ALL ComplaintForm fields, including unchanged fields.
7. Use null for fields that are genuinely unavailable.
8. Preserve dates as provided by the user.
9. Do not invent missing parts of dates.
10. Preserve quantity and units.
11. initial_severity must be one of:
    Critical, Major, Minor, or null.
12. priority must be one of:
    High, Medium, Low, or null.

Important field ownership rules:

- impacted_non_product_materials is displayed as read-only on the
  review form, but it may be updated through the RHS conversational
  editor when the user explicitly provides the NPM information.

- originating_site_block is a structured field.
  Only change it when the user explicitly provides a site block.
  Do not invent site block names.

If the user's instruction is ambiguous or does not clearly identify a field,
preserve the existing value rather than guessing.

Return ONLY valid JSON.
"""


def edit_complaint(
    current_form: ComplaintForm,
    user_message: str,
) -> ComplaintForm:

    current_form_json = current_form.model_dump_json(indent=2)

    prompt = f"""
Current ComplaintForm:

{current_form_json}

User instruction:

{user_message}

Return the complete updated ComplaintForm.
"""

    response = client.chat.completions.create(
        model=GROQ_EXTRACTION_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Complaint editing model returned an empty response.")

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Complaint editing model returned invalid JSON: {exc}"
        ) from exc

    return ComplaintForm.model_validate(data)