from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import END
from langgraph.graph import StateGraph

from agent.GraphAgent import GraphAgent
from agent.chatbot.chatbot_type import ChatbotAgentState
from prompt.chatbot_prompt import GENERAL_CHATBOT_SYSTEM_PROMPT, GENERAL_HUMAN_PROMPT
from utility.utility_method import gpt_model, get_langfuse_callback


class ChatbotGraphAgent(GraphAgent):
    def __init__(self, name: str, personality: str, background: str, goal: str):
        self._name = name
        self._personality = personality
        self._background = background
        self._goal = goal

    async def chat_chain(self, state: ChatbotAgentState):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", GENERAL_CHATBOT_SYSTEM_PROMPT),
            ("user", GENERAL_HUMAN_PROMPT),
        ])

        variables = {
            'name': self._name,
            'personality': self._personality,
            'background': self._background,
            'goal': self._goal,
            'summary': '',
            'query': state['query']
        }

        chain = (prompt_template | gpt_model() | StrOutputParser())

        result = await chain.ainvoke(variables)

        return {'final_message': result}

    def create_graph(self):
        g_workflow = StateGraph(ChatbotAgentState)

        g_workflow.add_node('real_work', self.chat_chain)
        g_workflow.set_entry_point('real_work')
        g_workflow.add_edge('real_work', END)

        g_compile = g_workflow.compile()

        return g_compile
