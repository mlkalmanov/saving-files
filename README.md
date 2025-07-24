# Сохранение файлов и их транскрибация
Учебная страница для сохранения файлов и их транскрибации. 
В процессе создания использовались **Python Flask** и модель для транскрибации **faster-whisper**.
## Запуск
* Перед использованием установите все необходимые библиотеки
```
from flask import Flask, request, render_template, send_from_directory
import os
from faster_whisper import WhisperModel
```
```Flask``` - основной класс приложения

```request``` - для работы с HTTP запросами (получение загруженных файлов)

```render_temlate``` - для отображения HTML шаблонов (index.html и list.html)

```send_from_directory``` - для отправки файлов пользователю на скачивание

```os``` - для работы с файловой системой

```WhisperModel``` - модель для транскрибации

* Чтобы запустить приложение, вернитесь в терминал и выполните команду ```python saving_files.py``` или нажмите кнопку "Run" в текстовом редакторе.
* Далее передите в браузер и откройте страницу http://127.0.0.1:5000 или просто перейдите по ссылке, которая вывелась в консоль.

<img width="314" height="134" alt="image" src="https://github.com/user-attachments/assets/4d0d0ad4-e739-4abd-a926-76b42a242c60" />


## Работа на странице 

### Главная страница 

<img width="624" height="403" alt="image" src="https://github.com/user-attachments/assets/ca315888-35ce-4630-84fb-63fab8226b0a" />


* Файл можно выбрать либо перетащив в поле, либо, нажав на кнопку **"Choose file"**, выбрать файл из проводника.
* После выбора нажмите кнопку **"save"**
* После этого вы автоматически перейдёте на страницу с уведомлением об успешной загрузке файла.
 
**ИЛИ**
 
* Если файл был с расширением ***mp3***, то так же выведется расшифровка аудиофайла.

### Сохранение файлов и расшифровок
Все фалы после выбора сохраняются в папку uploads, а для сохранения расшифровки создаётся тектовый файл с таким же названием как у изначального файла, но с расширением **txt**, который в свою очередь сохраняется в папку transcripts.

*Кодом предусмотрено, что если папка заранее не создана, то папка создаётся автоматически.*
```
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

TRANSCRIPTS_FOLDER = 'transcripts'
if not os.path.exists(TRANSCRIPTS_FOLDER):
    os.makedirs(TRANSCRIPTS_FOLDER)
```



### Список файлов
<img width="626" height="135" alt="image" src="https://github.com/user-attachments/assets/c3c0178c-bd2c-4be7-8eb2-9f0677e5db06" />


Нажав на кнопку downloads, вы попадаете на страницу list.

<img width="840" height="358" alt="image" src="https://github.com/user-attachments/assets/a3a4c3b9-2b86-4278-b269-17cdad773f74" />


При генерации берутся данные о находящихся в папке uploads файлов и при наличии файла с идентичным именем с расширением txt в папке transcripts рядом с файлом пишется расшифровка.

```
@app.route('/list')
def file_list():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_info = [] # Список для информации о файлах
    for filename in files:
        # Проверяем, является ли файл MP3
        if filename.lower().endswith('.mp3'):
            # Создаем имя файла расшифровки
            transcript_filename = os.path.splitext(filename)[0] + ".txt"
            # Создаем полный путь к файлу расшифровки
            transcript_file_path = os.path.join(app.config['TRANSCRIPTS_FOLDER'], transcript_filename)
            # Проверяем, существует ли файл расшифровки
            if os.path.exists(transcript_file_path):
                # Читаем содержимое файла расшифровки
                with open(transcript_file_path, 'r', encoding='utf-8') as f:
                    transcript = f.read()
            else:
                transcript = ""
        else:
            # Для не-MP3 файлов расшифровка пустая
            transcript = ""

        file_info.append({'filename': filename, 'transcript': transcript})

    return render_template('list.html', file_info=file_info)
```

Также при нажатии на имя файла можно его скачать.

```
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #отправляем файл пользователю как вложение для скачивания
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
```

Нажав на кнопку "Back to download", пользователь возвращается на главную страницу.
## faster-whisper

Настройка модели Whisper

```
device = "cpu" # Используем CPU для обработки
whisper_model = WhisperModel(
    "Systran/faster-whisper-base", # Название модели
    compute_type="int8", # Тип вычислений (int8 для экономии памяти)
    device=device # Устройство для вычислений
)
```

Функция для транскрибации
```
def transcribe_mp3(file_path):
    # Получаем сегменты и информацию о файле
    segments, info = whisper_model.transcribe(file_path, beam_size=5)
    text = "" # Инициализируем пустую строку для текста
    # Проходим по всем сегментам и собираем текст
    for segment in segments:
        text += segment.text.strip() + " "
    return text.strip() # Возвращаем текст без лишних пробелов
```


