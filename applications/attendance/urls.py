from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from applications.attendance.api.api import ListUsersWorkDay, MarkInAndOutAPIView, MarkInAndOutUserAPIView
from applications.attendance.views import collaborators_working_day, mark_in_out, work_day_report


app_name = 'attendance_app'

urlpatterns = [

    path('jornada-colaboradores', collaborators_working_day, name='collaborators_working_day'),
    path('marcar-jornada-laboral', mark_in_out, name='mark_in_out'),
    path('reportes-asistencia/<str:user_id>', work_day_report, name='work_day_report'),
    

    path('in-and-out/', MarkInAndOutAPIView.as_view(), name='MarkInAndOutAPIView'),
    path('in-and-out-user/<pk>', MarkInAndOutUserAPIView.as_view(), name='MarkInAndOutUserAPIView'),
    path('list-user-work-dayclear/<pk>', ListUsersWorkDay.as_view(), name='ListUsersWorkDay'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


