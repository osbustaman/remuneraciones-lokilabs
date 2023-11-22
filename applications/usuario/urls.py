from django.urls import path
from applications.usuario.api.api import AfpDetailApiView, ApiGetDataUserPage, ApiGetPersonalData, ApiLoadPageColaborator, ListColaborate, PersonalDataCreateView, PersonalDataEditView

from applications.usuario.views import (
    add_forecast_data,
    collaborator_file
    , add_collaborator_file
    , edit_collaborator_file
    , add_contact
    , contact_delete
    , add_personal_information
    , add_form_payment
    , add_family_responsibilities,
    edit_collaborator_file_old
    , edit_family_responsibilities
    , family_responsibilities_delete,
    init_page
)


app_name = 'usuario_app'

urlpatterns = [

    path('mi-perfil', init_page, name='init_page'),

    path('collaborator/file/', collaborator_file, name='collaborator_file'),
    path('collaborator/file/add/', add_collaborator_file, name='add_collaborator_file'),
    path('editar-colaborador/<str:id>/<str:col_id>', edit_collaborator_file, name='edit_collaborator_file'),

    path('editar-colaborador/old/<str:id>/<str:col_id>', edit_collaborator_file_old, name='edit_collaborator_file_old'),

    path('collaborator/add/contact/<int:user_id>/<int:col_id>/', add_contact, name='add_contact'),
    path('collaborator/delete/contact/<int:con_id>/<int:user_id>/<int:col_id>/', contact_delete, name='contact_delete'),

    path('collaborator/add/personal/information/<int:user_id>/<int:col_id>/', add_personal_information, name='add_personal_information'),
    path('collaborator/add/form/payment/<int:user_id>/<int:col_id>/', add_form_payment, name='add_form_payment'),
    path('collaborator/add/forecast/data/<int:user_id>/<int:col_id>/', add_forecast_data, name='add_forecast_data'),

    path('collaborator/add/family/responsibilities/<int:user_id>/<int:col_id>/', add_family_responsibilities, name='add_family_responsibilities'),
    path('collaborator/edit/family/responsibilities/<int:fr_id>/<int:user_id>/<int:col_id>/', edit_family_responsibilities, name='edit_family_responsibilities'),
    path('collaborator/delete/family/responsibilities/<int:fr_id>/<int:user_id>/<int:col_id>/', family_responsibilities_delete, name='family_responsibilities_delete'),

    #API
    path('collaborator/api/search/data/afp/<pk>/', AfpDetailApiView.as_view(), name='AfpDetailApiView'),
    path('mi-perfil/<pk>/', ApiGetDataUserPage.as_view(), name='mi_perfil'),
    path('lista-colaboradores/<pk>', ListColaborate.as_view(), name='ListColaborate'),
    path('datos-personales/<pk>', ApiGetPersonalData.as_view(), name='ApiGetPersonalData'),
    path('api-editar-colaborador', ApiLoadPageColaborator.as_view(), name='ApiLoadPageColaborator'),
    path('api-editar-colaborador', ApiLoadPageColaborator.as_view(), name='ApiLoadPageColaborator'),

    path('api/edit-personal-data/<int:user>', PersonalDataEditView.as_view(), name='PersonalDataEditView'),
    path('api/create-persona-data/', PersonalDataCreateView.as_view(), name='PersonalDataCreateView'),




]