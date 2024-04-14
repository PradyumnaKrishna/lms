from rest_framework import serializers
from course.models import Announcement, Resource, CoursePage

from wagtail.documents.models import Document


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['course', 'title', 'body']


class ResourceSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=False)
    course = serializers.PrimaryKeyRelatedField(queryset=CoursePage.objects.all(), write_only=True)

    class Meta:
        model = Resource
        fields = ['title', 'content', 'attachment', 'course']

    def create(self, validated_data):
        course = validated_data.pop('course')
        attachment = validated_data.pop('attachment', None)

        if attachment:
            document = Document(title=attachment.name, file=attachment)
            document.save()
            validated_data['attachment'] = document

        resource = Resource(**validated_data)
        course.add_child(instance=resource)
        resource.save_revision().publish()

        return resource
