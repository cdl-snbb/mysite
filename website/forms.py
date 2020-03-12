from django import forms
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):

    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'))