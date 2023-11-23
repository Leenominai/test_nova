# Создание текстовых документов в Google Drive

## Описание ТЗ

Перед получением информации о выполненном проекте предлагаю ознакомиться с подробной информацией о целях проекта:

<details>
  <summary>Открыть</summary>
   
### Требования:

1. Сделать API метод, который можно будет запустить POST запросом с параметрами:
   - data = Текстовое содержимое файла
   - name = Название файла
2. Необходимо создать в google drive документ с названием = name и содержимым = data
3. Предварительно нужно создать Гугл аккаунт пустой и авторизовать приложение, чтобы получить токены
4. Нужно использовать фреймворк Django

### Критерии оценки:

1. Работоспособность согласно ТЗ.
2. Архитектура решения.
3. Удобство чтения кода и комментарии.
4. Удобство проверки (GIT + развернутый рабочий сервер на момент проверки).

### Результат тестового задания необходимо отправить в HH:

- Ссылка на репозиторий.
- URL и описание метода.

</details>

## О выполненном проекте docmanager

Этот проект представляет собой API для загрузки текстовых файлов в Google Drive, с контейнеризацией Docker, интеграцией Google Drive API, аутентификацией через Google и легкостью расширения.

### Важными особенностями проекта являются:

- **Контейнеризация с Docker**: Проект упакован в контейнеры с использованием Docker и Docker Compose, обеспечивая легкость развертывания в различных окружениях.

- **Автоматизация с pre-commit**: В проекте реализован pre-commit, автоматизирующий проверку кода на соответствие стандартам перед каждым коммитом. Это обеспечивает единообразие кода и улучшает его качество.

- **Логгирование для отслеживания действий**: Внедрено логгирование, которое фиксирует ключевые действия приложения, обеспечивая прозрачность и отслеживание работы системы.

- **Шифрование токенов**: Конфиденциальные данные, такие как файл credentials.json, шифруются с использованием ключа, который хранится в .env файле и GitHub Secrets. Это обеспечивает безопасность при хранении и передаче важной информации, предотвращая несанкционированный доступ.

### Используемый стек

- **Python**: Версия 3.11
- **Django**: Версия 4.2.7
- **Django REST framework**: Библиотека для разработки RESTful API.
- **google-api-python-client**: Используется для взаимодействия с Google Drive, обеспечивает загрузку и обработку файлов.
- **python-dotenv**: Загрузка переменных окружения из файлов .env для конфигурации.
- **gunicorn**: WSGI HTTP-сервер для обслуживания Django-приложения.
- **pre-commit**: Автоматическая проверка и форматирование кода перед коммитом (blake8)

### Внешнее ПО

- **PyCharm**: Интегрированная среда разработки Python.
- **Docker**: Контейнеризация приложения и зависимостей для легкого развертывания.
- **Postman**: Инструмент для тестирования и проверки функциональности API.
- **Google Chrome**: Браузер для проверки работоспособности приложения.

## Демонстрация приложения на активном сервере

### Доступные пути API

- **http://158.160.61.104/api/v1/upload/**: путь для принятия POST-запросов на загрузку файлов

- **http://158.160.61.104/api/v1/redoc/**: Redoc - Интерактивная документация API для ознакомления с функциональностью и возможными ошибками.
- **http://158.160.61.104/api/v1/swagger-ui/#/**: Swagger - Интерактивная документация API для ознакомления с функциональностью и возможными ошибками.

## Локальный запуск приложения (при необходимости)

<details>
  <summary>Подробная инструкция (<b>нажмите на эту строчку, чтобы открыть</b>):</summary>


#### Для локальной установки проекта необходимо выполнить следующие шаги:

### Установка и настройка внешнего ПО:
- Docker: Если у вас ещё не установлен Docker, следуйте инструкциям на официальном сайте Docker для вашей операционной системы: https://docs.docker.com/get-docker/. После установки убедитесь, что Docker Daemon запущен.
  - Docker Compose: Установите Docker Compose, если он ещё не установлен. Docker Compose используется для управления многоконтейнерными приложениями. Инструкции по установке можно найти здесь: https://docs.docker.com/compose/install/

