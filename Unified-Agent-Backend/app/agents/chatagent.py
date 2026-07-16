# file: agents/chat_agent.py
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4")

def chat_agent(user_message, chat_history):
    messages = [SystemMessage(content="You are a helpful library assistant.")]
    for msg in chat_history:
        messages.append(HumanMessage(content=msg))
    messages.append(HumanMessage(content=user_message))
    return llm(messages).content