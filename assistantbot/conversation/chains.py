import os
import pickle
from pathlib import Path

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate

from assistantbot.ai.text.llm import chat_llm
from assistantbot.ai.text.prompts.conversation import (
    CONVERSATION_BASE_TEMPLATE,
)

# The path to the conversation chains
CONVERSATION_PATHS = "assistantbot/conversation/chains/"
PATH_CONVERSATION_CHAINS = os.path.join(CONVERSATION_PATHS, "{user_id}.pkl")


def update_memory(
    user_id: int, conversation_chain: ConversationChain
) -> None:
    """
    This function updates the memory of the conversation chain in the pkl
    file.

    Parameters
    ----------
    user_id : int
        The user ID.
    conversation_chain : ConversationChain
        The conversation chain.
    """
    # Replace the conversation file
    CONVERSATION_FILE_USER = PATH_CONVERSATION_CHAINS.format(user_id=user_id)

    # Save the conversation file
    with open(CONVERSATION_FILE_USER, "wb") as f:
        pickle.dump(conversation_chain, f)


def get_conversation_chain(user_id: int) -> ConversationChain:
    """
    This function returns the conversation chain for the user.

    Parameters
    ----------
    user_id : int
        The user ID.

    Returns
    -------
    ConversationChain
        The conversation chain.
    """
    CONVERSATION_FILE_USER = PATH_CONVERSATION_CHAINS.format(user_id=user_id)
    # Get the dictionary of the conversations
    if not os.path.exists(CONVERSATION_FILE_USER):
        conversation_chain = ConversationChain(
            prompt=PromptTemplate(
                input_variables=["history", "input"],
                template=CONVERSATION_BASE_TEMPLATE,
            ),
            llm=chat_llm,
            verbose=False,
            memory=ConversationBufferMemory(ai_prefix="AssistantBot"),
        )
        # Save the conversation file
        with open(CONVERSATION_FILE_USER, "wb") as f:
            pickle.dump(conversation_chain, f)

    # Load the conversation file
    with open(CONVERSATION_FILE_USER, "rb") as f:
        conversation_chain = pickle.load(f)

    return conversation_chain


def clean_all_conversations() -> None:
    """
    This function cleans all the conversations.
    """
    for conversation_file in os.listdir(Path(CONVERSATION_PATHS)):
        if conversation_file.endswith(".pkl"):
            os.remove(
                os.path.join(Path(CONVERSATION_PATHS), conversation_file)
            )
