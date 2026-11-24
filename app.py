
import streamlit as st

from retrieval.hybrid_retriever import retrieve_context
from generation.answer_generator import generate_answer
from generation.eligibility_verifier import verify_eligibility


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="UniGrant AI",
    page_icon="🎓",
    layout="wide"
)


# ---------------- CUSTOM STYLING ----------------

st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #888888;
        margin-top: 4px;
        margin-bottom: 25px;
    }

    .stChatMessage {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("🎓 UniGrant AI")

    st.caption("Hybrid University Intelligence")

    st.divider()

    st.subheader("System Architecture")

    st.markdown("""
    - **Router:** Query classification
    - **SQL:** SQLite database
    - **Vector:** ChromaDB
    - **Embeddings:** Sentence Transformers
    - **LLM:** Groq
    - **Verification:** Rule-based eligibility
    """)

    st.divider()

    st.subheader("Try these questions")

    st.markdown("""
    **SQL**
    - How many students are enrolled?
    - How many students belong to IT?

    **VECTOR**
    - What are the research grant requirements?
    - What documents are needed for a scholarship?

    **HYBRID**
    - Is student 1 eligible for the Research Excellence Grant?
    - What grants can student 1 apply for?
    """)

    st.divider()

    st.caption(
        "Demo uses synthetic university data. "
        "It is not connected to a real university database."
    )

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------------- MAIN HEADER ----------------

st.markdown(
    '<p class="main-title">UniGrant AI</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">'
    'Your intelligent university information assistant'
    '</p>',
    unsafe_allow_html=True
)

st.info(
    "Ask questions about student records, course enrollment, "
    "grant policies and academic eligibility."
)


# ---------------- DISPLAY CHAT HISTORY ----------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and "route" in message:

            with st.expander("View retrieval details"):

                st.write("**Selected route:**", message["route"])

                st.write("**SQL evidence:**")
                st.json(message["sql_data"])

                st.write("**Retrieved documents:**")

                if message["documents"]:
                    for doc in message["documents"]:
                        st.markdown(f"**Source:** `{doc['source']}`")
                        st.write(doc["text"])
                        st.caption(
                            f"Vector distance: {doc['distance']:.4f}"
                        )
                else:
                    st.write("No documents retrieved.")

                if message["verification"]:
                    st.write("**Eligibility verification:**")
                    st.json(message["verification"])


# ---------------- USER INPUT ----------------

question = st.chat_input(
    "Ask UniGrant AI a question..."
)


# ---------------- PROCESS QUESTION ----------------

if question:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Retrieve and generate response
    with st.chat_message("assistant"):

        try:
            with st.spinner("Retrieving information and generating answer..."):

                context = retrieve_context(question)

                answer = generate_answer(
                    question,
                    context
                )

                verification = verify_eligibility(
                    question,
                    context
                )

            st.markdown(answer)

            st.success(
                f"Retrieval route: {context['route']}"
            )

            # Store complete response for chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "route": context["route"],
                "sql_data": context["sql_data"],
                "documents": context["documents"],
                "verification": verification
            })

            with st.expander("View retrieval details"):

                st.write("**Selected route:**", context["route"])

                st.write("**SQL evidence:**")
                st.json(context["sql_data"])

                st.write("**Retrieved documents:**")

                if context["documents"]:
                    for doc in context["documents"]:
                        st.markdown(f"**Source:** `{doc['source']}`")
                        st.write(doc["text"])
                        st.caption(
                            f"Vector distance: {doc['distance']:.4f}"
                        )
                else:
                    st.write("No documents retrieved.")

                if verification:
                    st.write("**Eligibility verification:**")
                    st.json(verification)

        except Exception as e:
            error_message = (
                f"Something went wrong while processing your question: {e}"
            )

            st.error(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })
