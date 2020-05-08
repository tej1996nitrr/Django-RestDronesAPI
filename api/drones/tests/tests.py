from django.test import TestCase
from django.utils.http import urlencode
from django.urls import reverse
from rest_framework import status
from ..models import DroneCategory
from ..views import DroneCategoryList,DroneCategoryDetail,DroneDetail,DroneList,ApiRoot
from rest_framework.test import APITestCase
import pytest
pytestmark = pytest.mark.django_db
from django.test import RequestFactory 

class TestHomeView(APITestCase):
    def test_anonymous(self):
        req = RequestFactory().get('/')
        resp = ApiRoot.as_view()(req)
        assert resp.status_code==200,'Should be callable by anyone'

class TestDroneCategory(APITestCase):
    def post_drone_category(self,name):
        url = reverse(DroneCategoryList.name)
        data  = {'name':name}
        response = self.client.post(url,data,format='json')
        return response

    def test_post_and_get_drone_category(self):
        new_drone_category_name = "Hexacopter"
        response = self.post_drone_category(new_drone_category_name)
        assert response.status_code == status.HTTP_201_CREATED
        assert DroneCategory.objects.count()==1
        assert DroneCategory.objects.get().name == new_drone_category_name


