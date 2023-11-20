from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from .serializers import (
    ConflictErrorSerializer,
    InternalServerErrorSerializer,
)


user_me_view_request_schema = extend_schema(
    summary="Метод для загрузки файлов в Google Drive",
    description="Этот метод позволяет загрузить файл в Google Drive.",
    responses={
        200: OpenApiResponse(
            description="Документ успешно создан.",
        ),
        409: OpenApiResponse(
            response=ConflictErrorSerializer,
            description="Error: Конфликт файлов.",
        ),
        500: OpenApiResponse(
            response=InternalServerErrorSerializer,
            description="Error: Internal server error",
        ),
    },
)
