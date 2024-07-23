from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import END
from langgraph.graph import StateGraph

from agent.GraphAgent import GraphAgent
from agent.agent_utility import streaming_exec
from agent.chatbot.chatbot_type import ChatbotAgentState
from prompt.chatbot_prompt import GENERAL_CHATBOT_SYSTEM_PROMPT, GENERAL_HUMAN_PROMPT
from router.chatbot_route_model import ChatbotStreamingInput
from utility.static_text import OpenAI_Model_4o_mini, OpenAI_Model_3_5
from utility.utility_method import gpt_model, get_langfuse_callback
from websocket.websocket_manager import WebSocketManager


class ChatbotGraphAgent(GraphAgent):
    def __init__(self, name: str, personality: str, background: str, goal: str,
                 chatroom_id:int, streaming_input: ChatbotStreamingInput, websocket: WebSocketManager):
        self._name = name
        self.chatroom_id = chatroom_id
        self._personality = personality
        self._background = background
        self._goal = goal
        self._streaming_input = streaming_input
        self._websocket = websocket

    async def prepare_chatbot_config(self, state: ChatbotAgentState):

        pass

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

        chain = (prompt_template | gpt_model(model_name=OpenAI_Model_4o_mini) | StrOutputParser())

        stram_chain = chain.astream(variables)
        result = await streaming_exec(websockets=self._websocket, session_id=self._streaming_input.session_id,
                                      token=self._streaming_input.token,
                                      stream=stram_chain)
        return {'final_message': result}

    def create_graph(self):
        g_workflow = StateGraph(ChatbotAgentState)

        g_workflow.add_node('real_work', self.chat_chain)
        g_workflow.set_entry_point('real_work')
        g_workflow.add_edge('real_work', END)

        g_compile = g_workflow.compile()

        return g_compile
