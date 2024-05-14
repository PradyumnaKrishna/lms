from typing import List

from langchain.output_parsers import PydanticOutputParser

from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field

from . import BaseAgent
from .topics import TopicMap


class Question(BaseModel):
    question: str = Field(description="Question")
    options: List[str] = Field(description="Options for multiple choice")
    answer: str = Field(description="Correct answer to the question")


class QuestionPaper(BaseModel):
    questions: List[Question] = Field(description="List of questions")


class QAAgent(BaseAgent):
    """
    Generates Question Paper using the ``TopicMap`` provided.

    """

    parser = PydanticOutputParser(pydantic_object=QuestionPaper)
    prompt = PromptTemplate.from_template(
        """
        You are a smart assistant designed to help graduate students practicing exam with multiple choice questions.
        Given a piece of text, you must come up with some question and answer pairs from the topics provided that can be used to test a student's abilities.
        When coming up with this question/answer pair, you must respond in the following format: {instructions}
        The questions must come from the following topics: {topics}

        {context}"""
    ).partial(instructions=parser.get_format_instructions())

    def run(self, mapping: List[TopicMap]) -> QuestionPaper:
        chain = self.prompt | self.llm | self.parser

        question_paper = QuestionPaper(questions=[])
        for topicmap in mapping:
            question_paper.questions.extend(
                chain.invoke({
                    "topics": ", ".join(topicmap.topics),
                    "context": topicmap.document.page_content,
                }).questions
            )

        return question_paper
