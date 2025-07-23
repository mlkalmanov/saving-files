# Сохранение файлов и их транскрибация
Учебная страница для сохранения файлов и их транскрибации. 
В процессе создания использовались **Python Flask** и модель для транскрибации **faster-whisper**
## Запуск
* Чтобы запустить приложение, вернитесь в терминал и выполните команду "python saving_files.py" или нажмите кнопку "Run" в текстовом редокторе
* Далее передите в браузер и откройте страницу http://127.0.0.1:5000 или просто перейдите по ссылке, которая вывелась в консоль

## Работа на странице 

### Главная страница 
<img width="651" height="463" alt="image" src="https://github.com/user-attachments/assets/2ad17c1f-139a-4405-bbbc-9cb144564a87" />

* Файл можно выбрать либо перетащив в поле, либо, нажав на кнопку **"Choose file"**, выбрать файл из проводника
* После выбора нажмите кнопку **"save"**
* После этого вы автоматически перейдёте на страницу с уведомлением об успешной загрузке файла
 <img width="372" height="43" alt="image" src="https://github.com/user-attachments/assets/b0a568df-3ddd-461f-8983-bd23727dc5ca" />
 
**ИЛИ**
 
* Если файл был с расширением ***mp3***, то так же выведется расшифровка аудиофайла
 <img width="509" height="41" alt="image" src="https://github.com/user-attachments/assets/70c77a6d-c154-42f5-8526-a582987878e9" />

### Сохранение файлов и расшифровок
Все фалы после выбора сохраняются в папку uploads, а для сохранения расшифровки создаётся тектовый файл с таким же названием как у изначального файла, но с расширением **txt**, который в свою очередь сохраняется в папку transcripts
*Кодом предусмотрено, что если папка заранее не создана, то папка создаётся автоматически*

<img width="530" height="67" alt="image" src="https://github.com/user-attachments/assets/51819f9c-3791-4142-917f-0a975f8e3f02" />

Содрежимое папки uploads:

  <img width="635" height="66" alt="image" src="https://github.com/user-attachments/assets/1b32a085-82e6-41c2-8bdb-32ab732f695c" />

  
Содержимое папки transcripts:

  <img width="612" height="29" alt="image" src="https://github.com/user-attachments/assets/13fde39a-7ded-4df5-95f8-007d1f66f1bb" />

### Список файлов
<img width="622" height="125" alt="image" src="https://github.com/user-attachments/assets/515a1ece-5787-484f-ab58-5ca4ad0bd9dd" />

Нажав на кнопку downloads, вы попадаете на страницу list

<img width="883" height="376" alt="image" src="https://github.com/user-attachments/assets/ff87036e-4611-41f5-a5b8-d685c5d3a423" />

При генерации берутся данные о находящихся в папке uploads файлов и при наличии файла с идентичным именем с расширением txt в папке transcripts рядом с файлом пишется расшифровка.

Нажав на кнопку "Back to downloads", пользователь возвращается на главную страницу
