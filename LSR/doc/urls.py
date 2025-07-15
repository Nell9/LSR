from django.urls import path
from doc.views import download_file

app_name = 'doc'

urlpatterns = [
    path('download-file/<int:file_id>/', download_file, name='download_file'),
]
