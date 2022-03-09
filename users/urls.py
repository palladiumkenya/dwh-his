
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('connect/authorize/callback/', views.signup_callback, name='signup_callback'),
    path('signin-oidc/', views.signin_oidc, name='signin_oidc'),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('', views.HelloView.as_view(), name='hello'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

