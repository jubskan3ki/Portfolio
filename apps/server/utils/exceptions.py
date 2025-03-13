"""
Gestion centralisée des exceptions API pour Django Rest Framework.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomAPIException(Exception):
    """Exception personnalisée pour les erreurs d'API."""

    def __init__(self, detail, status_code=status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code


def custom_exception_handler(exc, context):
    """
    Gestionnaire d'exceptions personnalisé pour DRF.
    Convertit les exceptions Python en réponses JSON.
    """
    response = exception_handler(exc, context)

    if isinstance(exc, CustomAPIException):
        return Response({"error": exc.detail}, status=exc.status_code)

    if response is not None:
        response.data = {
            "error": response.data.get("detail", "Une erreur s'est produite."),
            "status_code": response.status_code,
        }

    return response
