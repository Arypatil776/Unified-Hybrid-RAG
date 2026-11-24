
from generation.query_planner import create_query_plan

from retrieval.sql_retriever import (
    get_student,
    get_grants,
    get_enrollment_count,
    get_branch_student_count,
    get_student_count,
    get_students,
    get_top_student,
    get_average_gpa
)

from retrieval.vector_retriever import search_documents


def retrieve_context(question):

    # Step 1: Understand the question using the LLM planner
    plan = create_query_plan(question)

    route = plan["route"]
    intent = plan["intent"]

    print("\n[Query Planner]")
    print("Intent:", intent)
    print("Route:", route)
    print("Plan:", plan)

    context = {
        "route": route,
        "intent": intent,
        "query_plan": plan,
        "sql_data": [],
        "documents": []
    }

    # --------------------------------
    # STEP 2: STRUCTURED SQL RETRIEVAL
    # --------------------------------

    if route in ("SQL", "HYBRID"):

        student_id = plan.get("student_id")
        branch = plan.get("branch")
        year = plan.get("year")
        min_gpa = plan.get("min_gpa")

        # Individual student profile
        if intent == "student_profile" or student_id is not None:

            if student_id is not None:
                context["sql_data"].append({
                    "student_profile": get_student(student_id)
                })

        # Total or branch-wise student count
        if intent == "student_count":

            if branch:
                context["sql_data"].append({
                    "branch_student_count":
                        get_branch_student_count(branch)
                })
            else:
                context["sql_data"].append({
                    "total_student_count":
                        get_student_count()
                })

        # Student filtering
        elif intent == "student_filter":

            context["sql_data"].append({
                "filtered_students": get_students(
                    branch=branch,
                    year=year,
                    min_gpa=min_gpa
                )
            })

        # Highest GPA student
        elif intent == "top_student":

            context["sql_data"].append({
                "top_student": get_top_student(branch)
            })

        # Average GPA
        elif intent == "average_gpa":

            context["sql_data"].append({
                "average_gpa": get_average_gpa(branch)
            })

        # Enrollment count
        elif intent == "enrollment_count":

            context["sql_data"].append({
                "enrollment_count": get_enrollment_count()
            })

        # Grant listing
        elif intent == "grant_list":

            context["sql_data"].append({
                "available_grants": get_grants()
            })

        # Eligibility requires student and grant data
        elif intent == "eligibility_check":

            if student_id is not None and not any(
                "student_profile" in item
                for item in context["sql_data"]
            ):
                context["sql_data"].append({
                    "student_profile": get_student(student_id)
                })

            context["sql_data"].append({
                "available_grants": get_grants()
            })

        # Additional grant data for combined questions
        if (
            route == "HYBRID"
            and intent != "eligibility_check"
            and any(word in question.lower() for word in [
                "grant", "scholarship"
            ])
        ):
            context["sql_data"].append({
                "available_grants": get_grants()
            })

    # --------------------------------
    # STEP 3: VECTOR DOCUMENT RETRIEVAL
    # --------------------------------

    if route in ("VECTOR", "HYBRID"):

        context["documents"] = search_documents(question)

    return context


# --------------------------------
# TESTING
# --------------------------------

if __name__ == "__main__":

    test_questions = [
        "Provide me the data of student 1",
        "How many students are currently in the database?",
        "How many IT students are there?",
        "List all IT students",
        "Show students with GPA above 8.5",
        "Who has the highest GPA in IT?",
        "What is the average GPA of IT students?",
        "How many students are enrolled?",
        "What are the research grant requirements?",
        "Is student 1 eligible for the Research Excellence Grant?"
    ]

    for question in test_questions:

        print("\n" + "=" * 65)
        print("Question:", question)

        result = retrieve_context(question)

        print("\nSQL Evidence:")
        print(result["sql_data"])

        print("\nDocuments Retrieved:", len(result["documents"]))

        for document in result["documents"]:
            print("Source:", document["source"])
