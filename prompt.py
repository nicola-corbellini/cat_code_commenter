"""Hooks to modify the prompts.

Here is a collection of methods to hook the prompts components that instruct the *Agent*.

"""

import time
from typing import List, Dict
from datetime import timedelta
from langchain.docstore.document import Document

from cat.utils import verbal_timedelta
from cat.mad_hatter.decorators import hook


@hook(priority=1)
def agent_prompt_prefix(cat) -> str:
    prefix = ""

    return prefix


@hook(priority=1)
def agent_prompt_suffix(cat) -> str:

    if cat.working_memory["code_extension"]["task"] == "comment":
        suffix = """Add comments to the code.
     Code
     ----
     {input}
    
    Only answer with commented code. Don't add anything else.
    
    {agent_scratchpad}"""
    elif cat.working_memory["code_extension"]["task"] == "make_function":
        suffix = """"""

    return suffix


@hook(priority=1)
def agent_prompt_chat_history(chat_history: List[Dict], cat) -> str:

    history = ""
   
    return history