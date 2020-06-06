from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import News


class NewsCreateForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget)

    class Meta:
        model = News
        fields = ('title', 'text', 'published')
