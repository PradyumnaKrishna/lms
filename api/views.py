import logging

from enum import Enum

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from llm.agents.classification import ClassificationAgent

from .apps import APIConfig
from .serializers import AnnouncementSerializer, ResourceSerializer
from course.models import QuestionPaper, CoursePage
from course.tasks import generate_paper


logger = logging.getLogger(__name__)


class NotificationType(str, Enum):
    ANNOUNCEMENT = "announcement"
    RESOURCE = "resource"


class NotificationView(APIView):
    parser_classes = [MultiPartParser]
    llm = APIConfig.llm

    def post(self, request, format=None):
        data = request.data
        serializer = AnnouncementSerializer(data=data)
        if "attachment" in data:
            serializer = ResourceSerializer(
                data={
                    "course": data["course"],
                    "title": data["title"],
                    "content": data["body"],
                    "attachment": data["attachment"],
                }
            )

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        agent = ClassificationAgent(self.llm, NotificationType)

        notification_type = None
        try:
            notification_type = agent.run(data["body"])
        except Exception as e:
            logger.error(f"Error classifying: {e}")

        if notification_type == NotificationType.RESOURCE:
            serializer = ResourceSerializer(
                data={
                    "title": data["title"],
                    "content": data["body"],
                    "course": data["course"],
                }
            )
        else:
            serializer = AnnouncementSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GeneratePaperView(APIView):
    def post(self, request, format=None):
        course_id = request.data.get("course_id")

        course = CoursePage.objects.get(id=course_id)
        question_paper = QuestionPaper.objects.filter(course=course, live=False)

        if question_paper.exists():
            return Response(
                {"message": "Already a request is submitted for this course. Try again later."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        generate_paper(course_id)
        response_data = {"message": "Request submitted successfully", "course_id": course_id}
        return Response(response_data, status=status.HTTP_200_OK)
