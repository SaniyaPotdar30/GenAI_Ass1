import os
import chromadb
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
from langchain.chat_models import init_chat_model

embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

llm = init_chat_model(
    model="llama-3.2-1b-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

def load_pdf_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return " ".join([page.page_content for page in docs])

def get_chroma_collection():
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_or_create_collection(name="resumes")

def ingest_resumes(folder_path):
    collection = get_chroma_collection()

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            resume_id = file
            pdf_path = os.path.join(folder_path, file)

            existing = collection.get(ids=[resume_id])
            if existing["ids"]:
                continue

            resume_text = load_pdf_resume(pdf_path)
            embedding = embed_model.embed_documents([resume_text])

            collection.add(
                ids=[resume_id],
                documents=[resume_text],
                embeddings=embedding
            )

def extract_skills(resume_text):
    clean_text = " ".join(resume_text.split())

    prompt = f"""
Extract ONLY skills, tools, technologies, or competencies
EXPLICITLY written in the resume.

Rules:
- Output ONLY a comma-separated list
- No explanation
- No headings
- If none found, output exactly: No skills listed

Resume:
{clean_text[:2500]}
"""

    response = llm.invoke(prompt).content.strip()
    skills = response.splitlines()[0].strip(" ,")

    if len(skills.split(",")) < 2:
        return "No skills listed"

    return skills

def generate_reason(job_role, resume_text, skills):
    clean_text = " ".join(resume_text.split())

    prompt = f"""
Job Role:
{job_role}

Extracted Skills:
{skills}

Resume Content:
{clean_text[:1200]}

Write 2–3 professional sentences explaining
why this candidate fits the job role.
Mention candidate name if available.
Use ONLY resume content.
"""

    return llm.invoke(prompt).content.strip()


def shortlist_resumes(job_role, top_k):
    collection = get_chroma_collection()

    query_embedding = embed_model.embed_query(job_role)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    shortlisted = []

    for i in range(len(results["ids"][0])):
        resume_id = results["ids"][0][i]
        resume_text = results["documents"][0][i]

        skills = extract_skills(resume_text)
        reason = generate_reason(job_role, resume_text, skills)

        shortlisted.append({
            "resume_id": resume_id,
            "skills": skills,
            "reason": reason
        })

    return shortlisted

#streamlit

st.set_page_config(page_title="Resume Shortlisting", layout="wide")

st.title("📄 Resume Shortlisting System")
st.markdown("Shortlist resumes based on job role.")

st.sidebar.header("⚙️ Controls")

resume_folder = st.sidebar.text_input(
    "Resume Folder Path",
    r"C:\Users\saniy\Downloads\fake-resumes"
)

if st.sidebar.button("📥 Upload Resumes"):
    with st.spinner("Uploading resumes..."):
        ingest_resumes(resume_folder)
    st.sidebar.success("Resumes uploaded successfully!")

job_role = st.text_input("Enter Job Role")
top_k = st.number_input("Number of resumes to shortlist", min_value=1, max_value=10, value=3)

if st.button("🔍 Shortlist Resumes"):
    if not job_role:
        st.warning("Please enter a job role.")
    else:
        with st.spinner("Shortlisting resumes..."):
            results = shortlist_resumes(job_role, top_k)

        for res in results:
            st.divider()
            st.subheader(f"📌 {res['resume_id']}")
            st.markdown(f"**Skills:** {res['skills']}")
            st.markdown(f"**Reason:** {res['reason']}")
