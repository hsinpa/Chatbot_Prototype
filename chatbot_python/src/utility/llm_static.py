from enum import Enum

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether

OpenAI_Model_4o = 'gpt-4o'
OpenAI_Model_3_5 = 'gpt-3.5-turbo'
OpenAI_Model_4o_mini = 'gpt-4o-mini'
Llama_3_1_8b = 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'
Grok_Llama_3_1_8b = 'llama-3.1-8b-instant'


class LLMModel(Enum):
    OpenAI = 2,
    TogetherAI = 3,
    Groq = 4,


def get_model(model_enum: LLMModel, model_name: str, **kwargs):
    if model_enum.value == LLMModel.OpenAI.value:
        return ChatOpenAI(
            model_name=model_name,
            **kwargs
        )

    if model_enum.value == LLMModel.TogetherAI.value:
        return ChatTogether(
            model=model_name,
            **kwargs
        )

    if model_enum.value == LLMModel.Groq.value:
        return ChatGroq(
            model_name=model_name,
            **kwargs
        )
