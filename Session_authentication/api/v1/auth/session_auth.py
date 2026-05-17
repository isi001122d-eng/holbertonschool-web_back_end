#!/usr/bin/env python3
""" Session Authentication module
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User  # User modelini import edirik


class SessionAuth(Auth):
    """ SessionAuth class that inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns a User instance based on a cookie value
        """
        if request is None:
            return None

        # 1. Sorğudan kuki (Session ID) dəyərini götürürük
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        # 2. Həmin Session ID-yə bağlı olan User ID-ni tapırıq
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # 3. User ID vasitəsilə bazadan real istifadəçini çəkirik
        return User.get(user_id)
