# 🚀 Quick Git Workflow - Шпаргалка

## 📝 Каждый день (когда хочешь писать код)

### 1. Создай ветку для новой фичи

```bash
cd argus

# Убедись что на main
git checkout main

# Скачай последние изменения
git pull

# Создай ветку (замени feature-name на свое)
git checkout -b feature-cost-tracking
```

### 2. Пиши код

```bash
# Открой VS Code, пиши код
# Сохраняй файлы (Cmd+S)

# Проверь что изменилось
git status

# Добавь все изменения
git add .

# Сохрани с описанием
git commit -m "Add cost tracking for OpenAI"

# Загрузи на GitHub (в ветку, не в main!)
git push -u origin feature-cost-tracking
```

### 3. Когда готово - слей в main

**Через GitHub (проще):**
1. Зайди на https://github.com/sh1esty1769/argus
2. Увидишь "Compare & pull request" → нажми
3. Проверь изменения
4. Нажми "Merge pull request"
5. Готово! Код в `main`

**Через терминал:**
```bash
git checkout main
git merge feature-cost-tracking
git push
```

---

## 🎯 Типичные сценарии

### Новая фича

```bash
git checkout main
git pull
git checkout -b feature-email-alerts
# пишешь код
git add .
git commit -m "Add email alerts"
git push -u origin feature-email-alerts
# Pull Request на GitHub → Merge
```

### Исправить баг

```bash
git checkout main
git pull
git checkout -b bugfix-dashboard-crash
# фиксишь баг
git add .
git commit -m "Fix dashboard crash"
git push -u origin bugfix-dashboard-crash
# Pull Request → Merge
```

### Эксперимент (не уверен что нужно)

```bash
git checkout -b experiment-new-ui
# экспериментируешь
git add .
git commit -m "Try new UI"
git push -u origin experiment-new-ui

# Если не понравилось - удали ветку
git checkout main
git branch -D experiment-new-ui
git push origin --delete experiment-new-ui
```

---

## 🔍 Полезные команды

```bash
# Где я сейчас?
git branch

# Переключиться на main
git checkout main

# Переключиться на ветку
git checkout feature-name

# Посмотреть все ветки
git branch -a

# Удалить ветку локально
git branch -d feature-name

# Удалить ветку на GitHub
git push origin --delete feature-name
```

---

## ✅ Правила

1. **Никогда не коммить в `main` напрямую**
2. **Всегда создавай ветку для новой фичи**
3. **Понятные названия веток** (`feature-X`, `bugfix-Y`)
4. **Часто коммить** (каждые 30 минут)
5. **Сливать через Pull Request** (проверка перед продакшном)

---

## 🎯 Твоя структура веток

```
main (продакшн - все видят)
  ↓
develop (разработка - твоя песочница)
  ↓
feature-X (новые фичи)
bugfix-Y (исправления)
```

---

**Теперь ты можешь писать код не боясь сломать продакшн! 🚀**
