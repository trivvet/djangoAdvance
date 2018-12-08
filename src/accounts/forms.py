from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
    )

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, ButtonHolder

User = get_user_model()

class UserLoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.template_pack = 'bootstrap3'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper

        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Sign in'),
        )

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(
                username=username, 
                password=password)
            if not user:
                raise forms.ValidationError(
                    "User with such username or password does not exist")

            if not user.is_active:
                raise forms.ValidationError(
                    "This user is not longer active")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



