from django.urls import path
from . import views

app_name = 'account_base'

urlpatterns = [
    path('', views.login_client, name='login_client'),
    path('logout/client/', views.logout_client, name='logout_client'),
    path('bases/', views.login_view, name='login_base'),
    path('accounts/login/', views.login_view, name='accounts-login'),
    path('logout/', views.logout_view, name='logout'),
]