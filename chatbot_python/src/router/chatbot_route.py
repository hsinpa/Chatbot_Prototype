from fastapi import APIRouter, HTTPException
from langchain_core.output_parsers import StrOutputParser

from agent.chatbot.ChatbotGraphAgent import ChatbotGraphAgent
from utility.utility_method import get_langfuse_callback

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post("/chat")
async def chat(text: str):
    chat_agent = ChatbotGraphAgent(name='Honey', personality='naughty', goal='teach fruit knowledge',
                                   background='Once a school teacher, now out of job')

    chat_graph = chat_agent.create_graph()
    chat_graph = chat_graph.with_config({'callbacks': [get_langfuse_callback()], "run_name": 'Chatbot chat chain'})

    r = await chat_graph.ainvoke({'query': text, 'messages': []})

    return r
