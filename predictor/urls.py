from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_predictor, name='predictor'),
    path('upload', views.csv_file_list_create_view, name='predictor_upload'),
    path('csv-files/<int:pk>/', views.csv_file_detail_view, name='csv-file-detail'),
    path('csv-files/<int:pk>/preview/', views.csv_file_preview_view, name='csv-file-preview'),
]
