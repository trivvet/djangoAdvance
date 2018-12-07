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

        user = authenticate(request, 
                username=username, 
                password=password)

        return self



