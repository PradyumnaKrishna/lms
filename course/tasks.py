import json
import uuid

from huey.contrib.djhuey import task

from course.models import Answer, CoursePage, Question, QuestionPaper, Resource
from home.models import HomePage, InstitutePage
from llm.tasks import _generate_paper


@task()
def generate_paper(course_id: int):
    course = CoursePage.objects.get(id=course_id)
    resources = course.get_children().type(Resource)

    parent = InstitutePage.objects.filter(slug="question-papers").first()
    if parent is None:
        parent = InstitutePage(title="Question Papers", short_name="QP", slug="question-papers")

        home = HomePage.objects.get()
        home.add_child(instance=parent)

    question_paper = QuestionPaper(course=course, title=uuid.uuid4())
    parent.add_child(instance=question_paper)

    topics = []
    for resource in resources:
        topics.extend(json.loads(resource.specific.topics))

    paper = _generate_paper(course_id, topics).get(blocking=True).questions

    questions = []
    for _question in paper:
        question = Question(question=_question.question)
        question.answers = [
            Answer(answer=answer, is_correct=_question.answer.lower() == answer.lower())
            for answer in _question.options
        ]
        questions.append(question)

    question_paper.questions = questions
    question_paper.save()
