from langchain_core.output_parsers import JsonOutputParser
from langgraph.constants import END
from langgraph.graph import StateGraph

from agent.GraphAgent import GraphAgent
from agent.memory.memory_prompt import MEMORY_PREFACE_SYSTEM_PROMPT
from agent.memory.memory_type import ChatbotMemoryState, ChatNewKnowledgeType
from agent.tools.ultimate_json_parser import UltiJsonOutputParser
from model.chatbot_model import ChatMessageDBInputType
from utility.llm_static import LLMModel, Llama_3_1_8b
from utility.simple_prompt_factory import SimplePromptFactory


class MemoryGraphAgent(GraphAgent):
    def __init__(self, chatroom_id: int, messages: list[ChatMessageDBInputType]):
        self.chatroom_id = chatroom_id
        self._messages = messages

    async def _execute_preface_chain(self, state: ChatbotMemoryState):
        simple_factory = SimplePromptFactory(trace_name='Preface check', json_response=True)
        simple_chain = simple_factory.create_chain(
            output_parser=JsonOutputParser(pydantic_object=ChatNewKnowledgeType),
            human_prompt_text=MEMORY_PREFACE_SYSTEM_PROMPT,
            partial_variables={'interest': 'Fruit and everything from cook or baking', 'knowledge': ''}
        )

        new_knowledge_type = await simple_chain.ainvoke({})

        return {'new_knowledge': new_knowledge_type}

    async def _execute_preface_check(self, state: ChatbotMemoryState):
        return str(state['new_knowledge']['result'])

    def create_graph(self):
        g_workflow = StateGraph(ChatbotMemoryState)

        g_workflow.add_node('preface_chain', self._execute_preface_chain)

        g_workflow.set_entry_point('preface_chain')

        g_workflow.add_conditional_edges('preface_chain', self._execute_preface_check, {
            'False': END,
            'True': END
        })

        g_compile = g_workflow.compile()

        return g_compile
