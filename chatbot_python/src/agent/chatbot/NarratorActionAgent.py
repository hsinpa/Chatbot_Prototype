from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.constants import END
from langgraph.graph import StateGraph

from agent.GraphAgent import GraphAgent
from agent.agent_utility import streaming_exec
from agent.chatbot.ChatbotGraphAgent import ChatbotGraphAgent
from agent.chatbot.narrator_type import NarratorActionState, ActionType
from model.chatbot_model import ChatbotNPCDBType, ChatbotUserEnum
from prompt.chatbot_prompt import GENERAL_NARRATOR_SYSTEM_PROMPT, GENERAL_HUMAN_PROMPT
from prompt.scenario_prompt import ScenarioValidationPrompt
from router.chatbot_route_model import ChatbotStreamingInput
from utility.llm_static import LLMModel, Llama_3_1_8b, get_model
from utility.simple_prompt_factory import SimplePromptFactory
from utility.utility_method import gpt_model
from websocket.websocket_manager import WebSocketManager


class NarratorActionAgent(GraphAgent):

    def __init__(self, narrator: ChatbotNPCDBType, user_action: str, scenario: str,
                 streaming_input: ChatbotStreamingInput, websocket: WebSocketManager):
        self._narrator = narrator
        self._user_action = user_action
        self._scenario = scenario
        self._streaming_input = streaming_input
        self._websocket = websocket

    async def validation_chain(self, state: NarratorActionState):
        factory = SimplePromptFactory(
            llm_model=LLMModel.TogetherAI,
            model_name=Llama_3_1_8b,
            json_response=True,
            pydantic_schema=ActionType.schema()
        )

        simple_chain = factory.create_chain(
            output_parser=JsonOutputParser(pydantic_object=ActionType),
            human_prompt_text=ScenarioValidationPrompt,
            partial_variables={'scenario': self._scenario, 'action': self._user_action},
        )

        validation_result: ActionType = await simple_chain.ainvoke({})
        print(validation_result)

        return {'is_valid': validation_result.is_valid}

    async def mix_scenario_chain(self, state: NarratorActionState):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", GENERAL_NARRATOR_SYSTEM_PROMPT),
            ("user", GENERAL_HUMAN_PROMPT),
        ])

        variables = {
            **ChatbotGraphAgent.bot_variable(self._narrator, self._scenario),
            'query': self._user_action
        }

        chain = (prompt_template | gpt_model() | StrOutputParser())

        stram_chain = chain.astream(variables)
        result = await streaming_exec(websockets=self._websocket, session_id=self._streaming_input.session_id,
                                      token=self._streaming_input.token, identity=ChatbotUserEnum.narrator,
                                      stream=stram_chain)
        return {'narrator_response': result}

    def condition_router(self, state: NarratorActionState):
        if state['is_valid']:
            return 'mix_scenario'
        return END

    def create_graph(self):
        g_workflow = StateGraph(NarratorActionState)

        g_workflow.add_node('validation', self.validation_chain)
        g_workflow.add_node('mix_scenario', self.mix_scenario_chain)

        g_workflow.set_entry_point('validation')
        g_workflow.add_conditional_edges('validation', self.condition_router)
        g_workflow.add_edge('mix_scenario', END)

        g_compile = g_workflow.compile()

        return g_compile
