from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('upload/', views.file_upload_view , name='python'),
    path('stats/', views.stats , name='statistiques'),
    path('fichiers/', views.fichierLirepython , name='fichier')
]

