from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import AttachedFile
import mimetypes

def download_file(request, file_id):
    attached_file = get_object_or_404(AttachedFile, pk=file_id)

    if not attached_file.file:
        raise Http404("Файл не найден")

    file_path = attached_file.file.path
    filename = attached_file.file.name.split('/')[-1]

    # Определяем MIME-тип (например, для docx)
    mime_type, _ = mimetypes.guess_type(filename)
    if not mime_type:
        mime_type = 'application/octet-stream'

    response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
    # Задаем inline, чтобы браузер попытался открыть файл в окне, а не скачать
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    # Разрешаем кеширование (по желанию)
    response['Cache-Control'] = 'private, max-age=3600'

    return response
