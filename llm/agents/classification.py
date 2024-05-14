from enum import Enum
from typing import Type

from langchain.output_parsers import EnumOutputParser
from langchain_core.language_models import BaseLLM
from langchain_core.prompts import BasePromptTemplate, PromptTemplate

from . import BaseAgent


class ClassificationAgent(BaseAgent):
    """
    Classifies a message into a type obtained from an Enum.
    """

    prompt: BasePromptTemplate
    parser: EnumOutputParser

    def __init__(self, llm: BaseLLM, enum: Type[Enum]):
        self.parser = EnumOutputParser(enum=enum)
        self.prompt = PromptTemplate.from_template(
            "Classify the message into: {instructions}\nMessage: {message}"
        ).partial(instructions=f"{self.parser.get_format_instructions()}")

        super().__init__(llm)

    def run(self, message: str) -> Enum:
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"message": message})
