import json
from typing import Any, Optional, Type, List
from langchain_core.output_parsers import JsonOutputToolsParser
from langchain_core.outputs import Generation
from pydantic import BaseModel


class UltiToolsOutputParser(JsonOutputToolsParser):
    """Custom boolean parser."""
    tools: List[Type[BaseModel]]

    def parse_result(self, result: List[Generation], *, partial: bool = False) -> Any:
        print('parse_result')
        print(result)

        try:
            chat_generation = result[0]
            tool_result: List[BaseModel] = []

            for tool_model, tool_json in zip(self.tools, chat_generation.message.tool_calls):
                tool_name = tool_json['name']
                tool_args = tool_json['args']

                tool_result.append(tool_model(name=tool_name, **tool_args))

            return tool_result

        except Exception as e:
            print('UltiToolsOutputParser Error ', e)
            return []
