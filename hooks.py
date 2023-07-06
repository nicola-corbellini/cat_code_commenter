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
    if "task" in user_message_json["prompt_settings"]:  # and "language" in user_message_json.keys():
        cat.working_memory["task"] = user_message_json["prompt_settings"]["task"]

    if "language" in user_message_json["prompt_settings"]:
        cat.working_memory["language"] = user_message_json["prompt_settings"]["language"]

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
    log(message, "ERROR")

    if "task" in cat.working_memory and cat.working_memory["task"] == "comment":
        answer = cat.llm.predict(
            f"""Write a JSON like this:
                {{  
                    'language': the programming language name
                    'code': the code
                }}
            Sentence
            --------
            {message["content"]}
            Only write the structered sentence.
        """)

        message["content"] = answer

        log(answer, "ERROR")

    return message
