import base64
import binascii

from django.core.files.base import ContentFile

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from wagtail.documents.models import Document

from course.models import CoursePage, Resource
from .serializers import AnnouncementSerializer, ResourceSerializer



class AnnouncementView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        data = request.data
        serializer = AnnouncementSerializer(data=data)
        if serializer.is_valid():
            if "attachment" in request.FILES:
                parent = CoursePage.objects.get(pk=data["course"])

                attachment = request.FILES["attachment"]
                filename = attachment.name
                document = Document(title=filename, file=ContentFile(attachment.read(), name=filename))
                document.save()

                resource = Resource(
                    title=data['title'],
                    content=data['body'],
                    attachment=document,
                )

                parent.add_child(instance=resource)
                resource.save_revision().publish()

                serializer = ResourceSerializer(resource)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            if "attachment" in request.data:
                return Response({"error": "attachment must be a file"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
