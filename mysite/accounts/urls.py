from django.urls import path
from .views import CustomLoginView
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseBadRequest

app_name = 'accounts'

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']  

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() not in self.http_method_names:
            return HttpResponseBadRequest("잘못된 접근입니다.")
        return super().dispatch(request, *args, **kwargs)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile')
]