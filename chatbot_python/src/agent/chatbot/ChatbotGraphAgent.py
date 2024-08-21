from typing import List

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import END
from langgraph.graph import StateGraph

from agent.GraphAgent import GraphAgent
from agent.agent_utility import streaming_exec, bot_variable, db_message_to_prompt
from agent.chatbot.NarratorActionAgent import NarratorActionAgent
from agent.chatbot.chatbot_type import ChatbotAgentState
from model.chatbot_model import ChatbotNPCDBType, ChatbotUserEnum, ChatMessageDBInputType
from prompt.chatbot_prompt import GENERAL_CHATBOT_SYSTEM_PROMPT, GENERAL_HUMAN_PROMPT, \
    GENERAL_CHATBOT_MESSAGE_MERGE_PROMPT, GENERAL_NARRATOR_SYSTEM_PROMPT
from router.chatbot_route_model import ChatbotStreamingInput
from utility.llm_static import OpenAI_Model_4o_mini
from utility.simple_prompt_factory import SimplePromptFactory
from utility.utility_method import gpt_model
from websocket.socket_static import SocketEvent
from websocket.websocket_manager import WebSocketManager


class ChatbotGraphAgent(GraphAgent):
    def __init__(self, chatbot: ChatbotNPCDBType, narrator_agent: NarratorActionAgent,
                 m_history: List[ChatMessageDBInputType], chatroom_summary: str,
                 streaming_input: ChatbotStreamingInput, websocket: WebSocketManager):

        self._narrator_agent = narrator_agent
        self._chatbot = chatbot
        self._m_history = m_history[-5:]
        self._chatroom_summary = chatroom_summary
        self._streaming_input = streaming_input
        self._websocket = websocket

    def scenario_planning(self, state: ChatbotAgentState):
        return {'query': state['query']}

    def conditional_planning(self, state: ChatbotAgentState):
        start_sentence = state['query'][:7]

        print(start_sentence)
        if start_sentence == 'action:':
            return 'narrator_talk'
        else:
            return 'chatbot_talk'

    async def summary_chatbot_message(self, state: ChatbotAgentState):
        summary_factory = SimplePromptFactory(trace_name='Message Summary', trace_langfuse=False)

        summary_chain = summary_factory.create_chain(
            output_parser=StrOutputParser(),
            human_prompt_text=GENERAL_CHATBOT_MESSAGE_MERGE_PROMPT,
            partial_variables={
                'past_summary': self._chatroom_summary,
                'ai_message': state['final_message'],
                'user_message': state['query'],
            }
        )

        summary_str = await summary_chain.ainvoke({})
        return {'new_chatroom_summary': summary_str}

    async def mix_scenario(self, state: ChatbotAgentState):
        pass

    async def chat_chain(self, state: ChatbotAgentState):

        prompt_template = db_message_to_prompt(system_prompt=GENERAL_CHATBOT_SYSTEM_PROMPT,
                                               human_prompt=GENERAL_HUMAN_PROMPT,
                                               messages=self._m_history)
        # prompt_template = ChatPromptTemplate.from_messages([
        #     ("system", GENERAL_CHATBOT_SYSTEM_PROMPT),
        #     ("user", GENERAL_HUMAN_PROMPT),
        # ])

        variables = {
            **bot_variable(self._chatbot, self._chatroom_summary),
            'query': state['query']
        }

        chain = (prompt_template | gpt_model(model_name=OpenAI_Model_4o_mini) | StrOutputParser())

        stram_chain = chain.astream(variables)
        result = await streaming_exec(websockets=self._websocket, event_tag=SocketEvent.bot, websocket_id=self._streaming_input.websocket_id,
                                      session_id=self._streaming_input.session_id,
                                      token=self._streaming_input.token,
                                      bot_id=self._chatbot.id, identity=ChatbotUserEnum.bot,
                                      stream=stram_chain)
        return {'final_message': [result]}

    def create_graph(self):
        g_workflow = StateGraph(ChatbotAgentState)

        g_workflow.add_node('scenario_planning', self.scenario_planning)

        g_workflow.add_node('chatbot_talk', self.chat_chain)
        g_workflow.add_node('narrator_talk', self._narrator_agent.create_graph())
        g_workflow.add_node('mix_scenario', self.mix_scenario)

        g_workflow.add_node('message_summary', self.summary_chatbot_message)

        g_workflow.set_entry_point('scenario_planning')

        g_workflow.add_conditional_edges('scenario_planning', self.conditional_planning)

        g_workflow.add_edge('narrator_talk', 'chatbot_talk')
        g_workflow.add_edge('chatbot_talk', 'message_summary')
        g_workflow.add_edge('chatbot_talk', 'mix_scenario')

        g_workflow.add_edge('message_summary', END)
        g_workflow.add_edge('mix_scenario', END)

        g_compile = g_workflow.compile()

        return g_compile

