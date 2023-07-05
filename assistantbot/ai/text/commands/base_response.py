from typing import Optional

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from assistantbot.ai.text.llm import chat_llm


class BaseResponse:
    """
    This class is the base class for all response commands.
    """

    def __init__(
        self,
        base_prompt: str,
        user_prompt: str,
        llm: Optional[ChatOpenAI] = chat_llm,
    ) -> None:
        """
        This function initializes the class.

        Parameters
        ----------
        base_prompt : str
            The base prompt for the command.
        user_prompt : str
            The user prompt for the command.
        llm : Optional[ChatOpenAI]
            The language model to use.
        """
        self.base_prompt = base_prompt
        self.user_prompt = user_prompt
        self.llm = llm

    def create_response(self, **kwargs) -> str:
        """
        This function creates the response for the command.

        Returns
        -------
        str
            The response for the command.
        """
        # Create the system and human prompt
        system_prompt = SystemMessagePromptTemplate.from_template(
            self.base_prompt
        )
        human_prompt = HumanMessagePromptTemplate.from_template(
            self.user_prompt
        )

        # Create the chat prompt
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_prompt, human_prompt]
        )

        return self.llm(
            chat_prompt.format_prompt(**kwargs).to_messages()
        ).content
