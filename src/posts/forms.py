from django import forms

from crispy_forms.helper import FormHelper
from pagedown.widgets import PagedownWidget

from .models import Post


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]