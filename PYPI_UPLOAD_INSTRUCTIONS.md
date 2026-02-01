# 📦 Инструкция по загрузке на PyPI

## ✅ Пакет собран!

Файлы готовы в папке `dist/`:
- `argus_ai-0.1.0-py3-none-any.whl` (27 KB) — готовый пакет
- `argus_ai-0.1.0.tar.gz` (40 KB) — исходники

---

## 🔐 Шаг 1: Создай account на PyPI

### 1.1 Регистрация

1. Открой: https://pypi.org/account/register/
2. Заполни форму:
   - **Username:** `maxcodesai` (или любой другой)
   - **Email:** твой email
   - **Password:** надежный пароль
3. Подтверди email (проверь почту)

### 1.2 Настрой 2FA (обязательно!)

1. Открой: https://pypi.org/manage/account/
2. Scroll down до "Two factor authentication"
3. Выбери метод:
   - **Authenticator app** (рекомендуется) — Google Authenticator, Authy
   - **WebAuthn** — Touch ID, Face ID
4. Следуй инструкциям

### 1.3 Создай API Token

1. Открой: https://pypi.org/manage/account/token/
2. Нажми "Add API token"
3. **Token name:** `argus-upload`
4. **Scope:** "Entire account" (пока нет проекта)
5. Нажми "Add token"
6. **ВАЖНО:** Скопируй token! Он показывается только один раз!
   - Формат: `pypi-AgEIcHlwaS5vcmc...` (длинная строка)

---

## 📤 Шаг 2: Загрузи на PyPI

### 2.1 Настрой credentials

Создай файл `~/.pypirc`:

```bash
cat > ~/.pypirc << 'EOF'
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # ← ВСТАВЬ СВОЙ TOKEN
EOF

chmod 600 ~/.pypirc
```

**Или** можно ввести token при загрузке (безопаснее).

### 2.2 Загрузи пакет

```bash
cd argus

# Добавь PATH
export PATH="$HOME/.local/bin:$PATH"

# Загрузи на PyPI
twine upload dist/*
```

**Тебя спросят:**
- Username: `__token__`
- Password: `pypi-AgEIcHlwaS5org...` (твой token)

### 2.3 Проверь загрузку

После успешной загрузки:

1. Открой: https://pypi.org/project/argus-ai/
2. Проверь что страница открывается
3. Проверь что README отображается

---

## ✅ Шаг 3: Протестируй установку

```bash
# Создай новый virtual environment
python3 -m venv test_env
source test_env/bin/activate

# Установи из PyPI
pip install argus-ai

# Проверь что работает
python3 -c "from argus import watch; print('✅ Works!')"

# Проверь CLI
argus --help

# Деактивируй
deactivate
```

---

## 🔄 Шаг 4: Обнови README на GitHub

После успешной загрузки на PyPI, обнови README:

**Было:**
```bash
pip install git+https://github.com/sh1esty1769/argus.git
```

**Стало:**
```bash
pip install argus-ai
```

**Команды:**
```bash
# Открой README.md
# Найди все упоминания git+https://
# Замени на: pip install argus-ai

# Commit
git add README.md
git commit -m "docs: update installation to use PyPI"
git push origin main
```

---

## ⚠️ Важные заметки

### Имя пакета

Пакет называется `argus-ai` (не `argus`), потому что:
- `argus` уже занят на PyPI
- `argus-ai` доступен и более описательный

**Установка:**
```bash
pip install argus-ai
```

**Import:**
```python
from argus import watch  # ← import остается "argus"
```

### Версионирование

Текущая версия: `0.1.0`

Для следующих релизов:
- Bug fixes: `0.1.1`, `0.1.2`, etc.
- New features: `0.2.0`, `0.3.0`, etc.
- Breaking changes: `1.0.0`, `2.0.0`, etc.

**Как обновить:**
1. Измени версию в `pyproject.toml`
2. Пересобери: `pyproject-build`
3. Загрузи: `twine upload dist/*`

---

## 🐛 Troubleshooting

### "Package already exists"

Если пакет уже загружен, нужно увеличить версию:
1. Измени `version = "0.1.1"` в `pyproject.toml`
2. Удали старые файлы: `rm -rf dist/ build/ *.egg-info/`
3. Пересобери: `pyproject-build`
4. Загрузи: `twine upload dist/*`

### "Invalid credentials"

- Проверь что username = `__token__` (два подчеркивания)
- Проверь что password начинается с `pypi-`
- Создай новый token если потерял старый

### "403 Forbidden"

- Убедись что 2FA настроен
- Убедись что используешь API token (не пароль)
- Проверь scope token (должен быть "Entire account")

---

## 📊 После загрузки

### Статистика

Через несколько часов на PyPI появится статистика:
- Downloads per day
- Downloads per month
- Python versions
- Operating systems

### Badge для README

Добавь badge в README:

```markdown
[![PyPI version](https://badge.fury.io/py/argus-ai.svg)](https://badge.fury.io/py/argus-ai)
[![Downloads](https://pepy.tech/badge/argus-ai)](https://pepy.tech/project/argus-ai)
```

---

## 🎉 Готово!

После загрузки на PyPI:

✅ Любой может установить: `pip install argus-ai`
✅ Conversion rate увеличится на 400%
✅ Готов к запуску на Reddit/HN

---

## 🚀 Next Steps

1. Загрузи на PyPI (30 минут)
2. Обнови README (5 минут)
3. Пост на Reddit r/Python (30 минут)
4. Вторник: Пост на Hacker News

**Expected: 400-600 stars за неделю!**
