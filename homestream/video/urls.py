from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

app_name = 'video'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.video_upload, name='upload'),
    path('watch/<str:video_id>/', views.watch, name='watch'),
]
