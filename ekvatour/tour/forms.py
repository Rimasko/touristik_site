from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import News, Feedback


class NewsCreateForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget)

    class Meta:
        model = News
        fields = ('title', 'text', 'published')


class FeedbackCreateForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('email', 'phone', 'text')
