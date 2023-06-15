from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from applications.base.views import (
    controlPanel
    , list_clients
    , dashboard
    , add_client
    , edit_client
    , delete_client
    , add_admin
    , delete_admin
)

app_name = 'base_app'

urlpatterns = [
    path('control-panel/', controlPanel, name='control-panel'),
    path('list-clients/', list_clients, name='list-clients'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-client/', add_client, name='add-client'),
    path('client/add/', add_client, name='add_client'),
    path('client/edit/<int:client_id>/', edit_client, name='edit_client'),
    path('client/delete/<int:client_id>/', delete_client, name='delete_client'),
    path('add/user/admin/<int:client_id>/', add_admin, name='add_admin'),
    path('delete/user/admin/<int:client_id>/<int:user_id>/',
         delete_admin, name='delete_admin'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
