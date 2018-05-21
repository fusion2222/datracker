from django import forms
from django.contrib.auth import authenticate, login


class LoginForm(forms.Form):
    """
    Custom login form.
    """
    username = forms.CharField(
        label='Username', max_length=100, required=True)
    password = forms.CharField(
        label='Password',
        max_length=100,
        required=True,
        widget=forms.PasswordInput
    )

    def clean(self, *args, **kwargs):
        output = super().clean(*args, **kwargs)

        auth_kwargs = {
            'username': self.cleaned_data.get('username'),
            'password': self.cleaned_data.get('password'),
        }

        user = authenticate(self.request, **auth_kwargs)

        if user is not None:
            login(self.request, user=user)

        else:
            raise forms.ValidationError(
                'Invalid login credidentals. Try again please.',
                code='invalid'
            )

        return output

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
