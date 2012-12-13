from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
import hmac
import hashlib
from django.conf import settings


class SimpleText(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="foo")
        self.u.set_password("bar")
        self.u.save()
        self.c = Client()

    def tearDown(self):
        self.u.delete()

    def test_invalid_auth(self):
        response = self.c.get("/mediathread/")
        self.assertEquals(
            response.content,
            "invalid authentication token")

    def test_upload_form(self):
        # make a correct one
        nonce = 'foobar'
        set_course = 'course_foo'
        username = 'foo'
        redirect_to = "http://www.example.com/"
        hmc = hmac.new(settings.MEDIATHREAD_SECRET,
                       '%s:%s:%s' % (username, redirect_to, nonce),
                       hashlib.sha1
                       ).hexdigest()

        response = self.c.get(
            "/mediathread/",
            {
                'nonce': nonce,
                'as': username,
                'redirect_url': redirect_to,
                'set_course': set_course,
                'hmac': hmc
                }
            )
        self.assertNotEquals(
            response.content,
            "invalid authentication token")