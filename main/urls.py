from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('nazariy/', views.nazariy_qisim, name='nazariy'),
    path('amaily/', views.amaliy_qisim, name='amaliy'),
    path('video/', views.media_qisim, name='video'),
    path('test/', views.test_qisim, name='test'),
    path('masala/', views.masala_qisim, name='masala'),
    path('masala/<int:pk>/', views.masala_detail, name='masala_detail'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('test/<int:pk>/', views.test_detail, name='test_detail'),
    path('media/videolar/<path:path>', views.range_video_view, name='range_video'),
    path('test_task/<int:pk>/', views.test_tasks, name='test_tasks'),


]
