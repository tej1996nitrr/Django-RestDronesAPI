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
    def post_pilot(self, name,gender, race_count):
        url = reverse(PilotList.name)
        print(url)
        data  ={"name":name,"gender":gender,"race_count":race_count}
        response  = self.client.post(url,data,format="json")
        print(response)
        return response
    
    def create_user_and_set_token_creds(self):
        user = User.objects.create_user('user01',"user01@gmail.com","userpwd45")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token.key))
    