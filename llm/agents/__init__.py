"""
Define Abstract Agent class
"""

from abc import abstractmethod

from langchain_core.language_models import BaseLLM


class BaseAgent:
    """
    Base LLM Agent class
    """

    llm: BaseLLM

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        runs the agent
        """
        pass
