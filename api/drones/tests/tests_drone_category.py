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


class TestDroneCategory(APITestCase):
    def post_drone_category(self, name):
        url = reverse(DroneCategoryList.name)
        data = {'name': name}
        response = self.client.post(url,data,format='json')
        return response

    def test_post_and_get_drone_category(self):
        new_drone_category_name = "Hexacopter"
        response = self.post_drone_category(new_drone_category_name)
        assert response.status_code == status.HTTP_201_CREATED
        assert DroneCategory.objects.count()==1
        assert DroneCategory.objects.get().name == new_drone_category_name

    def test_post_existing_drone_category_name(self):
        """
        Ensure we cannot create a DroneCategory with an existing name
        """
        url = reverse(DroneCategoryList.name)
        new_drone_category_name = 'Duplicated Copter'
        data = {'name': new_drone_category_name}
        response1 = self.post_drone_category(new_drone_category_name)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = self.post_drone_category(new_drone_category_name)
        print(response2)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_update_drone_category(self):
        """Test if a single field can be updated in category"""
        drone_category_name = "Initial Name"
        response = self.post_drone_category(drone_category_name)
        url = reverse(DroneCategoryDetail.name, None, {response.data['pk']})
        data = {'name': 'Updated Name'}
        patch_response = self.client.patch(url, data, format="json")
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['name'] == 'Updated Name'

    def test_get_drone_category(self):
        """test to get single drone category by id"""
        drone_category_name="Some Name"
        response = self.post_drone_category(drone_category_name)
        url = reverse(DroneCategoryDetail.name,None,{response.data['pk']})
        get_response = self.client.get(url, format='json')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['name'] == drone_category_name

    def test_filter_drone_category(self):
        drone_category_name1 = "Hexocopter"
        self.post_drone_category(drone_category_name1)
        drone_category_name2 = "Octocopter"
        self.post_drone_category(drone_category_name2)
        filter_name = {'name':drone_category_name1}
        url = '{0}?{1}'.format(reverse(DroneCategoryList.name),urlencode(filter_name))
        print(url)
        response = self.client.get(url, format='json')
        print(response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == drone_category_name1
