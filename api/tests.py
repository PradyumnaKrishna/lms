from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile

from wagtail.models import Page, Site
from wagtail.documents.models import Document
from wagtail.test.utils import WagtailPageTestCase

from api.views import AnnouncementView
from course.models import Announcement, CoursePage, Resource


class AnnouncementViewTestCase(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        root = Page.get_first_root_node()
        
        Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
            site_name="testserver",
        )
        cls.course = CoursePage(
            title='Test Course',
            description="test",
            code='TST123',
            credit=3,
            topics='Test Topics'
        )

        root.add_child(instance=cls.course)
        cls.course.save_revision()
        cls.view = AnnouncementView.as_view()

    def test_create_announcement(self):
        request = self.factory.post('/api/announcements/', {
            'title': 'Test Announcement',
            'body': 'Test Body',
            'course': self.course.pk,
        })
        response = self.view(request)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Resource.objects.count(), 0)
        self.assertEqual(Announcement.objects.count(), 1)

    def test_create_resource(self):
        request = self.factory.post('/api/announcements/', {
            'title': 'test',
            'body': 'Test Body',
            'course': self.course.pk,
            'attachment': SimpleUploadedFile("file.txt", b"file_content"),
        })
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Resource.objects.count(), 1)
        self.assertEqual(Announcement.objects.count(), 0)

        resources = CoursePage.objects.get(pk=self.course.pk).get_children_count()
        self.assertEqual(resources, 1)
        attachment_content = Resource.objects.get(title="test").attachment.file.read()
        self.assertEqual(attachment_content, b"file_content")

    def test_create_resource_with_invalid_data(self):
        request = self.factory.post('/api/announcements/', {
            'title': 'test',
            'body': 'Test Body',
            'course': -1,
        })
        response = self.view(request)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Resource.objects.count(), 0)

    def test_create_resource_with_invalid_attachment(self):
        request = self.factory.post('/api/announcements/', {
            'title': 'test',
            'body': 'Test Body',
            'course': self.course.pk,
            'attachment': 'invalid_attachment',
        })
        response = self.view(request)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Resource.objects.count(), 0)
        self.assertEqual(Document.objects.count(), 0)
