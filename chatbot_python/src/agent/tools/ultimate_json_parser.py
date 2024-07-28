import json
from typing import Any, Optional, Type, List
from langchain_core.output_parsers import JsonOutputToolsParser
from langchain_core.outputs import Generation
from pydantic.v1 import BaseModel


class UltiToolsOutputParser(JsonOutputToolsParser):
    """Custom boolean parser."""
    tools: List[Type[BaseModel]]

    def parse_result(self, result: List[Generation], *, partial: bool = False) -> Any:
        print('parse_result')
        print(result)
        chat_generation = result[0]
        tool_result: List[BaseModel] = []

        for tool_model, tool_json in zip(self.tools, chat_generation.message.tool_calls):
            tool_name = tool_json['name']
            tool_args = tool_json['args']

            tool_result.append(tool_model(name=tool_name, **tool_args))

        # raw_json = result[0]
        # print(raw_json)
        #
        # tools = raw_json.message.tool_calls
        # print(tools[0]['name'])
        # print(tools[0]['args'])

        return tool_result
