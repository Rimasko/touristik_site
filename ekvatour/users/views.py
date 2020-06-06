from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from .forms import ProfileChangeForm


class ProfileView(LoginRequiredMixin, views.View):
    template_name = "LK.html"
    form_class = ProfileChangeForm

    def get(self, request, *args, **kwargs):
        user = request.user
        user_tours = user.reserved_tours.all()  
        user_reviews = user.review_set.all()
        data = {
            "user_tours": user_tours,
            "user_reviews": user_reviews
        }
        return render(request, self.template_name, context=data)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            user.last_name = form.cleaned_data['last_name']
            user.first_name = form.cleaned_data['first_name']
            user.patronymic_name = form.cleaned_data['patronymic_name']
            user.phone = form.cleaned_data['phone']

            return render(request, self.template_name)
        else:
            return render(request, self.template_name, {'form': form})
