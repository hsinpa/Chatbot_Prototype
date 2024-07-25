from enum import Enum

from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether

OpenAI_Model_4o = 'gpt-4o'
OpenAI_Model_3_5 = 'gpt-3.5-turbo'
OpenAI_Model_4o_mini = 'gpt-4o-mini'
Llama_3_1_8b = 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'


class LLMModel(Enum):
    TogetherAI = 1,
    OpenAI = 2,


def get_model(model_enum: LLMModel, model_name: str, **kwargs):
    if model_enum == LLMModel.OpenAI:
        return ChatOpenAI(
            model_name=model_name,
            **kwargs
        )

    if model_enum == LLMModel.TogetherAI:
        return ChatTogether(
            model=model_name,
            **kwargs
        )
