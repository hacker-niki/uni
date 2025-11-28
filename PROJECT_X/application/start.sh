#!/bin/bash

echo "🚀 Запуск TestGen MVP приложения..."
echo ""

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Проверка наличия Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

echo "✅ Docker и Docker Compose обнаружены"
echo ""

# Остановка старых контейнеров
echo "🛑 Остановка старых контейнеров..."
docker-compose down 2>/dev/null

echo ""
echo "🔨 Сборка и запуск контейнеров..."
docker-compose up --build

# Cleanup при выходе
trap 'docker-compose down' EXIT
