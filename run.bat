@echo off

:: Пути и настройки

set "PROJECT_DIR=D:\LSR\LSR\"
set "VENV_DIR=D:\LSR\"

cd /d "%VENV_DIR%"
call venv\Scripts\activate.bat

cd /d "%PROJECT_DIR%"
python manage.py runserver 0.0.0.0:8000

echo Сервер запущен
pause