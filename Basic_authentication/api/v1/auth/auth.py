#!/usr/bin/env python3
""" Authentication management module """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Public method to check if auth is required for a path """
        return False

    def authorization_header(self, request=None) -> str:
        """ Public method to get authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Public method to get current user """
        return None
