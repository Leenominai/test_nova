from rest_framework import serializers


class BadRequestErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        default="Неверный запрос.",
        help_text="Сообщение об ошибке",
    )


class InternalServerErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        default="Internal server error.",
        help_text="Сообщение об ошибке",
    )
