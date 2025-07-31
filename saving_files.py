from flask import Flask, request, render_template, send_from_directory, jsonify
import os
from faster_whisper import WhisperModel
from datetime import datetime

# Папки для хранения файлов
UPLOAD_FOLDER = 'uploads'  # Папка для загруженных файлов
TRANSCRIPTS_FOLDER = 'transcripts'  # Папка для текстовых расшифровок

# Создание папок, если они не существуют
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(TRANSCRIPTS_FOLDER):
    os.makedirs(TRANSCRIPTS_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRANSCRIPTS_FOLDER'] = TRANSCRIPTS_FOLDER

# Инициализация модели Whisper
device = "cpu"  # Используем CPU для обработки
whisper_model = WhisperModel(
    "Systran/faster-whisper-base",  # Название модели
    compute_type="int8",  # Тип вычислений (int8 для экономии памяти)
    device=device  # Устройство для вычислений
)


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


@app.route('/')
def index():
    """Отображает главную страницу с формой загрузки файлов.

    Returns:
        str: HTML шаблон главной страницы.
    """
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Обрабатывает загруженный файл и сохраняет его на сервере.

    Если файл MP3 - выполняет транскрибацию и сохраняет результат.

    Returns:
        JSON: Результат обработки файла.
    """
    if 'file' not in request.files:
        return jsonify(success=False, message='Файл не выбран'), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, message='Имя файла пустое'), 400

    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        if file.filename.lower().endswith('.mp3'):
            transcription_text = transcribe_mp3(filepath)
            transcript_filename = os.path.splitext(file.filename)[0] + ".txt"
            transcript_file_path = os.path.join(app.config['TRANSCRIPTS_FOLDER'], transcript_filename)

            with open(transcript_file_path, 'w', encoding='utf-8') as f:
                f.write(transcription_text)

            return jsonify(success=True, message=f'Файл {file.filename} успешно сохранён.')
        else:
            return jsonify(success=True, message=f'Файл {file.filename} успешно сохранён.')
    except Exception as e:
        return jsonify(success=False, message=f'Ошибка обработки файла: {str(e)}'), 500

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify(success=False, message='Файл аудио не найден')
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify(success=False, message='Нет выбранного файла')

    webm_to_mp3_file = os.path.splitext(audio_file.filename)[0] + ".mp3"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], webm_to_mp3_file)
    audio_file.save(filepath)


    transcription_text = transcribe_mp3(filepath)
    transcript_filename = os.path.splitext(audio_file.filename)[0] + ".txt"
    transcript_file_path = os.path.join(app.config['TRANSCRIPTS_FOLDER'], transcript_filename)

    with open(transcript_file_path, 'w', encoding='utf-8') as f:
        f.write(transcription_text)

    return jsonify(success=True)



@app.route('/list')
def file_list():
    """Отображает список всех загруженных файлов и их расшифровок (если есть).

    Returns:
        str: HTML шаблон со списком файлов.
    """
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_info = []

    for filename in files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        created_time = datetime.fromtimestamp(os.path.getctime(filepath))
        formatted_time = created_time.strftime('%d.%m.%Y %H:%M:%S')

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

        file_info.append({'filename': filename, 'transcript': transcript, 'created_time': formatted_time})

    return render_template('list.html', file_info=file_info)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Позволяет скачать загруженный файл.

    Args:
        filename (str): Имя файла для скачивания.

    Returns:
        Response: Файл для скачивания.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)