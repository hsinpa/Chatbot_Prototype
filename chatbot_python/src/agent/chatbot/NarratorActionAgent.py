from typing import List

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import END
from langgraph.graph import StateGraph
from langfuse.callback import CallbackHandler

from agent.GraphAgent import GraphAgent
from agent.agent_utility import streaming_exec, bot_variable
from agent.chatbot.narrator_type import NarratorActionState, ActionType
from model.chatbot_model import ChatbotNPCDBType, ChatbotUserEnum, ChatMessageDBInputType
from prompt.chatbot_prompt import GENERAL_NARRATOR_SYSTEM_PROMPT, GENERAL_NARRATOR_HUMAN_PROMPT
from prompt.scenario_prompt import ScenarioValidationPrompt
from router.chatbot_route_model import ChatbotStreamingInput
from utility.llm_static import LLMModel, Llama_3_1_8b, Grok_Llama_3_1_8b
from utility.simple_prompt_factory import SimplePromptFactory
from utility.utility_method import gpt_model
from websocket.websocket_manager import WebSocketManager


class NarratorActionAgent(GraphAgent):

    def __init__(self, narrator: ChatbotNPCDBType, m_history: List[ChatMessageDBInputType],
                 user_action: str, scenario: str,
                 streaming_input: ChatbotStreamingInput, websocket: WebSocketManager):
        self._narrator = narrator
        self._user_action = user_action
        self._scenario = scenario
        self._streaming_input = streaming_input
        self._websocket = websocket

    async def validation_chain(self, state: NarratorActionState):
        factory = SimplePromptFactory(
            llm_model=LLMModel.Groq,
            model_name=Grok_Llama_3_1_8b,
            json_response=True,
            trace_name='Validation Chain'
        )

        simple_chain = factory.create_chain(
            output_parser=JsonOutputParser(pydantic_object=ActionType),
            human_prompt_text=ScenarioValidationPrompt,
            input_variables=['scenario', 'action'],
        )

        validation_result = ActionType(**await simple_chain.ainvoke(
            {'scenario': self._scenario, 'action': self._user_action}
        ))
        print('validation_result', validation_result)
        return {'is_valid': validation_result.is_valid, 'validation_analysis': validation_result.thought}

    async def scenario_expand_chain(self, state: NarratorActionState):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", GENERAL_NARRATOR_SYSTEM_PROMPT),
            ("user", GENERAL_NARRATOR_HUMAN_PROMPT),
        ])

        variables = {
            **bot_variable(self._narrator, self._scenario),
            'query': self._user_action, 'validation_analysis': state['validation_analysis']
        }

        chain = (prompt_template | gpt_model() | StrOutputParser()).with_config(
            {'run_name': 'Mix Scenario', "callbacks": [CallbackHandler(user_id='hsinpa')]}
        )

        stram_chain = chain.astream(variables)

        print('self._streaming_input', self._streaming_input)
        result = await streaming_exec(websockets=self._websocket, session_id=self._streaming_input.session_id,
                                      websocket_id=self._streaming_input.websocket_id,
                                      token=self._streaming_input.token, bot_id=self._narrator.id,
                                      identity=ChatbotUserEnum.narrator,
                                      stream=stram_chain)
        return {'narrator_response': result, 'final_message': [result]}

    def create_graph(self):
        g_workflow = StateGraph(NarratorActionState)

        g_workflow.add_node('validation_node', self.validation_chain)
        g_workflow.add_node('scenario_node', self.scenario_expand_chain)

        g_workflow.set_entry_point('validation_node')
        g_workflow.add_edge('validation_node', 'scenario_node')
        g_workflow.add_edge('scenario_node', END)

        g_compile = g_workflow.compile()

        return g_compile
