from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from .models import TourUser


class TourUserCreationForm(UserCreationForm):
    class Meta:
        model = TourUser
        fields = ('email', 'password', 'first_name', 'last_name', 'patronymic_name', 'gender', 'phone', 'birth_date')


class TourUserChangeForm(UserChangeForm):
    class Meta:
        model = TourUser
        fields = ('email', 'password', 'first_name', 'last_name', 'patronymic_name', 'gender', 'phone', 'birth_date')
        exclude = ["password"]


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = TourUser
        fields = ('first_name', 'last_name', 'patronymic_name', 'phone')


class RegistrationForm(SignupForm):
    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    )

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    patronymic_name = forms.CharField(max_length=30, required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    phone = forms.CharField(max_length=12, required=True)
    birth_date = forms.DateField()

    def save(self, request):
        user = super(RegistrationForm, self).save(request)
        data = self.cleaned_data
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.gender = data['gender']
        user.patronymic_name = data['patronymic_name']
        user.phone = data['phone']
        user.birth_date = data['birth_date']
        user.save()
        return user
