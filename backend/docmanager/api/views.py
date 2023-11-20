import io
import logging
import os

from cryptography.fernet import Fernet
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .decorators import user_me_view_request_schema


SCOPES = ["https://www.googleapis.com/auth/drive.file"]
logging.basicConfig(level=logging.INFO)


def validate_request_data(data, name):
    """
    Проверяет данные запроса на наличие обязательных полей.

    Args:
        data (str): Текстовое содержимое документа.
        name (str): Название документа.

    Returns:
        Response: Объект ответа Django REST framework в случае ошибки, иначе None.
    """
    if data is None or name is None:
        return Response(
            {"Ошибка": "Поле 'data' и 'name' должны быть указаны в запросе."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(name) == 0:
        return Response(
            {"Ошибка": "Поле 'name' должно быть заполнено."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(name) > 128:
        return Response(
            {"Ошибка": "Длина поля 'name' не должна превышать 128 символов."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(data) > 3145728:
        return Response(
            {"Ошибка": "Файл не должен превышать 3 МБ."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return None


def decrypt_json_data(encrypted_file_path, key):
    """
    Расшифровывает файл с использованием ключа и сохраняет расшифрованные данные в новом файле.

    Args:
        encrypted_file_path (str): Путь к файлу, который требуется расшифровать.
        key (str): Ключ для расшифровки.

    Returns:
        str: Путь к созданному расшифрованному файлу.
    """
    cipher_suite = Fernet(key)

    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = cipher_suite.decrypt(encrypted_data)

    decrypted_file_path = encrypted_file_path[:-4]
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    logging.info(f"Файл успешно расшифрован: {decrypted_file_path}")

    return decrypted_file_path


def initialize_google_drive(credentials_path, token_path):
    """
    Инициализирует объект Google Drive API.

    Args:
        credentials_path (str): Путь к файлу credentials.json.
        token_path (str): Путь к файлу token.json.

    Returns:
        Resource: Объект Google Drive API.
    """
    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if creds.expired:
            creds.refresh(Request())

            with open(token_path, "w") as token:
                token.write(creds.to_json())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    logging.info("Объект Google Drive API успешно инициализирован.")

    return build("drive", "v3", credentials=creds)


def create_google_drive_file(drive, name, data):
    """
    Создает новый документ в Google Drive.

    Args:
        drive (Resource): Объект Google Drive API.
        name (str): Имя файла.
        data (str): Текстовое содержимое документа.

    Returns:
        str: Идентификатор созданного файла.
    """
    file = (
        drive.files()
        .create(
            body={"name": name, "mimeType": "text/plain"},
        )
        .execute()
    )

    media_body = MediaIoBaseUpload(
        io.BytesIO(data.encode("utf-8")),
        mimetype="text/plain",
        resumable=True,
    )
    drive.files().update(
        fileId=file["id"], media_body=media_body
    ).execute()

    return file["id"]


def check_existing_file(drive, name):
    """
    Проверяет, существует ли файл с указанным именем в Google Drive.

    Args:
        drive (Resource): Объект Google Drive API.
        name (str): Имя файла.

    Returns:
        bool: True, если файл существует, иначе False.
    """
    existing_files = (
        drive.files()
        .list(q=f"name='{name}'", pageSize=1, fields="files(id, name)")
        .execute()
    )

    return bool(existing_files.get("files"))


@extend_schema(tags=["Загрузка файла в Google Drive"])
@user_me_view_request_schema
@csrf_exempt
@api_view(["POST"])
def create_google_drive_document(request):
    """
    Создает документ в Google Drive.

    Args:
        request.data:
            data (str): Текстовое содержимое документа.
            name (str): Название документа.

    Returns:
        Response: Ответ API с результатом выполнения операции.
        :param request:
    """
    if request.method == "POST":
        data = request.data.get("data")
        name = request.data.get("name")

        validation_result = validate_request_data(data, name)
        if validation_result:
            return validation_result

        encrypted_credentials_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "credentials.json.enc"
        )
        encrypted_token_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "token.json.enc"
        )
        DECRYPTION_KEY = os.getenv("DECRYPTION_KEY")

        if os.path.exists(encrypted_credentials_path):
            decrypt_json_data(encrypted_credentials_path, DECRYPTION_KEY)
        if os.path.exists(encrypted_token_path):
            decrypt_json_data(encrypted_token_path, DECRYPTION_KEY)

        credentials_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "credentials.json"
        )
        token_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "token.json"
        )

        drive = initialize_google_drive(credentials_path, token_path)

        if check_existing_file(drive, name):
            logging.warning(f"Документ с именем {name} уже существует.")
            return Response(
                {"Ошибка": "Документ с таким именем уже существует."},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            file_id = create_google_drive_file(drive, name, data)

            logging.info(f"Документ успешно создан с именем: {name}")

            file_info = drive.files().get(fileId=file_id).execute()

            return Response(
                {
                    "Выполнено": "Документ успешно создан.",
                    "file_name": file_info["name"],
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logging.exception("Произошла ошибка при создании документа.")

            return Response(
                {"Ошибка": f"Произошла ошибка при создании документа: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    logging.warning("Неверный запрос.")

    return Response(
        {"error": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST
    )
