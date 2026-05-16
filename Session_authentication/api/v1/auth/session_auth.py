#!/usr/bin/env python3
""" Session Authentication module
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ SessionAuth class that inherits from Auth
    """
    # Klas atributu (In-memory storage)
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Unikal Session ID yaradırıq (string formatında)
        session_id = str(uuid.uuid4())

        # Lüğətə Session ID-ni açar, user_id-ni isə dəyər olaraq yazırıq
        self.user_id_by_session_id[session_id] = user_id

        return session_id
