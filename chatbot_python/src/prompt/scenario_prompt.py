ScenarioTemplatePrompt = '''
The human player set on the chair, with both hand been cuffed at back.
Room is pretty small, with only one exist door lead to kitchen. However, it is locked two.
So basically, human player need find two different key, in order to leave the dark room.

One key to unlock handcuff is under player's chair, but they can hardly been seen. 
The send one for exist, is the prize of puzzle.

The room has a huge poster of president Lincoln, and his story of saving Black slaves.   
'''

ScenarioValidationPrompt = '''
Given the following scenario illustration
"""
{scenario}
"""

The human player do an action
"""
{action}
"""

Give your reason first and verify if the action is valid

Return the output in JSON format, and no extra word beside json string

thought: str = Field(..., description='Reason for your validation output')
is_valid: bool = Field(..., description='Is the action valid')

```json
{{
    "thought": "",
    "is_valid": false
}}
'''
