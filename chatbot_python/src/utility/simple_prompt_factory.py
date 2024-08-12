from typing import Sequence, Any, Type, Literal

from langchain_core.output_parsers import BaseOutputParser
from langchain.schema.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_openai.chat_models.base import BaseChatOpenAI
from langfuse.callback import CallbackHandler
from pydantic import BaseModel

from src.utility.llm_static import LLMModel, get_model, OpenAI_Model_4o_mini

load_dotenv()


class SimplePromptFactory():
    """A factory only accept and run one prompt, nothing more"""

    def __init__(
            self,
            temperature: float = 0.75,
            llm_model: LLMModel = LLMModel.OpenAI,
            model_name: str = OpenAI_Model_4o_mini,
            json_response: bool = False,
            pydantic_schema: dict[str, Any] = None,
            trace_langfuse: bool = True,
            tools_calling: Sequence[dict[str, Any] | Type[BaseModel] | Type[BaseModel]] = None,
            tools_choice:  Literal["auto", "none", "required", "any"] = 'auto',
            trace_name: str = None
    ):
        kwargs = {'temperature': temperature}
        if json_response is True:
            kwargs['model_kwargs'] = {"response_format": {"type": "json_object"}}

        if json_response is True and pydantic_schema is not None:
            kwargs['model_kwargs']['response_format']['schema'] = pydantic_schema

        self._langfuse_handler = None
        if trace_langfuse is True:
            self._langfuse_handler = CallbackHandler(user_id='hsinpa')

        self._llm: BaseChatOpenAI = get_model(model_enum=llm_model, model_name=model_name, **kwargs)

        if tools_calling is not None:
            self._llm = self._llm.bind_tools(tools=tools_calling, tool_choice=tools_choice)

        self.trace_name = trace_name

    def create_chain(
            self,
            output_parser: BaseOutputParser,
            human_prompt_text: str,
            system_prompt_text: str = None,
            input_variables: list[str] = None,
            partial_variables: dict = None,
    ):

        if partial_variables is None:
            partial_variables = {}
        if input_variables is None:
            input_variables = []
        if system_prompt_text is None:
            system_prompt_text = "You are a helpful assistant."

        prompt = self._create_prompt(system_prompt_text, human_prompt_text, input_variables, partial_variables)
        chain = prompt | self._llm | output_parser
        chain = chain.with_fallbacks([chain])

        if self._langfuse_handler is not None:
            chain = chain.with_config({"callbacks": [self._langfuse_handler]})

        if self.trace_name is not None:
            chain = chain.with_config({"run_name": self.trace_name})

        return chain

    def _create_prompt(self, system_prompt: str, human_prompt: str, input_variables: list[str],
                       partial_variables: dict):
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt),
        ]

        template = ChatPromptTemplate(
            messages=messages, input_variables=input_variables, partial_variables=partial_variables
        )

        return template
