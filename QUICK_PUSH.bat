@echo off
REM ADEM LLM Voice Assistant - Quick GitHub Push Script
REM Автоматический пуш для Windows (3-5 мин)

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo  ADEM LLM Voice Assistant - Quick GitHub Push
echo ==========================================
echo.

REM Проверка git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git не установлен!
    echo Установите: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo [OK] Git найден
echo.

REM Получение URL репозитория
if "%~1"=="" (
    echo.
    echo Использование:
    echo   QUICK_PUSH.bat ^<repo-url^>
    echo.
    echo Пример:
    echo   QUICK_PUSH.bat https://github.com/username/adem-llm-voice-assistant.git
    echo.
    echo Или создайте репозиторий на GitHub:
    echo   1. Перейдите на https://github.com/new
    echo   2. Название: adem-llm-voice-assistant
    echo   3. Описание: LLM Voice Assistant with Python API integration
    echo   4. Оставьте пустым (без README)
    echo   5. Скопируйте URL и запустите:
    echo      QUICK_PUSH.bat ^<URL^>
    pause
    exit /b 1
)

set REPO_URL=%~1

echo [OK] URL репозитория: %REPO_URL%
echo.

REM Инициализация git
if not exist ".git" (
    echo [...] Инициализация git...
    git init
    echo [OK] Git инициализирован
) else (
    echo [OK] Git уже инициализирован
)
echo.

REM Добавление всех файлов
echo [...] Добавление файлов...
git add .
echo [OK] Файлы добавлены
echo.

REM Коммит
echo [...] Создание коммита...
git commit -m "Initial commit: ADEM LLM Voice Assistant" -m "- Voice recognition with Whisper/Google Speech API" -m "- LLM integration (OpenAI/Gemini/Claude)" -m "- TTS with ElevenLabs/Google TTS" -m "- Complete configuration system" -m "- Ready for deployment"
echo [OK] Коммит создан
echo.

REM Установка удалённого репозитория
echo [...] Установка origin...
git remote | findstr "origin" >nul
if %errorlevel% equ 0 (
    git remote set-url origin %REPO_URL%
) else (
    git remote add origin %REPO_URL%
)
echo [OK] Origin установлен
echo.

REM Переименование ветки в main (если нужно)
for /f "tokens=*" %%a in ('git rev-parse --abbrev-ref HEAD') do set CURRENT_BRANCH=%%a
if not "!CURRENT_BRANCH!"=="main" (
    echo [..] Переименование ветки в main...
    git branch -M main
    echo [OK] Ветка переименована
    echo.
)

REM Push в репозиторий
echo [...] Отправка в GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo  ГОТОВО!
    echo ==========================================
    echo.
    echo Репозиторий успешно загружен на GitHub!
    echo Откройте: %REPO_URL:.git=%
    echo.
    echo Следующие шаги:
    echo   1. Скопируйте .env.example в .env
    echo   2. Добавьте ваши API ключи в .env
    echo   3. Установите зависимости: pip install -r requirements.txt
    echo   4. Запустите: python main_startup.py
    echo.
    echo Подробнее: START_HERE.md
) else (
    echo.
    echo [ERROR] Ошибка при отправке в GitHub!
    echo Проверьте:
    echo   - Правильность URL
    echo   - Доступ к репозиторию
    echo   - Интернет соединение
)

echo.
pause
