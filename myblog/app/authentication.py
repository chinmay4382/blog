from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
UserModel = get_user_model()


class EmailAuthBackend(ModelBackend):
    print("hello")

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
            print("reached here")
        try:
            user = UserModel.objects.get(email=username)
            print(user)
        except UserModel.DoesNotExist:

            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
