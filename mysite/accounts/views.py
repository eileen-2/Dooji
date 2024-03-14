from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect('blog:post_list')
        else:
            return self.form_invalid(form)
    
class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

signup = SignupView.as_view()

class LoginView(LoginView):
    template_name = 'accounts/login.html'

login = LoginView.as_view()

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() not in self.http_method_names:
            return HttpResponseBadRequest("잘못된 접근입니다.")
        return super().dispatch(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'