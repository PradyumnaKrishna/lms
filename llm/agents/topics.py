from typing import List

from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.output_parsers import BooleanOutputParser, PydanticOutputParser

from langchain_core.language_models import BaseLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever

from pydantic import BaseModel, Field
from pydantic.v1 import BaseModel as V1BaseModel

from . import BaseAgent


class Topics(BaseModel):
    topics: List[str] = Field(description="Important topics")


class TopicMap(V1BaseModel):
    document: Document
    topics: List[str]


class MapTopics(BaseAgent):
    """
    Maps topics to documents.

    The agent finds checks the topic is relevant to the document and then
    maps the topics to the document. Returns a list of TopicMap objects.
    """

    prompt = PromptTemplate.from_template(
        "Is the text relevant to the topic provided. Answer only with YES or NO, nothing else.\nTopic: {topic}\nContext: {context}"
    )
    parser = BooleanOutputParser()

    def run(self, topics: Topics, retriever: VectorStoreRetriever) -> List[TopicMap]:

        chain = self.prompt | self.llm | self.parser

        mapping = []
        for topic in topics.topics:
            doc = retriever.invoke(topic)[0]
            is_relevant = chain.invoke({
                "topic": topic,
                "context": doc,
            })
            if is_relevant:
                for tm in mapping:
                    if tm.document == doc:
                        tm.topics.append(topic)
                        break
                else:
                    mapping.append(TopicMap(document=doc, topics=[topic]))

        return mapping


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
