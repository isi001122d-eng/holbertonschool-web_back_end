#!/usr/bin/env python3
""" Authentication management module """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Public method to check if auth is required for a path """
        if path is None:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        # Slash tolerant: path-in sonuna slash əlavə edib yoxlamaq üçün təmizləyirik
        normalized_path = path if path.endswith('/') else path + '/'

        for excluded in excluded_paths:
            # Siyahıdakı hər bir istisnanın da sonuna slash zəmanəti veririk
            normalized_excluded = excluded if excluded.endswith('/') else excluded + '/'
            if normalized_path == normalized_excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Public method to get authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Public method to get current user """
        return None
