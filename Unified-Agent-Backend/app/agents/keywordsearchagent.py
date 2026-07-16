# file: agents/rag_keyword_agent.py
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import re

llm = ChatOpenAI(model="gpt-4")

def keyword_search(query, documents):
    keywords = re.findall(r"\w+", query.lower())
    results = [doc for doc in documents if any(k in doc.lower() for k in keywords)]
    return results

def rag_keyword_agent(query, documents):
    context = "\n".join(keyword_search(query, documents))
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a library assistant."),
        ("human", f"Answer using context:\n{context}\n\nQuestion: {query}")
    ])
    return llm(prompt.format_messages()).content
