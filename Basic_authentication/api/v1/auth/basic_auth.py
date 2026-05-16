#!/usr/bin/env python3
""" Basic Authentication module """
import base64
from api.v1.auth.auth import Auth


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
            # Base64 string-i əvvəlcə baytlara çevirib decode edirik
            decoded_bytes = base64.b64decode(base64_authorization_header, validate=True)
            # Baytları normal UTF-8 mətninə çeviririk
            return decoded_bytes.decode('utf-8')
        except Exception:
            # Əgər hər hansı bir xəta baş verərsə (düzgün base64 deyilsə) None qaytarırıq
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

        # split(':', 1) yazırıq ki, əgər şifrənin öz daxilində də : işarəsi olarsa,
        # mətni səhvən çox parçaya bölməsin, yalnız ilk tapdığı : işarəsindən bölsün.
        parts = decoded_base64_authorization_header.split(':', 1)
        return parts[0], parts[1]
