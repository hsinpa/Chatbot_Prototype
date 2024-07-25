MEMORY_PREFACE_SYSTEM_PROMPT = """
Your job is to assess a brief chat history in order to determine if the conversation contains any details about human user. 

You play the critical role of assessing the message to determine if it contains any information worth recording in the knowledge base.

You are only interested in the following categories of information:
{interest}

What the user already knows
{knowledge}

Return in JSON format, as follow

thought: str = Field(..., description='Analyze the message for new information, in contrast to what user already know')
result: bool = Field(..., description='If it has any information worth recording, return TRUE. If not, return FALSE')

Take a deep breath, think step by step, and then analyze the following message:
"""