from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from accounts.models import User


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class UserSignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")
