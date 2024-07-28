import json
from typing import List, Any, Optional, Type

from langchain_core.output_parsers import BaseOutputParser, JsonOutputToolsParser
from langchain_core.outputs import Generation
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field


class WeatherToolType(BaseModel):
    name: Optional[str] = Field(..., alias='name of function')
    location: str = Field(..., description='Location of a country, area or city given by the user')
    time: int = Field(..., description="""Hour time of the weather event, use 24-Hour Clock Time in specific""")


@tool(args_schema=WeatherToolType, return_direct=True)
def weather_tool(location: str, time: int) -> bool:
    """A weather report tool, will only return bool stand as shining or false if raining"""
    return True


class WeatherOutputParser(JsonOutputToolsParser):
    """Custom boolean parser."""
    tools: List[Type[BaseModel]]

    def parse_result(self, result: List[Generation], *, partial: bool = False) -> Any:
        print(result)
        raw_json = result[0]
        print(raw_json)

        tools = raw_json.message.tool_calls
        print(tools[0]['name'])
        return WeatherToolType(name=tools[0]['name'], **tools[0]['args'])