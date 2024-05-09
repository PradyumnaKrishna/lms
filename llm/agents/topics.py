from typing import List

from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.output_parsers import PydanticOutputParser

from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseLLM

from pydantic import BaseModel, Field

from . import BaseAgent


class Topics(BaseModel):
    topics: List[str] = Field(description="Important topics")


class TopicModelling(BaseAgent):
    """
    Extracts topics from a list of documents.

    The agent uses a map-reduce chain to summarize each document into relevant
    topics and then combines these topics into a final list of topics.
    """

    parser = PydanticOutputParser(pydantic_object=Topics)
    prompt = PromptTemplate.from_template(
        """Summarize the most significant topics explained in the following text, nothing else:\n{text}\nTopics:"""
    )
    combine_prompt = PromptTemplate.from_template(
        """Reduce these topics into relevant topics, based on the topics provided only.\nInstructions: {instructions}\nTopics: {text}"""
    ).partial(instructions=f"{parser.get_format_instructions()}")

    def __init__(self, llm: BaseLLM):
        super().__init__(llm)

    def run(self, docs: List[Document]) -> Topics:
        chain = load_summarize_chain(
            self.llm,
            chain_type="map_reduce",
            map_prompt=self.prompt,
            combine_prompt=self.combine_prompt
        )

        summary = chain.run(docs)
        return self.parser.parse(summary)
