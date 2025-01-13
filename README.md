# tg_proj
python-telegram-bot
  
  part_1_get_exec.py
  
  contains:
  - ivitation link generate via invite_data.txt using unfilled strings
  - generating invitation QR code
  - posting into group via text_schedule.txt using datetime less then current datetime. part of post is in text_schedule.txt + picture from repo
  
  part_2_handler_exec.py

contains:
- confirmation about group join requests with filling responde_data.txt
- bot chatting buttons

  Main idea is to connect more obvious invitation(perhaps you gess when you share your welcome) link with obviousless users
![pyton_telegram_bot_scheme](https://github.com/user-attachments/assets/258ecc30-d1db-4941-aad3-9db11ae0fbe9)


Проект на основе python-telegram-bot
Библиотеки:
python-telegram-bot v21.10
pandas - Python Data Analysis Library
qrcode · PyPI

Цели:

Идентификация пользователя на этапе регистрации. т.е. осознание(учёт в таблицах хранилища данных в проекте реализованы как .txt файлы) принадлежности к укрупненной выборке.

Задачи:

Формирование пригласительных ссылок
Ведение реестра пригласительных ссылок

Перевод строк ссылок на QR отображение
Одобрение/ отклонение(если регистрируется Бот) регистрации по ранее сформированным пригласительным
Формирование связи(учёт в таблицах хранилища данных) между зарегистрированным лицом и сформированной пригласительной ссылкой
Печать постов в TG группе по указанному расписанию
Взаимодействие с зарегистрированными пользователями путём рассылки файлов(.txt), кнопочная форма чат-Бот.

Схема работы в приложении

Файлы:

invite_data.txt:

реестр сформированных ссылок/ либо ссылок необходимых к формированию. Левая часть содержит данные-основу, правая - сформированные ссылки.

responde_data.txt:

данные по учёту зарегистрированных пользователей. Содержит связь аккаунт - ссылка.

text_schedule.txt:

данные по времени печати постов в группе. Текстовая информация по постам.
0001...0003 jpg:

картинки к постам
Папка LINKS:
1..3 png :

QR-коды ссылок из файла invite_data.txt

Файл key_bb.txt :

пример файла раздачи при взаимодействии с ботом

part_1_get_exec.py файл:

формирования пригласительных ссылок

печать постов в группу

part_2_handler_exec.py файл:
одобрение/отклонение на вступление в группу по пригласительным ссылкам

переписка чат-Бота с пользователем
