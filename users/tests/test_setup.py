from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetup(APITestCase):
    def setUp(self):
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        
        self.user_data = {
            'email': "email@gmail.com",
            'username': "email",
            'first_name': "firstname",
            'phone_number': "0736382625",
            'password': "malintode"
            
        }
        
        return super().setUp()
    
    def tearDown(self):
        # tearDown is forcleaning up stuff from your setUp method, not related to the database. 
        return super().tearDown()
    
    