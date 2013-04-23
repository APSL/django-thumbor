# -*- coding: utf-8 -*-

from mock import patch
from unittest import TestCase
from django_thumbor import generate_url, conf
from django.test.utils import override_settings
from django.conf import settings


class TestGenerateURL(TestCase):

    url = 'domain.com/path/image.jpg'

    def assertPassesArgsToCrypto(self, *args, **kwargs):
        with patch('django_thumbor.crypto.generate') as mock:
            generate_url(*args, **kwargs)
            mock.assert_called_with(*args, **kwargs)

    def test_should_pass_url_arg_to_crypto(self):
        with patch('django_thumbor.crypto.generate') as mock:
            generate_url(self.url)
            mock.assert_called_with(image_url=self.url)

    def test_should_pass_url_kwarg_to_crypto(self):
        self.assertPassesArgsToCrypto(image_url=self.url)

    def test_should_pass_extra_kwargs_to_crypto(self):
        self.assertPassesArgsToCrypto(
            image_url=self.url, width=300, height=200)

    def test_should_return_the_result(self):
        encrypted_url = 'encrypted-url.jpg'
        encrypted_url_with_host = 'http://localhost:8888/encrypted-url.jpg'

        with patch('django_thumbor.crypto.generate') as mock:
            mock.return_value = encrypted_url
            url = generate_url(self.url)

        self.assertEqual(url, encrypted_url_with_host)


class TestURLFixing(TestCase):

    def assertURLEquals(self, original, expected):
        with patch('django_thumbor.crypto.generate') as mock:
            generate_url(original)
            mock.assert_called_with(image_url=expected)

    def test_should_prepend_the_domain_to_media_url_images(self):
        self.assertURLEquals('/media/uploads/image.jpg',
                             'localhost:8000/media/uploads/image.jpg')

    def test_should_remove_the_scheme_from_external_images(self):
        self.assertURLEquals('http://some.domain.com/path/image.jpg',
                             'some.domain.com/path/image.jpg')


class TestThumborArguments(TestCase):

    url = 'domain.com/path/image.jpg'

    def test_smart_mode_on(self):
        url = generate_url(self.url, smart=True).split('/')
        self.assertTrue('smart' in url)

    @override_settings(THUMBOR_ARGUMENTS={'smart': True})
    def test_get_argumentes_settings(self):
        url = generate_url(self.url).split('/')
        self.assertTrue('smart' in url)
