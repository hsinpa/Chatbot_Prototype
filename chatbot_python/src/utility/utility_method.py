import os
import re

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

def parse_block(code: str, raw_message: str) -> str | None:
    regex_sympy = r'```{code}(?:.|\n)*?```'
    regex_sympy = regex_sympy.replace('{code}', code)

    sympy_codes: list[str] = re.findall(regex_sympy, raw_message)

    if len(sympy_codes) > 0:
        raw_llm_msg: str = sympy_codes[0]
        raw_llm_msg = raw_llm_msg.replace(f'```{code}', '')
        raw_llm_msg = raw_llm_msg.replace('```', '')

        return raw_llm_msg

    return None
