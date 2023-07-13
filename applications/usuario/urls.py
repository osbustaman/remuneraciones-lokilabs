from django.urls import path

from applications.usuario.views import (
    collaborator_file
    , add_collaborator_file
    , edit_collaborator_file
    , add_contact
    , contact_delete
)


app_name = 'usuario_app'

urlpatterns = [

    path('collaborator/file/', collaborator_file, name='collaborator_file'),
    path('collaborator/file/add/', add_collaborator_file, name='add_collaborator_file'),
    path('collaborator/file/edit/<int:id>/<int:col_id>/', edit_collaborator_file, name='edit_collaborator_file'),

    path('collaborator/add/contact/<int:user_id>/<int:col_id>/', add_contact, name='add_contact'),
    path('collaborator/delete/contact/<int:con_id>/<int:user_id>/<int:col_id>/', contact_delete, name='contact_delete'),
]