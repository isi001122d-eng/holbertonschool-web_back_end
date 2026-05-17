#!/usr/bin/env python3
""" Authentication management module """
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Auth class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Public method to check if auth is required for a path """
        if path is None:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        normalized_path = path if path.endswith('/') else path + '/'

        for excluded in excluded_paths:
            normalized_excluded = excluded if excluded.endswith('/') else excluded + '/'
            if normalized_path == normalized_excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Public method to get authorization header """
        if request is None:
            return None
        
        # Request header-lərindən 'Authorization' bərabərliyini götürürük
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Public method to get current user """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request
        """
        if request is None:
            return None

        # Mühit dəyişənindən kuki adını götürürük (məsələn, '_my_session_id')
        cookie_name = getenv('SESSION_NAME')
        if cookie_name is None:
            return None

        # .get() metodunu mütləq şəkildə istifadə edərək kuki dəyərini qaytarırıq
        return request.cookies.get(cookie_name)
