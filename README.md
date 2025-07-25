# Сохранение файлов и их транскрибация
Учебная страница для сохранения файлов и их транскрибации. 
В процессе создания использовались **Python Flask** и модель для транскрибации **faster-whisper**.
## Запуск
* Перед использованием установите все необходимые библиотеки
``` python
from flask import Flask, request, render_template, send_from_directory, jsonify
import os
from faster_whisper import WhisperModel
```
```Flask``` - основной класс приложения

```request``` - для работы с HTTP запросами (получение загруженных файлов)

```render_temlate``` - для отображения HTML шаблонов (index.html и list.html)

```send_from_directory``` - для отправки файлов пользователю на скачивание

```os``` - для работы с файловой системой

```WhisperModel``` - модель для транскрибации

```jsonify``` - для преобразования данных в формат json

* Чтобы запустить приложение, вернитесь в терминал и выполните команду ```python saving_files.py``` или нажмите кнопку "Run" в текстовом редакторе.
* Далее передите в браузер и откройте страницу http://127.0.0.1:5000 или просто перейдите по ссылке, которая вывелась в консоль.

<img width="314" height="134" alt="image" src="https://github.com/user-attachments/assets/4d0d0ad4-e739-4abd-a926-76b42a242c60" />


## Работа на странице 

### Главная страница 

<img width="773" height="809" alt="image" src="https://github.com/user-attachments/assets/a45ec522-6ae0-40ee-9864-06428113b907" />



* Файл можно выбрать либо перетащив в поле, либо, нажав на кнопку **"Choose file"**, выбрать файл из проводника.
* После выбора нажмите кнопку **"save"**
* После этого вы автоматически перейдёте на страницу с уведомлением об успешной загрузке файла.
* Если файл был с расширением ***mp3***, то так же выведется расшифровка аудиофайла.
  
**ИЛИ**

Можно записать голосовое сообщение самостоятельно:

<img width="760" height="266" alt="image" src="https://github.com/user-attachments/assets/61891570-1959-49c4-8819-43293cd85119" />


* Нажмите на кнопку "Начать запись"
* Скажите всё, что необходимо
* Завершите запись, нажав на кнопку повторно

(Загрузка голосовых сообщений и их обработка займёт больше времени, чем загрузка обычных файлов из-за транскрибации)
### Сохранение файлов и расшифровок
Все фалы после выбора сохраняются в папку uploads, а для сохранения расшифровки создаётся тектовый файл с таким же названием как у изначального файла, но с расширением **txt**, который в свою очередь сохраняется в папку transcripts.

*Кодом предусмотрено, что если папка заранее не создана, то папка создаётся автоматически.*
``` python
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

TRANSCRIPTS_FOLDER = 'transcripts'
if not os.path.exists(TRANSCRIPTS_FOLDER):
    os.makedirs(TRANSCRIPTS_FOLDER)
```



### Список файлов
<img width="759" height="156" alt="image" src="https://github.com/user-attachments/assets/c00b5bc3-6039-4629-9a96-1f9ce8074259" />



Нажав на кнопку "История переговоров", вы попадаете на страницу list.

<img width="840" height="358" alt="image" src="https://github.com/user-attachments/assets/a3a4c3b9-2b86-4278-b269-17cdad773f74" />


При генерации берутся данные о находящихся в папке uploads файлов и при наличии файла с идентичным именем с расширением txt в папке transcripts рядом с файлом пишется расшифровка.

``` python
@app.route('/list')
def file_list():
    """Отображает список всех загруженных файлов и их расшифровок (если есть).

    Returns:
        str: HTML шаблон со списком файлов.
    """
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_info = []

    for filename in files:
        if filename.lower().endswith('.mp3'):
            transcript_filename = os.path.splitext(filename)[0] + ".txt"
            transcript_file_path = os.path.join(app.config['TRANSCRIPTS_FOLDER'], transcript_filename)

            if os.path.exists(transcript_file_path):
                with open(transcript_file_path, 'r', encoding='utf-8') as f:
                    transcript = f.read()
            else:
                transcript = ""
        else:
            transcript = ""

        file_info.append({'filename': filename, 'transcript': transcript})

    return render_template('list.html', file_info=file_info)
```

Также при нажатии на имя файла можно его скачать.

``` python
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Позволяет скачать загруженный файл.

    Args:
        filename (str): Имя файла для скачивания.

    Returns:
        Response: Файл для скачивания.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
```

Нажав на кнопку "Назад к загрузке", пользователь возвращается на главную страницу.
## faster-whisper

Настройка модели Whisper

``` python
device = "cpu"  # Используем CPU для обработки
whisper_model = WhisperModel(
    "Systran/faster-whisper-base",  # Название модели
    compute_type="int8",  # Тип вычислений (int8 для экономии памяти)
    device=device  # Устройство для вычислений
)
```

Функция для транскрибации
``` python
def transcribe_mp3(file_path):
    """Транскрибирует MP3 файл с помощью модели Whisper.

    Args:
        file_path (str): Путь к MP3 файлу для транскрибации.

    Returns:
        str: Текстовая расшифровка аудиофайла.
    """
    segments, info = whisper_model.transcribe(file_path, beam_size=5)
    text = ""
    for segment in segments:
        text += segment.text.strip() + " "
    return text.strip()
```


