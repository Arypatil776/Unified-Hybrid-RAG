
import re


def verify_eligibility(question, context):
    sql_data = context.get("sql_data", [])
    documents = context.get("documents", [])

    # Extract student and grant records from SQL results
    student = None
    grants = []

    for item in sql_data:
        if isinstance(item, dict):
            profiles = item.get("student_profile", [])
            grant_records = item.get("available_grants", [])

            if profiles:
                student = profiles[0]

            grants.extend(grant_records)

    if not student:
        return {
            "status": "INSUFFICIENT_DATA",
            "reason": "Student profile was not found."
        }

    # Identify the requested grant
    question_lower = question.lower()

    selected_grant = None

    for grant in grants:
        if grant["grant_name"].lower() in question_lower:
            selected_grant = grant
            break

    if not selected_grant and len(grants) == 1:
        selected_grant = grants[0]

    if not selected_grant:
        return {
            "status": "INSUFFICIENT_DATA",
            "reason": "Could not identify the requested grant."
        }

    # Deterministic academic checks
    gpa_pass = student["gpa"] >= selected_grant["minimum_gpa"]
    year_pass = student["year"] == selected_grant["eligible_year"]

    checks = {
        "student_name": student["name"],
        "student_gpa": student["gpa"],
        "required_gpa": selected_grant["minimum_gpa"],
        "gpa_check": "PASS" if gpa_pass else "FAIL",
        "student_year": student["year"],
        "required_year": selected_grant["eligible_year"],
        "year_check": "PASS" if year_pass else "FAIL",
        "grant_name": selected_grant["grant_name"],
        "deadline": selected_grant["deadline"]
    }

    # Extract required documents from the matching policy
    required_documents = []

    for document in documents:
        content = document["text"]

        if selected_grant["grant_name"].lower() in content.lower():
            match = re.search(
                r"Required Documents:\s*(.*)",
                content,
                re.IGNORECASE | re.DOTALL
            )

            if match:
                required_documents = [
                    line.strip().lstrip("- ").strip()
                    for line in match.group(1).splitlines()
                    if line.strip().startswith("-")
                ]

            break

    checks["required_documents"] = required_documents
    checks["document_submission_status"] = "UNKNOWN"

    if not gpa_pass or not year_pass:
        checks["status"] = "NOT_ELIGIBLE"
    elif required_documents:
        checks["status"] = "ACADEMICALLY_ELIGIBLE_COMPLETENESS_UNVERIFIED"
    else:
        checks["status"] = "ACADEMICALLY_ELIGIBLE_POLICY_INCOMPLETE"

    return checks


if __name__ == "__main__":
    from retrieval.hybrid_retriever import retrieve_context

    question = (
        "Is student 1 eligible for the "
        "Research Excellence Grant?"
    )

    context = retrieve_context(question)

    result = verify_eligibility(question, context)

    print("\n--- Deterministic Eligibility Verification ---")
    for key, value in result.items():
        print(f"{key}: {value}")
