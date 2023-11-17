import io
import json
import logging
import os

from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseUpload
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .decorators import user_me_view_request_schema

logger = logging.getLogger(__name__)


def load_credentials():
    credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')
    with open(credentials_path) as f:
        credentials_data = json.load(f)

    return service_account.Credentials.from_service_account_info(credentials_data)


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

        credentials = load_credentials()
        user = request.user
        print(user.id)

        drive = discovery.build('drive', 'v3', credentials=credentials)

        try:
            file = drive.files().create(
                body={"name": name, "mimeType": "text/plain"},
            ).execute()

            media_body = MediaIoBaseUpload(io.BytesIO(data.encode("utf-8")), mimetype="text/plain", resumable=True)
            drive.files().update(fileId=file["id"], media_body=media_body).execute()

            logger.info(f"Документ успешно создан с именем: {name}")

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
            logger.warning(f"Документ с именем {name} уже существует.")

            return Response(
                {"message": "Документ с таким именем уже существует."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception("Произошла ошибка при создании документа.")

            return Response({
                "error": f"Произошла ошибка при создании документа: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    logger.warning("Неверный запрос.")

    return Response(
        {"error": "Неверный запрос."},
        status=status.HTTP_400_BAD_REQUEST
    )
