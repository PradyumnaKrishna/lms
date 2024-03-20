from rest_framework import serializers
from course.models import Announcement, Resource


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['course', 'title', 'body']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['title', 'content', 'attachment']
