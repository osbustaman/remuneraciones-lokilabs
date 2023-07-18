from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from applications.configurations.views import (
    concepts,
    concepts_add,
    concepts_edit,
    concepts_delete,
    countries,
    health_edit
    , regions
    , communes
    , health
    , health_add
    , health_edit
    , health_delete
    , afp
    , afp_add
    , afp_edit
    , afp_delete
    , compensation_box
    , compensation_box_add
    , compensation_box_edit
    , compensation_box_delete
    , banks
    , banks_add
    , banks_edit
    , delete_bank
    , apv
    , apv_add
    , apv_edit
    , apv_delete
    , mutual_security
    , mutual_security_add
    , mutual_security_edit
    , mutual_security_delete
)


app_name = 'conf_app'

urlpatterns = [

    path('company/countries/', countries, name='countries_app'),
    path('company/regions/', regions, name='regions_app'),
    path('company/communes/', communes, name='communes_app'),

    path('company/afp/', afp, name='afp_app'),
    path('company/afp/add/', afp_add, name='afp_add'),
    path('company/afp/edit/<int:afp_id>/', afp_edit, name='afp_edit'),
    path('company/afp/delete/<int:afp_id>/', afp_delete, name='afp_delete'),

    path('company/health/', health, name='health_app'),
    path('company/health/add/', health_add, name='health_add'),
    path('company/health/edit/<int:sa_id>/', health_edit, name='health_edit'),
    path('company/health/delete/<int:sa_id>/', health_delete, name='health_delete'),


    path('company/compensation/box/', compensation_box, name='compensation_box_app'),
    path('company/compensation/box/add/', compensation_box_add, name='compensation_box_add'),
    path('company/compensation/box/edit/<int:cc_id>/', compensation_box_edit, name='compensation_box_edit'),
    path('company/compensation/box/delete/<int:cc_id>/', compensation_box_delete, name='compensation_box_delete'),

    path('company/banks/', banks, name='banks_app'),
    path('company/banks/add/', banks_add, name='banks_add'),
    path('company/banks/edit/<int:ban_id>/', banks_edit, name='banks_edit'),
    path('company/banks/delete/<int:ban_id>/', delete_bank, name='delete_bank'),

    path('company/apv/', apv, name='apv_app'),
    path('company/apv/add/', apv_add, name='apv_add'),
    path('company/apv/edit/<int:apv_id>/', apv_edit, name='apv_edit'),
    path('company/apv/delete/<int:apv_id>/', apv_delete, name='apv_delete'),

    path('company/mutual/security/', mutual_security, name='mutual_security_app'),
    path('company/mutual/security/add/', mutual_security_add, name='mutual_security_add'),
    path('company/mutual/security/edit/<int:ms_id>/', mutual_security_edit, name='mutual_security_edit'),
    path('company/mutual/security/delete/<int:ms_id>/', mutual_security_delete, name='mutual_security_delete'),

    path('company/concepts/', concepts, name='concepts_app'),
    path('company/concepts/add/', concepts_add, name='concepts_add'),
    path('company/concepts/edit/<int:conc_id>/', concepts_edit, name='concepts_edit'),
    path('company/concepts/delete/<int:conc_id>/', concepts_delete, name='concepts_delete'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)