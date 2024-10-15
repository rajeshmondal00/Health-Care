from django.contrib.auth.backends import ModelBackend
from .models import Auto_generate
from django.contrib.auth.hashers import check_password 
## custome authencation model
        
class CustomAuth(ModelBackend):

    def authenticate(**credentials):
        return super(CustomAuth, self).authenticate(**credentials)

    def check_user(user_id, auto_user_id,password, auto_password): ## check the user id and password
        hash_password= check_password(password,auto_password)
        print(hash_password)
        if user_id == auto_user_id and check_password(password,auto_password):
            return True
        else:
            return False
    
    # def check_password(password, auto_password): ## check the user password
    #     hash_password= make_password(password)
    #     print(hash_password,password)
    #     if auto_password == hash_password:
    #         return True
    #     else:
    #         return False
    
    def authenticate(self, email=None , user_id=None, password=None):    
        # Check the password and return a User.
        if  email!= None and user_id!= None and password != None:
            # Get the user
                user = Auto_generate.objects.get(email=email.lower()) ## to select the user we need primary key
                print(user)
                print(user.auto_password,password)
                if  CustomAuth.check_user(user_id,user.auto_user_id,password,user.auto_password): ## check the password and user id of the user
                    print(user.auto_password,password)
                    return user
                else:
                    return None
        return None

    def get_user(self, user_id):
        try:
            Auto_generate.objects.get(auto_user_id=user_id)
        except Auto_generate.DoesNotExist:
           return None