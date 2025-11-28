#!/bin/bash

echo "=========================================="
echo "Проверка авторизации TestGen MVP"
echo "=========================================="
echo ""

# Проверка backend health
echo "1. Проверка состояния backend..."
HEALTH=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo "✅ Backend доступен"
    echo "$HEALTH" | python3 -m json.tool
else
    echo "❌ Backend недоступен"
    exit 1
fi

echo ""
echo "=========================================="
echo ""

# Проверка авторизации администратора
echo "2. Тест авторизации: Администратор"
ADMIN_LOGIN=$(curl -s -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "admin@testgen.com"}')

if echo "$ADMIN_LOGIN" | grep -q "access_token"; then
    echo "✅ Авторизация admin успешна"
    echo "$ADMIN_LOGIN" | python3 -m json.tool | grep -E '"email"|"full_name"|"roles"'
else
    echo "❌ Ошибка авторизации admin"
    echo "$ADMIN_LOGIN"
fi

echo ""
echo "=========================================="
echo ""

# Проверка авторизации преподавателя
echo "3. Тест авторизации: Преподаватель"
TEACHER_LOGIN=$(curl -s -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "teacher@testgen.com"}')

if echo "$TEACHER_LOGIN" | grep -q "access_token"; then
    echo "✅ Авторизация teacher успешна"
    echo "$TEACHER_LOGIN" | python3 -m json.tool | grep -E '"email"|"full_name"|"roles"'
else
    echo "❌ Ошибка авторизации teacher"
    echo "$TEACHER_LOGIN"
fi

echo ""
echo "=========================================="
echo ""

# Проверка авторизации студента
echo "4. Тест авторизации: Студент"
STUDENT_LOGIN=$(curl -s -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "student1@testgen.com"}')

if echo "$STUDENT_LOGIN" | grep -q "access_token"; then
    echo "✅ Авторизация student успешна"
    echo "$STUDENT_LOGIN" | python3 -m json.tool | grep -E '"email"|"full_name"|"roles"'
else
    echo "❌ Ошибка авторизации student"
    echo "$STUDENT_LOGIN"
fi

echo ""
echo "=========================================="
echo ""

# Проверка /me endpoint с токеном
echo "5. Тест endpoint /api/auth/me"
TOKEN="user_1_admin@testgen.com"
ME_RESPONSE=$(curl -s http://localhost:8000/api/auth/me \
    -H "Authorization: Bearer $TOKEN")

if echo "$ME_RESPONSE" | grep -q "admin@testgen.com"; then
    echo "✅ Endpoint /me работает корректно"
    echo "$ME_RESPONSE" | python3 -m json.tool
else
    echo "❌ Ошибка endpoint /me"
    echo "$ME_RESPONSE"
fi

echo ""
echo "=========================================="
echo ""

# Проверка фронтенда
echo "6. Проверка frontend"
FRONTEND_RESPONSE=$(curl -s http://localhost:3000/ | head -5)
if echo "$FRONTEND_RESPONSE" | grep -q "TestGen"; then
    echo "✅ Frontend доступен на http://localhost:3000"
else
    echo "❌ Frontend недоступен"
fi

echo ""
echo "=========================================="
echo "ИТОГО:"
echo "=========================================="
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Тестовые пользователи:"
echo "  - admin@testgen.com     (администратор)"
echo "  - teacher@testgen.com   (преподаватель)"
echo "  - student1@testgen.com  (студент)"
echo "  - student2@testgen.com  (студент)"
echo ""
echo "=========================================="
