from django.contrib.auth import get_user_model
from django.http import request
from django.http.request import HttpRequest
from django.test import TestCase
from rest_framework import status
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# Create your tests here.
class SnippetViewSetTest(APITestCase):
    fixtures = [
        'users.json',
        'snippets.json',
    ]

    def setUp(self) -> None:
        self.User = get_user_model()
        # Fix the passwords of fixtures
        for user in self.User.objects.all():
            user.set_password(user.password)
            user.save()
        self.user = self.User.objects.get(pk=1)

    def test_snippet_list(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('snippet-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        db_snippets = Snippet.objects.count()
        data = response.json()
        self.assertEqual(data['count'], db_snippets)

    def test_snippet_detail(self):
        self.client.force_login(self.user)
        snippet_1 = Snippet.objects.get(pk=1)

        response = self.client.get(reverse('snippet-detail', kwargs={'pk': snippet_1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data['title'], snippet_1.title)
        self.assertEqual(data['code'], snippet_1.code)

    def test_snippet_create(self):
        self.client.force_login(self.user)

        snippet_data = {
            'title': 'Test title',
            'code': 'a = 1'
        }
        response = self.client.post(reverse('snippet-list'), data=snippet_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertEqual(data['title'], snippet_data['title'])
        self.assertEqual(data['owner'], self.user.username)

    def test_snippet_update(self):
        user_2 = self.User.objects.get(pk=2)
        self.client.force_login(user_2)
        snippet_user_2 = Snippet.objects.get(owner=user_2)

        update_payload = {'title': 'New title'}

        response = self.client.patch(reverse('snippet-detail', kwargs={'pk': snippet_user_2.id}), data=update_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data['title'], update_payload['title'])

        self.client.force_login(self.user)
        response = self.client.patch(reverse('snippet-detail', kwargs={'pk': snippet_user_2.id}), data=update_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
