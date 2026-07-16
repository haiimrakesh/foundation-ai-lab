# file: agents/rag_semantic_agent.py
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

llm = ChatOpenAI(model="gpt-4")
embeddings = OpenAIEmbeddings()

def build_vectorstore(documents):
    return FAISS.from_texts(documents, embeddings)

def rag_semantic_agent(query, vectorstore):
    docs = vectorstore.similarity_search(query, k=2)
    context = "\n".join([d.page_content for d in docs])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a library assistant."),
        ("human", f"Answer using context:\n{context}\n\nQuestion: {query}")
    ])
    return llm(prompt.format_messages()).content
