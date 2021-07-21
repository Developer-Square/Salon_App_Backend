from google.auth.transport import requests
from google.oauth2 import id_token

CLIENT_ID = '555068933656-haou46l4vec87gf7akedbudgm653c1a6.apps.googleusercontent.com'


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:  #issue it matches if string is in  'accouunts.google.com' or 'https://accouunts.google.com'
                return idinfo

        except:
            return "The token is either invalid or has expired"