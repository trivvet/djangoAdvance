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

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.template_pack = 'bootstrap3'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper

        self.helper.layout = Layout(
            'username',
            'email',
            'email2',
            'password',
            Submit('submit', 'Register'),
        )
    
    email = forms.EmailField(label='Email')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        users_same_email = User.objects.filter(email=email)
        if users_same_email.count():
            raise forms.ValidationError(
                "A user with the same email already exists")

        return email

    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        
        if email != email2:
            raise forms.ValidationError(
                "Both emails must be the same")
        
        return email2



