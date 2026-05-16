#!/usr/bin/env python3
""" Basic Authentication module """
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth """

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """ Extracts the Base64 part of the Authorization header """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """ Decodes a Base64 string into a UTF-8 string """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """ Extracts user email and password from the decoded Base64 string """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None

        parts = decoded_base64_authorization_header.split(':', 1)
        return parts[0], parts[1]

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """ Returns the User instance based on his email and password """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            # Email-ə görə istifadəçiləri axtarırıq
            users = User.search({"email": user_email})
        except Exception:
            return None

        # Əgər heç bir istifadəçi tapılmayıbsa
        if not users or len(users) == 0:
            return None

        # Tapılan ilk istifadəçini götürürük və şifrəsini yoxlayırıq
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth.current_user to retrieve the User instance """
        if request is None:
            return None

        # 1. Header-i götür
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # 2. Base64 hissəsini ayır
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None

        # 3. Mətni deşifrə (decode) et
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None

        # 4. Email və şifrəni çıxart
        email, password = self.extract_user_credentials(decoded_header)
        if email is None or password is None:
            return None

        # 5. İstifadəçi obyektini bazadan tap və qaytar
        return self.user_object_from_credentials(email, password)
