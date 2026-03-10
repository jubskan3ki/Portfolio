"""Vues pour la gestion des sessions utilisateur."""

import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.security import SessionManager, generate_fingerprint

from ..docs import SESSION_LIST_RESPONSES, SESSION_REVOKE_RESPONSES
from ..services.token import TokenBlacklistService
from ..throttles import SessionThrottle

logger = logging.getLogger(__name__)


class AdminSessionsView(APIView):
    """Gestion des sessions utilisateur."""

    permission_classes = [IsAdminUser]
    throttle_classes = [SessionThrottle]

    @swagger_auto_schema(
        operation_summary="Lister les sessions",
        operation_description="Recupere la liste des sessions actives de l'utilisateur.",
        responses=SESSION_LIST_RESPONSES,
        tags=["Users"],
    )
    def get(self, request):
        """Recupere les sessions actives."""
        session_manager = SessionManager(request.user.id)
        sessions = session_manager.get_sessions()

        # Get current session fingerprint
        current_fingerprint = generate_fingerprint(request)
        current_session_id = current_fingerprint.fingerprint_hash

        # Format sessions with is_current flag
        formatted_sessions = [
            {
                "id": session.get("id", ""),
                "device": session.get("device", {}),
                "created_at": session.get("created_at", ""),
                "last_activity": session.get("last_activity", ""),
                "is_current": session.get("id") == current_session_id,
            }
            for session in sessions
        ]

        return Response(
            {
                "sessions": formatted_sessions,
                "count": len(formatted_sessions),
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Revoquer des sessions",
        operation_description="Revoque une session specifique ou toutes les autres sessions.",
        responses=SESSION_REVOKE_RESPONSES,
        tags=["Users"],
    )
    def delete(self, request):
        """Revoque une ou plusieurs sessions."""
        session_manager = SessionManager(request.user.id)
        session_id = request.query_params.get("session_id")
        revoke_all = request.query_params.get("all", "false").lower() == "true"

        # Get current session to preserve it if revoking all
        current_fingerprint = generate_fingerprint(request)
        current_session_id = current_fingerprint.fingerprint_hash

        if revoke_all:
            # Revoke all sessions except current
            revoked_sessions = session_manager.revoke_all_sessions(except_session_id=current_session_id)
            # Blacklist all revoked tokens
            blacklisted_count = sum(
                1 for session in revoked_sessions if TokenBlacklistService.blacklist_session_token(session)
            )
            logger.info("Revoked %d sessions, blacklisted %d tokens", len(revoked_sessions), blacklisted_count)
            return Response(
                {
                    "detail": f"{len(revoked_sessions)} session(s) revoquee(s).",
                },
                status=status.HTTP_200_OK,
            )

        if session_id:
            # Don't allow revoking current session via this endpoint
            if session_id == current_session_id:
                return Response(
                    {
                        "detail": "Utilisez la deconnexion pour fermer la session actuelle.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            removed_session = session_manager.remove_session(session_id)
            if removed_session:
                TokenBlacklistService.blacklist_session_token(removed_session)
                return Response(
                    {
                        "detail": "Session revoquee.",
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "detail": "Session non trouvee.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "detail": "Specifiez session_id ou all=true.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
