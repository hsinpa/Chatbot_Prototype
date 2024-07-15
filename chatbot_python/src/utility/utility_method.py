import os

from langchain_openai import ChatOpenAI
from langfuse.callback import CallbackHandler

from utility.static_text import OpenAI_Model_3_5


def gpt_model(model_name: str = OpenAI_Model_3_5, temperature=0.7, json_response=False):
    kwargs = {'model_name': model_name, 'temperature': temperature}
    if json_response is True:
        kwargs['response_format'] = {"type": "json_object"}

    return ChatOpenAI(**kwargs)


def get_langfuse_callback():
    return CallbackHandler(
        user_id=os.environ['LANGFUSE_USER'])
