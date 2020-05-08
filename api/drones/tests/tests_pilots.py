from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.http import urlencode
from django.urls import reverse
from rest_framework import status
from ..models import DroneCategory, Pilot
from ..views import DroneCategoryList, DroneCategoryDetail, DroneDetail, DroneList, ApiRoot,PilotList,PilotDetail
from rest_framework.test import APITestCase
import pytest
from django.test import RequestFactory
pytestmark = pytest.mark.django_db

class PilotTestCase(APITestCase):
    def post_pilot(self, name,gender, races_count):
        url = reverse(PilotList.name)
        print(url)
        data  ={"name":name,"gender":gender,"races_count":races_count}
        response  = self.client.post(url,data,format="json")
        print(response)
        return response
    
    def create_user_and_set_token_creds(self):
        user = User.objects.create_user('user01',"user01@gmail.com","userpwd45")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token.key))
    
    def test_post_and_get_pilot(self):
        """Test if  new  pilot is created and retrieved """
        self.create_user_and_set_token_creds()
        new_pilot_name = 'Sherlock'
        new_pilot_gender = Pilot.MALE
        new_pilot_races_count = 5
        response = self.post_pilot(new_pilot_name, new_pilot_gender, new_pilot_races_count)
        assert response.status_code == status.HTTP_201_CREATED
        assert Pilot.objects.count() == 1
        saved_pilot = Pilot.objects.get()
        assert saved_pilot.name == new_pilot_name
        assert saved_pilot.gender == new_pilot_gender
        assert saved_pilot.races_count == new_pilot_races_count
        url = reverse( PilotDetail.name, None, {saved_pilot.pk})
        authorized_get_response = self.client.get(url, format='json')
        assert authorized_get_response.status_code ==status.HTTP_200_OK
        assert authorized_get_response.data['name'] == new_pilot_name
        self.client.credentials() #without arguments to clear
        unauthorized_get_response = self.client.get(url, format='json') 
        assert unauthorized_get_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_to_post_pilot_without_token(self):
        """
        Test we cannot create a pilot without a token
        """
        new_pilot_name = 'Unauthorized Pilot'
        new_pilot_gender = Pilot.MALE
        new_pilot_races_count = 5
        response = self.post_pilot(new_pilot_name,new_pilot_gender,races_count=new_pilot_races_count)
        print(response)
        print(Pilot.objects.count())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Pilot.objects.count() == 0
            