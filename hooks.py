"""Hooks to modify the Cat's flow of execution.

Here is a collection of methods to hook into the Cat execution pipeline.

"""

from cat.mad_hatter.decorators import hook
from cat.log import log


# Called when a user message arrives.
# Useful to edit/enrich user input (e.g. translation)
@hook(priority=1)
def before_cat_reads_message(user_message_json: dict, cat) -> dict:
    # Get task
    cat.working_memory["code_extension"] = {}

    cat.working_memory["code_extension"]["task"] = user_message_json["task"]
    cat.working_memory["code_extension"]["language"] = user_message_json["language"]

    return user_message_json


# Hook called just before sending response to a client.
@hook(priority=1)
def before_cat_sends_message(message: dict, cat) -> dict:
    """Hook the outgoing Cat's message.

    Allows to edit the JSON dictionary that will be sent to the client via WebSocket connection.

    This hook can be used to edit the message sent to the user or to add keys to the dictionary.

    Parameters
    ----------
    message : dict
        JSON dictionary to be sent to the WebSocket client.
    cat : CheshireCat
        Cheshire Cat instance.

    Returns
    -------
    message : dict
        Edited JSON dictionary with the Cat's answer.

    Notes
    -----
    Default `message` is::

            {
                "error": False,
                "type": "chat",
                "content": cat_message["output"],
                "why": {
                    "input": cat_message["input"],
                    "output": cat_message["output"],
                    "intermediate_steps": cat_message["intermediate_steps"],
                    "memory": {
                        "vectors": {
                            "episodic": episodic_report,
                            "declarative": declarative_report
                        }
                    },
                },
            }

    """
    # Add valid code check in JSON response
    # message["valid_code"] = cat.working_memory["valid_code"]

    answer = cat.llm(
        f"""Structure the sentence in a JSON with this format:
            {{  
                'language': the programming language name
                'code': the code
            }}
        Sentence
        --------
        {message["content"]}
    """)

    message["content"] = answer
    log(answer, "ERROR")
    return message