### Запуск приложения:
- Клонирование репозитория
```
git@github.com:Leenominai/test_nova.git
```
- Переход в рабочую папку приложения
```
cd backend
```
- Настройка файлов окружения: Создайте файл окружения .env в корне вашего проекта.
- Скопируйте все данные из файла .env.example в файл .env:
  - Сейчас в файле .env.example присутствуют значения всех необходимых переменных только для локальной проверки приложения, а для сервера все переменные скрыты в GitHub Secrets.
- Запуск контейнеров: Запустите приложение с помощью Docker Compose:
```
cd ..
cd docker_local
docker-compose up -d
```
- Применение миграций Django и создание администратора (не обязательно):
```
docker exec -it test_backend bash
python manage.py migrate
python manage.py createsuperuser
exit
```

- Открытие приложения:
Ваше приложение должно быть доступно по адресу http://127.0.0.1:8000/ в браузере.

### Доступные пути API

- **http://127.0.0.1:8000/api/v1/upload/**: путь для принятия POST-запросов на загрузку файлов

- **http://127.0.0.1:8000/api/v1/redoc/**: Redoc - Интерактивная документация API для ознакомления с функциональностью и использованием.
- **http://127.0.0.1:8000/api/v1/swagger-ui/#/**: Swagger - Интерактивная документация API с возможностью отправки запросов и получения ответов непосредственно из браузера для тестирования.
</details>

## Тестирование в Postman приложения на сервере

Для сервера все ключи авторизации Google API для проверки приложения уже сохранены в системе в зашифрованном виде и подгружаются при выполнении запроса для тестового аккаунта (информация о нём будет дальше).

Для тестирования через программу Postman необходимо:
- Установить её на свою рабочую машину с официального сайта: https://www.postman.com/
- После установки необходимо перейти в раздел Workspaces
- Создать новый Request через +, либо изменить стандартный
- В шкалу URL необходимо ввести следующий адрес: http://158.160.61.104/api/v1/upload/
- Слева от введённого адреса выбрать тип запроса: POST
- Далее, необходимо выбрать блок Body и раздел form-data под ним.
- Для загрузки используем следующий формат:
```
    | Key      | Value                 | Допустимые значения для поля Value |
    | ---------| --------------------- | ---------------------------------- |
    | data     | <Ваш текст>           | Длина до 3145728 символов (3 МБ)   |
    | name     | <Ваше название файла> | Длина до 128 символов              |

```
- Нажать кнопку Send (отправить запрос)
<details>
  <summary>При возможных ошибках загрузок в блоке Headers ставим следующую настройку (<b>нажмите на эту строчку, чтобы открыть</b>):</summary>

    | Key         | Value            |
    | ----------- | ---------------- |
    | ContentType | application/json |

</details>

- После успешного выполнения запроса будет получен ответ системы:

  ```
  [
      {
          "Выполнено": "Документ успешно создан.",
          "file_name": "test_document1"
      }
  ]
  ```
- Если такой файл уже существует в хранилище Google Drive, то система выдаст соответствующую ошибку:
   ```
   [
       {
           "Ошибка": "Документ с таким именем уже существует."
       }
   ]
   ```

#### Загруженный файл можно проверить визуально. Для этого необходимо:

- Необходимо перейти на официальную страницу Google Drive: https://drive.google.com/drive/u/2/my-drive
- После этого необходимо авторизоваться в системе под данными тестового аккаунта Google, созданного для проверки приложения:

  <details>
    <summary>Данные для авторизации в Google-аккаунт (<b>нажмите на эту строчку, чтобы открыть</b>):</summary>

      | Email    | test.nova.user001@gmail.com |
      | Password | test_nova                   |

  </details>

- В списке файлов можно будет увидеть только что созданный файл.

## Тестирование в Postman при локальной установке

