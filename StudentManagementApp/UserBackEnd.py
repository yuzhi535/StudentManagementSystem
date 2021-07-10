from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class UserBackEnd(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(user_id=username)
        except:
            return None
        else:
            if user.check_password(password):
                return user
            return None
