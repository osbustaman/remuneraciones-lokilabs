from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from applications.attendance.api.api import MarkInAndOutAPIView, MarkInAndOutUserAPIView

app_name = 'attendance_app'

urlpatterns = [

    path('in-and-out/', MarkInAndOutAPIView.as_view(), name='MarkInAndOutAPIView'),
    path('in-and-out-user/<pk>', MarkInAndOutUserAPIView.as_view(), name='MarkInAndOutUserAPIView'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


