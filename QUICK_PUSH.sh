#!/bin/bash
# ADEM LLM Voice Assistant - Quick GitHub Push Script
# Автоматический пуш для Linux/Mac (3-5 мин)

set -e

echo "🚀 ADEM LLM Voice Assistant - Quick GitHub Push"
echo "================================================"
echo ""

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Проверка git
if ! command -v git &> /dev/null; then
    echo "${RED}❌ Git не установлен!${NC}"
    echo "Установите: https://git-scm.com/downloads"
    exit 1
fi

echo "${GREEN}✓${NC} Git найден"

# Получение URL репозитория
if [ -z "$1" ]; then
    echo ""
    echo "${YELLOW}Использование:${NC}"
    echo "  bash QUICK_PUSH.sh <repo-url>"
    echo ""
    echo "${YELLOW}Пример:${NC}"
    echo "  bash QUICK_PUSH.sh https://github.com/username/adem-llm-voice-assistant.git"
    echo ""
    echo "${YELLOW}Или создайте репозиторий на GitHub:${NC}"
    echo "  1. Перейдите на https://github.com/new"
    echo "  2. Название: adem-llm-voice-assistant"
    echo "  3. Описание: LLM Voice Assistant with Python API integration"
    echo "  4. Оставьте пустым (без README)"
    echo "  5. Скопируйте URL и запустите:"
    echo "     bash QUICK_PUSH.sh <URL>"
    exit 1
fi

REPO_URL=$1

echo "${GREEN}✓${NC} URL репозитория: $REPO_URL"
echo ""

# Инициализация git
if [ ! -d ".git" ]; then
    echo "${YELLOW}⚙${NC}  Инициализация git..."
    git init
    echo "${GREEN}✓${NC} Git инициализирован"
else
    echo "${GREEN}✓${NC} Git уже инициализирован"
fi

# Добавление всех файлов
echo "${YELLOW}⚙${NC}  Добавление файлов..."
git add .
echo "${GREEN}✓${NC} Файлы добавлены"

# Коммит
echo "${YELLOW}⚙${NC}  Создание коммита..."
git commit -m "Initial commit: ADEM LLM Voice Assistant

- Voice recognition with Whisper/Google Speech API
- LLM integration (OpenAI/Gemini/Claude)
- TTS with ElevenLabs/Google TTS
- Complete configuration system
- Ready for deployment"
echo "${GREEN}✓${NC} Коммит создан"

# Установка удалённого репозитория
echo "${YELLOW}⚙${NC}  Установка origin..."
if git remote | grep -q "origin"; then
    git remote set-url origin $REPO_URL
else
    git remote add origin $REPO_URL
fi
echo "${GREEN}✓${NC} Origin установлен"

# Переименование ветки в main (если нужно)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "${YELLOW}⚙${NC}  Переименование ветки в main..."
    git branch -M main
    echo "${GREEN}✓${NC} Ветка переименована"
fi

# Push в репозиторий
echo "${YELLOW}⚙${NC}  Отправка в GitHub..."
git push -u origin main

echo ""
echo "${GREEN}✅ ГОТОВО!${NC}"
echo ""
echo "Репозиторий успешно загружен на GitHub!"
echo "Откройте: ${REPO_URL%.git}"
echo ""
echo "${YELLOW}Следующие шаги:${NC}"
echo "  1. Скопируйте .env.example в .env"
echo "  2. Добавьте ваши API ключи в .env"
echo "  3. Установите зависимости: pip install -r requirements.txt"
echo "  4. Запустите: python main_startup.py"
echo ""
echo "📖 Подробнее: START_HERE.md"
