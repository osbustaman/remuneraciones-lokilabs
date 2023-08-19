from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from applications.empresa.api.api import BulkLoadExcelPositionCreateAPIView, DownloadBranchUploadTemplateCreateAPIView

from applications.empresa.views import (
    list_company
    , add_company
    , edit_company
    , add_branch_office
    , edit_branch_office
    , delete_branch_office
    , add_position
    , edit_position
    , delete_position
    , add_gcc
    , edit_gcc
    , delete_gcc
    , add_cc
    , edit_cc
    , delete_cc
    , add_associated_entities
    , cambiarEmpresa
)
app_name = 'emp_app'

urlpatterns = [

    path('cambiar-empresa/<int:emp_id>', cambiarEmpresa, name='cambiar_empresa'),

    path('company/list/', list_company, name='list_company'),
    path('company/add/', add_company, name='add_company'),
    path('company/edit/<int:emp_id>', edit_company, name='edit_company'),

    path('company/add/branch/office/<int:emp_id>', add_branch_office, name='add_branch_office'),
    path('company/edit/branch/office/<int:emp_id>/<int:suc_id>', edit_branch_office, name='edit_branch_office'),
    path('company/delete/branch/office/<int:emp_id>/<int:suc_id>', delete_branch_office, name='delete_branch_office'),

    path('company/add/position/<int:emp_id>', add_position, name='add_position'),
    path('company/edit/position/<int:emp_id>/<int:car_id>', edit_position, name='edit_position'),
    path('company/delete/position/<int:emp_id>/<int:car_id>', delete_position, name='delete_position'),

    path('company/add/gcc/<int:emp_id>', add_gcc, name='add_gcc'),
    path('company/edit/gcc/<int:emp_id>/<int:gcencost_id>', edit_gcc, name='edit_gcc'),
    path('company/delete/gcc/<int:emp_id>/<int:gcencost_id>', delete_gcc, name='delete_gcc'),

    path('company/add/cc/<int:emp_id>/<int:gcencost_id>', add_cc, name='add_cc'),
    path('company/edit/cc/<int:emp_id>/<int:gcencost_id>/<int:cencost_id>', edit_cc, name='edit_cc'),
    path('company/delete/cc/<int:emp_id>/<int:gcencost_id>/<int:cencost_id>', delete_cc, name='delete_cc'),

    path('company/add/associated/entities/<int:emp_id>', add_associated_entities, name='add_associated_entities'),


    path('company/api/load/excel/<pk>/', BulkLoadExcelPositionCreateAPIView.as_view(), name='BulkLoadExcelPositionCreateAPIView'),
    path('company/api/template/excel/company/', DownloadBranchUploadTemplateCreateAPIView.as_view(), name='DownloadBranchUploadTemplateCreateAPIView'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)