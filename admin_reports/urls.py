from django.urls import path
from . import views

app_name = 'admin_reports'

urlpatterns = [
    path('export/', views.export_data, name='export'),
]