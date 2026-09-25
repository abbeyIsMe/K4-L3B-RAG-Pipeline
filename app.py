import streamlit as st
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(
    page_title="HUTECH tuyển sinh 2026",
    page_icon=":material/school:",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("RAG Chatbot")
    st.caption("Thay mô tả theo đề tài của nhóm")
    top_k = st.slider("Số chunks", 3, 10, 5)

st.title("RAG Chatbot")
st.caption("Thay tiêu đề và hướng dẫn sử dụng")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            render_sources(message["sources"])

chat_prompt = st.chat_input(
    "Ví dụ: HUTECH 2026 có những phương thức xét tuyển nào?",
    submit_mode="disable",
)
prompt = chat_prompt or prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # TODO: Gọi generate_with_citation(query, top_k).
        answer = "TODO: Itegration RAG Pipeline hêre"
        sources = []
        st.markdown(answer)
        render_sources(result["sources"])

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": result["sources"],
        }
    )
