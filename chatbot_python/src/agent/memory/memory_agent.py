from typing import List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.constants import END
from langgraph.graph import StateGraph

from agent.GraphAgent import GraphAgent
from agent.agent_utility import reform_db_message, db_message_to_str, db_memory_to_str
from agent.memory.memory_prompt import MEMORY_PREFACE_SYSTEM_PROMPT, MEMORY_TOOL_SYSTEM_PROMPT
from agent.memory.memory_type import ChatbotMemoryState, ChatNewKnowledgeType, ChatKnowledgeOpsType, Action, \
    knowledge_ops_facade_tool, ChatKnowledgeType
from agent.tools.ultimate_json_parser import UltiToolsOutputParser
from model.chatbot_model import ChatMessageDBInputType
from utility.llm_static import LLMModel, get_model, OpenAI_Model_4o_mini
from utility.simple_prompt_factory import SimplePromptFactory
from utility.utility_method import get_langfuse_callback


class MemoryGraphAgent(GraphAgent):
    def __init__(self, chatroom_id: int, messages: list[ChatMessageDBInputType], knowledge: List[ChatKnowledgeType]):
        self.chatroom_id = chatroom_id
        self._messages = messages
        self._knowledge = knowledge
        self._knowledge_str = db_memory_to_str(knowledge)

    async def _execute_preface_chain(self, state: ChatbotMemoryState):
        past_message = db_message_to_str(self._messages)
        simple_factory = SimplePromptFactory(trace_name='Preface check', json_response=True)
        simple_chain = simple_factory.create_chain(
            output_parser=JsonOutputParser(pydantic_object=ChatNewKnowledgeType),
            human_prompt_text=MEMORY_PREFACE_SYSTEM_PROMPT,
            partial_variables={'interest': 'Fruit and everything from cook or baking', 'past_messages': past_message,
                               'knowledge': self._knowledge_str}
        )

        new_knowledge_type = await simple_chain.ainvoke({})

        return {'new_knowledge': new_knowledge_type}

    async def _preface_conditional_check(self, state: ChatbotMemoryState):
        return str(state['new_knowledge']['result'])

    async def _execute_knowledge_ops_chain(self, state: ChatbotMemoryState):
        past_messages = reform_db_message(self._messages)
        past_messages.insert(0, ("system", MEMORY_TOOL_SYSTEM_PROMPT))

        prompt_template = ChatPromptTemplate.from_messages(past_messages)
        llm = get_model(LLMModel.OpenAI, OpenAI_Model_4o_mini)
        llm_tool = llm.bind_tools([knowledge_ops_facade_tool])

        chain = (prompt_template | llm_tool | UltiToolsOutputParser(tools=[ChatKnowledgeOpsType])).with_config(
            {'callbacks': [get_langfuse_callback()], "run_name": 'Memory: function tool'}
        )

        result = await chain.ainvoke({
            'interest': 'Fruit and everything from cook or baking',
            'knowledge': self._knowledge_str
        })

        return {'knowledge_ops': result}

    def create_graph(self):
        g_workflow = StateGraph(ChatbotMemoryState)

        g_workflow.add_node('preface_chain', self._execute_preface_chain)
        g_workflow.add_node('knowledge_chain', self._execute_knowledge_ops_chain)

        g_workflow.set_entry_point('preface_chain')

        g_workflow.add_conditional_edges('preface_chain', self._preface_conditional_check, {
            'False': END,
            'True': 'knowledge_chain'
        })

        g_workflow.add_edge('knowledge_chain', END)

        g_compile = g_workflow.compile()

        return g_compile
