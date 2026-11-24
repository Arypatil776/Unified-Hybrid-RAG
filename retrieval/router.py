
def route_query(question):
    question = question.lower()

    # Structured database queries
    sql_keywords = [
        "student", "students", "student id",
        "enrollment", "enrolled",
        "branch", "course",
        "gpa", "cgpa",
        "how many", "count", "number of",
        "list all", "show all",
        "highest", "top student",
        "average", "avg",
        "above", "greater than",
        "third year", "second year",
        "first year", "fourth year",
        "year 1", "year 2", "year 3", "year 4",
        "grant list", "available grants"
    ]

    # Unstructured policy/document queries
    vector_keywords = [
        "eligibility", "eligible", "requirements",
        "policy", "deadline", "application",
        "research proposal", "recommendation",
        "required documents", "scholarship rules"
    ]

    sql_match = any(word in question for word in sql_keywords)
    vector_match = any(word in question for word in vector_keywords)

    if sql_match and vector_match:
        return "HYBRID"

    if sql_match:
        return "SQL"

    if vector_match:
        return "VECTOR"

    return "VECTOR"


if __name__ == "__main__":

    test_questions = [
        "How many IT students are there?",
        "Tell me about student 1",
        "List all IT students",
        "Show third-year students",
        "Find students with GPA above 8.5",
        "Who has the highest GPA?",
        "What is the average GPA of IT students?",
        "What are the research grant requirements?",
        "Is student 1 eligible for the Research Excellence Grant?"
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")
        print(f"Route: {route_query(question)}")
