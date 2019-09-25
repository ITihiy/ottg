from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('send_login_email', views.send_login_email, name='send_email'),
    path('login', views.login, name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='lists/home.html'), name='logout'),
]