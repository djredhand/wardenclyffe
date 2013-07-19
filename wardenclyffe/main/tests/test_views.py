from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from wardenclyffe.main.models import Collection, Video, File
import uuid


class SimpleTest(TestCase):
    """ most of these tests are just about getting
    the absolute bare minimum of test coverage in place,
    hitting pages and just making sure they return the
    appropriate 200/302 status instead of generating a
    server error. *Real* tests can come later.
    """
    def setUp(self):
        self.u = User.objects.create(username="foo", is_staff=True)
        self.u.set_password("bar")
        self.u.save()
        self.c = Client()
        self.collection = Collection.objects.create(
            title="Mediathread Spring 2012",
            subject="test subject",
            uuid=uuid.uuid4())
        self.video = Video.objects.create(collection=self.collection,
                                          title="test video",
                                          creator="anp8",
                                          subject="test subject",
                                          uuid=uuid.uuid4())
        self.file = File.objects.create(
            video=self.video,
            label="CUIT File",
            location_type="cuit",
            filename=("/media/h264/ccnmtl/secure/"
                      "courses/56d27944-4131-11e1-8164-0017f20ea192"
                      "-Mediathread_video_uploaded_by_mlp55.mp4"),
        )

    def tearDown(self):
        self.u.delete()

    def test_index(self):
        response = self.c.get('/')
        self.assertEquals(response.status_code, 302)

        self.c.login(username="foo", password="bar")
        response = self.c.get('/')
        self.assertEquals(response.status_code, 200)

    def test_dashboard(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/dashboard/")
        self.assertEquals(response.status_code, 200)

    def test_received_invalid(self):
        response = self.c.post("/received/")
        assert response.content == "expecting a title"

    def test_received(self):
        response = self.c.post("/received/",
                               {'title': 'some title. not a uuid'})
        assert response.content == "ok"

    def test_recent_operations(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/recent_operations/")
        self.assertEquals(response.status_code, 200)

    def test_upload_form(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/upload/")
        self.assertEquals(response.status_code, 200)

        response = self.c.get("/scan_directory/")
        self.assertEquals(response.status_code, 200)

    def test_upload_errors(self):
        # if we try to post without logging in, should get redirected
        response = self.c.post("/upload/post/")
        self.assertEquals(response.status_code, 302)

        self.c.login(username="foo", password="bar")
        # GET should not work
        response = self.c.get("/upload/post/")
        self.assertEquals(response.status_code, 302)

        # invalid form
        response = self.c.post("/upload/post/")
        self.assertEquals(response.status_code, 302)

    def test_subject_autocomplete(self):
        response = self.c.get("/api/subjectautocomplete/", dict(q="test"))
        self.assertEquals(response.status_code, 200)

    def test_uuid_search(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/uuid_search/", dict(uuid=self.video.uuid))
        self.assertEquals(response.status_code, 200)

    def test_search(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/search/", dict(q="test"))
        self.assertEquals(response.status_code, 200)

    def test_file_filter(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get(
            "/file/filter/",
            dict(
                include_collection=self.collection.id,
            ))
        self.assertEquals(response.status_code, 200)

    def test_video_index(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/video/")
        self.assertEquals(response.status_code, 200)

    def test_file_index(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/file/")
        self.assertEquals(response.status_code, 200)

    def test_user_page(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/user/foo/")
        self.assertEquals(response.status_code, 200)

    def test_collection_videos(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/collection/%d/videos/" % self.collection.id)
        self.assertEquals(response.status_code, 200)

    def test_collection_operations(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/collection/%d/operations/"
                              % self.collection.id)
        self.assertEquals(response.status_code, 200)

    def test_collection_page(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/collection/%d/" % self.collection.id)
        self.assertEquals(response.status_code, 200)

    def test_slow_operations(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/slow_operations/")
        self.assertEquals(response.status_code, 200)


class TestSurelink(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="foo", is_staff=True)
        self.u.set_password("bar")
        self.u.save()
        self.c = Client()
        self.c.login(username="foo", password="bar")
        self.collection = Collection.objects.create(
            title="Mediathread Spring 2012",
            uuid=uuid.uuid4())
        self.video = Video.objects.create(collection=self.collection,
                                          title="test video",
                                          creator="anp8",
                                          uuid=uuid.uuid4())
        self.file = File.objects.create(
            video=self.video,
            label="CUIT File",
            location_type="cuit",
            filename=("/media/h264/ccnmtl/secure/"
                      "courses/56d27944-4131-11e1-8164-0017f20ea192"
                      "-Mediathread_video_uploaded_by_mlp55.mp4"),
        )
        self.public_file = File.objects.create(
            video=self.video,
            label="CUIT File",
            location_type="cuit",
            filename=("/media/h264/ccnmtl/public/"
                      "courses/56d27944-4131-11e1-8164-0017f20ea192"
                      "-Mediathread_video_uploaded_by_mlp55.mp4"),
        )

    def tearDown(self):
        self.u.delete()

    def test_surelink_form(self):
        response = self.c.get("/surelink/")
        self.assertEquals(response.status_code, 200)

    def test_file_surelink_form(self):
        response = self.c.get("/file/%d/" % self.file.id)
        self.assertEquals(response.status_code, 200)

        response = self.c.get("/file/%d/surelink/" % self.file.id)
        self.assertEquals(response.status_code, 200)

    def test_file_surelink_public_stream(self):
        """ regression test for PMT #87084 """
        response = self.c.get("/file/%d/" % self.file.id)
        self.assertEquals(response.status_code, 200)

        response = self.c.get(
            "/file/%d/surelink/" % self.public_file.id,
            {'file': self.public_file.filename,
             'captions': '',
             'poster': ('http://wardenclyffe.ccnmtl.columbia.edu/'
                        'uploads/images/11213/00000238.jpg'),
             'width': self.public_file.guess_width(),
             'height': self.public_file.guess_height(),
             'protection': 'mp4_public_stream',
             'authtype': '',
             'player': 'v4',
             })
        self.assertEquals(response.status_code, 200)
        assert "&lt;iframe" in response.content
        assert "file=/media/h264/ccnmtl/" not in response.content
        assert "file=/course" in response.content


class TestFeed(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="foo")
        self.u.set_password("bar")
        self.u.save()
        self.c = Client()
        self.collection = Collection.objects.create(
            title="Mediathread Spring 2012",
            uuid=uuid.uuid4())
        self.video = Video.objects.create(collection=self.collection,
                                          title="test video",
                                          creator="anp8",
                                          uuid=uuid.uuid4())
        self.file = File.objects.create(
            video=self.video,
            label="CUIT File",
            location_type="cuit",
            filename=("/media/h264/ccnmtl/secure/"
                      "courses/56d27944-4131-11e1-8164-0017f20ea192"
                      "-Mediathread_video_uploaded_by_mlp55.mp4"),
        )

    def tearDown(self):
        self.u.delete()

    def test_rss_feed(self):
        response = self.c.get("/collection/%d/rss/" % self.collection.id)
        self.assertEquals(response.status_code, 200)


class TestStats(TestCase):
    def test_stats_page(self):
        self.c = Client()
        response = self.c.get("/stats/")
        self.assertEquals(response.status_code, 200)
