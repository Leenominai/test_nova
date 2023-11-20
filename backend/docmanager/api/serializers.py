from rest_framework import serializers


class ConflictErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        default="Конфликт файлов.",
        help_text="Сообщение об ошибке",
    )


class InternalServerErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        default="Internal server error.",
        help_text="Сообщение об ошибке",
    )