Для тестирования через программу Postman необходимо:
- Установить её на свою рабочую машину с официального сайта: https://www.postman.com/
- После установки необходимо перейти в раздел Workspaces
- Создать новый Request через +, либо изменить стандартный
- В шкалу URL необходимо ввести следующий адрес: http://127.0.0.1:8000/api/v1/upload/
- Слева от введённого адреса выбрать тип запроса: POST
- Далее, необходимо выбрать блок Body и раздел form-data под ним.
- Для загрузки используем следующий формат:
```
    | Key      | Value                 | Допустимые значения для поля Value |
    | ---------| --------------------- | ---------------------------------- |
    | data     | <Ваш текст>           | Длина до 3145728 символов (3 МБ)   |
    | name     | <Ваше название файла> | Длина до 128 символов              |

```
- Нажать кнопку Send (отправить запрос)
<details>
  <summary>При возможных ошибках загрузок в блоке Headers ставим следующую настройку (<b>нажмите на эту строчку, чтобы открыть</b>):</summary>

    | Key         | Value            |
    | ----------- | ---------------- |
    | ContentType | application/json |

</details>

- После успешного выполнения запроса будет получен ответ системы:

  ```
  [
      {
          "Выполнено": "Документ успешно создан.",
          "file_name": "test_document1"
      }
  ]
  ```
- Если такой файл уже существует в хранилище Google Drive, то система выдаст соответствующую ошибку:
   ```
   [
       {
           "Ошибка": "Документ с таким именем уже существует."
       }
   ]
   ```

#### Можно визуально проверить создание токена и авторизацию через браузер, для этого необходимо:

- Перейти в рабочую папку Django-проекта в приложение api:
  ```
    cd ..
    cd backend/docmanager/api
  ```
- Удалить файл с существующим токеном авторизации тестового аккаунта через визуальный интерфейс или командой в консоли:
  ```
    rm token.json.enc
  ```
- Нажать кнопку Send (отправить запрос)
- После этого при выполнении запроса будет выполнено автоматическое перенаправление на страницу авторизации аккаунта Google в вашем браузере по-умолчанию, где будет необходимо войти в аккаунт Google со следующими данными:

    <details>
      <summary>Данные для авторизации в Google-аккаунт (<b>нажмите на эту строчку, чтобы открыть</b>):</summary>

        | Email    | test.nova.user001@gmail.com |
        | Password | test_nova                   |

    </details>

        Это новый тестовый аккаунт для тестирования данного приложения.
        Он авторизован в системе Google Drive API как доступный для тестирования.
        Прочие аккаунты будут заблокированы для доступа к API.

- Если пользователь уже вошёл под этим аккаунтом, то ему отобразится список авторизованных аккаунтов, в списке которого нужно будет выбрать Test User:

    ![google_account.png](media%2Fgoogle_account.png)

- После чего будет необходимо предоставить доступ приложению на работу с Google Drive API.

    <details>
      <summary>Визуальная инструкция - как это будет выглядеть в браузере (<b>нажмите на эту строчку, чтобы открыть</b>):</summary>

  ![google_api1.png](media%2Fgoogle_api1.png)
  ![google_api1.png](media%2Fgoogle_api2.png)

    </details>

- После чего пользователь на странице авторизации в браузере получит ответ:
    ```
    The authentication flow has completed. You may close this window.
    ```

- Необходимо снова вернуться в интерфейс программы Postman, где можно будет увидеть ответ системы:
    ```
    [
        {
            "Выполнено": "Документ успешно создан.",
            "file_name": "test_document1"
        }
    ]
    ```

 - Если такой файл уже существует в хранилище Google Drive, то система выдаст соответствующую ошибку:
    ```
    [
        {
            "Ошибка": "Документ с таким именем уже существует."
        }
    ]
    ```

#### Загруженный файл можно проверить визуально. Для этого необходимо:

- Необходимо перейти на официальную страницу Google Drive: https://drive.google.com/drive/u/2/my-drive
- После этого необходимо авторизоваться в системе под данными тестового аккаунта Google, созданного для проверки приложения:

  <details>
    <summary>Данные для авторизации в Google-аккаунт (<b>нажмите на эту строчку, чтобы открыть</b>):</summary>

      | Email    | test.nova.user001@gmail.com |
      | Password | test_nova                   |

  </details>

- В списке файлов можно будет увидеть только что созданный файл.

## Разработчики

Проект разработан и поддерживается Александром Рассыхаевым.

GitHub: [Ссылка на GitHub профиль](https://github.com/Leenominai)

Telegram: [@Leenominai](https://t.me/Leenominai)
