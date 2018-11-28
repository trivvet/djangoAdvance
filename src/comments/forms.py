from django import forms

from crispy_forms.helper import FormHelper

from .models import Comment

class CommentForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    # parent_id = forms.IntegerField(
    #     widget=forms.HiddenInput,
    #     required=False
    #     )
    # user = forms.CharField(widget=forms.HiddenInput)
    content = forms.CharField(
        label=False, 
        widget=forms.Textarea(attrs={'cols': 20, 'rows': 2})
        )

    # class Meta:
    #     model = Comment
    #     fields = ['content', 'user', 'content_type', 'object_id']