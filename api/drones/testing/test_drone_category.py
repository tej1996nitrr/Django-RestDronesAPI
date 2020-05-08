from django.test import TestCase
from django.utils.http import urlencode
from django.urls import reverse
from rest_framework import status
from ..models import DroneCategory
from ..views import DroneCategoryList, DroneCategoryDetail, DroneDetail, DroneList, ApiRoot
from rest_framework.test import APITestCase
import pytest
from django.test import RequestFactory
pytestmark = pytest.mark.django_db


class TestHomeView(APITestCase):
    def test_anonymous(self):
        req = RequestFactory().get('/')
        resp = ApiRoot.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by anyone'