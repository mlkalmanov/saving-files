from flask import Flask, request, render_template, send_from_directory
import os
from faster_whisper import WhisperModel

#пределяем папку для сохранения
UPLOAD_FOLDER = 'uploads'
TRANSCRIPTS_FOLDER = 'transcripts'


#если папки "uploads" не существует, создаём папку
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(TRANSCRIPTS_FOLDER):
    os.makedirs(TRANSCRIPTS_FOLDER)




app = Flask(__name__)
#сохрянем путь к папке в конфигурации приложения
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRANSCRIPTS_FOLDER'] = TRANSCRIPTS_FOLDER

device = "cpu"
whisper_model = WhisperModel(
    "Systran/faster-whisper-base",
    compute_type="int8",
    device=device
)

#функция транскрибирования
def transcribe_mp3(file_path):
    segments, info = whisper_model.transcribe(file_path, beam_size=5)
    text = ""
    for segment in segments:
        text += segment.text.strip() + " "
    return text.strip()

#главная страница
@app.route('/')
def index():
    # отдаёт HTML с формой
    return render_template('index.html')

#страница после сохранения файла
@app.route('/upload', methods=['POST'])
def upload_file():
    #проверяем выбран ли файл
    if 'file' not in request.files:
        return "the file is not selected", 400
    #получаем файл из запроса
    file = request.files['file']
    #проверяем пустое ли имя файла
    if file.filename == '':
        return "The file name is empty", 400
    # Сохраняем файл в папку uploads
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    #проверка необходимого расширения для транскрибирования
    if file.filename.lower().endswith('.mp3'):
        transcription_text = transcribe_mp3(filepath)
        transcript_filename = os.path.splitext(file.filename)[0] + ".txt"
        transcript_file_path = os.path.join(app.config['TRANSCRIPTS_FOLDER'], transcript_filename)
        with open(transcript_file_path, 'w', encoding='utf-8') as f:
            f.write(transcription_text)
        #если файл с расширением mp3 то выводится сообщение об успешной установке и расшифровка
        return f'Файл {file.filename} успешно сохранён. Расшифровка: {transcription_text}'
    else:
        #иначе только сообщение об успешной установке
        return f'Файл {file.filename} успешно сохранён.'

@app.route('/list')
def file_list():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_info = []
    for filename in files:
        # Проверяем, является ли файл MP3
        if filename.lower().endswith('.mp3'):
            transcript_filename = os.path.splitext(filename)[0] + ".txt"
            transcript_file_path = os.path.join(app.config['TRANSCRIPTS_FOLDER'], transcript_filename)
            if os.path.exists(transcript_file_path):
                with open(transcript_file_path, 'r', encoding='utf-8') as f:
                    transcript = f.read()
            else:
                transcript = ""
        else:
            # Для не-MP3 файлов расшифровка пустая
            transcript = ""

        file_info.append({'filename': filename, 'transcript': transcript})

    return render_template('list.html', file_info=file_info)


# Маршрут для скачивания файла
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #отправляем файл пользователю как вложение для скачивания
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    #запускаем flask сервер в режимо отладки
    app.run(debug=True)




