
import random
from django.core.mail import EmailMessage


def get_random_code():
    numberList = [1,2,3,4,5,6,7,8,9,0]
    num = []
    for x in range(5):
        single_num =  random.choice(numberList)
        num.append(single_num)
    number = "".join(str(item) for item in num)
    return number

get_random_code()



class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'] , to=[data['to_email' ]] )
        email.send()
        
    @staticmethod
    def send_sms(data):
        pass