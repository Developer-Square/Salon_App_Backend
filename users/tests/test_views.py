from .test_setup import TestSetup
from ..models import NewUser
'''
import pdb
pdb.set_trace()

'''
import pdb


class TestViews(TestSetup):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)       
        self.assertEqual(res.status_code, 400)
        
    def test_user_can_register_successfully(self):
        res = self.client.post(self.register_url, self.user_data, format="json")  
       
        self.assertEqual(res.data['email'], self.user_data['email']) 
        self.assertEqual(res.data['username'], self.user_data['username'])       
        self.assertEqual(res.data['phone_number'], self.user_data['phone_number'])    
        self.assertEqual(res.data['first_name'], self.user_data['first_name'])    
          
        self.assertEqual(res.status_code, 201)
        
    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 400)
        
        
 