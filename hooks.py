"""Hooks to modify the Cat's flow of execution.

Here is a collection of methods to hook into the Cat execution pipeline.

"""

from cat.mad_hatter.decorators import hook
from cat.log import log

# Called when a user message arrives.
# Useful to edit/enrich user input (e.g. translation)
@hook(priority=0)
def before_cat_reads_message(user_message_json: dict, cat) -> dict:
    """Hook the incoming user's JSON dictionary.

    Allows to edit and enrich the incoming message received from the WebSocket connection.

    For instance, this hook can be used to translate the user's message before feeding it to the Cat.
    Another use case is to add custom keys to the JSON dictionary.

    The incoming message is a JSON dictionary with keys:
        {
            "text": message content
        }

    Parameters
    ----------
    user_message_json : dict
        JSON dictionary with the message received from the chat.
    cat : CheshireCat
        Cheshire Cat instance.


    Returns
    -------
    user_message_json : dict
        Edited JSON dictionary that will be fed to the Cat.

    Notes
    -----
    For example:

        {
            "text": "Hello Cheshire Cat!",
            "custom_key": True
        }

    where "custom_key" is a newly added key to the dictionary to store any data.

    """
    # Ask Language Model is the given input is code
    prompt = f"""Is this a valid code?
    {user_message_json['text']}
    Answer yes or no."""

    answer = cat.llm(prompt)

    # Save check in Working Memory
    if answer.lower() == "yes":
        cat.working_memory["valid_code"] = True
    else:
        cat.working_memory["valid_code"] = False
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
        f"""Reformulate this sentence in a JSON with this form.
        Example:
            {{  
                'language': programming language in the sentence.
                'commented_code': the code here
            }}
        Sentence:
        {message["content"]}
    """)

    message["content"] = answer
    log(answer, "ERROR")
    return message
