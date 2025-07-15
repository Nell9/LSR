@chcp 65001 >nul
@echo off
:: === Параметры ===
set "PROJECT_DIR=D:\LSR\LSR"
set "BACKUP_DIR=\\Pc-09\общий каталог\Несекретно\server_backups"
set "DB_NAME=db_5tab.sqlite3"
set "MEDIA_NAME=media"
set "DATE=%date%"
set "TIME=%time:~0,2%-%time:~3,2%"

:: Удаление лишних пробелов в TIME
if "%TIME:~0,1%"==" " set TIME=0%TIME:~1%

:: Создание папки бэкапа, если не существует
if not exist "%BACKUP_DIR%" (
    mkdir "%BACKUP_DIR%"
)

:: === Бэкап базы данных ===
echo Копируем базу данных: %DB_NAME%
copy "%PROJECT_DIR%\%DB_NAME%" "%BACKUP_DIR%\db_%DATE%_%TIME%.sqlite3"

:: === Бэкап медиа ===
echo Копируем медиа-папку: %MEDIA_NAME%
robocopy "%PROJECT_DIR%\%MEDIA_NAME%" "%BACKUP_DIR%\%MEDIA_NAME%_%DATE%_%TIME%" /E

echo Бэкап завершён: %DATE% %TIME%
pause


