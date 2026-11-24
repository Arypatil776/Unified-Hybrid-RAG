
import os
import json

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found.")

client = Groq(api_key=API_KEY)


PLANNER_PROMPT = """
You are the query planner for UniGrant AI.

Analyze the user's question and return a JSON object.

Identify:
- intent
- route
- student_id
- branch
- year
- min_gpa
- grant_name

Allowed intents:
student_profile
student_count
student_filter
top_student
average_gpa
enrollment_count
grant_list
policy_search
eligibility_check
general

Allowed routes:
SQL
VECTOR
HYBRID

Routing rules:

1. Student profiles, student counts, student filtering,
   GPA statistics and enrollment counts use SQL.

2. Grant policy requirements and deadlines use VECTOR.

3. Student grant eligibility questions use HYBRID.

4. Questions combining student records and policy
   information use HYBRID.

5. General university policy questions use VECTOR.

6. Never invent student IDs, branches, GPA values or years.

7. branch must be IT, CS or null.

8. year must be an integer from 1 to 4 or null.

9. min_gpa must be a number or null.

10. student_id must be an integer or null.

11. If the intent is unclear, use general and VECTOR.

Return only valid JSON with this structure:

{
    "intent": "student_profile",
    "route": "SQL",
    "student_id": 1,
    "branch": null,
    "year": null,
    "min_gpa": null,
    "grant_name": null
}
"""


ALLOWED_INTENTS = {
    "student_profile",
    "student_count",
    "student_filter",
    "top_student",
    "average_gpa",
    "enrollment_count",
    "grant_list",
    "policy_search",
    "eligibility_check",
    "general"
}

ALLOWED_ROUTES = {"SQL", "VECTOR", "HYBRID"}


def create_query_plan(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": PLANNER_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    try:
        plan = json.loads(
            response.choices[0].message.content
        )
    except (json.JSONDecodeError, TypeError):
        return {
            "intent": "general",
            "route": "VECTOR",
            "student_id": None,
            "branch": None,
            "year": None,
            "min_gpa": None,
            "grant_name": None
        }

    # Validate intent and route
    if plan.get("intent") not in ALLOWED_INTENTS:
        plan["intent"] = "general"

    if plan.get("route") not in ALLOWED_ROUTES:
        plan["route"] = "VECTOR"

    # Validate student ID
    student_id = plan.get("student_id")

    if (
        not isinstance(student_id, int)
        or isinstance(student_id, bool)
        or student_id <= 0
    ):
        plan["student_id"] = None

    # Validate branch
    branch = plan.get("branch")

    if isinstance(branch, str):
        branch = branch.upper()

    if branch not in ("IT", "CS"):
        plan["branch"] = None
    else:
        plan["branch"] = branch

    # Validate academic year
    year = plan.get("year")

    if (
        not isinstance(year, int)
        or isinstance(year, bool)
        or year not in (1, 2, 3, 4)
    ):
        plan["year"] = None

    # Validate GPA threshold
    min_gpa = plan.get("min_gpa")

    if (
        not isinstance(min_gpa, (int, float))
        or isinstance(min_gpa, bool)
        or not 0 <= min_gpa <= 10
    ):
        plan["min_gpa"] = None

    # Validate grant name
    grant_name = plan.get("grant_name")

    if not isinstance(grant_name, str) or not grant_name.strip():
        plan["grant_name"] = None

    return plan


if __name__ == "__main__":

    test_questions = [
        "Provide me the data of student 1",
        "Show students with GPA above 8.5",
        "Who has the highest GPA in IT?",
        "What are the research grant requirements?",
        "Is student 1 eligible for the Research Excellence Grant?",
        "How many students are currently in the database?"
    ]

    for question in test_questions:

        print("\n" + "=" * 60)
        print("Question:", question)

        plan = create_query_plan(question)

        print(json.dumps(plan, indent=4))
