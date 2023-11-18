import io
import logging
import os

from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from google.auth.transport.requests import Request
from google.api_core.exceptions import NotFound
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


@extend_schema(tags=["Загрузка файла в Google Drive"])
@user_me_view_request_schema
@csrf_exempt
@api_view(["POST"])
def create_google_drive_document(request):
    """
    Создает документ в Google Drive.

    request.data:
        data: Текстовое содержимое документа
        name: Название документа

    """

    if request.method == "POST":
        data = request.data.get("data")
        name = request.data.get("name")

        if data is None or name is None:
            return Response(
                {"error": "Поле 'data' и 'name' должны быть указаны в запросе."},
                status=status.HTTP_400_BAD_REQUEST
            )

        creds = None
        token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json')

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            if creds.expired:
                creds.refresh(Request())

                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
        else:
            credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        try:
            drive = build("drive", "v3", credentials=creds)

            existing_files = (
                drive.files()
                .list(q=f"name='{name}'", pageSize=1, fields="files(id, name)")
                .execute()
            )
            if existing_files.get("files"):
                # Файл с таким именем уже существует
                logging.warning(f"Документ с именем {name} уже существует.")
                return Response(
                    {"message": "Документ с таким именем уже существует."},
                    status=status.HTTP_200_OK
                )

            file = drive.files().create(
                body={"name": name, "mimeType": "text/plain"},
            ).execute()

            media_body = MediaIoBaseUpload(io.BytesIO(data.encode("utf-8")), mimetype="text/plain", resumable=True)
            drive.files().update(fileId=file["id"], media_body=media_body).execute()

            logging.info(f"Документ успешно создан с именем: {name}")

            file_id = file["id"]
            file_info = drive.files().get(fileId=file_id).execute()

            return Response(
                {
                    "message": "Документ успешно создан.",
                    "file_id": file_id,
                    "file_name": file_info["name"],
                },
                status=status.HTTP_200_OK
            )
        except NotFound:
            logging.warning(f"Документ с именем {name} уже существует.")

            return Response(
                {"message": "Документ с таким именем уже существует."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logging.exception("Произошла ошибка при создании документа.")

            return Response({
                "error": f"Произошла ошибка при создании документа: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    logging.warning("Неверный запрос.")

    return Response(
        {"error": "Неверный запрос."},
        status=status.HTTP_400_BAD_REQUEST
    )
