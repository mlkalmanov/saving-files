# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем ffmpeg (необходим для faster-whisper)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Копируем остальные файлы
COPY . .

# Создаем папки для загрузок
RUN mkdir -p uploads transcripts

# Открываем порт
EXPOSE 5000

# Запускаем приложение
CMD ["python", "saving_files.py"]