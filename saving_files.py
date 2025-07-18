from flask import Flask, request, render_template, send_from_directory
import os

#пределяем папку для сохранения
UPLOAD_FOLDER = 'uploads'
#если папки "uploads" не существует, создаём папку
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


app = Flask(__name__)
#сохрянем путь к папке в конфигурации приложения
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#главная страница
@app.route('/')
def index():
    # отдаёт HTML с формой
    return render_template('index.html')

#страница после сохранения файла
@app.route('/upload', methods=['POST'])
def upload_file():
    #проверяем есть ли поле file в запросе
    if 'file' not in request.files:
        return "Файл не выбран", 400
    #получаем файл из запроса
    file = request.files['file']
    #проверяем пустое ли имя файла
    if file.filename == '':
        return "Имя файла пустое", 400
    # Сохраняем файл в папку uploads
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return f"Файл {file.filename} успешно сохранён"

#страница со списков скачанных файлов
@app.route('/list')
def file_list():
    #получаем список всех файлов из папки
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    # Отправляем список файлов в шаблон
    return render_template('list.html', files=files)

# Маршрут для скачивания файла
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #отправляем файл пользователю как вложение для скачивания
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    #запускаем flask сервер в режимо отладки
    app.run(debug=True)


