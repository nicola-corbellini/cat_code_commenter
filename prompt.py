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

    task = cat.working_memory["task"]
    using_vs_ext = "task" in cat.working_memory

    if using_vs_ext and task == "comment":
        suffix = """{episodic_memory}

{declarative_memory}

{chat_history}
    Add comments this code.
     Code
     ----
     {input}
    
    Only answer with commented code"""
    elif using_vs_ext and task == "function":
        suffix = """{episodic_memory}

{declarative_memory}

{chat_history}

    {input}"""

    return suffix

    # You are an expert software engineer that writes good quality code.
    # Complete the code using the comment.
    # Code
    # ----
@hook(priority=1)
def agent_prompt_chat_history(chat_history: List[Dict], cat) -> str:

    history = ""
   
    return history
