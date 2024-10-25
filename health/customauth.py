from django.contrib.auth.backends import ModelBackend
from .models import Auto_generate
from django.contrib.auth.hashers import check_password 
from django.contrib.auth.models import User
## custome authencation model
        
class CustomAuth(ModelBackend):

    def authenticate(**credentials):
        return super(CustomAuth, self).authenticate(**credentials)

    def authenticate(self, user_id=None, password=None):    
        # Check the password and return a User.
        if  user_id!= None and password != None:
            # Get the user
                user1 = User.objects.get(username=user_id) ## to select the user we need primary key of the User table
                if user1.is_superuser == True:
                    if check_password(password,user1.password):
                        return user1
                    else:
                        return None
                else:
                    user2 = Auto_generate.objects.get(auto_user_id=user_id) ## to select the user we need primary key of the Auto_generate table
                    if  check_password(password,user2.password): ## check the password of the user
                        return user1
                    else:
                        return None
        return None

    def get_user(self, user_id):
        try:
            Auto_generate.objects.get(auto_user_id=user_id)
        except Auto_generate.DoesNotExist:
           return None